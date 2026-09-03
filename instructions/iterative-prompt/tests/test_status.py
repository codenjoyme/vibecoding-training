from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "status.py"
SPEC = importlib.util.spec_from_file_location("iterative_prompt_status", SCRIPT)
assert SPEC and SPEC.loader
status = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(status)


def run_git(directory: Path, *arguments: str) -> None:
    environment = os.environ.copy()
    environment["GIT_CONFIG_NOSYSTEM"] = "1"
    subprocess.run(
        ["git", "-C", str(directory), *arguments],
        check=True,
        capture_output=True,
        env=environment,
    )


class StatusTests(unittest.TestCase):
    def test_helm_name_uses_folder_and_prompt_file_stem(self) -> None:
        self.assertEqual(
            status._helm_name(
                r"C:\work\iterative-prompt\main.prompt.md"
            ),
            "iterative-prompt_main",
        )
        self.assertEqual(
            status._helm_name(
                r"C:\factory\work\tokenomics\reference1\main.prompt.md"
            ),
            "tokenomics_reference1_main",
        )
        self.assertEqual(
            status._helm_name(r"C:\work\common\audit.prompt.md"),
            "common_audit",
        )

    def test_status_fields_have_canonical_order(self) -> None:
        payload = status.build_status(
            Path("."),
            environ={
                "ITERATIVE_PROMPT_AUTOCOMMIT": "true",
                "ITERATIVE_PROMPT_TRACE": "true",
            },
            now=datetime(2024, 6, 5, 12, 0, tzinfo=timezone.utc),
            status_value="start",
            helm_log=r"C:\work\iterative-prompt\main.prompt.md",
            upd_id="UPD12",
        )
        self.assertEqual(
            list(payload)[:3],
            ["status", "upd-id", "helm-name"],
        )
        self.assertEqual(payload["helm-name"], "iterative-prompt_main")

    def test_rewrite_status_log_adds_helm_name_and_current_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "status.jsonl"
            path.write_text(
                json.dumps(
                    {
                        "autocommit": True,
                        "trace": True,
                        "hash": "12345678",
                        "timestamp": "2024-06-05T12:00:00Z",
                        "git": {"last_commits": [], "paths": []},
                        "status": "start",
                        "started_from": None,
                        "helm-name": "reference1_main",
                        "helm-log": r"C:\factory\work\tokenomics\reference1\main.prompt.md",
                        "upd-id": "UPD12",
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            self.assertEqual(status.rewrite_status_log(path), 1)
            line = path.read_text(encoding="utf-8").splitlines()[0]
            record = json.loads(line)
            self.assertEqual(
                list(record),
                [
                    "status", "upd-id", "helm-name", "autocommit", "trace",
                    "hash", "timestamp", "git", "started_from", "helm-log",
                    "upd-line", "result-lines",
                ],
            )
            self.assertEqual(record["helm-name"], "tokenomics_reference1_main")
            self.assertIsNone(record["upd-line"])
            self.assertIsNone(record["result-lines"])

    def test_nearest_env_values_win_and_process_values_have_priority(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            nested = root / "nested"
            nested.mkdir()
            (root / ".env").write_text(
                "ITERATIVE_PROMPT_AUTOCOMMIT=false\nITERATIVE_PROMPT_TRACE=false\n",
                encoding="utf-8",
            )
            (nested / ".env").write_text(
                "ITERATIVE_PROMPT_AUTOCOMMIT=true\n",
                encoding="utf-8",
            )

            settings = status.resolve_settings(nested, environ={})
            self.assertEqual(settings, {
                "ITERATIVE_PROMPT_AUTOCOMMIT": True,
                "ITERATIVE_PROMPT_TRACE": False,
            })
            overridden = status.resolve_settings(
                nested,
                environ={"ITERATIVE_PROMPT_AUTOCOMMIT": "false"},
            )
            self.assertFalse(overridden["ITERATIVE_PROMPT_AUTOCOMMIT"])

    def test_nested_repositories_are_reported_inner_first(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            outer = root / "outer"
            inner = outer / "inner"
            start = inner / "deep"
            inner.mkdir(parents=True)
            start.mkdir()

            run_git(outer, "init", "-q")
            (outer / "outer.txt").write_text("outer\n", encoding="utf-8")
            run_git(outer, "add", "outer.txt")
            run_git(
                outer,
                "-c",
                "user.name=Status Test",
                "-c",
                "user.email=status@example.invalid",
                "commit",
                "-qm",
                "outer",
            )

            run_git(inner, "init", "-q")
            (inner / "inner.txt").write_text("inner\n", encoding="utf-8")
            run_git(inner, "add", "inner.txt")
            run_git(
                inner,
                "-c",
                "user.name=Status Test",
                "-c",
                "user.email=status@example.invalid",
                "commit",
                "-qm",
                "inner",
            )

            repositories = status.discover_repositories(start)
            self.assertEqual(repositories, [inner.resolve(), outer.resolve()])
            payload = status.build_status(
                start,
                environ={
                    "ITERATIVE_PROMPT_AUTOCOMMIT": "true",
                    "ITERATIVE_PROMPT_TRACE": "true",
                },
                now=datetime(2024, 6, 5, 12, 0, tzinfo=timezone.utc),
            )
            self.assertEqual(payload["git"]["paths"], [str(inner.resolve()), str(outer.resolve())])
            self.assertEqual(len(payload["git"]["last_commits"]), 2)
            self.assertEqual(payload["timestamp"], "2024-06-05T12:00:00Z")
            expected_input = json.dumps(
                {
                    "timestamp": payload["timestamp"],
                    "helm-log": payload["helm-log"],
                    "upd-id": payload["upd-id"],
                },
                sort_keys=True,
                separators=(",", ":"),
            )
            expected_hash = hashlib.sha256(expected_input.encode("utf-8")).hexdigest()[:8]
            self.assertEqual(payload["hash"], expected_hash)

    def test_hash_ignores_git_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            timestamp = datetime(2024, 6, 5, 12, 0, tzinfo=timezone.utc)
            metadata = {
                "helm_log": str(root / "main.prompt.md"),
                "upd_id": "UPD10",
            }
            with patch.object(
                status,
                "git_snapshot",
                side_effect=[
                    {"last_commits": ["before"], "paths": ["/repo"]},
                    {"last_commits": ["after"], "paths": ["/repo"]},
                ],
            ):
                before = status.build_status(root, now=timestamp, **metadata)
                after = status.build_status(root, now=timestamp, **metadata)

            self.assertNotEqual(before["git"], after["git"])
            self.assertEqual(before["hash"], after["hash"])

    def test_no_repositories_produces_empty_git_lists(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            payload = status.build_status(Path(temporary), environ={})
            self.assertEqual(payload["git"], {"last_commits": [], "paths": []})
            self.assertTrue(payload["autocommit"])
            self.assertTrue(payload["trace"])

    def test_pretty_json_is_indented_valid_json_with_final_newline(self) -> None:
        payload = {
            "autocommit": True,
            "trace": False,
            "git": {"last_commits": [], "paths": []},
        }
        rendered = status.pretty_json(payload)
        self.assertEqual(
            rendered,
            '{\n'
            '  "autocommit": true,\n'
            '  "trace": false,\n'
            '  "git": {\n'
            '    "last_commits": [],\n'
            '    "paths": []\n'
            '  }\n'
            '}\n',
        )
        self.assertEqual(json.loads(rendered), payload)

    def test_start_and_finish_write_jsonl_and_track_helm_log(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            helm_log = root / "work" / "iterative-prompt" / "main.prompt.md"
            helm_log.parent.mkdir(parents=True)
            helm_log.write_text(
                "Preamble.\n## UPD8 \n\nRequest body.\n## UPD9\n\nFuture body.\n",
                encoding="utf-8",
            )
            (root / ".env").write_text(
                "ITERATIVE_PROMPT_STATUS_DIR=.dark-factory/teams/iterative_prompt\n",
                encoding="utf-8",
            )
            environment = {
                "ITERATIVE_PROMPT_AUTOCOMMIT": "true",
                "ITERATIVE_PROMPT_TRACE": "true",
            }
            start_time = datetime(2024, 6, 5, 12, 0, tzinfo=timezone.utc)
            start_payload = status.start_status(
                root,
                helm_log,
                "upd8",
                environ=environment,
                now=start_time,
            )
            status_path = root / ".dark-factory" / "teams" / "iterative_prompt" / "status.jsonl"
            self.assertTrue(status_path.is_file())
            start_line = status_path.read_text(encoding="utf-8").splitlines()[0]
            self.assertNotIn("\n", start_line)
            self.assertNotIn(": ", start_line)
            stored_start = json.loads(start_line)
            self.assertEqual(stored_start, start_payload)
            self.assertEqual(stored_start["status"], "start")
            self.assertIsNone(stored_start["started_from"])
            self.assertEqual(stored_start["helm-log"], str(helm_log.resolve()))
            self.assertEqual(stored_start["upd-id"], "UPD8")
            self.assertEqual(stored_start["helm-name"], "iterative-prompt_main")
            self.assertEqual(stored_start["upd-line"], 2)
            self.assertIsNone(stored_start["result-lines"])

            helm_log.write_text(
                "Preamble.\n## UPD8 \n\nRequest body.\n### RESULT (UPD8)\nDone.\n"
                "### RESULT (UPD8)\nContinued.\n## UPD9\n\nFuture body.\n"
                "### RESULT (UPD9)\nFuture done.\n",
                encoding="utf-8",
            )

            finish_payload = status.finish_status(
                root,
                str(start_payload["hash"]),
                environ=environment,
                now=start_time + timedelta(seconds=1),
            )
            records = [json.loads(line) for line in status_path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(records), 2)
            self.assertEqual(records[1], finish_payload)
            self.assertEqual(finish_payload["status"], "finish")
            self.assertEqual(finish_payload["started_from"], start_payload["hash"])
            self.assertEqual(finish_payload["helm-log"], str(helm_log.resolve()))
            self.assertEqual(finish_payload["upd-id"], "UPD8")
            self.assertEqual(finish_payload["helm-name"], "iterative-prompt_main")
            self.assertEqual(finish_payload["upd-line"], 2)
            self.assertEqual(finish_payload["result-lines"], [5, 7])
            self.assertEqual(
                helm_log.read_text(encoding="utf-8"),
                f"Preamble.\n## UPD8 (tracked: {start_payload['hash']} : {finish_payload['hash']})\n\n"
                "Request body.\n### RESULT (UPD8)\nDone.\n### RESULT (UPD8)\nContinued.\n"
                "## UPD9\n\nFuture body.\n"
                "### RESULT (UPD9)\nFuture done.\n",
            )

    def test_start_uses_end_of_file_when_upd_header_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            helm_log = root / "main.prompt.md"
            helm_log.write_text("First line.\nSecond line.\n", encoding="utf-8")
            payload = status.start_status(
                root,
                helm_log,
                "UPD11",
                environ={
                    "ITERATIVE_PROMPT_AUTOCOMMIT": "true",
                    "ITERATIVE_PROMPT_TRACE": "false",
                },
            )

            self.assertEqual(payload["upd-line"], 3)
            self.assertIsNone(payload["result-lines"])

    def test_disabled_trace_does_not_write_jsonl_or_update_helm_log(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            helm_log = root / "main.prompt.md"
            original = "## UPD9\n\nRequest body.\n"
            helm_log.write_text(original, encoding="utf-8")
            environment = {
                "ITERATIVE_PROMPT_AUTOCOMMIT": "true",
                "ITERATIVE_PROMPT_TRACE": "false",
                "ITERATIVE_PROMPT_STATUS_DIR": str(root / "status"),
            }
            start_payload = status.start_status(
                root,
                helm_log,
                "UPD9",
                environ=environment,
            )
            finish_payload = status.finish_status(
                root,
                str(start_payload["hash"]),
                environ=environment,
            )
            self.assertEqual(start_payload["status"], "start")
            self.assertEqual(finish_payload["status"], "finish")
            self.assertFalse((root / "status" / "status.jsonl").exists())
            self.assertEqual(helm_log.read_text(encoding="utf-8"), original)

    def test_cli_start_and_finish_accept_documented_arguments(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            helm_log = root / "main.prompt.md"
            helm_log.write_text("## UPD10\n\nRequest body.\n", encoding="utf-8")
            environment = {
                "ITERATIVE_PROMPT_AUTOCOMMIT": "true",
                "ITERATIVE_PROMPT_TRACE": "true",
                "ITERATIVE_PROMPT_STATUS_DIR": str(root / "status"),
            }
            with patch.dict(os.environ, environment, clear=False):
                start_output = io.StringIO()
                with redirect_stdout(start_output):
                    self.assertEqual(
                        status.main(
                            [
                                "--start",
                                "--cwd",
                                str(root),
                                "--helm-log",
                                str(helm_log),
                                "--upd-id",
                                "UPD10",
                            ]
                        ),
                        0,
                    )
                start_payload = json.loads(start_output.getvalue())

                finish_output = io.StringIO()
                with redirect_stdout(finish_output):
                    self.assertEqual(
                        status.main(
                            [
                                "--finish",
                                "--cwd",
                                str(root),
                                "--started_from",
                                start_payload["hash"],
                            ]
                        ),
                        0,
                    )
                finish_payload = json.loads(finish_output.getvalue())

            self.assertEqual(start_payload["status"], "start")
            self.assertEqual(finish_payload["status"], "finish")
            self.assertEqual(finish_payload["started_from"], start_payload["hash"])
            self.assertIn(
                f"(tracked: {start_payload['hash']} : {finish_payload['hash']})",
                helm_log.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()