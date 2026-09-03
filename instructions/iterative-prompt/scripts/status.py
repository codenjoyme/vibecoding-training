"""Print the iterative-prompt runtime status as JSON.

The script is intentionally standalone so it also works when the brick is
copied without the rest of the factory. Environment values come from the
process first, then from the nearest discovered ``.dark-factory/.env`` or
``.env`` files while walking towards the filesystem root.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Optional


_SETTING_NAMES = ("ITERATIVE_PROMPT_AUTOCOMMIT", "ITERATIVE_PROMPT_TRACE")
_STATUS_DIR_NAME = "ITERATIVE_PROMPT_STATUS_DIR"
_DEFAULT_STATUS_DIR = Path(".dark-factory") / "teams" / "iterative_prompt"
_TRUE_VALUES = frozenset(("1", "true", "yes", "on"))
_FALSE_VALUES = frozenset(("0", "false", "no", "off"))
_UPD_ID_RE = re.compile(r"^UPD\d+$", re.IGNORECASE)
_UPD_HEADER_LINE_RE = re.compile(
    r"^##[ \t]+(?P<id>UPD\d+)(?:[ \t]+\(tracked:.*\))?[ \t]*$",
    re.IGNORECASE,
)
_RESULT_HEADER_LINE_RE = re.compile(r"^###[ \t]+RESULT\b", re.IGNORECASE)
_STATUS_FIELD_ORDER = (
    "status",
    "upd-id",
    "helm-name",
    "autocommit",
    "trace",
    "hash",
    "timestamp",
    "git",
    "started_from",
    "helm-log",
    "upd-line",
    "result-lines",
)


def _start_directory(start: Optional[Path] = None) -> Path:
    path = (start or Path.cwd()).expanduser().resolve()
    return path.parent if path.is_file() else path


def _ancestors(start: Optional[Path] = None) -> list[Path]:
    here = _start_directory(start)
    return [here, *here.parents]


def discover_env_files(start: Optional[Path] = None) -> list[Path]:
    """Return discovered env files in nearest-first precedence order."""
    seen: set[Path] = set()
    result: list[Path] = []
    for ancestor in _ancestors(start):
        for relative in (Path(".dark-factory") / ".env", Path(".env")):
            candidate = (ancestor / relative).resolve()
            if candidate in seen:
                continue
            seen.add(candidate)
            if candidate.is_file():
                result.append(candidate)
    return result


def parse_env_file(path: Path) -> dict[str, str]:
    """Parse the simple KEY=value format used by the env-loader brick."""
    values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return values
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        values[key] = value
    return values


def resolve_settings(
    start: Optional[Path] = None,
    environ: Optional[Mapping[str, str]] = None,
) -> dict[str, bool]:
    """Resolve iterative-prompt booleans with environment precedence."""
    source = os.environ if environ is None else environ
    raw_values: dict[str, Optional[str]] = {
        name: source.get(name) or None for name in _SETTING_NAMES
    }
    unresolved = {name for name, value in raw_values.items() if value is None}
    for env_file in discover_env_files(start):
        if not unresolved:
            break
        parsed = parse_env_file(env_file)
        for name in tuple(unresolved):
            value = parsed.get(name)
            if value:
                raw_values[name] = value
                unresolved.remove(name)
    return {
        name: parse_bool(raw_values[name], default=True)
        for name in _SETTING_NAMES
    }


def resolve_status_dir(
    start: Optional[Path] = None,
    environ: Optional[Mapping[str, str]] = None,
) -> Path:
    """Resolve the JSONL directory, defaulting to the factory team directory."""
    source = os.environ if environ is None else environ
    raw_value = source.get(_STATUS_DIR_NAME) or None
    if raw_value is None:
        for env_file in discover_env_files(start):
            raw_value = parse_env_file(env_file).get(_STATUS_DIR_NAME) or None
            if raw_value is not None:
                break
    configured = Path(raw_value).expanduser() if raw_value else _DEFAULT_STATUS_DIR
    if configured.is_absolute():
        return configured.resolve()
    return (_start_directory(start) / configured).resolve()


def parse_bool(value: Optional[str], *, default: bool) -> bool:
    """Convert common dotenv boolean spellings, falling back safely."""
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in _TRUE_VALUES:
        return True
    if normalized in _FALSE_VALUES:
        return False
    return default


def discover_repositories(start: Optional[Path] = None) -> list[Path]:
    """Find git repositories from the starting directory towards its parents."""
    repositories: list[Path] = []
    seen: set[Path] = set()
    for candidate in _ancestors(start):
        if not (candidate / ".git").exists():
            continue
        try:
            result = subprocess.run(
                ["git", "-C", str(candidate), "rev-parse", "--show-toplevel"],
                capture_output=True,
                check=False,
                text=True,
                timeout=5,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if result.returncode != 0 or not result.stdout.strip():
            continue
        repository = Path(result.stdout.strip()).resolve()
        if repository not in seen:
            seen.add(repository)
            repositories.append(repository)
    return repositories


def latest_commit(repository: Path) -> str:
    """Return a repository's short HEAD hash, or an empty string if unavailable."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repository), "log", "-1", "--format=%h"],
            capture_output=True,
            check=False,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def git_snapshot(start: Optional[Path] = None) -> dict[str, list[str]]:
    """Return latest commits and absolute repository paths in nested-first order."""
    repositories = discover_repositories(start)
    return {
        "last_commits": [latest_commit(repository) for repository in repositories],
        "paths": [str(repository) for repository in repositories],
    }


