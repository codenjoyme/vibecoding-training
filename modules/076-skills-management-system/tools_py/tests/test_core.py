from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path

from skills_cli.lib import config, manifest
from skills_cli.lib.errors import ConfigError, ManifestError


class ConfigTests(unittest.TestCase):
    def test_save_load_is_pretty_and_defaults_missing_lists(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            original = Path.cwd()
            try:
                Path(directory).resolve().joinpath(".marker").touch()
                import os

                os.chdir(directory)
                config.save(config.Config("../skills", ["alpha"], [], []))
                text = Path("skills.json").read_text(encoding="utf-8")
                self.assertIn("\n  \"groups\"", text)
                self.assertEqual(config.load().to_dict()["groups"], ["alpha"])
                Path("skills.json").write_text('{"repo_url":"../skills"}', encoding="utf-8")
                loaded = config.load()
                self.assertEqual(loaded.groups, [])
                self.assertEqual(loaded.extra_skills, [])
                self.assertEqual(loaded.excluded_skills, [])
            finally:
                os.chdir(original)

    def test_missing_config_is_actionable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            original = Path.cwd()
            try:
                import os

                os.chdir(directory)
                with self.assertRaisesRegex(ConfigError, "not a skills workspace"):
                    config.load()
            finally:
                os.chdir(original)


class ManifestTests(unittest.TestCase):
    def test_resolves_nested_subconfigs_cycles_and_deduplicates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest_dir = Path(directory) / ".manifest"
            manifest_dir.mkdir()
            (manifest_dir / "_global.json").write_text(
                json.dumps({"skills": ["global", "shared"]}), encoding="utf-8"
            )
            (manifest_dir / "alpha.json").write_text(
                json.dumps({"skills": ["alpha", "shared"], "sub-configs": ["security"]}),
                encoding="utf-8",
            )
            (manifest_dir / "security.json").write_text(
                json.dumps({"skills": ["security"], "sub-configs": ["nested"]}),
                encoding="utf-8",
            )
            (manifest_dir / "nested.json").write_text(
                json.dumps({"skills": ["nested"], "sub-configs": ["security"]}),
                encoding="utf-8",
            )
            self.assertEqual(
                manifest.resolve_skills(directory, ["alpha"]),
                ["alpha", "global", "nested", "security", "shared"],
            )

    def test_missing_nested_config_warns_but_missing_top_level_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest_dir = Path(directory) / ".manifest"
            manifest_dir.mkdir()
            (manifest_dir / "_global.json").write_text('{"skills": []}', encoding="utf-8")
            (manifest_dir / "alpha.json").write_text(
                '{"skills": ["alpha"], "sub-configs": ["missing"]}', encoding="utf-8"
            )
            warnings = StringIO()
            with redirect_stderr(warnings):
                self.assertEqual(manifest.resolve_skills(directory, ["alpha"]), ["alpha"])
            self.assertIn('config "missing" not found', warnings.getvalue())
            with self.assertRaises(ManifestError):
                manifest.resolve_skills(directory, ["unknown"])
