"""
WinAPI MCP server — minimal, single-file MCP server exposing Windows automation
tools (screenshots, mouse, keyboard, clipboard, process & window inspection)
over stdio. Designed to be invoked from .vscode/mcp.json or .cursor/mcp.json
through the bundled run.ps1 (which activates the local .venv).

Tools exposed:
  screenshot_window     - capture a window (by title substring) and return as image
  screenshot_area       - capture a screen rectangle and return as image
  mouse_click           - click at (x, y) with optional button / double-click
  mouse_click_window    - click at (x, y) RELATIVE to a window's top-left, after focusing it
  mouse_move            - move cursor to (x, y)
  mouse_drag            - press, move, release: drag from (x1, y1) to (x2, y2)
  mouse_scroll          - scroll the wheel at (x, y) by N clicks (negative = down)
  mouse_position        - report the current cursor position
  send_hotkey           - send hotkeys / keys / text / sequences (PID-targeted or global)
  clipboard_get         - read text from the system clipboard
  clipboard_set         - write text to the system clipboard
  list_processes        - list processes (optionally only those with main windows)
  window_list           - list visible top-level windows with their pid, title, class, rect
  window_focus          - bring a window to the foreground (by pid or window_name)
  window_get_rect       - return rect/title/class/pid for a window matched by name
  wait_for_window       - poll until a window with given title appears, then return its rect
  window_tree           - dump the window tree for a given PID
  get_window_content    - deep UI Automation dump of a process
  find_element          - find UI Automation elements by name (and optional control_type) under a pid
  click_element         - find an element by name under a pid and click its center (auto-focus)
  screen_size           - return primary monitor + virtual screen dimensions

This is a deliberately narrow port of mcpyrex's `lng_winapi/*` tools, plus
mouse and screenshot capabilities, packaged so it can be installed and run
from a single folder without the rest of mcpyrex.
"""
from __future__ import annotations

import asyncio
import base64
import ctypes
import ctypes.wintypes
import json
import os
import re
import sys
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any

import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

# ---------------------------------------------------------------------------
# Lazy / optional imports — fail loudly only when the relevant tool is invoked.
# ---------------------------------------------------------------------------

def _missing(pkg: str) -> str:
    return (
        f"Required Python package '{pkg}' is not installed in the server's "
        f"virtualenv. Re-run install.ps1 or 'pip install {pkg}' inside .venv."
    )

try:
    import mss  # type: ignore
except Exception:  # pragma: no cover
    mss = None

try:
    from PIL import Image  # type: ignore
except Exception:  # pragma: no cover
    Image = None  # type: ignore

try:
    import psutil  # type: ignore
except Exception:  # pragma: no cover
    psutil = None  # type: ignore

try:
    import pyautogui  # type: ignore
    pyautogui.FAILSAFE = False  # do not abort if cursor lands in a screen corner
except Exception:  # pragma: no cover
    pyautogui = None  # type: ignore

try:
    import pyperclip  # type: ignore
except Exception:  # pragma: no cover
    pyperclip = None  # type: ignore

# Windows-only modules
try:
    import win32api  # type: ignore
    import win32con  # type: ignore
    import win32gui  # type: ignore
except Exception:  # pragma: no cover
    win32api = win32con = win32gui = None  # type: ignore

try:
    import pywinauto  # type: ignore
    from pywinauto.keyboard import send_keys, CODES  # type: ignore
except Exception:  # pragma: no cover
    pywinauto = None  # type: ignore
    send_keys = None  # type: ignore
    CODES = {}  # type: ignore


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _safe_name(value: str, max_len: int = 60) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")
    return (cleaned or "untitled")[:max_len]


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def _png_to_image_content(image_bytes: bytes, caption: str, file_path: Path) -> list[types.Content]:
    """Save PNG bytes to disk and return both a text caption and an image content."""
    file_path.write_bytes(image_bytes)
    b64 = base64.b64encode(image_bytes).decode("ascii")
    return [
        types.TextContent(
            type="text",
            text=f"{caption}\nSaved to: {file_path}",
        ),
        types.ImageContent(type="image", mimeType="image/png", data=b64),
    ]


def _err(message: str) -> list[types.Content]:
    return [types.TextContent(type="text", text=json.dumps({"error": message}, ensure_ascii=False))]


def _ok(payload: Any) -> list[types.Content]:
    return [types.TextContent(type="text", text=json.dumps(payload, ensure_ascii=False, indent=2))]


# ---------------------------------------------------------------------------
# Window enumeration helpers (winapi-only path, no pywinauto needed)
# ---------------------------------------------------------------------------

def _get_window_text(hwnd: int) -> str:
    user32 = ctypes.windll.user32
    length = user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value


def _get_class_name(hwnd: int) -> str:
    user32 = ctypes.windll.user32
    buf = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(hwnd, buf, 256)
    return buf.value


def _enum_top_level_windows() -> list[int]:
    user32 = ctypes.windll.user32
    found: list[int] = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
    def cb(hwnd, _lp):
        if user32.IsWindowVisible(hwnd):
            found.append(hwnd)
        return True

    user32.EnumWindows(cb, 0)
    return found


def _enum_child_windows(parent: int) -> list[int]:
    user32 = ctypes.windll.user32
    found: list[int] = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
    def cb(hwnd, _lp):
        found.append(hwnd)
        return True

    user32.EnumChildWindows(parent, cb, 0)
    return found


