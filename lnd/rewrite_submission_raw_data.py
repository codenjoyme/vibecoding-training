"""UPD17: rewrite the per-module agent prompt to collect RAW artifacts only.

The previous version (UPD16) asked the user-side agent to make judgments
("Yes/No", "Quality: ...", "Description quality: ..."). That lets the user
edit the file before submission and cheat. UPD17 changes the philosophy:

    * The user-side agent collects RAW data only — file contents verbatim,
      command outputs verbatim, file lists, git metadata.
    * The server-side `autocheck` agent reads those raw artifacts and decides
      whether the submission is acceptable.

Cosmetic change also requested: use a regular 3-backtick ```markdown fence
for the prompt block. Inner code fences inside the report template use
tilde fences (`~~~lang ... ~~~`) so they don't terminate the outer block.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from textwrap import dedent

OUTPUT_DIR = Path(__file__).resolve().parent / "output"

PROMPT_PREAMBLE = (
    "You are a data-collection agent. Your job is to gather RAW artifacts from "
    "my project workspace and write them into a file named `report.md` in the "
    "project root. Do NOT make judgments, do NOT summarize, do NOT add "
    "opinions. Paste file contents verbatim. Paste command outputs verbatim. "
    "If a value is genuinely missing, write `N/A`. Use tilde fences (`~~~`) "
    "for every inner code block so they don't conflict with the outer "
    "markdown fence. Replace any real `tokens`, `API keys`, passwords, or "
    "secrets with the literal text `[REDACTED]` everywhere they appear."
)


COMMON_HEADER = dedent("""\
    # {title}
    - Module: {module_no} — {module_name}
    - Repository remote URL: `[output of `git remote get-url origin` or `N/A`]`
    - Repository local path: `[absolute path to the project root]`
    - Current commit SHA: `[output of `git rev-parse HEAD`]`
    - Current branch: `[output of `git rev-parse --abbrev-ref HEAD`]`
    - Report generated at: `[ISO 8601 timestamp]`
    """)


def header(title: str, module_no: str, module_name: str) -> str:
    return COMMON_HEADER.format(
        title=title, module_no=module_no, module_name=module_name
    )


def build_section(agent_prompt_body: str, criteria_lines: list[str]) -> str:
    prompt_block = "\n".join(
        ("   " + line).rstrip() for line in agent_prompt_body.splitlines()
    )
    criteria_block = "\n".join(f"   {line}" for line in criteria_lines)
    return (
        f"**Submit your `report.md` for automated check:**\n"
        "\n"
        "1. In your AI agent (`Copilot` / `Cursor` / `Claude Code`), open your project workspace and run the prompt below. The agent will collect raw artifacts from your project and write them into a `report.md` file in the project root. The server-side `autocheck` will read the raw data and decide whether the submission is acceptable — your local agent must NOT make judgments itself.\n"
        "\n"
        "   ```markdown\n"
        f"{prompt_block}\n"
        "   ```\n"
        "\n"
        "2. Submit `report.md` to the `autocheck` system (the submission endpoint is being set up in parallel; instructions for accessing it will be shared once it is available).\n"
        "3. The `autocheck` system will check that:\n"
        f"{criteria_block}\n"
    )


MODULES: dict[str, dict] = {
    "module-08-clarifying-requirements.md": {
        "agent_prompt": (
            f"{PROMPT_PREAMBLE}\n\n"
            "Collect the following raw artifacts for Module 08 — Clarifying Requirements. Write them into `report.md` in this exact structure (do not change headings, do not add or remove sections):\n\n"
            + header("Module 08 Submission — Raw Data", "08", "Clarifying Requirements")
            + dedent("""\

                ## Specification File Metadata
                - Path: `[relative/path/to/spec/file.md]`
                - Size (bytes): `[N]`
                - Last modified: `[ISO 8601 timestamp]`
                - SHA-256 of file contents: `[hash]`

                ## Specification File — Verbatim Contents
                ~~~markdown
                [Paste the ENTIRE file contents here, byte-for-byte. Do NOT summarize, edit, or reformat.]
                ~~~

                ## Recent Commits Touching This File
                Output of `git log --oneline -10 -- [path/to/spec/file.md]`:
                ~~~
                [paste output verbatim]
                ~~~

                ## Repository File Tree (top level)
                Output of `git ls-files | head -50`:
                ~~~
                [paste output verbatim]
                ~~~
                """)
        ),
        "criteria": [
            "- Covers the automation goal clearly",
            "- Includes at least the key requirements surfaced during the AI interview",
            "- Is written in English",
            "- Is structured (not a single paragraph of free text)",
        ],
    },
    "module-09-agent-memory-management.md": {
        "agent_prompt": (
            f"{PROMPT_PREAMBLE}\n\n"
            "Collect the following raw artifacts for Module 09 — Agent Memory Management. Write them into `report.md` in this exact structure:\n\n"
            + header("Module 09 Submission — Raw Data", "09", "Agent Memory Management")
            + dedent("""\

                ## project_spec.md — Metadata
                - Path: `[relative/path/to/project_spec.md]`
                - Size (bytes): `[N]`
                - Last modified: `[ISO 8601 timestamp]`

                ## project_spec.md — Verbatim Contents
                ~~~markdown
                [Paste the ENTIRE file contents here, byte-for-byte.]
                ~~~

                ## backlog.md — Metadata
                - Path: `[relative/path/to/backlog.md]`
                - Size (bytes): `[N]`
                - Last modified: `[ISO 8601 timestamp]`

                ## backlog.md — Verbatim Contents
                ~~~markdown
                [Paste the ENTIRE file contents here, byte-for-byte.]
                ~~~

                ## Recent Commits Touching These Files
                Output of `git log --oneline -10 -- project_spec.md backlog.md`:
                ~~~
                [paste output verbatim]
                ~~~
                """)
        ),
        "criteria": [
            "- `project_spec.md` clearly states the automation goal, requirements, and quality standards.",
            "- `backlog.md` breaks the work into phases with checkboxes and specific, actionable tasks.",
            "- Both files are written in English and are committed to your repository.",
        ],
    },
    "module-10-custom-instructions.md": {
        "agent_prompt": (
            f"{PROMPT_PREAMBLE}\n\n"
            "Collect the following raw artifacts for Module 10 — Custom Instructions. Write them into `report.md` in this exact structure:\n\n"
            + header("Module 10 Submission — Raw Data", "10", "Custom Instructions")
            + dedent("""\

                ## Instructions Folder Listing
                Output of `git ls-files instructions/`:
                ~~~
                [paste output verbatim — every file under instructions/]
                ~~~

                ## Entry-Point File
                - Path: `[.github/copilot-instructions.md | .cursor/rules/main.mdc | N/A]`

                ### Entry-Point File — Verbatim Contents
                ~~~markdown
                [Paste full contents here. If file does not exist, write the literal text: FILE NOT FOUND]
                ~~~

                ## Catalog File: instructions/main.agent.md

                ### Catalog — Verbatim Contents
                ~~~markdown
                [Paste full contents of instructions/main.agent.md here. If file does not exist, write FILE NOT FOUND.]
                ~~~

                ## Each Instruction File — Verbatim Contents
                For EVERY file in `instructions/` (one block per file), paste:

                ### `[relative/path/to/file.agent.md]`
                ~~~markdown
                [Paste full contents here.]
                ~~~

                [Repeat the heading + tilde block above for each file. Do not omit any.]
                """)
        ),
        "criteria": [
            "- Uses the `[verb]-[subject].agent.md` naming convention for each instruction file.",
            "- Each instruction covers a single workflow (no catch-all files).",
            "- All instructions are listed with descriptions in `instructions/main.agent.md`.",
            "- The entry point file (`.github/copilot-instructions.md` or `.cursor/rules/main.mdc`) exists and references the catalog.",
            "- All files are committed to your repository.",
        ],
    },
    "module-11-learning-from-hallucinations.md": {
        "agent_prompt": (
            f"{PROMPT_PREAMBLE}\n\n"
            "Collect the following raw artifacts for Module 11 — Learning From Hallucinations. Write them into `report.md` in this exact structure:\n\n"
            + header("Module 11 Submission — Raw Data", "11", "Learning From Hallucinations")
            + dedent("""\

                ## Updated Instruction File
                - Path: `[relative/path/to/instructions/file.agent.md]`
                - Size (bytes): `[N]`
                - Last modified: `[ISO 8601 timestamp]`

                ### Verbatim Contents (current version)
                ~~~markdown
                [Paste full current contents here, byte-for-byte.]
                ~~~

                ## Diff Against the Previous Commit
                Output of `git log -p -1 --follow [path/to/instruction/file]` (or `git diff HEAD~1 HEAD -- [path]`):
                ~~~diff
                [paste output verbatim]
                ~~~

                ## Hallucination Evidence
                If a chat transcript, conversation log, or notes file documenting the hallucination exists in the repository (e.g., under `requests/`, `chat-history/`, `notes/`, or similar), paste it verbatim below. Otherwise write `NO TRANSCRIPT FILE FOUND`.

                ### Source File
                - Path: `[relative/path | N/A]`

                ### Verbatim Contents
                ~~~
                [paste full contents OR `NO TRANSCRIPT FILE FOUND`]
                ~~~

                ## Recent Commits to Instructions Folder
                Output of `git log --oneline -10 -- instructions/`:
                ~~~
                [paste output verbatim]
                ~~~
                """)
        ),
        "criteria": [
            "- A specific, real `hallucination` is described (not a hypothetical example).",
            "- The `instruction` fix targets the root cause, not just the symptom.",
            "- The updated `instruction` has a rule that prevents the `hallucination` from recurring.",
            "- The file is committed to your repository.",
        ],
    },
    "module-12-ai-skills-tools-creation.md": {
        "agent_prompt": (
            f"{PROMPT_PREAMBLE}\n\n"
            "Collect the following raw artifacts for Module 12 — AI Skills / Tools Creation. Write them into `report.md` in this exact structure:\n\n"
            + header("Module 12 Submission — Raw Data", "12", "AI Skills / Tools Creation")
            + dedent("""\

                ## Instruction File
                - Path: `[relative/path/to/instructions/[name].agent.md]`
                - Size (bytes): `[N]`

                ### Verbatim Contents
                ~~~markdown
                [Paste full file contents here, byte-for-byte.]
                ~~~

                ## Tool / Script File
                - Path: `[relative/path/to/script]`
                - Size (bytes): `[N]`
                - Language / runtime: `[Python | Node.js | Bash | ...]`

                ### Verbatim Contents
                ~~~
                [Paste full file contents here, byte-for-byte. Use a tilde fence; pick the language hint that matches.]
                ~~~

                ## Recent Commits Touching These Files
                Output of `git log --oneline -10 -- [instruction-path] [tool-path]`:
                ~~~
                [paste output verbatim]
                ~~~
                """)
        ),
        "criteria": [
            "- The task genuinely requires precision (calculation, API query, or data operation).",
            "- The instruction clearly specifies when and how to invoke the tool.",
            "- The tool accepts parameters - nothing is hardcoded.",
            "- Both files are committed to your repository.",
        ],
    },
    "module-13-mcp-model-context-protocol.md": {
        "agent_prompt": (
            f"{PROMPT_PREAMBLE}\n\n"
            "Collect the following raw artifacts for Module 13 — MCP. Write them into `report.md` in this exact structure. CRITICAL: scan the configuration for any `tokens`, `API keys`, or password-like values and replace them with `[REDACTED]` BEFORE pasting; never paste real secrets.\n\n"
            + header("Module 13 Submission — Raw Data", "13", "MCP (Model Context Protocol)")
            + dedent("""\

                ## MCP Config File
                - Path: `[.vscode/mcp.json | .cursor/mcp.json]`
                - Size (bytes): `[N]`

                ### Verbatim Contents (with secrets redacted)
                ~~~json
                [Paste full JSON contents here. Replace every token/key/secret value with the literal string "[REDACTED]". Keep all keys, server names, command paths, and tool lists intact.]
                ~~~

                ## Git Tracking Status
                Output of `git ls-files .vscode/mcp.json .cursor/mcp.json`:
                ~~~
                [paste output verbatim]
                ~~~

                ## Secret Audit Detection
                List every key/path in the JSON that you replaced with `[REDACTED]` (one per line, format `key.path: REDACTED`). If none, write `NONE`:
                ~~~
                [list]
                ~~~
                """)
        ),
        "criteria": [
            "- At least one `MCP` server is configured and functional.",
            "- Only tools relevant to your project are enabled.",
            "- The configuration file is committed to your repository with no credentials or `tokens` included.",
        ],
    },
    "module-14-mcp-github-integration-issues.md": {
        "agent_prompt": (
            f"{PROMPT_PREAMBLE}\n\n"
            "Collect the following raw artifacts for Module 14 — MCP GitHub Integration / Issues. Write them into `report.md` in this exact structure:\n\n"
            + header("Module 14 Submission — Raw Data", "14", "MCP GitHub Integration / Issues")
            + dedent("""\

                ## backlog.md
                - Path: `[relative/path/to/backlog.md]`
                - Size (bytes): `[N]`
                - Last modified: `[ISO 8601 timestamp]`

                ### Verbatim Contents
                ~~~markdown
                [Paste full file contents here, byte-for-byte.]
                ~~~

                ## GitHub Issues (live)
                Output of `gh issue list --state all --limit 50 --json number,title,state,createdAt,author,url` (or `gh issue list --limit 50` if `--json` is unavailable). If `gh` CLI is not installed, write `gh CLI NOT AVAILABLE`:
                ~~~json
                [paste output verbatim]
                ~~~

                ## Issue Creation Evidence
                If a chat transcript, MCP log, or session file in the repository shows that issues were created from the AI chat using the `GitHub` `MCP` server, list those file paths and paste their contents below. Otherwise write `NO MCP-CREATION TRANSCRIPT FOUND`.

                ### Source files
                ~~~
                [list paths or NO MCP-CREATION TRANSCRIPT FOUND]
                ~~~

                ### Verbatim contents
                ~~~
                [paste full contents of each listed file, separated by `--- next file ---`]
                ~~~

                ## Recent Commits to backlog.md
                Output of `git log --oneline -10 -- [path/to/backlog.md]`:
                ~~~
                [paste output verbatim]
                ~~~
                """)
        ),
        "criteria": [
            "- At least 3 backlog tasks have corresponding `GitHub` issue numbers or URLs added.",
            "- Issues were created from the AI chat using the `GitHub` `MCP` server (not manually through the web interface).",
            "- The updated `backlog.md` is committed to your repository.",
        ],
    },
    "module-15-bulk-file-processing.md": {
        "agent_prompt": (
            f"{PROMPT_PREAMBLE}\n\n"
            "Collect the following raw artifacts for Module 15 — Bulk File Processing. Write them into `report.md` in this exact structure:\n\n"
            + header("Module 15 Submission — Raw Data", "15", "Bulk File Processing")
            + dedent("""\

                ## Approach Marker
                One of: `single-request` | `iterative` | `script`. Determined mechanically: if a script file is present and was used, write `script`; if multiple chat sessions for the same task exist, write `iterative`; otherwise `single-request`.
                - Approach: `[single-request | iterative | script]`

                ## Source Folder
                - Path: `[relative/path]`

                ### File listing
                Output of `git ls-files [source-folder]`:
                ~~~
                [paste output verbatim]
                ~~~

                - File count: `[N]`
                - File extension(s): `[.md | .json | ...]`

                ## Script (if any)
                - Path: `[relative/path/to/script | N/A]`

                ### Verbatim Contents
                ~~~
                [Paste full script contents byte-for-byte, OR write `NO SCRIPT — APPROACH WAS [single-request|iterative]`. Use a tilde fence with the matching language hint.]
                ~~~

                ## Justification Note
                - Path: `[relative/path/to/note.md | N/A]`

                ### Verbatim Contents
                ~~~markdown
                [Paste full note contents, OR write `NO NOTE FILE`. The note should describe why this approach matches the batch size and consistency requirement.]
                ~~~

                ## Recent Commits Touching Source Folder or Script
                Output of `git log --oneline -10 -- [source-folder] [script-path]`:
                ~~~
                [paste output verbatim]
                ~~~
                """)
        ),
        "criteria": [
            "- The approach matches the batch size and consistency requirements from the module.",
            "- If a script was used, each file is processed in a separate `context window`.",
            "- The choice of approach is clearly justified.",
        ],
    },
    "module-16-development-environment-setup.md": {
        "agent_prompt": (
            f"{PROMPT_PREAMBLE}\n\n"
            "Collect the following raw artifacts for Module 16 — Development Environment Setup. Write them into `report.md` in this exact structure. Each command output must be pasted VERBATIM, including any error messages.\n\n"
            + header("Module 16 Submission — Raw Data", "16", "Development Environment Setup")
            + dedent("""\

                ## Host
                - OS: `[output of `uname -a` on Unix, or `[System.Environment]::OSVersion` on Windows]`
                - Shell: `[$SHELL on Unix, or $PSVersionTable.PSVersion on Windows]`

                ## node --version
                ~~~
                [paste full output verbatim, including stderr if any. If command is not found, paste the shell error verbatim.]
                ~~~

                ## npm --version
                ~~~
                [paste full output verbatim]
                ~~~

                ## nvm --version
                ~~~
                [paste full output verbatim]
                ~~~

                ## docker --version
                ~~~
                [paste full output verbatim]
                ~~~

                ## node --print process.versions
                ~~~
                [paste full output verbatim, OR `N/A` if node is missing]
                ~~~
                """)
        ),
        "criteria": [
            "- All four tools are installed and return a version number.",
            "- `Node.js` version is 20 or higher (LTS recommended).",
            "- `Docker` is installed and returns a version (it does not need to be running).",
        ],
    },
    "module-17-rapid-prototyping-speckit.md": {
        "agent_prompt": (
            f"{PROMPT_PREAMBLE}\n\n"
            "Collect the following raw artifacts for Module 17 — Rapid Prototyping with SpecKit. Write them into `report.md` in this exact structure:\n\n"
            + header("Module 17 Submission — Raw Data", "17", "Rapid Prototyping with SpecKit")
            + dedent("""\

                ## Specification File
                - Path: `[relative/path/to/specification.md]`
                - Size (bytes): `[N]`

                ### Verbatim Contents
                ~~~markdown
                [Paste full file contents here, byte-for-byte.]
                ~~~

                ## Task List File
                - Path: `[relative/path/to/task-list.md | N/A]`

                ### Verbatim Contents
                ~~~markdown
                [Paste full file contents here. If no task list file exists, write `NO TASK LIST FILE`.]
                ~~~

                ## Recent Commits (last 20)
                Output of `git log --oneline -20`:
                ~~~
                [paste output verbatim]
                ~~~

                ## Last Commit Diff Stat
                Output of `git show --stat HEAD`:
                ~~~
                [paste output verbatim]
                ~~~

                ## Implementation Evidence
                For the most recent commit that implements work from the task list, paste the diff:
                Output of `git show [SHA]`:
                ~~~diff
                [paste output verbatim, truncated at ~500 lines if longer; note "TRUNCATED AT N LINES" at the end if so]
                ~~~
                """)
        ),
        "criteria": [
            "- The specification describes a real use case from your project (not a placeholder example).",
            "- Tasks are broken into baby steps with clear acceptance criteria.",
            "- At least one task was implemented, verified, and committed.",
            "- A repository URL or commit reference demonstrates working code was produced.",
        ],
    },
    "module-18-chrome-devtools-mcp-qa.md": {
        "agent_prompt": (
            f"{PROMPT_PREAMBLE}\n\n"
            "Collect the following raw artifacts for Module 18 — Chrome DevTools MCP QA. Write them into `report.md` in this exact structure:\n\n"
            + header("Module 18 Submission — Raw Data", "18", "Chrome DevTools MCP QA")
            + dedent("""\

                ## QA Report File
                - Path: `[relative/path/to/qa-report.md]`
                - Size (bytes): `[N]`
                - Last modified: `[ISO 8601 timestamp]`

                ### Verbatim Contents
                ~~~markdown
                [Paste full QA report contents here, byte-for-byte.]
                ~~~

                ## Recent Commits Touching the QA Report
                Output of `git log --oneline -10 -- [path/to/qa-report.md]`:
                ~~~
                [paste output verbatim]
                ~~~

                ## Recent Bug-Fix Commits (last 30)
                Output of `git log --oneline -30`:
                ~~~
                [paste output verbatim]
                ~~~

                ## Repository State
                - Output of `git status --short`:
                ~~~
                [paste output verbatim]
                ~~~
                """)
        ),
        "criteria": [
            "- The report covers at least 3 distinct UI scenarios (e.g., page navigation, form submission, error handling).",
            "- Found bugs are documented with descriptions.",
            "- All bugs found were fixed and committed before the report was finalized.",
            "- The report confirms the prototype passed QA in its final state.",
        ],
    },
    "module-19-github-coding-agent-delegation.md": {
        "agent_prompt": (
            f"{PROMPT_PREAMBLE}\n\n"
            "Collect the following raw artifacts for Module 19 — GitHub Coding Agent Delegation. Write them into `report.md` in this exact structure. Use the `gh` CLI for every fetch. If `gh` is not installed, write `gh CLI NOT AVAILABLE` in each affected block.\n\n"
            + header("Module 19 Submission — Raw Data", "19", "GitHub Coding Agent Delegation")
            + dedent("""\

                ## Issue Identifier
                - Repository: `[owner/repo]`
                - Issue number: `[N]`

                ## Issue — Raw
                Output of `gh issue view [N] --json number,title,body,state,createdAt,author,assignees,labels,url`:
                ~~~json
                [paste output verbatim]
                ~~~

                ## Pull Request — Raw
                Output of `gh pr list --state all --search "linked:#[N]" --json number,title,state,createdAt,author,url,isDraft,headRefName`:
                ~~~json
                [paste output verbatim]
                ~~~

                Output of `gh pr view [PR-number] --json number,title,body,state,createdAt,author,url,reviews,commits`:
                ~~~json
                [paste output verbatim]
                ~~~

                ## Pull Request Diff Stat
                Output of `gh pr diff [PR-number] --name-only`:
                ~~~
                [paste output verbatim]
                ~~~

                ## Review Comments — Raw
                Output of `gh api repos/[owner]/[repo]/pulls/[PR-number]/comments`:
                ~~~json
                [paste output verbatim]
                ~~~

                ## Local Instruction File Updates Triggered by Agent Mistakes
                Output of `git log --oneline -10 -- instructions/`:
                ~~~
                [paste output verbatim]
                ~~~
                """)
        ),
        "criteria": [
            "- The `GitHub` issue has a clear description with acceptance criteria.",
            "- The PR was created by the coding `agent` (not manually committed).",
            "- You submitted all review comments at once (not one by one).",
            "- Any `agent` mistakes were treated as `instruction` improvement opportunities.",
        ],
    },
    "module-20-dial-api-key-curl-access.md": {
        "agent_prompt": (
            f"{PROMPT_PREAMBLE}\n\n"
            "Collect the following raw artifacts for Module 20 — DIAL API Key & cURL Access. Write them into `report.md` in this exact structure. CRITICAL: replace the real `API key` value in the command with `[REDACTED]` — never paste the actual key. The full JSON response stays unredacted.\n\n"
            + header("Module 20 Submission — Raw Data", "20", "DIAL API Key & cURL Access")
            + dedent("""\

                ## Endpoint
                - URL: `[full request URL]`
                - HTTP method: `[GET | POST | ...]`

                ## cURL Command (with API key redacted)
                ~~~bash
                [Paste the exact command verbatim. Replace the API key value with the literal string [REDACTED]. Do not remove any other parameter.]
                ~~~

                ## Request Body (with secrets redacted)
                ~~~json
                [Paste the JSON request body verbatim if applicable, OR write `NO BODY` for GET requests. Redact any secret values.]
                ~~~

                ## HTTP Status
                ~~~
                [paste status line and headers verbatim from `-i` output, OR just the numeric status if only the body is available]
                ~~~

                ## Response Body — Verbatim JSON
                ~~~json
                [Paste the FULL response body byte-for-byte. Do not redact response content; redact only credentials in the request.]
                ~~~

                ## Use Case Context File
                - Path: `[relative/path/to/file describing why this API call matters in my project | N/A]`

                ### Verbatim Contents
                ~~~markdown
                [Paste full file contents, OR write `NO CONTEXT FILE`.]
                ~~~
                """)
        ),
        "criteria": [
            "- The request reaches the `DIAL` endpoint and returns a valid `JSON` response.",
            "- The model, temperature, and max_tokens parameters are visible in the command.",
            "- The `API key` is not included in plain text - replace it with `[REDACTED]`.",
            "- The response demonstrates a real use case relevant to your project context.",
        ],
    },
}


SUBMIT_HEADING_RE = re.compile(
    r"\*\*Submit your [^\n]*for automated check:\*\*\n(?:.|\n)*$",
    re.MULTILINE,
)


def main() -> int:
    if not OUTPUT_DIR.exists():
        print(f"Output dir not found: {OUTPUT_DIR}")
        return 1

    changed = 0
    for filename, spec in MODULES.items():
        path = OUTPUT_DIR / filename
        if not path.exists():
            print(f"  MISSING: {filename}")
            continue

        original = path.read_text(encoding="utf-8")
        if not SUBMIT_HEADING_RE.search(original):
            print(f"  no submission heading: {filename}")
            continue

        new_section = build_section(
            agent_prompt_body=spec["agent_prompt"].rstrip(),
            criteria_lines=spec["criteria"],
        )

        updated = SUBMIT_HEADING_RE.sub(lambda _m: new_section, original)
        if not updated.endswith("\n"):
            updated += "\n"

        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"  updated: {filename}")
        else:
            print(f"  no change: {filename}")

    print(f"\nDone. {changed}/{len(MODULES)} files updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