def _absolute_path(value: str | Path) -> str:
    return str(Path(value).expanduser().resolve())


def _helm_name(helm_log: Optional[str | Path]) -> Optional[str]:
    """Return the path below ``work`` joined with ``_`` and no prompt suffix."""
    if helm_log is None:
        return None
    path = Path(helm_log).expanduser()
    filename = path.name
    suffix = ".prompt.md"
    file_name = filename[: -len(suffix)] if filename.lower().endswith(suffix) else path.stem
    parent_parts = list(path.parent.parts)
    work_indexes = [
        index
        for index, part in enumerate(parent_parts)
        if part.casefold() == "work"
    ]
    if work_indexes:
        name_parts = parent_parts[work_indexes[-1] + 1 :] + [file_name]
        return "_".join(part for part in name_parts if part) or None
    folder = path.parent.name
    if not folder:
        return file_name or None
    return f"{folder}_{file_name}" if file_name else folder


def _normalize_upd_id(value: str) -> str:
    normalized = value.strip().upper()
    if not _UPD_ID_RE.fullmatch(normalized):
        raise ValueError(f"upd-id must match UPD<number>, got {value!r}")
    return normalized


def _format_timestamp(now: Optional[datetime] = None) -> str:
    value = now or datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


def _status_hash(timestamp: str, helm_log: Optional[str], upd_id: Optional[str]) -> str:
    hash_input = json.dumps(
        {
            "timestamp": timestamp,
            "helm-log": helm_log,
            "upd-id": upd_id,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]


def build_status(
    start: Optional[Path] = None,
    *,
    environ: Optional[Mapping[str, str]] = None,
    now: Optional[datetime] = None,
    status_value: Optional[str] = None,
    started_from: Optional[str] = None,
    helm_log: Optional[str] = None,
    upd_id: Optional[str] = None,
    upd_line: Optional[int] = None,
    result_lines: Optional[list[int]] = None,
) -> dict[str, object]:
    """Build the JSON-serializable status payload."""
    settings = resolve_settings(start, environ)
    timestamp = _format_timestamp(now)
    git = git_snapshot(start)
    status_hash = _status_hash(timestamp, helm_log, upd_id)
    return {
        "status": status_value,
        "upd-id": upd_id,
        "helm-name": _helm_name(helm_log),
        "autocommit": settings["ITERATIVE_PROMPT_AUTOCOMMIT"],
        "trace": settings["ITERATIVE_PROMPT_TRACE"],
        "hash": status_hash,
        "timestamp": timestamp,
        "git": git,
        "started_from": started_from,
        "helm-log": helm_log,
        "upd-line": upd_line,
        "result-lines": result_lines,
    }


def pretty_json(payload: object) -> str:
    """Render a payload as human-readable UTF-8 JSON with a final newline."""
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def compact_json(payload: object) -> str:
    """Render one JSONL record without pretty-print whitespace."""
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def normalize_status_record(record: Mapping[str, object]) -> dict[str, object]:
    """Serialize old and current records in the current canonical field order."""
    normalized = dict(record)
    helm_log = normalized.get("helm-log")
    if isinstance(helm_log, str):
        normalized["helm-name"] = _helm_name(helm_log)
    return {field: normalized.get(field) for field in _STATUS_FIELD_ORDER}


def rewrite_status_log(path: Path) -> int:
    """Migrate every valid JSONL record to the current status schema in place."""
    records = _read_status_records(path)
    if not records:
        return 0
    payload = "".join(compact_json(normalize_status_record(record)) + "\n" for record in records)
    temporary_path: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="\n",
            delete=False,
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
        ) as stream:
            temporary_path = Path(stream.name)
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except OSError:
                pass
    return len(records)