def _find_window_by_name(name: str) -> int | None:
    """Find a window whose title contains `name` (case-insensitive substring).

    Searches top-level windows first; if nothing matches, descends into children.
    """
    if win32gui is None:
        return None
    needle = name.lower()
    # Pass 1: top-level visible windows
    for hwnd in _enum_top_level_windows():
        title = _get_window_text(hwnd)
        if title and needle in title.lower():
            return hwnd
    # Pass 2: children of every top-level window
    for parent in _enum_top_level_windows():
        for hwnd in _enum_child_windows(parent):
            title = _get_window_text(hwnd)
            cls = _get_class_name(hwnd)
            if (title and needle in title.lower()) or (cls and needle in cls.lower()):
                return hwnd
    return None


def _get_window_rect(hwnd: int) -> tuple[int, int, int, int] | None:
    if win32gui is None:
        return None
    try:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if right <= left or bottom <= top:
            return None
        return left, top, right, bottom
    except Exception:
        return None


def _get_pid_for_hwnd(hwnd: int) -> int | None:
    if win32gui is None:
        return None
    try:
        user32 = ctypes.windll.user32
        ppid = ctypes.wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(ppid))
        return int(ppid.value) if ppid.value else None
    except Exception:
        return None


def _resolve_window(name: str | None, pid: int | None) -> tuple[int | None, int | None, str]:
    """Resolve a (hwnd, pid, error) tuple from optional name and/or pid.

    If name is given, find by substring. If only pid, return its first
    visible top-level main window. Returns (None, None, error_message)
    when nothing matches.
    """
    if not name and pid is None:
        return None, None, "Provide window_name or pid"
    if name:
        hwnd = _find_window_by_name(name)
        if not hwnd:
            return None, None, f"No window matching: {name!r}"
        return hwnd, _get_pid_for_hwnd(hwnd), ""
    # pid only
    if win32gui is None:
        return None, None, _missing("pywin32")
    user32 = ctypes.windll.user32
    target_pid = int(pid)
    for cand in _enum_top_level_windows():
        if _get_pid_for_hwnd(cand) == target_pid:
            return cand, target_pid, ""
    return None, target_pid, f"No visible top-level window for pid {target_pid}"


def _try_focus_pid(pid: int | None) -> str | None:
    """Best-effort focus; returns error string or None on success."""
    if pid is None:
        return "no pid"
    if pywinauto is None:
        return _missing("pywinauto")
    try:
        _focus_pid(int(pid))
        return None
    except Exception as exc:
        return str(exc)


# ---------------------------------------------------------------------------
# Screenshot tools
# ---------------------------------------------------------------------------

def _capture_bbox(left: int, top: int, right: int, bottom: int) -> bytes:
    if mss is None or Image is None:
        raise RuntimeError(_missing("mss / Pillow"))
    width, height = right - left, bottom - top
    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid bbox: ({left}, {top}, {right}, {bottom})")
    with mss.mss() as sct:
        raw = sct.grab({"left": left, "top": top, "width": width, "height": height})
        img = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")
        buf = BytesIO()
        img.save(buf, format="PNG", optimize=True)
        return buf.getvalue()


async def _tool_screenshot_window(arguments: dict) -> list[types.Content]:
    args = arguments or {}
    name = args.get("window_name")
    if not name:
        return _err("window_name is required")
    if win32gui is None:
        return _err(_missing("pywin32"))
    hwnd = _find_window_by_name(name)
    if not hwnd:
        return _err(f"No window matching: {name!r}")
    bring_to_front = bool(args.get("bring_to_front", True))
    if bring_to_front:
        pid = _get_pid_for_hwnd(hwnd)
        if pid is not None:
            _try_focus_pid(pid)
            time.sleep(0.15)
    rect = _get_window_rect(hwnd)
    if not rect:
        return _err(f"Window {hwnd} has no usable rectangle")
    try:
        png = _capture_bbox(*rect)
    except Exception as exc:
        return _err(f"Capture failed: {exc}")
    title = _get_window_text(hwnd) or name
    out = OUTPUT_DIR / f"window-{_safe_name(title)}-{_timestamp()}.png"
    caption = (
        f"Captured window hwnd={hwnd} title={title!r} "
        f"rect=({rect[0]},{rect[1]},{rect[2]},{rect[3]}) "
        f"size={rect[2]-rect[0]}x{rect[3]-rect[1]}"
    )
    return _png_to_image_content(png, caption, out)


async def _tool_screenshot_area(arguments: dict) -> list[types.Content]:
    args = arguments or {}
    try:
        x1 = int(args["x1"]); y1 = int(args["y1"])
        x2 = int(args["x2"]); y2 = int(args["y2"])
    except (KeyError, TypeError, ValueError):
        return _err("x1, y1, x2, y2 are required integers")
    left, right = sorted((x1, x2))
    top, bottom = sorted((y1, y2))
    try:
        png = _capture_bbox(left, top, right, bottom)
    except Exception as exc:
        return _err(f"Capture failed: {exc}")
    out = OUTPUT_DIR / f"area-{left}_{top}-{right}_{bottom}-{_timestamp()}.png"
    caption = (
        f"Captured area ({left},{top})-({right},{bottom}) "
        f"size={right-left}x{bottom-top}"
    )
    return _png_to_image_content(png, caption, out)


# ---------------------------------------------------------------------------
# Mouse tools
# ---------------------------------------------------------------------------

async def _tool_mouse_move(arguments: dict) -> list[types.Content]:
    if pyautogui is None:
        return _err(_missing("pyautogui"))
    args = arguments or {}
    try:
        x = int(args["x"]); y = int(args["y"])
    except (KeyError, TypeError, ValueError):
        return _err("x, y are required integers")
    duration = float(args.get("duration", 0.0))
    pyautogui.moveTo(x, y, duration=duration)
    return _ok({"action": "move", "x": x, "y": y, "duration": duration})


