<follow>
iterative-prompt.agent.md
</follow>

## UPD1

Давай сделаем модуль тренинговый, следуя инструкции по созданию модулей, который будет с индексом 650 и делать следующее. Вот у нас есть целый модуль про [400-installing-mcpyrex-mcp-python-toolbox](../../modules/400-installing-mcpyrex-mcp-python-toolbox/about.md) но там мне интересно только пару тулов, которые про `winapi` давай сделаем для них тут `skill.md` внутри модуля в на основе тех же скриптов, этот `skill` будет настраивать `MCP` сервер для работы через `MCP` как сделано в `mcpyrex`, `virtualenv` ставить питон и все такое прочее. Прям в папке скила (весь питоновский стафф пусть будет загитигнорен). Все что делают те тулы в `mcpyrex` пусть делает и тут. С минимумом изменений. Для этого форкни `mcpyrex` в `work` папку и исследуй его там как референс. Потом создай `modules/650-winapi/tools/SKILL.md` и рядом с ним весь остальной стафф в папке `modules/650-winapi/tools/scipts/`. Ну и пропиши в `skill.md` как настраивать `mcp.json` файл для `cursor` и `copilot` на `vscode` помня что там `mcpServers` и `servers` отличия в имени поля. И инструцию по запуску `MCP` в идеешках тоже надо, но это уже все пойдет в `walkthrough.md` модуля.   

`Tool` по производству скриншотов сделай таким, который сможет делать скриншоты не всего экрана, а либо заданного `child window`, либо в заданных координатах (`x1`, `x2`, `y1`, `y2`). Ну чтобы я мог универсально делать скриншоты в разных местах. Приатачивай скриншоты так, как мы это делали в [107-mcp-image-viewer](../../modules/107-mcp-image-viewer/about.md), атачем к ответу `MCP`. Пусть будет 2 команды: `screenshot window <window_name>` и `screenshot area <x1> <y1> <x2> <y2>`. И там и там результатом будет сохраненный в папку `output` скриншот с именем, включающим название окна или координаты. И приатаченный к ответу. 

Так же мне в дополнение к тем `tools` что есть нужны тулы для работы с мышью и клавиатурой (с клавиатурой вроде как там есть что-то по хоткеям, даже сценарии писать можно - мне то все точно надо). По мыши - прям всякие `drag and drop` чтобы можно было сделать. 

Короче главная идея, чтобы я могу дать тебе возможность через `MCP` давать доступ к моей операционке, и ты все мог прокликать сам, глядя за скриншотами. 

Тестируй все сам, я наблюдаю за твоей работой. Go.

### RESULT

Created module **650-winapi** — a self-contained Python MCP server that exposes
WinAPI tools (screenshots, mouse, keyboard, clipboard, process & window
inspection) over stdio. Used `work/400-task/mcp_server/tools/lng_winapi/` as
reference and ported the relevant tools into a single `server.py`.

Files created:

- [modules/650-winapi/about.md](../../modules/650-winapi/about.md) — module overview, prerequisites, learning outcome
- [modules/650-winapi/walkthrough.md](../../modules/650-winapi/walkthrough.md) — 6-part hands-on (inspect → install → boot test → register VS Code → register Cursor → drive desktop)
- [modules/650-winapi/tools/SKILL.md](../../modules/650-winapi/tools/SKILL.md) — AI-facing skill reference with both `servers` (VS Code) and `mcpServers` (Cursor) config blocks
- [modules/650-winapi/tools/scripts/server.py](../../modules/650-winapi/tools/scripts/server.py) — single-file MCP server with 11 tools registered through a `TOOLS` dict
- [modules/650-winapi/tools/scripts/install.ps1](../../modules/650-winapi/tools/scripts/install.ps1) — bootstrap (creates `.venv`, falls back to `virtualenv` if `venv` module is unavailable, idempotent)
- [modules/650-winapi/tools/scripts/run.ps1](../../modules/650-winapi/tools/scripts/run.ps1) — launcher used by `mcp.json` (forces UTF-8 stdio)
- [modules/650-winapi/tools/scripts/requirements.txt](../../modules/650-winapi/tools/scripts/requirements.txt) — `mcp`, `mss`, `pywin32`, `psutil`, `pyautogui`, `pyperclip`, `pywinauto`, `Pillow`
- [modules/650-winapi/tools/scripts/test_client.py](../../modules/650-winapi/tools/scripts/test_client.py) — Python smoke-test client (initialize → tools/list → screenshot_area → list_processes → clipboard round-trip)
- [modules/650-winapi/tools/scripts/output/](../../modules/650-winapi/tools/scripts/output/) — auto-created folder for saved screenshots (gitignored except `.gitkeep`)
- [modules/650-winapi/tools/.vscode/mcp.json](../../modules/650-winapi/tools/.vscode/mcp.json), [modules/650-winapi/tools/.cursor/mcp.json](../../modules/650-winapi/tools/.cursor/mcp.json) — ready-to-copy IDE configs
- [modules/650-winapi/tools/.gitignore](../../modules/650-winapi/tools/.gitignore) — keeps `.venv/`, `__pycache__/`, `output/` out of git
- [training-plan.md](../../training-plan.md) — added entry for module 650 between 620 and 900

