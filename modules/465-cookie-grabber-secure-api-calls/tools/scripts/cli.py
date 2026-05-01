#!/usr/bin/env python3
"""
Cookie CLI — make authenticated HTTP requests using encrypted cookies.

Usage:
  python cli.py status                              check if cookies are stored
  python cli.py info                                show metadata (no plaintext values)
  python cli.py get  --url URL [--header K=V ...]   GET with decrypted cookies
  python cli.py post --url URL --data '{...}'       POST with decrypted cookies
  python cli.py clear                               delete stored cookie file

Credentials:
  Priority order for master password:
    1. --password VALUE       explicit flag (visible in shell history — use only in safe environments)
    2. --ask-password / -P    force interactive prompt (getpass — hidden input, no echo)
    3. MASTER_PASSWORD env    environment variable
    4. automatic prompt       if none of the above is set, getpass is called automatically

  COOKIE_FILE env var  — or --cookie-file flag (default: ./data/cookies.enc)
"""

import argparse
import base64
import getpass
import json
import os
import sys
from pathlib import Path

import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DEFAULT_COOKIE_FILE = Path(os.getenv("COOKIE_FILE", "./data/cookies.enc"))


# ── Crypto ────────────────────────────────────────────────────────────────────

def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    return kdf.derive(password.encode("utf-8"))


def _decrypt(blob: dict, password: str) -> list[dict]:
    salt = base64.b64decode(blob["salt"])
    iv = base64.b64decode(blob["iv"])
    ciphertext = base64.b64decode(blob["ciphertext"])
    key = _derive_key(password, salt)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(iv, ciphertext, None)
    return json.loads(plaintext.decode("utf-8"))


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_blob(cookie_file: str) -> dict:
    cf = Path(cookie_file)
    if not cf.exists():
        print("❌ No cookies stored. Run the browser extension first.", file=sys.stderr)
        sys.exit(1)
    return json.loads(cf.read_text(encoding="utf-8"))


def _resolve_password(args: argparse.Namespace) -> str:
    """Determine master password from args → env → interactive prompt."""
    if getattr(args, "password", None):
        return args.password
    if getattr(args, "ask_password", False):
        return getpass.getpass("Master password: ")
    env_pw = os.getenv("MASTER_PASSWORD")
    if env_pw:
        return env_pw
    return getpass.getpass("Master password: ")


def _load_cookies(cookie_file: str, args: argparse.Namespace | None = None) -> tuple[list[dict], str]:
    blob = _load_blob(cookie_file)
    password = _resolve_password(args) if args is not None else (
        os.getenv("MASTER_PASSWORD") or getpass.getpass("Master password: ")
    )
    try:
        cookies = _decrypt(blob, password)
    except Exception:
        print("❌ Decryption failed — wrong master password or corrupted file.", file=sys.stderr)
        sys.exit(1)
    return cookies, blob.get("domain", "")


def _cookies_dict(cookies: list[dict]) -> dict[str, str]:
    return {c["name"]: c["value"] for c in cookies}


def _parse_headers(header_list: list[str] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for h in (header_list or []):
        if "=" in h:
            k, v = h.split("=", 1)
            result[k.strip()] = v.strip()
    return result


def _print_response(resp: requests.Response) -> None:
    print(f"HTTP {resp.status_code}")
    try:
        print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(resp.text)


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_status(args: argparse.Namespace) -> None:
    cf = Path(args.cookie_file)
    if cf.exists():
        blob = json.loads(cf.read_text(encoding="utf-8"))
        print(f"✅ Cookies stored")
        print(f"   Domain  : {blob.get('domain', '?')}")
        print(f"   File    : {cf.resolve()}")
    else:
        print("❌ No cookies stored. Use the Chrome extension to grab and send cookies.")


def cmd_info(args: argparse.Namespace) -> None:
    blob = _load_blob(args.cookie_file)
    print(f"Domain  : {blob.get('domain', '?')}")
    print(f"Version : {blob.get('version', '?')}")
    print("Cookies : [encrypted — values hidden; use 'get' or 'post' to make API calls]")


def cmd_clear(args: argparse.Namespace) -> None:
    cf = Path(args.cookie_file)
    if cf.exists():
        cf.unlink()
        print("✅ Cookie file deleted.")
    else:
        print("Nothing to clear.")


def cmd_get(args: argparse.Namespace) -> None:
    cookies, _ = _load_cookies(args.cookie_file, args)
    headers = _parse_headers(args.header)
    resp = requests.get(args.url, cookies=_cookies_dict(cookies), headers=headers, timeout=30)
    _print_response(resp)


def cmd_post(args: argparse.Namespace) -> None:
    cookies, _ = _load_cookies(args.cookie_file, args)
    headers = _parse_headers(args.header)
    body = json.loads(args.data) if args.data else {}
    resp = requests.post(args.url, json=body, cookies=_cookies_dict(cookies), headers=headers, timeout=30)
    _print_response(resp)


# ── Argument parser ───────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Cookie CLI — authenticated API calls using encrypted browser cookies",
    )
    p.add_argument(
        "--cookie-file",
        default=str(DEFAULT_COOKIE_FILE),
        help="Path to encrypted cookie file (default: ./data/cookies.enc)",
    )
    pw_group = p.add_mutually_exclusive_group()
    pw_group.add_argument(
        "--password",
        metavar="PASSWORD",
        help="Master password as plain text flag (use only in secure environments — visible in shell history)",
    )
    pw_group.add_argument(
        "--ask-password", "-P",
        action="store_true",
        dest="ask_password",
        help="Force interactive password prompt (hidden input via getpass)",
    )
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Check if cookies are stored")
    sub.add_parser("info", help="Show cookie metadata without decrypting values")
    sub.add_parser("clear", help="Delete stored cookie file")

    g = sub.add_parser("get", help="HTTP GET with decrypted cookies")
    g.add_argument("--url", required=True, help="Target URL")
    g.add_argument("--header", nargs="*", metavar="K=V", help="Extra request headers")

    po = sub.add_parser("post", help="HTTP POST with decrypted cookies")
    po.add_argument("--url", required=True, help="Target URL")
    po.add_argument("--data", help='JSON request body (e.g. \'{"key":"val"}\')')
    po.add_argument("--header", nargs="*", metavar="K=V", help="Extra request headers")

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    dispatch = {
        "status": cmd_status,
        "info": cmd_info,
        "clear": cmd_clear,
        "get": cmd_get,
        "post": cmd_post,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