async def _tool_mouse_click(arguments: dict) -> list[types.Content]:
    if pyautogui is None:
        return _err(_missing("pyautogui"))
    args = arguments or {}
    x = args.get("x"); y = args.get("y")
    button = (args.get("button") or "left").lower()
    if button not in ("left", "right", "middle"):
        return _err("button must be one of: left, right, middle")
    clicks = int(args.get("clicks", 2 if args.get("double") else 1))
    interval = float(args.get("interval", 0.05))
    if x is not None and y is not None:
        pyautogui.click(x=int(x), y=int(y), clicks=clicks, interval=interval, button=button)
    else:
        pyautogui.click(clicks=clicks, interval=interval, button=button)
    return _ok({"action": "click", "x": x, "y": y, "button": button, "clicks": clicks})


async def _tool_mouse_drag(arguments: dict) -> list[types.Content]:
    if pyautogui is None:
        return _err(_missing("pyautogui"))
    args = arguments or {}
    try:
        x1 = int(args["x1"]); y1 = int(args["y1"])
        x2 = int(args["x2"]); y2 = int(args["y2"])
    except (KeyError, TypeError, ValueError):
        return _err("x1, y1, x2, y2 are required integers")
    duration = float(args.get("duration", 0.5))
    button = (args.get("button") or "left").lower()
    if button not in ("left", "right", "middle"):
        return _err("button must be one of: left, right, middle")
    pyautogui.moveTo(x1, y1)
    pyautogui.mouseDown(button=button)
    try:
        pyautogui.moveTo(x2, y2, duration=duration)
    finally:
        pyautogui.mouseUp(button=button)
    return _ok({
        "action": "drag", "from": [x1, y1], "to": [x2, y2],
        "duration": duration, "button": button,
    })


async def _tool_mouse_scroll(arguments: dict) -> list[types.Content]:
    if pyautogui is None:
        return _err(_missing("pyautogui"))
    args = arguments or {}
    try:
        clicks = int(args.get("clicks", -3))
    except (TypeError, ValueError):
        return _err("'clicks' must be an integer (negative = scroll down)")
    pid = args.get("pid")
    if pid is not None:
        err = _try_focus_pid(int(pid))
        if err:
            return _err(f"Could not focus pid {pid}: {err}")
    x = args.get("x"); y = args.get("y")
    if x is not None and y is not None:
        pyautogui.moveTo(int(x), int(y))
        time.sleep(0.05)
    pyautogui.scroll(clicks)
    return _ok({"action": "scroll", "clicks": clicks, "x": x, "y": y, "pid": pid})


async def _tool_mouse_position(_args: dict) -> list[types.Content]:
    if pyautogui is None:
        return _err(_missing("pyautogui"))
    pos = pyautogui.position()
    return _ok({"x": int(pos.x), "y": int(pos.y)})


async def _tool_mouse_click_window(arguments: dict) -> list[types.Content]:
    """Click at coordinates RELATIVE to a window's top-left, after focusing it.

    Solves the common bug where the agent computes pixel coords from a window
    screenshot but the window itself sits at non-zero (or even negative)
    desktop coordinates, so a global click misses.
    """
    if pyautogui is None or win32gui is None:
        return _err(_missing("pyautogui / pywin32"))
    args = arguments or {}
    try:
        rel_x = int(args["x"]); rel_y = int(args["y"])
    except (KeyError, TypeError, ValueError):
        return _err("x and y are required integers (relative to window's top-left)")
    button = (args.get("button") or "left").lower()
    if button not in ("left", "right", "middle"):
        return _err("button must be one of: left, right, middle")
    clicks = int(args.get("clicks", 2 if args.get("double") else 1))
    interval = float(args.get("interval", 0.05))

    hwnd, pid, err = _resolve_window(args.get("window_name"), args.get("pid"))
    if err:
        return _err(err)
    rect = _get_window_rect(hwnd)
    if not rect:
        return _err(f"Window {hwnd} has no usable rectangle")
    if bool(args.get("focus", True)):
        _try_focus_pid(pid)
        time.sleep(0.1)
    abs_x = rect[0] + rel_x
    abs_y = rect[1] + rel_y
    pyautogui.click(x=abs_x, y=abs_y, clicks=clicks, interval=interval, button=button)
    return _ok({
        "action": "click_window", "hwnd": hwnd, "pid": pid,
        "window_origin": [rect[0], rect[1]],
        "window_size": [rect[2] - rect[0], rect[3] - rect[1]],
        "relative": [rel_x, rel_y], "absolute": [abs_x, abs_y],
        "button": button, "clicks": clicks,
    })


# ---------------------------------------------------------------------------
# Keyboard tool (port of mcpyrex lng_winapi/send_hotkey, simplified)
# ---------------------------------------------------------------------------

