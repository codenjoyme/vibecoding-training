#!/usr/bin/env python3
"""
Bulk Reverse-Engineering of Project Conventions from Commit History

Iterates through git commits (oldest→newest), extracts the commit message
(as issue substitute) and diff, then calls GitHub Copilot CLI with the
reverse-engineer-conventions instruction to build an accumulated
conventions document incrementally.

Usage:
    python extract_conventions.py [--repo <path>] [--limit <N>] [--skip-merges]

Output:
    ./accumulated-conventions.md — incrementally built conventions file
    ./commits-processed.log     — log of processed commits
"""

import os
import subprocess
import argparse
import textwrap
from pathlib import Path
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────────────
NODE_PATH = "C:\\Java\\nvm\\v20.19.0"  # Adjust to your nvm path
INSTRUCTION_FILE = Path("instructions/reverse-engineer-conventions.agent.md")  # Relative to repo root
OUTPUT_FILE = Path("accumulated-conventions.md")
LOG_FILE = Path("commits-processed.log")


def find_copilot_bat():
    """Find copilot.bat in system."""
    result = subprocess.run(
        ["where.exe", "copilot"], capture_output=True, text=True
    )
    if result.returncode == 0:
        return result.stdout.strip().split("\n")[0]
    return None


def get_commits(repo_path, skip_merges=False, limit=None):
    """Get list of commits oldest→newest as [(hash, subject)]."""
    cmd = ["git", "-C", str(repo_path), "log", "--reverse", "--format=%H %s"]
    if skip_merges:
        cmd.append("--no-merges")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"git log failed: {result.stderr}")
    lines = [l for l in result.stdout.strip().splitlines() if l]
    commits = []
    for line in lines:
        sha, subject = line.split(" ", 1)
        commits.append((sha, subject))
    if limit:
        commits = commits[:limit]
    return commits


def get_commit_diff(repo_path, sha):
    """Get the full diff for a single commit."""
    result = subprocess.run(
        ["git", "-C", str(repo_path), "show", "--stat", "--patch", sha],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        return None
    return result.stdout


def get_commit_message(repo_path, sha):
    """Get full commit message (subject + body)."""
    result = subprocess.run(
        ["git", "-C", str(repo_path), "log", "-1", "--format=%B", sha],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def build_prompt(commit_msg, diff_text, existing_conventions, sha):
    """Build the prompt for Copilot CLI."""
    conv_section = existing_conventions if existing_conventions else "None yet — this is the first commit."

    # Truncate diff if too large (context window limits)
    max_diff_chars = 30000
    if len(diff_text) > max_diff_chars:
        diff_text = diff_text[:max_diff_chars] + "\n\n... [diff truncated for context window] ..."

    prompt = textwrap.dedent(f"""\
        Follow the instruction in ./instructions/reverse-engineer-conventions.agent.md

        ## Commit {sha[:8]}
        {commit_msg}

        ## Diff
        ```
        {diff_text}
        ```

        ## Existing Conventions So Far
        {conv_section}

        Extract any NEW project conventions visible in this commit.
        Only add insights not already present in Existing Conventions.
        Mark each new convention with "Source: Commit {sha[:8]}".

        Save the updated conventions to ./work/196-task/accumulated-conventions.md
    """)
    return prompt


def main():
    parser = argparse.ArgumentParser(description="Bulk reverse-engineer project conventions from commits")
    parser.add_argument("--repo", default=".", help="Path to git repository (default: current dir)")
    parser.add_argument("--limit", type=int, default=None, help="Max number of commits to process")
    parser.add_argument("--skip-merges", action="store_true", help="Skip merge commits")
    args = parser.parse_args()

    repo_path = Path(args.repo).resolve()
    script_dir = Path(__file__).parent.resolve()

    # Resolve paths
    output_path = script_dir / OUTPUT_FILE
    log_path = script_dir / LOG_FILE
    instruction_abs = (repo_path / INSTRUCTION_FILE).resolve()

    if not instruction_abs.exists():
        print(f"❌ Instruction file not found: {instruction_abs}")
        return

    # Find copilot
    copilot_path = find_copilot_bat()
    if not copilot_path:
        print("❌ Copilot CLI not found. Run: where.exe copilot")
        return

    print(f"📂 Repository: {repo_path}")
    print(f"📝 Instruction: {instruction_abs}")
    print(f"🤖 Copilot CLI: {copilot_path}")
    print()

    # Get commits
    commits = get_commits(repo_path, args.skip_merges, args.limit)
    print(f"Found {len(commits)} commits to process\n")

    # Setup environment
    env = os.environ.copy()
    env["PATH"] = f"{NODE_PATH};{env.get('PATH', '')}"

    # Load existing conventions if resuming
    existing_conventions = ""
    if output_path.exists():
        existing_conventions = output_path.read_text(encoding="utf-8")

    # Load already processed commits
    processed = set()
    if log_path.exists():
        processed = set(log_path.read_text(encoding="utf-8").strip().splitlines())

    original_dir = Path.cwd()

    for i, (sha, subject) in enumerate(commits, 1):
        if sha in processed:
            print(f"[{i}/{len(commits)}] ⏭️  Already processed: {subject[:60]}")
            continue

        print(f"[{i}/{len(commits)}] 🔍 {sha[:8]} — {subject[:60]}")

        # Get commit data
        commit_msg = get_commit_message(repo_path, sha)
        diff_text = get_commit_diff(repo_path, sha)

        if not diff_text:
            print(f"  ⚠️ No diff available, skipping")
            continue

        # Build prompt
        prompt = build_prompt(commit_msg, diff_text, existing_conventions, sha)

        # Write prompt to temp file (avoids shell escaping issues)
        prompt_file = script_dir / "_current_prompt.md"
        prompt_file.write_text(prompt, encoding="utf-8")

        try:
            os.chdir(repo_path)

            result = subprocess.run(
                ["cmd", "/c", copilot_path,
                 "-p", f"@{prompt_file}",
                 "--add-dir", ".",
                 "--allow-all",
                 "--no-ask-user",
                 "-s"],
                env=env,
                timeout=180,
                shell=True
            )

            # Read updated conventions
            if output_path.exists():
                existing_conventions = output_path.read_text(encoding="utf-8")
                print(f"  ✅ Conventions updated")
            else:
                print(f"  ⚠️ Output file not created")

            # Log processed commit
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"{sha}\n")
            processed.add(sha)

        except subprocess.TimeoutExpired:
            print(f"  ⚠️ Timeout (180s)")
        except Exception as e:
            print(f"  ⚠️ Error: {e}")
        finally:
            os.chdir(original_dir)

        print()

    # Cleanup temp file
    prompt_file = script_dir / "_current_prompt.md"
    if prompt_file.exists():
        prompt_file.unlink()

    print("=" * 50)
    print("✅ Complete!")
    print(f"   Processed: {len(processed)} commits")
    print(f"   Output: {output_path}")
    print("=" * 50)


if __name__ == "__main__":
    main()
