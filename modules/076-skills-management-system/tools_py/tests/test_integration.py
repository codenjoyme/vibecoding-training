from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "skills.py"


def run_git(directory: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=directory,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


class SkillsCliIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.central = self.root / "skills-repo"
        self._create_central_repo()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _create_central_repo(self) -> None:
        manifest_dir = self.central / ".manifest"
        manifest_dir.mkdir(parents=True)
        manifests = {
            "_global.json": {"skills": ["creating-instructions"]},
            "project-alpha.json": {
                "skills": ["code-review-base", "style-guidelines"],
                "sub-configs": ["security"],
            },
            "project-beta.json": {"skills": ["test-writing"], "sub-configs": []},
            "security.json": {"skills": ["security-guidelines"], "sub-configs": []},
        }
        for name, value in manifests.items():
            (manifest_dir / name).write_text(
                json.dumps(value, indent=2) + "\n", encoding="utf-8"
            )
        descriptions = {
            "creating-instructions": "Instruction authoring standards.",
            "code-review-base": "Baseline review checklist.",
            "style-guidelines": "Shared code style.",
            "security-guidelines": "Security review guidance.",
            "test-writing": "Automated test guidance.",
        }
        for name, description in descriptions.items():
            skill_dir = self.central / name
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(f"# {name}\n", encoding="utf-8")
            (skill_dir / "info.json").write_text(
                json.dumps({"description": description, "owner": f"{name}@example.com"}, indent=2),
                encoding="utf-8",
            )
        run_git(self.central, "init")
        run_git(self.central, "config", "user.email", "test@example.com")
        run_git(self.central, "config", "user.name", "Python CLI Tests")
        run_git(self.central, "add", ".")
        run_git(self.central, "commit", "-m", "init: test skills repository")
        run_git(self.central, "branch", "-M", "master")

    def run_cli(self, project: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(LAUNCHER), *args],
            cwd=project,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )

    def _new_project(self, name: str) -> Path:
        project = self.root / name
        project.mkdir()
        return project

    def test_help_and_unknown_command(self) -> None:
        project = self._new_project("help-project")
        help_result = self.run_cli(project, "help")
        self.assertEqual(help_result.returncode, 0)
        self.assertIn("init-repo", help_result.stdout)
        unknown = self.run_cli(project, "unknown")
        self.assertEqual(unknown.returncode, 1)
        self.assertIn('unknown command "unknown"', unknown.stderr)

    def test_init_list_metadata_and_global_only_mode(self) -> None:
        project = self._new_project("alpha")
        initialized = self.run_cli(
            project,
            "init",
            "--repo",
            "../skills-repo",
            "--groups",
            "project-alpha",
        )
        self.assertEqual(initialized.returncode, 0, initialized.stderr)
        self.assertTrue((project / "skills.json").exists())
        self.assertTrue((project / "instructions" / "code-review-base").exists())
        self.assertTrue((project / "instructions" / "security-guidelines").exists())
        self.assertFalse((project / "instructions" / "test-writing").exists())

        listed = self.run_cli(project, "list", "--json")
        self.assertEqual(listed.returncode, 0, listed.stderr)
        items = json.loads(listed.stdout)
        by_name = {item["name"]: item for item in items}
        self.assertTrue(by_name["code-review-base"]["active"])
        self.assertFalse(by_name["test-writing"]["active"])
        self.assertEqual(by_name["test-writing"]["owner"], "test-writing@example.com")

        global_project = self._new_project("global-only")
        global_init = self.run_cli(global_project, "init", "--repo", "../skills-repo")
        self.assertEqual(global_init.returncode, 0, global_init.stderr)
        self.assertTrue((global_project / "instructions" / "creating-instructions").exists())
        self.assertFalse((global_project / "instructions" / "code-review-base").exists())

    def test_toggle_create_force_disable_and_reinit(self) -> None:
        project = self._new_project("toggle")
        initialized = self.run_cli(
            project, "init", "--repo", "../skills-repo", "--groups", "project-alpha"
        )
        self.assertEqual(initialized.returncode, 0, initialized.stderr)

        enabled = self.run_cli(project, "enable", "group", "project-beta")
        self.assertEqual(enabled.returncode, 0, enabled.stderr)
        self.assertTrue((project / "instructions" / "test-writing").exists())
        disabled = self.run_cli(project, "disable", "group", "project-beta")
        self.assertEqual(disabled.returncode, 0, disabled.stderr)
        self.assertFalse((project / "instructions" / "test-writing").exists())

        created = self.run_cli(project, "create", "local-skill")
        self.assertEqual(created.returncode, 0, created.stderr)
        self.assertTrue((project / "instructions" / "local-skill" / "info.json").exists())
        cfg = json.loads((project / "skills.json").read_text(encoding="utf-8"))
        self.assertIn("local-skill", cfg["extra_skills"])

        security_dir = project / "instructions" / "security-guidelines"
        (security_dir / "untracked.txt").write_text("local work\n", encoding="utf-8")
        refused = self.run_cli(project, "disable", "security-guidelines")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("uncommitted local changes", refused.stderr)
        forced = self.run_cli(project, "disable", "security-guidelines", "--force")
        self.assertEqual(forced.returncode, 0, forced.stderr)
        self.assertFalse(security_dir.exists())
        self.assertIn("skills-cli: auto-stash", run_git(project / "instructions", "stash", "list"))

        generated = self.run_cli(project, "init-repo", "generated-repo")
        self.assertEqual(generated.returncode, 0, generated.stderr)
        generated_root = project / "generated-repo"
        self.assertTrue((generated_root / ".manifest" / "_global.json").exists())
        self.assertTrue((generated_root / "skills-cli" / "SKILL.md").exists())
        self.assertFalse((generated_root / ".git").exists())
        json_text = (generated_root / ".manifest" / "_global.json").read_text(encoding="utf-8")
        self.assertIn("\n  \"skills\"", json_text)

    def test_push_merge_pull_and_reinit(self) -> None:
        project = self._new_project("contributor")
        initialized = self.run_cli(
            project, "init", "--repo", "../skills-repo", "--groups", "project-alpha"
        )
        self.assertEqual(initialized.returncode, 0, initialized.stderr)
        skill_file = project / "instructions" / "code-review-base" / "SKILL.md"
        skill_file.write_text(skill_file.read_text(encoding="utf-8") + "- New check\n", encoding="utf-8")

        pushed = self.run_cli(project, "push", "code-review-base", "--groups", "project-beta", "new-group")
        self.assertEqual(pushed.returncode, 0, pushed.stderr)
        self.assertIn("pushed for review", pushed.stdout)
        self.assertEqual(run_git(self.central, "branch", "--list", "feature/code-review-base-update").strip(), "feature/code-review-base-update")
        self.assertEqual(run_git(project / "instructions", "branch", "--show-current"), "master")

        run_git(self.central, "merge", "feature/code-review-base-update")
        pulled = self.run_cli(project, "pull")
        self.assertEqual(pulled.returncode, 0, pulled.stderr)
        self.assertIn("New check", skill_file.read_text(encoding="utf-8"))

        group_manifest = self.central / ".manifest" / "new-group.json"
        self.assertEqual(json.loads(group_manifest.read_text(encoding="utf-8"))["skills"], ["code-review-base"])

        skill_file.write_text(skill_file.read_text(encoding="utf-8") + "- Second smoke check\n", encoding="utf-8")
        repeated_push = self.run_cli(project, "push", "code-review-base")
        self.assertEqual(repeated_push.returncode, 0, repeated_push.stderr)
        self.assertIn("pushed for review", repeated_push.stdout)
        self.assertEqual(run_git(project / "instructions", "branch", "--show-current"), "master")

        second = self.run_cli(project, "init")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertTrue((project / "instructions" / "code-review-base").exists())


if __name__ == "__main__":
    unittest.main()
