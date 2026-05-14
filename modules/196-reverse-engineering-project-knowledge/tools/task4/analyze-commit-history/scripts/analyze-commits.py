#!/usr/bin/env python3
"""
Commit History Analyzer — iterates through git commits, extracts diffs,
and uses GitHub Copilot CLI (Claude Opus 4.6) to build SDLC instruction files.

Part of the analyze-commit-history skill.
Location: instructions/analyze-commit-history/scripts/analyze-commits.py

Usage (from repository root):
    python instructions/analyze-commit-history/scripts/analyze-commits.py
    python instructions/analyze-commit-history/scripts/analyze-commits.py --ticket XYZA-233
    python instructions/analyze-commit-history/scripts/analyze-commits.py --last 5
    python instructions/analyze-commit-history/scripts/analyze-commits.py --from abc123 --to def456
    python instructions/analyze-commit-history/scripts/analyze-commits.py --dry-run
    python instructions/analyze-commit-history/scripts/analyze-commits.py --prefix XYZA --prefix ACT
    python instructions/analyze-commit-history/scripts/analyze-commits.py --skip-research
"""

import argparse
import atexit
import io
import json
import os
import re
import subprocess
import sys
import hashlib
from pathlib import Path

# Fix Unicode output on Windows (arrows, checkmarks, etc.)
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# --- Configuration -----------------------------------------------------------

GENERIC_TICKET_PATTERN = re.compile(r"\b([A-Z]{2,15}-\d+)\b")
ANALYSIS_DIR = Path("analysis")

# Resolve instruction file relative to this script's location
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
INSTRUCTION_FILE = SKILL_DIR / "references" / "analyze-commit-diff.instruction.md"
REVIEW_INSTRUCTION_FILE = SKILL_DIR / "references" / "review-instructions.instruction.md"
DISCOVER_INSTRUCTION_FILE = SKILL_DIR / "references" / "discover-prefixes.instruction.md"

# Manifest file (tracked in git, lives in config/ — part of project configuration)
MANIFEST_FILE = "commits-manifest.md"