Tools exposed by the server:
1. `screenshot_window` — capture window by title/class substring → MCP image content + saved PNG
2. `screenshot_area` — capture rectangle `(x1,y1)-(x2,y2)` → MCP image content + saved PNG
3. `mouse_move`, `mouse_click`, `mouse_drag` (drag-and-drop) — pyautogui-based
4. `send_hotkey` — port of mcpyrex's hotkey tool: hotkeys (`^t`, `%{F4}`), named keys, text, sequences (`[{type, value}, ...]`); optional `pid` to focus a process first
5. `clipboard_get` / `clipboard_set` — pyperclip
6. `list_processes`, `window_tree`, `get_window_content` — direct ports of mcpyrex tools (psutil + ctypes/pywinauto)

End-to-end test verified:
- `install.ps1` succeeds (after fallback to `virtualenv` for embedded Python)
- `test_client.py` confirms `initialize` returns `serverInfo: winapi-mcp`, `tools/list` returns all 11 tools, `screenshot_area` returns a 13 KB base64 PNG saved to `output/`, `list_processes filter=python` returns matches, clipboard round-trip works

## UPD2

Давай добавим сервер в [.vscode/mcp.json](../../.vscode/mcp.json) и я буду просить тебя сделать что-то в чате. Ну скажем открой хром, в нем зайди на гугл страничку, открой инспектор, и дойди до терминала, там вставь js инъекцию которая сделает снег на этой страничке. Сам смотри скриншотами что делаешь. И весь процесс сохраняй со скриншотами тут. А картинки в папку `img` и имену их как указано тут [organize-module-images.agent.md](../../instructions/lnd/organize-module-images.agent.md). Сохраняй прямо тут в `RESULT` блоке записывай что и как ты делаешь после каждого вызова `MCP` тула, мне интересно твое размышление. Go

### RESULT

**Step 1 — registered the server.** Added `winapi-mcp` to [.vscode/mcp.json](../../.vscode/mcp.json) right after `image-viewer-windows`:

```jsonc
"winapi-mcp": {
  "type": "stdio",
  "command": "powershell",
  "args": ["-ExecutionPolicy", "Bypass", "-File", "./modules/650-winapi/tools/scripts/run.ps1"]
}
```

**Step 2 — honest note about driving the demo from THIS chat.**

I cannot execute `screenshot_window`, `mouse_click`, etc. inside this very chat session. The reason is structural, not a missing skill:

- VS Code discovers MCP tools at the moment a chat session starts. The list of tools I receive at session start is frozen for this session.
- This chat began before `winapi-mcp` existed in `.vscode/mcp.json`, so the tools that the new server exposes (`screenshot_window`, `screenshot_area`, `mouse_*`, `send_hotkey`, `clipboard_*`, `list_processes`, `window_tree`, `get_window_content`) were never sent to me by the IDE.
- Therefore my "hands and eyes" for this demo do not actually exist in this session — calling them would just be me writing fake tool-call blocks. I will not do that.

**Step 3 — what to do to run the demo for real.**

1. In VS Code, open `.vscode/mcp.json`. Above the new `"winapi-mcp"` block VS Code shows an inline action bar — click **Start**. Confirm the Output panel → **Model Context Protocol** says `winapi-mcp ... Discovered 11 tools`.
2. Open a **new** Copilot Chat in **Agent Mode** (the existing one will still be missing the tools).
3. Paste a prompt like the one below — it tells the agent to drive the demo, screenshot every meaningful step, save the PNGs into `requests/650-winapi/img/`, and append its reasoning back into this same `RESULT` block.