VK_MAP = {
    **{c: 0x41 + i for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")},
    **{str(i): 0x30 + i for i in range(10)},
    **{f"f{i}": 0x6F + i for i in range(1, 13)},
    "space": 0x20, "enter": 0x0D, "tab": 0x09, "esc": 0x1B, "escape": 0x1B,
    "backspace": 0x08, "delete": 0x2E, "insert": 0x2D, "home": 0x24, "end": 0x23,
    "pageup": 0x21, "pagedown": 0x22, "up": 0x26, "down": 0x28, "left": 0x25, "right": 0x27,
}


def _parse_hotkey(s: str) -> dict:
    s_low = s.lower()
    ctrl = "^" in s_low
    alt = "%" in s_low
    win = "~" in s_low
    shift = False
    rest = s_low
    if rest.startswith("+"):
        shift = True
        rest = rest[1:]
    rest = rest.replace("^", "").replace("%", "").replace("~", "")
    if "+" in rest and (ctrl or alt or win):
        shift = True
        rest = rest.replace("+", "")
    if rest.startswith("{") and rest.endswith("}"):
        rest = rest[1:-1]
    return {"ctrl": ctrl, "shift": shift, "alt": alt, "win": win, "key": rest.strip()}


def _send_hotkey_global(hotkey: str) -> bool:
    if win32api is None:
        return False
    parsed = _parse_hotkey(hotkey)
    vk = VK_MAP.get(parsed["key"])
    if vk is None:
        return False
    if parsed["ctrl"]: win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    if parsed["shift"]: win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    if parsed["alt"]: win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
    if parsed["win"]: win32api.keybd_event(win32con.VK_LWIN, 0, 0, 0)
    win32api.keybd_event(vk, 0, 0, 0)
    time.sleep(0.01)
    win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
    if parsed["win"]: win32api.keybd_event(win32con.VK_LWIN, 0, win32con.KEYEVENTF_KEYUP, 0)
    if parsed["alt"]: win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
    if parsed["shift"]: win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
    if parsed["ctrl"]: win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    return True


def _escape_for_send_keys(s: str) -> str:
    out = s
    for ch in "{}+^%~()[]":
        out = out.replace(ch, "{" + ch + "}")
    out = out.replace(" ", "{SPACE}")
    return out


def _focus_pid(pid: int):
    if pywinauto is None:
        raise RuntimeError(_missing("pywinauto"))
    app = pywinauto.Application(backend="uia").connect(process=pid)
    win = app.top_window()
    try:
        win.set_focus(); time.sleep(0.1)
        win.restore(); win.set_focus(); time.sleep(0.1)
    except Exception:
        pass
    return win


async def _tool_send_hotkey(arguments: dict) -> list[types.Content]:
    if win32api is None:
        return _err(_missing("pywin32"))
    args = arguments or {}
    pid = args.get("pid")
    hotkey = args.get("hotkey")
    key = args.get("key")
    text = args.get("text")
    sequence = args.get("sequence")
    delay_ms = int(args.get("delay", 100))

    if not any([hotkey, key, text, sequence]):
        return _err("Provide one of: hotkey, key, text, sequence")

    if pid is not None:
        try:
            _focus_pid(int(pid))
        except Exception as exc:
            return _err(f"Could not focus pid {pid}: {exc}")

    log: list[dict] = []

    def do(action_type: str, value):
        nonlocal log
        if action_type == "hotkey":
            if not _send_hotkey_global(str(value)) and send_keys is not None:
                send_keys(str(value))
            log.append({"type": "hotkey", "value": value})
        elif action_type == "key":
            k = str(value).upper()
            if send_keys is None:
                return  # already errored
            send_keys("{" + k + "}" if k in CODES else k)
            log.append({"type": "key", "value": value})
        elif action_type == "text":
            if send_keys is None:
                return
            send_keys(_escape_for_send_keys(str(value)))
            log.append({"type": "text", "value": value})
        elif action_type == "delay":
            time.sleep(int(value) / 1000.0)
            log.append({"type": "delay", "value": value})
        elif action_type == "focus" and pid is not None:
            _focus_pid(int(pid))
            log.append({"type": "focus", "value": pid})
        else:
            raise ValueError(f"Unknown action type: {action_type}")

    try:
        if sequence:
            for i, action in enumerate(sequence):
                do(action.get("type"), action.get("value"))
                if i < len(sequence) - 1 and action.get("type") != "delay":
                    time.sleep(delay_ms / 1000.0)
        elif hotkey:
            do("hotkey", hotkey)
        elif key:
            do("key", key)
        elif text:
            do("text", text)
    except Exception as exc:
        return _err(f"Send failed after {len(log)} actions: {exc}")

    return _ok({"success": True, "pid": pid, "actions": log})


# ---------------------------------------------------------------------------
# Clipboard tools
# ---------------------------------------------------------------------------

async def _tool_clipboard_get(_args: dict) -> list[types.Content]:
    if pyperclip is None:
        return _err(_missing("pyperclip"))
    try:
        return _ok({"text": pyperclip.paste()})
    except Exception as exc:
        return _err(f"Clipboard read failed: {exc}")


async def _tool_clipboard_set(arguments: dict) -> list[types.Content]:
    if pyperclip is None:
        return _err(_missing("pyperclip"))
    text = (arguments or {}).get("text")
    if text is None:
        return _err("'text' is required")
    try:
        pyperclip.copy(str(text))
        return _ok({"success": True, "length": len(str(text))})
    except Exception as exc:
        return _err(f"Clipboard write failed: {exc}")


# ---------------------------------------------------------------------------
# Process & window inspection (ports of mcpyrex tools)
# ---------------------------------------------------------------------------

async def _tool_list_processes(arguments: dict) -> list[types.Content]:
    if psutil is None:
        return _err(_missing("psutil"))
    args = arguments or {}
    flt = (args.get("filter") or "").lower()
    only_with_windows = bool(args.get("only_with_windows", False))
    user32 = ctypes.windll.user32 if win32gui is not None else None

    def has_main_window(pid: int) -> bool:
        if user32 is None:
            return False
        found = False

        @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        def cb(hwnd, _lp):
            nonlocal found
            ppid = ctypes.wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(ppid))
            if ppid.value == pid and user32.IsWindowVisible(hwnd) and user32.GetParent(hwnd) == 0:
                style = user32.GetWindowLongW(hwnd, -16)
                if not (style & 0x08000000):
                    found = True
                    return False
            return True

        user32.EnumWindows(cb, 0)
        return found

    out = []
    for proc in psutil.process_iter(["pid", "name", "exe"]):
        try:
            info = proc.info
            name = info.get("name") or ""
            exe = info.get("exe") or ""
            if flt and flt not in name.lower() and flt not in exe.lower():
                continue
            pid = info.get("pid")
            if only_with_windows and not has_main_window(pid):
                continue
            out.append({"pid": pid, "name": name, "exe": exe})
        except Exception:
            continue
    return _ok(out)