def _status_log_path(
    start: Optional[Path],
    environ: Optional[Mapping[str, str]],
) -> Path:
    return resolve_status_dir(start, environ) / "status.jsonl"


def _append_status_record(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(compact_json(payload) + "\n")


def _read_status_records(path: Path) -> list[dict[str, object]]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    records: list[dict[str, object]] = []
    for line in lines:
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            records.append(record)
    return records


def _find_start_record(path: Path, started_from: str) -> Optional[dict[str, object]]:
    for record in reversed(_read_status_records(path)):
        if record.get("status") != "start":
            continue
        if record.get("hash") == started_from or record.get("started_from") == started_from:
            return record
    return None


def _find_upd_coordinates(
    path: Path,
    upd_id: str,
    *,
    missing_at_end: bool,
) -> tuple[int, list[int]]:
    """Return the 1-based UPD header and RESULT lines for one prompt block."""
    if not path.is_file():
        raise FileNotFoundError(f"helm-log not found: {path}")

    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        raise OSError(f"could not read helm-log: {path}") from exc

    normalized_id = _normalize_upd_id(upd_id)
    upd_line: Optional[int] = None
    result_lines: list[int] = []
    for line_number, line in enumerate(lines, start=1):
        header_match = _UPD_HEADER_LINE_RE.match(line)
        if header_match:
            if upd_line is not None:
                break
            if header_match.group("id").upper() == normalized_id:
                upd_line = line_number
            continue
        if upd_line is not None and _RESULT_HEADER_LINE_RE.match(line):
            result_lines.append(line_number)

    if upd_line is None:
        if missing_at_end:
            return len(lines) + 1, []
        raise ValueError(f"UPD header not found in {path}: {normalized_id}")
    return upd_line, result_lines


def _track_helm_log(
    path: Path,
    upd_id: str,
    start_hash: str,
    finish_hash: str,
) -> None:
    """Replace the matching UPD header with its start/finish tracking pair."""
    if not path.is_file():
        raise FileNotFoundError(f"helm-log not found: {path}")

    with path.open("r", encoding="utf-8", errors="replace", newline="") as stream:
        lines = stream.readlines()

    header_re = re.compile(
        r"^(?P<prefix>##[ \t]+)(?P<id>UPD\d+)"
        r"(?:[ \t]+\(tracked:.*\))?[ \t]*(?P<ending>\r\n|\n|\r)?$",
        re.IGNORECASE,
    )
    normalized_id = _normalize_upd_id(upd_id)
    updated = False
    for index, line in enumerate(lines):
        match = header_re.match(line)
        if match and match.group("id").upper() == normalized_id:
            ending = match.group("ending") or ""
            lines[index] = (
                f"{match.group('prefix')}{normalized_id} "
                f"(tracked: {start_hash} : {finish_hash}){ending}"
            )
            updated = True
            break

    if not updated:
        raise ValueError(f"UPD header not found in {path}: {normalized_id}")

    temporary_path: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="",
            delete=False,
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
        ) as stream:
            temporary_path = Path(stream.name)
            stream.write("".join(lines))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except OSError:
                pass