# Auto-detect copilot.bat
def find_copilot_bat() -> str | None:
    """Locate copilot.bat via where.exe, then fall back to known paths.

    On Windows ``where.exe copilot`` typically returns multiple matches, the
    first being an extensionless Node shim that ``subprocess.run`` cannot
    execute directly (raises ``WinError 193``). We prefer ``.bat`` / ``.cmd``
    entries and only fall back to the first line if none is found.
    """
    try:
        result = subprocess.run(
            ["where.exe", "copilot"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
            for line in lines:
                low = line.lower()
                if low.endswith(".bat") or low.endswith(".cmd"):
                    return line
            if lines:
                return lines[0]
    except Exception:
        pass

    # Fallback: common VS Code Insiders / Stable locations
    for variant in ("Code - Insiders", "Code"):
        candidate = (
            Path(os.environ.get("APPDATA", ""))
            / variant
            / "User"
            / "globalStorage"
            / "github.copilot-chat"
            / "copilotCli"
            / "copilot.bat"
        )
        if candidate.exists():
            return str(candidate)
    return None


# Auto-detect Node.js (needed by copilot.bat)
def find_node_dir() -> str | None:
    """Return directory containing node.exe."""
    try:
        result = subprocess.run(
            ["where.exe", "node"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return str(Path(result.stdout.strip().split("\n")[0]).parent)
    except Exception:
        pass
    return None


# --- Git helpers -------------------------------------------------------------

def git(*args: str) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git"] + list(args), capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=60
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed:\n{result.stderr}")
    return result.stdout


def get_commits(ticket: str | None, last: int | None,
                from_ref: str | None, to_ref: str | None,
                prefixes: list[str] | None = None,
                all_commits: bool = False) -> list[tuple[str, str]]:
    """Return list of (hash, subject) tuples matching the filter."""
    range_spec = []
    if from_ref and to_ref:
        range_spec = [f"{from_ref}..{to_ref}"]
    elif from_ref:
        range_spec = [f"{from_ref}..HEAD"]

    log_args = ["log", "--oneline", "--reverse", "--format=%H %s"] + range_spec
    raw = git(*log_args).strip()
    if not raw:
        return []

    active_prefixes = [p.upper() for p in prefixes] if prefixes else None

    commits = []
    for line in raw.splitlines():
        sha, subject = line.split(" ", 1)
        if all_commits:
            commits.append((sha, subject))
            continue
        match = GENERIC_TICKET_PATTERN.search(subject)
        if ticket:
            if match and match.group(1).upper() == ticket.upper():
                commits.append((sha, subject))
        elif active_prefixes:
            if match and match.group(1).split("-")[0].upper() in active_prefixes:
                commits.append((sha, subject))
        else:
            if match:
                commits.append((sha, subject))

    if last:
        commits = commits[-last:]
    return commits


def get_all_commits_raw() -> list[tuple[str, str]]:
    """Return ALL commits oldest-first as (full_sha, subject) tuples."""
    raw = git("log", "--reverse", "--format=%H %s").strip()
    if not raw:
        return []
    result = []
    for line in raw.splitlines():
        sha, subject = line.split(" ", 1)
        result.append((sha, subject))
    return result


def get_processed_shas() -> set[str]:
    """Read git log to find commits already analyzed (full SHAs).

    Looks for commits matching:
      analyze(instructions): <sha8>
    and resolves the 8-char SHA to full SHA via git rev-parse.
    """
    processed: set[str] = set()
    try:
        raw = git("log", "--format=%s", "HEAD").strip()
    except RuntimeError:
        return processed
    pattern = re.compile(r"analyze\(instructions\):\s+([0-9a-f]{7,40})[^+]", re.IGNORECASE)
    # Also handle batch entries like "6447c19b+9114c5e1+430454cd"
    batch_pattern = re.compile(r"analyze\(instructions\):\s+([0-9a-f+]{7,})", re.IGNORECASE)
    for subject in raw.splitlines():
        m = batch_pattern.search(subject)
        if m:
            for sha_part in m.group(1).split("+"):
                sha_part = sha_part.strip()[:8]
                if re.fullmatch(r"[0-9a-f]{7,8}", sha_part):
                    try:
                        full = git("rev-parse", sha_part).strip()
                        processed.add(full)
                    except RuntimeError:
                        processed.add(sha_part)  # store short SHA as fallback
    return processed


def extract_ticket(subject: str) -> str:
    """Extract ticket ID from commit subject, fallback to 'no-tag'."""
    match = GENERIC_TICKET_PATTERN.search(subject)
    return match.group(1).upper() if match else "no-tag"


def _is_root_commit(sha: str) -> bool:
    """Return True if sha has no parent (initial commit)."""
    try:
        parents = git("rev-list", "--parents", "-n", "1", sha).strip().split()
        return len(parents) <= 1  # only sha itself, no parent
    except RuntimeError:
        return False


def _safe_diff_filename(file_path: str, max_len: int = 120) -> str:
    """Convert a repo path into a filename safe for Windows MAX_PATH.

    Replaces separators with __, then if the result exceeds ``max_len`` chars
    keeps a readable head + short SHA-1 hash of the full path so the name stays
    unique but short.
    """
    flat = file_path.replace("/", "__").replace("\\", "__")
    if len(flat) <= max_len:
        return flat
    digest = hashlib.sha1(file_path.encode("utf-8")).hexdigest()[:12]
    head = flat[: max_len - len(digest) - 1]
    return f"{head}_{digest}"


def extract_diff_files(sha: str, dest: Path) -> list[str]:
    """Write per-file diffs into dest/ and return list of created files.

    Robust against:
    - root commits (no parent)
    - Windows MAX_PATH (long Java-style nested paths)
    - per-file write errors (warn + continue, don't kill the whole run)
    """
    if _is_root_commit(sha):
        # initial commit — use diff-tree --root to get full tree as additions
        diff_raw = git("diff-tree", "--root", "-p", sha)
    else:
        try:
            diff_raw = git("diff", f"{sha}~1", sha)
        except RuntimeError:
            diff_raw = git("diff-tree", "-p", sha)

    if not diff_raw or not diff_raw.strip():
        diff_raw = git("diff-tree", "-p", sha)

    dest.mkdir(parents=True, exist_ok=True)

    files_created: list[str] = []
    current_file: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_file, current_lines
        if current_file and current_lines:
            safe_name = _safe_diff_filename(current_file)
            out_path = dest / f"{safe_name}.diff"
            try:
                out_path.write_text("\n".join(current_lines), encoding="utf-8")
                files_created.append(out_path.name)
            except OSError as e:
                # MAX_PATH or any IO error — warn and continue, don't crash
                print(f"  ⚠️  Skipped diff for {current_file!r}: {e.__class__.__name__}: {e}")
        current_lines = []

    for line in diff_raw.splitlines():
        if line.startswith("diff --git"):
            flush()
            parts = line.split(" b/")
            current_file = parts[-1] if len(parts) > 1 else "unknown"
            current_lines = [line]
        else:
            current_lines.append(line)
    flush()

    return files_created


# --- Agent runner ------------------------------------------------------------

# Default model and timeout
DEFAULT_MODEL = "claude-opus-4.6"
DEFAULT_TIMEOUT = 600  # seconds per commit


def run_agent(commit_dir: Path, repo_root: Path, instruction_abs: Path,
              copilot_bat: str, env: dict, model: str = DEFAULT_MODEL,
              timeout: int = DEFAULT_TIMEOUT) -> bool:
    """Invoke Copilot CLI agent from repo root with access to commit dir and instructions."""
    instruction_rel = os.path.relpath(instruction_abs, repo_root)
    commit_dir_rel = os.path.relpath(commit_dir, repo_root)
    prompt_text = f"@{instruction_rel} Analyze commit diffs in: {commit_dir_rel}/diff/"
    try:
        print(f"  \u2192 Running AI agent (model={model}, timeout={timeout}s)...")
        sys.stdout.flush()
        result = subprocess.run(
            [
                copilot_bat,
                "-p", prompt_text,
                "--add-dir", str(commit_dir_rel),
                "--add-dir", "instructions",
                "--allow-all",
                "--no-ask-user",
                "--model", model,
                "--stream", "on",
            ],
            cwd=str(repo_root),
            env=env,
            timeout=timeout,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  Agent timed out ({timeout}s)")
        return False
    except FileNotFoundError as e:
        print(f"  ⚠️  Copilot CLI not found: {e}")
        return False
    except Exception as e:
        print(f"  ⚠️  Error: {e}")
        return False




def run_review(repo_root: Path, copilot_bat: str, env: dict,
               model: str = DEFAULT_MODEL, timeout: int = DEFAULT_TIMEOUT) -> bool:
    """Run AI agent to review instruction files for relevance."""
    review_abs = REVIEW_INSTRUCTION_FILE.resolve()
    if not review_abs.exists():
        print(f"❌ Review instruction not found: {review_abs}")
        return False

    review_rel = os.path.relpath(review_abs, repo_root)
    prompt_text = f"@{review_rel} Review all instruction files for relevance."
    print("\n" + "=" * 50)
    print("📋 Reviewing instruction files for relevance...")
    print("=" * 50 + "\n")
    sys.stdout.flush()
    try:
        result = subprocess.run(
            [
                copilot_bat,
                "-p", prompt_text,
                "--add-dir", "instructions",
                "--add-dir", "analysis",
                "--allow-all",
                "--no-ask-user",
                "--model", model,
                "--stream", "on",
            ],
            cwd=str(repo_root),
            env=env,
            timeout=timeout,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  Review agent timed out ({timeout}s)")
        return False
    except Exception as e:
        print(f"  ⚠️  Review error: {e}")
        return False


# --- Git single commit -------------------------------------------------------

def git_commit_single(repo_root: Path, sha: str, subject: str) -> bool:
    """Stage instructions/ and analysis/ and make one git commit for the analyzed source commit."""
    msg = f"analyze(instructions): {sha[:8]} — {subject[:80]}"
    try:
        subprocess.run(["git", "add", "instructions/"],
                       cwd=str(repo_root), check=True, timeout=30)
        result = subprocess.run(
            ["git", "commit", "-m", msg],
            cwd=str(repo_root), capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            print(f"  ✓ Committed: {msg[:90]}")
            return True
        if "nothing to commit" in result.stdout + result.stderr:
            print(f"  → Nothing to commit")
            return True
        print(f"  ⚠️  git commit failed: {result.stderr.strip()}")
        return False
    except Exception as e:
        print(f"  ⚠️  git commit error: {e}")
        return False


# --- Prefix discovery --------------------------------------------------------

def collect_commit_stats() -> dict[str, int]:
    """Scan all commits and return prefix -> count mapping."""
    raw = git("log", "--format=%s").strip()
    prefix_counts: dict[str, int] = {}
    for subject in raw.splitlines():
        match = GENERIC_TICKET_PATTERN.search(subject)
        if match:
            prefix = match.group(1).split("-")[0].upper()
            prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1
    return prefix_counts


def run_discovery_agent(repo_root: Path, copilot_bat: str, env: dict,
                        model: str = DEFAULT_MODEL,
                        timeout: int = DEFAULT_TIMEOUT) -> bool:
    """Invoke Copilot CLI to classify commit prefixes and write discovered-prefixes.json."""
    discover_abs = DISCOVER_INSTRUCTION_FILE.resolve()
    if not discover_abs.exists():
        print(f"  ⚠️  Discovery instruction not found: {discover_abs}")
        return False

    discover_rel = os.path.relpath(discover_abs, repo_root)
    stats_rel = str(ANALYSIS_DIR / "commit-stats.txt")
    prompt_text = f"@{discover_rel} Read {stats_rel} and classify commit prefixes."
    try:
        print(f"  \u2192 Running prefix discovery agent (model={model})...")
        sys.stdout.flush()
        result = subprocess.run(
            [
                copilot_bat,
                "-p", prompt_text,
                "--add-dir", str(ANALYSIS_DIR),
                "--add-dir", "instructions",
                "--allow-all",
                "--no-ask-user",
                "--model", model,
                "--stream", "on",
            ],
            cwd=str(repo_root),
            env=env,
            timeout=timeout,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  Discovery agent timed out ({timeout}s)")
        return False
    except Exception as e:
        print(f"  ⚠️  Discovery error: {e}")
        return False


def discover_prefixes(repo_root: Path, copilot_bat: str, env: dict,
                      model: str = DEFAULT_MODEL,
                      timeout: int = DEFAULT_TIMEOUT) -> list[str]:
    """Research phase: scan commits, classify prefixes via LLM, return relevant ones."""
    print("\n" + "=" * 50)
    print("\U0001f50d Research phase: discovering relevant commit prefixes...")
    print("=" * 50)

    prefix_counts = collect_commit_stats()
    if not prefix_counts:
        print("  \u2192 No ticket-like prefixes found in commit history.")
        print()
        return []

    print("  Candidate prefixes found:")
    for prefix, count in sorted(prefix_counts.items(), key=lambda x: -x[1]):
        print(f"    {prefix}: {count} commit(s)")

    # Write stats file for LLM
    analysis_dir = repo_root / ANALYSIS_DIR
    analysis_dir.mkdir(exist_ok=True)
    stats_path = analysis_dir / "commit-stats.txt"
    with open(stats_path, "w", encoding="utf-8") as f:
        f.write("Commit prefix statistics (prefix: number of commits):\n\n")
        for prefix, count in sorted(prefix_counts.items(), key=lambda x: -x[1]):
            f.write(f"  {prefix}: {count}\n")

    # Run LLM to classify prefixes
    ok = run_discovery_agent(repo_root, copilot_bat, env, model, timeout)

    # Read LLM output
    output_path = analysis_dir / "discovered-prefixes.json"
    if ok and output_path.exists():
        try:
            data = json.loads(output_path.read_text(encoding="utf-8"))
            relevant = data.get("relevant_prefixes", [])
            reasoning = data.get("reasoning", "")
            print(f"  \u2192 Relevant prefixes: {relevant}")
            if reasoning:
                print(f"  \u2192 Reasoning: {reasoning}")
            print()
            return relevant
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  ⚠️  Failed to parse discovery output: {e}")

    # Fallback: use all prefixes with more than 1 commit
    fallback = [p for p, c in prefix_counts.items() if c > 1] or list(prefix_counts.keys())
    print(f"  \u2192 Using fallback prefixes: {fallback}")
    print()
    return fallback


# --- Manifest ----------------------------------------------------------------

def generate_manifest(repo_root: Path) -> Path:
    """Create or refresh commits-manifest.md listing all commits with checkboxes.

    Symbols:
      [x]  already processed (found in git log of current branch)
      [>]  selected by user to process next (user edits [ ] → [>])
      [ ]  not yet selected
      [-]  explicitly skipped (not relevant for analysis)
    """
    all_commits = get_all_commits_raw()
    processed = get_processed_shas()

    # Preserve [-] marks from existing manifest
    skipped_shas: set[str] = set()
    manifest_path = repo_root / MANIFEST_FILE
    if manifest_path.exists():
        skip_pattern = re.compile(r"^- \[-\] `([0-9a-f]{7,40})`")
        for line in manifest_path.read_text(encoding="utf-8").splitlines():
            m = skip_pattern.match(line)
            if m:
                skipped_shas.add(m.group(1))

    lines = [
        "# Commit Analysis Manifest",
        "",
        "## Legend",
        "",
        "- `[x]` — already processed ✅",
        "- `[>]` — selected by user to process next (edit `[ ]` → `[>]`)",
        "- `[ ]` — not yet selected",
        "- `[-]` — explicitly skipped (not relevant for analysis)",
        "",
        "## How to Use",
        "",
        "1. Review the list below.",
        "2. Change `[ ]` to `[>]` for commits you want to analyze.",
        "3. Change `[ ]` to `[-]` for commits you want to permanently skip.",
        "4. Run: `python instructions/analyze-commit-history/scripts/analyze-commits.py --from-manifest`",
        "5. The script will process selected commits and mark them `[x]`.",
        "",
        "## All Commits (oldest → newest)",
        "",
    ]

    for sha, subject in all_commits:
        short = sha[:8]
        # Determine if this SHA (or its short form) is in processed set
        done = sha in processed or short in processed
        skipped = short in skipped_shas
        mark = "x" if done else "-" if skipped else " "
        lines.append(f"- [{mark}] `{short}` {subject}")

    manifest_path = repo_root / MANIFEST_FILE
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✓ Manifest written: {manifest_path}")
    print(f"  Total commits: {len(all_commits)}")
    done_count = sum(1 for sha, _ in all_commits if sha in processed or sha[:8] in processed)
    skipped_count = sum(1 for sha, _ in all_commits if sha[:8] in skipped_shas and sha not in processed and sha[:8] not in processed)
    print(f"  Already processed: {done_count}")
    print(f"  Explicitly skipped: {skipped_count}")
    print(f"  Available to select: {len(all_commits) - done_count - skipped_count}")
    return manifest_path


def classify_by_branch(repo_root: Path, branch: str) -> None:
    """Mark [ ] commits as [-] if they are NOT on the specified branch or are merge commits.

    Useful when working from a non-production branch (e.g. feature/dark-factory)
    and wanting to analyze only production commits that exist on develop.

    Steps:
      1. Find the last [x] processed commit SHA in the manifest.
      2. Get all SHAs reachable from origin/<branch> after the last [x].
      3. Get merge commit SHAs on that branch (merges carry no unique diffs).
      4. For each [ ] entry in the manifest:
         - NOT on the branch → mark [-]
         - Merge commit on the branch → mark [-]
         - Otherwise → keep [ ] (production candidate)
    """
    manifest_path = repo_root / MANIFEST_FILE
    if not manifest_path.exists():
        print(f"❌ Manifest not found: {manifest_path}")
        print("   Run --generate-manifest first.")
        return

    content = manifest_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    # Find last [x] SHA to scope the branch query
    last_processed_sha = None
    processed_pattern = re.compile(r"^- \[x\] `([0-9a-f]{7,40})`")
    for line in lines:
        m = processed_pattern.match(line)
        if m:
            last_processed_sha = m.group(1)

    if not last_processed_sha:
        print("⚠️  No [x] processed commits found. Classifying against full branch history.")
        branch_ref = f"origin/{branch}"
    else:
        branch_ref = f"origin/{branch}"

    # Get full SHAs on the target branch (after last processed)
    try:
        if last_processed_sha:
            branch_shas_raw = git("log", branch_ref, "--format=%H", "--not", last_processed_sha).strip()
        else:
            branch_shas_raw = git("log", branch_ref, "--format=%H").strip()
    except RuntimeError as e:
        print(f"❌ Cannot read branch '{branch_ref}': {e}")
        print(f"   Try: git fetch origin {branch}")
        return

    branch_shas_8 = set(h[:8] for h in branch_shas_raw.split("\n") if h.strip())

    # Get merge SHAs on the target branch
    try:
        if last_processed_sha:
            merge_shas_raw = git("log", branch_ref, "--merges", "--format=%H", "--not", last_processed_sha).strip()
        else:
            merge_shas_raw = git("log", branch_ref, "--merges", "--format=%H").strip()
    except RuntimeError:
        merge_shas_raw = ""

    merge_shas_8 = set(h[:8] for h in merge_shas_raw.split("\n") if h.strip())

    print(f"Branch '{branch_ref}': {len(branch_shas_8)} commits, {len(merge_shas_8)} merges (after last [x])")

    # Classify [ ] entries
    avail_pattern = re.compile(r"^- \[ \] `([0-9a-f]{7,40})`")
    marked_not_on_branch = 0
    marked_merge = 0
    kept = 0

    new_lines = []
    for line in lines:
        m = avail_pattern.match(line)
        if m:
            sha = m.group(1)
            if sha not in branch_shas_8:
                new_lines.append(line.replace("- [ ]", "- [-]", 1))
                marked_not_on_branch += 1
            elif sha in merge_shas_8:
                new_lines.append(line.replace("- [ ]", "- [-]", 1))
                marked_merge += 1
            else:
                new_lines.append(line)
                kept += 1
        else:
            new_lines.append(line)

    manifest_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    print(f"\n✓ Classification complete:")
    print(f"  [-] not on {branch}: {marked_not_on_branch}")
    print(f"  [-] merge commits: {marked_merge}")
    print(f"  [ ] production candidates: {kept}")


def read_manifest_selected(repo_root: Path) -> list[tuple[str, str]]:
    """Read commits-manifest.md and return (sha, subject) for all [>] entries."""
    manifest_path = repo_root / MANIFEST_FILE
    if not manifest_path.exists():
        print(f"❌ Manifest not found: {manifest_path}")
        print("   Run --generate-manifest first.")
        return []

    selected = []
    pattern = re.compile(r"^- \[>\] `([0-9a-f]{7,40})`\s+(.+)$")
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        m = pattern.match(line)
        if m:
            short_sha, subject = m.group(1), m.group(2)
            try:
                full_sha = git("rev-parse", short_sha).strip()
            except RuntimeError:
                full_sha = short_sha  # fallback
            selected.append((full_sha, subject))
    return selected


def update_manifest_done(repo_root: Path, sha: str, marker: str = "x") -> None:
    """Change [>] -> [<marker>] for the given SHA in the manifest.

    Default marker is 'x' (success). Use 'marker="!"' to record a failed run
    (so the operator can re-attempt without confusing it with a finished one).
    """
    manifest_path = repo_root / MANIFEST_FILE
    if not manifest_path.exists():
        return
    short = sha[:8]
    content = manifest_path.read_text(encoding="utf-8")
    updated = re.sub(
        rf"^(- )\[>\]( `{re.escape(short)}`)",
        rf"\1[{marker}]\2",
        content,
        flags=re.MULTILINE,
    )
    if updated != content:
        manifest_path.write_text(updated, encoding="utf-8")
        print(f"  ✓ Manifest updated: [{short}] → [{marker}]")


# --- Main --------------------------------------------------------------------

LOCK_FILE = Path("analysis") / ".analyze.lock"


def acquire_lock() -> None:
    """Ensure only one instance of this script runs at a time via a PID lock file."""
    if LOCK_FILE.exists():
        try:
            pid = int(LOCK_FILE.read_text().strip())
        except (ValueError, OSError):
            pid = None
        if pid:
            # Check if PID is still alive
            try:
                result = subprocess.run(
                    ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                    capture_output=True, text=True, timeout=10
                )
                if str(pid) in result.stdout:
                    print(f"❌ Another instance is already running (PID {pid}).")
                    print(f"   Lock file: {LOCK_FILE.resolve()}")
                    print("   Stop it first or delete the lock file manually.")
                    sys.exit(1)
            except Exception:
                pass  # Can't verify — overwrite the lock
        print(f"⚠️  Stale lock file found (PID {pid}), overwriting...")

    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOCK_FILE.write_text(str(os.getpid()))
    atexit.register(lambda: LOCK_FILE.unlink(missing_ok=True))


def main():
    parser = argparse.ArgumentParser(
        description="Analyze git commit history and extract SDLC instructions."
    )
    parser.add_argument("--ticket", help="Filter by ticket (e.g. XYZA-233)")
    parser.add_argument("--last", type=int, help="Process only last N matching commits")
    parser.add_argument("--from", dest="from_ref", help="Start commit (exclusive)")
    parser.add_argument("--to", dest="to_ref", help="End commit (inclusive)")
    parser.add_argument("--dry-run", action="store_true", help="Extract diffs only, skip agent")
    parser.add_argument("--copilot", help="Path to copilot.bat (auto-detected if omitted)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"AI model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help=f"Timeout per commit in seconds (default: {DEFAULT_TIMEOUT})")
    parser.add_argument("--interactive", action="store_true", help="Pause between commits for user review")
    parser.add_argument("--review", action="store_true", help="Review instruction relevance after processing (or standalone)")
    parser.add_argument("--prefix", action="append", metavar="PREFIX",
                        help="Ticket prefix to analyze (repeatable, e.g. --prefix XYZA --prefix ACT). "
                             "Skips auto-discovery when specified.")
    parser.add_argument("--skip-research", action="store_true",
                        help="Skip the prefix discovery research phase and process all ticket-like commits")
    parser.add_argument("--batch", type=int, default=0, metavar="N",
                        help="Process only the N oldest matching commits per run (oldest first). "
                             "Pass 0 (default) to process all matching commits.")
    parser.add_argument("--no-commit", action="store_true",
                        help="Skip auto git-commit of instructions after each processed commit")
    parser.add_argument("--all-commits", action="store_true",
                        help="Process ALL commits, including those without ticket prefixes")
    parser.add_argument("--generate-manifest", action="store_true",
                        help="Generate (or refresh) commits-manifest.md tracking all commits")
    parser.add_argument("--from-manifest", action="store_true",
                        help="Process commits marked [>] in commits-manifest.md, then mark them [x]")
    parser.add_argument("--classify-branch", metavar="BRANCH",
                        help="Classify [ ] manifest entries against a branch (e.g. develop). "
                             "Marks commits not on origin/<BRANCH> or merge commits as [-].")
    args = parser.parse_args()

    # Ensure only one instance runs at a time
    if not args.dry_run and not args.generate_manifest:
        acquire_lock()

    # Resolve paths
    repo_root = Path(git("rev-parse", "--show-toplevel").strip())
    os.chdir(repo_root)

    # --- Manifest generation (standalone, no agent needed) ---
    if args.generate_manifest:
        generate_manifest(repo_root)
        return

    # --- Classify manifest entries by branch (standalone, no agent needed) ---
    if args.classify_branch:
        classify_by_branch(repo_root, args.classify_branch)
        return

    instruction_abs = INSTRUCTION_FILE.resolve()
    if not instruction_abs.exists():
        print(f"❌ Instruction file not found: {instruction_abs}")
        sys.exit(1)

    copilot_bat = args.copilot or find_copilot_bat()
    if not copilot_bat and not args.dry_run:
        print("❌ copilot.bat not found. Pass --copilot <path> or install GitHub Copilot CLI.")
        sys.exit(1)

    # Prepare environment with Node.js in PATH
    env = os.environ.copy()
    node_dir = find_node_dir()
    if node_dir:
        env["PATH"] = f"{node_dir};{env.get('PATH', '')}"

    # Standalone review mode (no commits needed)
    if args.review and not args.from_ref and not args.to_ref and not args.ticket and not args.last and not args.prefix:
        run_review(repo_root, copilot_bat, env, model=args.model, timeout=args.timeout)
        return

    # Research phase: discover relevant prefixes unless manually specified or skipped
    active_prefixes: list[str] | None = args.prefix if args.prefix else None
    if active_prefixes is None and not args.ticket and not args.skip_research and not args.dry_run and not args.all_commits and not args.from_manifest:
        active_prefixes = discover_prefixes(repo_root, copilot_bat, env,
                                            model=args.model, timeout=args.timeout)
        if not active_prefixes:
            print("⚠️  No relevant prefixes discovered. Processing all ticket-like commits.\n")
            active_prefixes = None

    # Get commits
    if args.from_manifest:
        commits = read_manifest_selected(repo_root)
        if not commits:
            print("No commits selected in manifest. Edit commits-manifest.md and mark items [>].")
            sys.exit(0)
        print(f"Found {len(commits)} commit(s) selected in manifest [>]")
    else:
        commits = get_commits(args.ticket, args.last, args.from_ref, args.to_ref,
                              prefixes=active_prefixes,
                              all_commits=args.all_commits or args.skip_research)
    if not commits:
        print("No matching commits found.")
        sys.exit(0)

    # Apply batch limit: take the N oldest (first in list, since --reverse is used)
    if args.batch > 0:
        commits = commits[:args.batch]

    print(f"Found {len(commits)} commit(s) to analyze")
    if not args.dry_run and not args.no_commit:
        print("Auto-commit after each processed commit\n")
    else:
        print()

    analysis_root = repo_root / ANALYSIS_DIR
    success_count = 0

    for idx, (sha, subject) in enumerate(commits, 1):
        ticket = extract_ticket(subject)
        commit_dir = analysis_root / f"{ticket}-{sha[:8]}"
        diff_dir = commit_dir / "diff"

        print(f"[{idx}/{len(commits)}] {sha[:8]} {subject}")

        # Write commit metadata
        commit_dir.mkdir(parents=True, exist_ok=True)
        (commit_dir / "commit-info.txt").write_text(
            f"SHA: {sha}\nSubject: {subject}\nTicket: {ticket}\n",
            encoding="utf-8",
        )

        # Extract diffs
        try:
            diff_files = extract_diff_files(sha, diff_dir)
            print(f"  → Extracted {len(diff_files)} diff file(s)")
        except RuntimeError as e:
            print(f"  ⚠️  Failed to extract diffs: {e}")
            continue

        if not diff_files:
            print("  → No diffs, skipping")
            continue

        # Run agent
        if args.dry_run:
            print("  → Dry run — skipping agent")
        else:
            ok = run_agent(commit_dir, repo_root, instruction_abs, copilot_bat,
                          env, model=args.model, timeout=args.timeout)
            summary = commit_dir / "summary.md"
            summary_ok = summary.exists() and summary.stat().st_size > 0
            commit_ok = False
            if ok and summary_ok:
                success_count += 1
                print(f"  → Agent finished (✓ summary.md created)")
                if not args.no_commit:
                    commit_ok = git_commit_single(repo_root, sha, subject)
                else:
                    commit_ok = True  # treat dry/no-commit as success for manifest purposes
            elif ok and not summary_ok:
                print("  → Agent finished (⚠️  no summary.md — treating as failed)")
            else:
                print("  → Agent failed")

            if args.from_manifest:
                # Only mark [x] if BOTH the agent produced a summary AND git commit succeeded.
                # Otherwise mark [!] so the operator sees the failure and can re-run.
                marker = "x" if (ok and summary_ok and commit_ok) else "!"
                update_manifest_done(repo_root, sha, marker=marker)
                if not args.no_commit and marker == "x":
                    try:
                        subprocess.run(
                            ["git", "add", str(MANIFEST_FILE)],
                            cwd=str(repo_root), check=True, timeout=30
                        )
                    except Exception:
                        pass

        print()

        # Interactive pause between commits
        if args.interactive and idx < len(commits):
            try:
                answer = input("  ⏸  Press Enter to continue, 's' to skip next, 'q' to quit: ").strip().lower()
                if answer == "q":
                    print("\n  Stopped by user.")
                    break
                if answer == "s":
                    print("  → Will skip next commit")
                    # skip flag handled by continuing the loop
            except (EOFError, KeyboardInterrupt):
                print("\n  Stopped by user.")
                break


    print("=" * 50)
    print(f"✓ Complete! Processed {len(commits)} commits" +
          (f", {success_count} succeeded" if not args.dry_run else " (dry-run)"))
    print("=" * 50)

    # Post-processing: review instruction relevance
    if args.review and not args.dry_run:
        run_review(repo_root, copilot_bat, env, model=args.model, timeout=args.timeout)


if __name__ == "__main__":
    main()