async def _tool_window_tree(arguments: dict) -> list[types.Content]:
    if win32gui is None:
        return _err(_missing("pywin32"))
    pid = (arguments or {}).get("pid")
    if pid is None:
        return _err("pid is required")
    pid = int(pid)
    user32 = ctypes.windll.user32

    def build(hwnd: int) -> dict:
        return {
            "hwnd": hwnd,
            "title": _get_window_text(hwnd),
            "class": _get_class_name(hwnd),
            "children": [build(c) for c in _enum_child_windows(hwnd)],
        }

    roots: list[int] = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
    def cb(hwnd, _lp):
        ppid = ctypes.wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(ppid))
        if ppid.value == pid:
            roots.append(hwnd)
        return True

    user32.EnumWindows(cb, 0)
    return _ok([build(h) for h in roots])


async def _tool_get_window_content(arguments: dict) -> list[types.Content]:
    if pywinauto is None:
        return _err(_missing("pywinauto"))
    args = arguments or {}
    pid = args.get("pid")
    if pid is None:
        return _err("pid is required")
    pid = int(pid)
    target = (args.get("target_window") or "").lower()
    max_depth = args.get("max_depth")
    include_invisible = bool(args.get("include_invisible", False))

    try:
        app = pywinauto.Application(backend="uia").connect(process=pid)
    except Exception as exc:
        return _err(f"Connect failed: {exc}")

    def extract(el, depth=0):
        if max_depth is not None and depth > int(max_depth):
            return None
        try:
            info = {
                "depth": depth,
                "control_type": getattr(el.element_info, "control_type", "") or "",
                "class_name": getattr(el.element_info, "class_name", "") or "",
                "name": el.window_text(),
                "is_visible": True,
                "is_enabled": True,
                "position": {"x": 0, "y": 0, "width": 0, "height": 0},
                "children": [],
            }
            try:
                info["is_visible"] = el.is_visible()
                info["is_enabled"] = el.is_enabled()
            except Exception:
                pass
            try:
                r = el.rectangle()
                info["position"] = {
                    "x": r.left, "y": r.top,
                    "width": r.right - r.left, "height": r.bottom - r.top,
                }
            except Exception:
                pass
            if not include_invisible and not info["is_visible"]:
                return None
            try:
                for child in el.children():
                    sub = extract(child, depth + 1)
                    if sub:
                        info["children"].append(sub)
            except Exception:
                pass
            return info
        except Exception as exc:
            return {"depth": depth, "error": str(exc), "children": []}

    out_windows = []
    for w in app.windows():
        try:
            title = w.window_text()
            if target and target not in title.lower():
                continue
            out_windows.append({
                "window_title": title,
                "window_class": w.element_info.class_name,
                "window_handle": w.handle,
                "content": extract(w, 0),
            })
        except Exception as exc:
            out_windows.append({"error": str(exc)})

    return _ok({"pid": pid, "windows": out_windows, "count": len(out_windows)})


# ---------------------------------------------------------------------------
# New: window discovery / focus / wait helpers
# ---------------------------------------------------------------------------

async def _tool_window_list(arguments: dict) -> list[types.Content]:
    if win32gui is None:
        return _err(_missing("pywin32"))
    args = arguments or {}
    flt = (args.get("filter") or "").lower()
    out = []
    for hwnd in _enum_top_level_windows():
        title = _get_window_text(hwnd)
        cls = _get_class_name(hwnd)
        if not title and not cls:
            continue
        if flt and flt not in title.lower() and flt not in cls.lower():
            continue
        rect = _get_window_rect(hwnd)
        out.append({
            "hwnd": hwnd,
            "pid": _get_pid_for_hwnd(hwnd),
            "title": title,
            "class": cls,
            "rect": (
                {"left": rect[0], "top": rect[1], "right": rect[2], "bottom": rect[3],
                 "width": rect[2] - rect[0], "height": rect[3] - rect[1]}
                if rect else None
            ),
        })
    return _ok(out)


async def _tool_window_focus(arguments: dict) -> list[types.Content]:
    args = arguments or {}
    hwnd, pid, err = _resolve_window(args.get("window_name"), args.get("pid"))
    if err:
        return _err(err)
    err2 = _try_focus_pid(pid)
    if err2:
        return _err(f"Could not focus pid {pid}: {err2}")
    rect = _get_window_rect(hwnd) if hwnd else None
    return _ok({
        "focused": True, "hwnd": hwnd, "pid": pid,
        "title": _get_window_text(hwnd) if hwnd else None,
        "rect": list(rect) if rect else None,
    })


async def _tool_window_get_rect(arguments: dict) -> list[types.Content]:
    if win32gui is None:
        return _err(_missing("pywin32"))
    args = arguments or {}
    hwnd, pid, err = _resolve_window(args.get("window_name"), args.get("pid"))
    if err:
        return _err(err)
    rect = _get_window_rect(hwnd)
    if not rect:
        return _err(f"Window {hwnd} has no usable rectangle")
    left, top, right, bottom = rect
    return _ok({
        "hwnd": hwnd, "pid": pid,
        "title": _get_window_text(hwnd),
        "class": _get_class_name(hwnd),
        "rect": {
            "left": left, "top": top, "right": right, "bottom": bottom,
            "width": right - left, "height": bottom - top,
            "center_x": (left + right) // 2, "center_y": (top + bottom) // 2,
        },
    })