def start_status(
    start: Optional[Path],
    helm_log: str | Path,
    upd_id: str,
    *,
    environ: Optional[Mapping[str, str]] = None,
    now: Optional[datetime] = None,
) -> dict[str, object]:
    """Create and optionally persist a start record for one UPD."""
    normalized_upd_id = _normalize_upd_id(upd_id)
    absolute_helm_log = _absolute_path(helm_log)
    upd_line, _ = _find_upd_coordinates(
        Path(absolute_helm_log),
        normalized_upd_id,
        missing_at_end=True,
    )
    payload = build_status(
        start,
        environ=environ,
        now=now,
        status_value="start",
        helm_log=absolute_helm_log,
        upd_id=normalized_upd_id,
        upd_line=upd_line,
    )
    if payload["trace"]:
        _append_status_record(_status_log_path(start, environ), payload)
    return payload


def finish_status(
    start: Optional[Path],
    started_from: str,
    *,
    environ: Optional[Mapping[str, str]] = None,
    now: Optional[datetime] = None,
) -> dict[str, object]:
    """Finish a tracked UPD using metadata recovered from its start record."""
    log_path = _status_log_path(start, environ)
    if not resolve_settings(start, environ)["ITERATIVE_PROMPT_TRACE"]:
        return build_status(
            start,
            environ=environ,
            now=now,
            status_value="finish",
            started_from=started_from,
        )

    start_record = _find_start_record(log_path, started_from)
    if start_record is None:
        raise ValueError(f"start record not found for hash {started_from!r}: {log_path}")
    helm_log = start_record.get("helm-log")
    upd_id = start_record.get("upd-id")
    if not isinstance(helm_log, str) or not isinstance(upd_id, str):
        raise ValueError(f"start record is missing helm-log or upd-id: {started_from!r}")

    payload = build_status(
        start,
        environ=environ,
        now=now,
        status_value="finish",
        started_from=started_from,
        helm_log=helm_log,
        upd_id=upd_id,
    )
    _track_helm_log(Path(helm_log), upd_id, started_from, str(payload["hash"]))
    upd_line, result_lines = _find_upd_coordinates(
        Path(helm_log),
        upd_id,
        missing_at_end=False,
    )
    payload["upd-line"] = upd_line
    payload["result-lines"] = result_lines
    _append_status_record(log_path, payload)
    return payload


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    operation = parser.add_mutually_exclusive_group()
    operation.add_argument("--start", action="store_true", help="Record the start of an UPD.")
    operation.add_argument("--finish", action="store_true", help="Record the finish of an UPD.")
    operation.add_argument("--migrate", action="store_true", help="Rewrite status.jsonl using the current field schema.")
    parser.add_argument(
        "--cwd",
        type=Path,
        default=None,
        help="Directory used for .env discovery and nested git lookup (default: cwd).",
    )
    parser.add_argument("--helm-log", dest="helm_log", default=None)
    parser.add_argument("--upd-id", "--upd_id", dest="upd_id", default=None)
    parser.add_argument("--started-from", "--started_from", dest="started_from", default=None)
    args = parser.parse_args(argv)
    try:
        if args.start:
            if args.helm_log is None or args.upd_id is None:
                parser.error("--start requires --helm-log and --upd-id")
            payload = start_status(args.cwd, args.helm_log, args.upd_id)
        elif args.finish:
            if args.started_from is None:
                parser.error("--finish requires --started-from")
            payload = finish_status(args.cwd, args.started_from)
        elif args.migrate:
            status_path = _status_log_path(args.cwd, None)
            count = rewrite_status_log(status_path)
            payload = {"status": "migrate", "upd-id": None, "helm-name": None, "records": count}
        else:
            payload = build_status(args.cwd)
    except (FileNotFoundError, OSError, ValueError) as exc:
        parser.exit(2, f"status.py: {exc}\n")
    sys.stdout.write(pretty_json(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())