Ready-to-paste prompt for the new chat:

> You have access to the `winapi-mcp` MCP server. Run this demo end-to-end and
> document every step in `requests/650-winapi/main.prompt.md` under the
> `### RESULT` of UPD2.
>
> Naming convention for screenshots — follow
> [`instructions/lnd/organize-module-images.agent.md`](../../instructions/lnd/organize-module-images.agent.md):
> save every PNG produced by `screenshot_window` / `screenshot_area` into
> `requests/650-winapi/img/MM-short-description.png` (sequential `MM` from `01`,
> 2-5 lowercase words, hyphenated). The MCP server saves originals to
> `modules/650-winapi/tools/scripts/output/` — copy/rename them into
> `requests/650-winapi/img/` after each capture.
>
> Demo steps:
> 1. `list_processes filter=chrome only_with_windows=true`. If empty, launch
>    Chrome (PowerShell: `Start-Process chrome`). Re-list. Pick the PID with a
>    real main window.
> 2. `screenshot_window window_name="Google Chrome"` → save as
>    `01-chrome-just-launched.png`. Describe what is visible.
> 3. Use `send_hotkey` with that PID, hotkey `^l` (focus address bar), then
>    `text: "https://www.google.com"`, then `key: "ENTER"`. Wait ~1.5 s.
>    `screenshot_window` → `02-google-loaded.png`.
> 4. `send_hotkey` with that PID, hotkey `^+i` to open DevTools.
>    `screenshot_window` → `03-devtools-open.png`. If DevTools opened in a
>    separate window, also `screenshot_window window_name="DevTools"`.
> 5. Switch to the Console tab — `send_hotkey` hotkey `^+j` (or click the
>    "Console" tab using `mouse_click` after locating it via
>    `get_window_content target_window="DevTools"`).
>    `screenshot_window` → `04-console-tab.png`.
> 6. Inject the snow JS by `clipboard_set` then `send_hotkey` `^v`, `key
>    ENTER`. Use this payload (single line):
>    ```js
>    (()=>{const c=document.createElement('canvas');Object.assign(c.style,{position:'fixed',inset:'0',pointerEvents:'none',zIndex:'2147483647'});c.width=innerWidth;c.height=innerHeight;document.body.appendChild(c);const x=c.getContext('2d');const f=Array.from({length:200},()=>({x:Math.random()*c.width,y:Math.random()*c.height,r:1+Math.random()*3,s:0.5+Math.random()*1.5}));(function t(){x.clearRect(0,0,c.width,c.height);x.fillStyle='white';for(const k of f){x.beginPath();x.arc(k.x,k.y,k.r,0,7);x.fill();k.y+=k.s;if(k.y>c.height)k.y=0;}requestAnimationFrame(t);})();})();
>    ```
> 7. `screenshot_window` of the main Chrome window → `05-snow-running.png`.
>    Describe what changed visually.
>
> After each `screenshot_*` call, append a short paragraph into the RESULT
> block of UPD2 explaining (a) what you observed in the image, (b) what you
> decided to do next and why, (c) which tool you called next. Commit at the
> end with the iterative-prompt rules.

**Step 4 — why I am not also performing it via a sub-agent.**

A sub-agent would inherit the same fixed tool list (it spawns from the parent
session), so it would not see `winapi-mcp` either. The only path is a fresh
Agent Mode chat after the server is started — the IDE's MCP discovery runs at
session boot.

## UPD3

Я запустил сервер. Отвечай мне лаконично тут что дальше
![alt text](image.png) Go

### RESULT

Вижу `winapi-mcp ... Discovered 11 tools` — сервер живой.

Этот чат запустился до того как `winapi-mcp` появился в `mcp.json`, поэтому у меня самого его тулов нет (список тулов фиксируется на старте сессии). Чтобы прогнать демо:

1. Открой **новый** Copilot Chat → Agent Mode (в этом же воркспейсе).
2. Вставь туда промпт из RESULT-блока UPD2 (длинный, начиная с *"You have access to the `winapi-mcp` MCP server..."*).
3. Тот новый чат будет видеть все 11 тулов и сможет реально кликать/скриншотить/вставлять JS, дописывая свои размышления сюда же — в этот файл.

Я остаюсь в polling-loop здесь — пиши `## UPD4` если нужно что-то ещё со стороны кода/конфига.