async def _tool_wait_for_window(arguments: dict) -> list[types.Content]:
    if win32gui is None:
        return _err(_missing("pywin32"))
    args = arguments or {}
    name = args.get("window_name")
    if not name:
        return _err("window_name is required")
    timeout = float(args.get("timeout", 10.0))
    poll = float(args.get("poll", 0.25))
    started = time.time()
    deadline = started + timeout
    while time.time() < deadline:
        hwnd = _find_window_by_name(name)
        if hwnd:
            rect = _get_window_rect(hwnd)
            return _ok({
                "hwnd": hwnd,
                "pid": _get_pid_for_hwnd(hwnd),
                "title": _get_window_text(hwnd),
                "rect": list(rect) if rect else None,
                "waited_seconds": round(time.time() - started, 3),
            })
        await asyncio.sleep(poll)
    return _err(f"Window {name!r} did not appear within {timeout}s")


# ---------------------------------------------------------------------------
# New: UI Automation element search & click
# ---------------------------------------------------------------------------

def _scan_elements(root, needle: str, control_type: str | None,
                   max_depth: int, depth: int = 0,
                   visible_only: bool = True) -> list:
    out: list = []
    if depth > max_depth:
        return out
    try:
        txt = root.window_text() or ""
        ct = getattr(root.element_info, "control_type", "") or ""
        match_name = needle in txt.lower() if needle else True
        match_ct = (not control_type) or control_type.lower() == ct.lower()
        if match_name and match_ct:
            try:
                vis = root.is_visible() if hasattr(root, "is_visible") else True
            except Exception:
                vis = True
            if vis or not visible_only:
                try:
                    r = root.rectangle()
                    out.append({
                        "name": txt, "control_type": ct,
                        "class_name": getattr(root.element_info, "class_name", "") or "",
                        "is_visible": vis,
                        "rect": {
                            "left": r.left, "top": r.top,
                            "right": r.right, "bottom": r.bottom,
                            "width": r.right - r.left, "height": r.bottom - r.top,
                            "center_x": (r.left + r.right) // 2,
                            "center_y": (r.top + r.bottom) // 2,
                        },
                    })
                except Exception:
                    pass
        for child in root.children():
            out.extend(_scan_elements(child, needle, control_type, max_depth,
                                      depth + 1, visible_only))
    except Exception:
        pass
    return out


async def _tool_find_element(arguments: dict) -> list[types.Content]:
    if pywinauto is None:
        return _err(_missing("pywinauto"))
    args = arguments or {}
    pid = args.get("pid")
    name = args.get("name") or ""
    control_type = args.get("control_type")
    if pid is None or not name:
        return _err("pid and name are required")
    max_depth = int(args.get("max_depth", 8))
    visible_only = bool(args.get("visible_only", True))
    try:
        app = pywinauto.Application(backend="uia").connect(process=int(pid))
    except Exception as exc:
        return _err(f"Connect failed for pid {pid}: {exc}")
    matches: list = []
    needle = name.lower()
    for w in app.windows():
        matches.extend(_scan_elements(w, needle, control_type, max_depth, 0, visible_only))
    return _ok({"pid": int(pid), "matches": matches, "count": len(matches)})


async def _tool_click_element(arguments: dict) -> list[types.Content]:
    if pywinauto is None or pyautogui is None:
        return _err(_missing("pywinauto / pyautogui"))
    args = arguments or {}
    pid = args.get("pid")
    name = args.get("name") or ""
    control_type = args.get("control_type")
    if pid is None or not name:
        return _err("pid and name are required")
    button = (args.get("button") or "left").lower()
    clicks = int(args.get("clicks", 2 if args.get("double") else 1))
    max_depth = int(args.get("max_depth", 8))
    try:
        app = pywinauto.Application(backend="uia").connect(process=int(pid))
    except Exception as exc:
        return _err(f"Connect failed for pid {pid}: {exc}")
    matches: list = []
    needle = name.lower()
    for w in app.windows():
        matches.extend(_scan_elements(w, needle, control_type, max_depth, 0, True))
        if matches:
            break
    if not matches:
        return _err(f"No visible element matching name={name!r}"
                    + (f" control_type={control_type!r}" if control_type else ""))
    target = matches[0]
    _try_focus_pid(int(pid))
    time.sleep(0.1)
    cx = target["rect"]["center_x"]
    cy = target["rect"]["center_y"]
    pyautogui.click(x=cx, y=cy, clicks=clicks, button=button)
    return _ok({
        "clicked": target, "button": button, "clicks": clicks,
        "alternatives": matches[1:5],  # first few other matches for debugging
    })


# ---------------------------------------------------------------------------
# New: screen size
# ---------------------------------------------------------------------------

async def _tool_screen_size(_args: dict) -> list[types.Content]:
    if win32api is None:
        return _err(_missing("pywin32"))
    primary_w = win32api.GetSystemMetrics(0)
    primary_h = win32api.GetSystemMetrics(1)
    virtual_x = win32api.GetSystemMetrics(76)  # SM_XVIRTUALSCREEN
    virtual_y = win32api.GetSystemMetrics(77)  # SM_YVIRTUALSCREEN
    virtual_w = win32api.GetSystemMetrics(78)  # SM_CXVIRTUALSCREEN
    virtual_h = win32api.GetSystemMetrics(79)  # SM_CYVIRTUALSCREEN
    return _ok({
        "primary": {"width": primary_w, "height": primary_h},
        "virtual": {"x": virtual_x, "y": virtual_y,
                    "width": virtual_w, "height": virtual_h},
    })


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

TOOLS: dict[str, dict] = {
    "screenshot_window": {
        "handler": _tool_screenshot_window,
        "description": (
            "Capture a screenshot of a window whose title (or class name) contains the "
            "given substring. Returns the PNG as MCP image content and saves it to the "
            "scripts/output/ folder. By default the window is brought to the foreground "
            "first (set bring_to_front=false to skip). Use list_processes + window_tree "
            "if you need to discover the exact window name first."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "window_name": {
                    "type": "string",
                    "description": "Case-insensitive substring to match against the window title or class name.",
                },
                "bring_to_front": {"type": "boolean", "default": True},
            },
            "required": ["window_name"],
        },
    },
    "screenshot_area": {
        "handler": _tool_screenshot_area,
        "description": (
            "Capture a rectangular region of the (virtual) screen by absolute pixel "
            "coordinates. (x1, y1) is one corner and (x2, y2) the opposite corner — "
            "order does not matter. Returns the PNG as MCP image content and saves it."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "x1": {"type": "integer"}, "y1": {"type": "integer"},
                "x2": {"type": "integer"}, "y2": {"type": "integer"},
            },
            "required": ["x1", "y1", "x2", "y2"],
        },
    },
    "mouse_move": {
        "handler": _tool_mouse_move,
        "description": "Move the cursor to absolute screen coordinates (x, y). Optional 'duration' in seconds for smooth motion.",
        "schema": {
            "type": "object",
            "properties": {
                "x": {"type": "integer"}, "y": {"type": "integer"},
                "duration": {"type": "number", "default": 0.0},
            },
            "required": ["x", "y"],
        },
    },
    "mouse_click": {
        "handler": _tool_mouse_click,
        "description": (
            "Click the mouse. If x/y are provided the cursor moves there first, otherwise "
            "clicks at the current position. button = left|right|middle, clicks defaults to "
            "1 (or 2 when 'double': true)."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "x": {"type": "integer"}, "y": {"type": "integer"},
                "button": {"type": "string", "enum": ["left", "right", "middle"], "default": "left"},
                "clicks": {"type": "integer", "default": 1},
                "double": {"type": "boolean", "default": False},
                "interval": {"type": "number", "default": 0.05},
            },
            "required": [],
        },
    },
    "mouse_drag": {
        "handler": _tool_mouse_drag,
        "description": (
            "Drag the mouse from (x1, y1) to (x2, y2). Holds 'button' (left|right|middle) "
            "down for the full move. 'duration' is the seconds spent during the drag motion."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "x1": {"type": "integer"}, "y1": {"type": "integer"},
                "x2": {"type": "integer"}, "y2": {"type": "integer"},
                "duration": {"type": "number", "default": 0.5},
                "button": {"type": "string", "enum": ["left", "right", "middle"], "default": "left"},
            },
            "required": ["x1", "y1", "x2", "y2"],
        },
    },
    "send_hotkey": {
        "handler": _tool_send_hotkey,
        "description": (
            "Send a hotkey, key, text, or sequence of any of those. Modifiers in 'hotkey': "
            "^=Ctrl, +=Shift, %=Alt, ~=Win (e.g. '^t', '^+i', '%{F4}'). 'key' is a single named "
            "key (F12, ENTER, ESC, TAB, ...). 'text' is plain text. 'sequence' is an array of "
            "actions: {type: hotkey|key|text|delay|focus, value: ...}. If 'pid' is given, the "
            "main window of that process is focused first."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "pid": {"type": "integer"},
                "hotkey": {"type": "string"},
                "key": {"type": "string"},
                "text": {"type": "string"},
                "sequence": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "enum": ["hotkey", "key", "text", "delay", "focus"]},
                            "value": {},
                        },
                        "required": ["type", "value"],
                    },
                },
                "delay": {"type": "integer", "default": 100, "description": "Default delay between sequence actions, in ms."},
            },
            "required": [],
        },
    },
    "clipboard_get": {
        "handler": _tool_clipboard_get,
        "description": "Return the current text contents of the system clipboard.",
        "schema": {"type": "object", "properties": {}, "required": []},
    },
    "clipboard_set": {
        "handler": _tool_clipboard_set,
        "description": "Replace the system clipboard contents with the given text.",
        "schema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
    "list_processes": {
        "handler": _tool_list_processes,
        "description": (
            "List processes (pid, name, exe). Optional 'filter' is a case-insensitive "
            "substring matched against name or exe. 'only_with_windows': true restricts to "
            "processes that own at least one visible top-level window."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "filter": {"type": "string"},
                "only_with_windows": {"type": "boolean", "default": False},
            },
            "required": [],
        },
    },
    "window_tree": {
        "handler": _tool_window_tree,
        "description": "Dump the window hierarchy (hwnd, title, class) for every top-level and child window owned by the given pid.",
        "schema": {
            "type": "object",
            "properties": {"pid": {"type": "integer"}},
            "required": ["pid"],
        },
    },
    "get_window_content": {
        "handler": _tool_get_window_content,
        "description": (
            "UI-Automation deep dump of a process: control types, names, positions, "
            "visibility, and children. Use 'target_window' to restrict to one window by "
            "title substring; 'max_depth' to limit recursion."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "pid": {"type": "integer"},
                "target_window": {"type": "string"},
                "max_depth": {"type": "integer"},
                "include_invisible": {"type": "boolean", "default": False},
            },
            "required": ["pid"],
        },
    },
    "mouse_scroll": {
        "handler": _tool_mouse_scroll,
        "description": (
            "Scroll the mouse wheel by N clicks. Negative clicks scroll DOWN, positive UP. "
            "If x/y are provided, the cursor moves there first. If pid is provided, the "
            "process's main window is focused first (so the scroll lands in the right window)."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "clicks": {"type": "integer", "default": -3,
                           "description": "Negative scrolls down, positive scrolls up."},
                "x": {"type": "integer"}, "y": {"type": "integer"},
                "pid": {"type": "integer"},
            },
            "required": [],
        },
    },
    "mouse_position": {
        "handler": _tool_mouse_position,
        "description": "Return the current cursor position {x, y} in absolute screen coordinates.",
        "schema": {"type": "object", "properties": {}, "required": []},
    },
    "mouse_click_window": {
        "handler": _tool_mouse_click_window,
        "description": (
            "Click at (x, y) RELATIVE to a window's top-left corner, after focusing the window. "
            "Use this when you computed coordinates from a screenshot of the window: the screenshot "
            "is window-relative but mouse_click is screen-absolute, so global clicks miss when the "
            "window is at non-zero (or negative) desktop coordinates. Provide either window_name "
            "(substring) or pid."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "window_name": {"type": "string"},
                "pid": {"type": "integer"},
                "x": {"type": "integer", "description": "X relative to window's top-left corner."},
                "y": {"type": "integer", "description": "Y relative to window's top-left corner."},
                "button": {"type": "string", "enum": ["left", "right", "middle"], "default": "left"},
                "clicks": {"type": "integer", "default": 1},
                "double": {"type": "boolean", "default": False},
                "interval": {"type": "number", "default": 0.05},
                "focus": {"type": "boolean", "default": True,
                          "description": "Bring the window to the front first."},
            },
            "required": ["x", "y"],
        },
    },
    "window_list": {
        "handler": _tool_window_list,
        "description": (
            "List visible top-level windows with hwnd, pid, title, class, and rect. "
            "Optional case-insensitive substring 'filter' against title or class."
        ),
        "schema": {
            "type": "object",
            "properties": {"filter": {"type": "string"}},
            "required": [],
        },
    },
    "window_focus": {
        "handler": _tool_window_focus,
        "description": (
            "Bring a window to the foreground (set_focus + restore via pywinauto). "
            "Identify the target by 'window_name' (substring) or by 'pid'. Returns the "
            "focused window's hwnd, pid, title, and rect."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "window_name": {"type": "string"},
                "pid": {"type": "integer"},
            },
            "required": [],
        },
    },
    "window_get_rect": {
        "handler": _tool_window_get_rect,
        "description": (
            "Return rect/title/class/pid for a window matched by 'window_name' substring "
            "(or pid). Use this BEFORE clicks at known visual coordinates so you can convert "
            "from window-relative to screen-absolute, or to know the window's size for scroll/drag."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "window_name": {"type": "string"},
                "pid": {"type": "integer"},
            },
            "required": [],
        },
    },
    "wait_for_window": {
        "handler": _tool_wait_for_window,
        "description": (
            "Poll until a window whose title contains the given substring appears, then return "
            "its hwnd/pid/title/rect. Replaces ad-hoc 'delay' calls when waiting for an app to "
            "launch or a dialog to open. timeout in seconds (default 10), poll in seconds (default 0.25)."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "window_name": {"type": "string"},
                "timeout": {"type": "number", "default": 10.0},
                "poll": {"type": "number", "default": 0.25},
            },
            "required": ["window_name"],
        },
    },
    "find_element": {
        "handler": _tool_find_element,
        "description": (
            "Find UI Automation elements under a process whose 'name' (window_text) contains "
            "the substring (case-insensitive), optionally filtered by 'control_type' "
            "(e.g. 'Button', 'Edit', 'TabItem'). Returns a list of matches with rect & center "
            "coordinates so you can click them with mouse_click x=center_x y=center_y."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "pid": {"type": "integer"},
                "name": {"type": "string"},
                "control_type": {"type": "string"},
                "max_depth": {"type": "integer", "default": 8},
                "visible_only": {"type": "boolean", "default": True},
            },
            "required": ["pid", "name"],
        },
    },
    "click_element": {
        "handler": _tool_click_element,
        "description": (
            "Find an element by name (and optional control_type) under the given pid and click "
            "its center. Auto-focuses the process first. Convenience wrapper for find_element + "
            "mouse_click. Returns the element's metadata and a few alternative matches."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "pid": {"type": "integer"},
                "name": {"type": "string"},
                "control_type": {"type": "string"},
                "button": {"type": "string", "enum": ["left", "right", "middle"], "default": "left"},
                "clicks": {"type": "integer", "default": 1},
                "double": {"type": "boolean", "default": False},
                "max_depth": {"type": "integer", "default": 8},
            },
            "required": ["pid", "name"],
        },
    },
    "screen_size": {
        "handler": _tool_screen_size,
        "description": (
            "Return primary monitor and virtual screen dimensions. Useful before computing "
            "absolute coordinates so you don't go off-screen."
        ),
        "schema": {"type": "object", "properties": {}, "required": []},
    },
}


# ---------------------------------------------------------------------------
# MCP server wiring
# ---------------------------------------------------------------------------

app = Server("winapi-mcp")


@app.list_tools()
async def _list_tools() -> list[types.Tool]:
    return [
        types.Tool(name=name, description=meta["description"], inputSchema=meta["schema"])
        for name, meta in TOOLS.items()
    ]


@app.call_tool()
async def _call_tool(name: str, arguments: dict) -> list[types.Content]:
    meta = TOOLS.get(name)
    if not meta:
        return _err(f"Unknown tool: {name}")
    try:
        return await meta["handler"](arguments or {})
    except Exception as exc:  # pragma: no cover
        return _err(f"Tool '{name}' raised: {exc}")


async def _amain() -> None:
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())


def main() -> int:
    asyncio.run(_amain())
    return 0


if __name__ == "__main__":
    sys.exit(main())
