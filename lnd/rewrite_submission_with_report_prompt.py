"""UPD16: replace the "Locate X" first step in every module's autocheck
submission section with an agent prompt that produces a unified `report.md`.

Per UPD16: only the first numbered step changes; the "Submit it to the
`autocheck` system" step and the "The `autocheck` system will check that:" step
(with its criteria bullets) stay the same. For modules that had an extra
"prepare a brief note" preparation step, that step is folded into the agent
prompt and removed from the list (so the final list is always 3 items).

The script rewrites the entire submission block per module from a small
per-module specification (subject, agent prompt body, criteria bullets).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from textwrap import dedent

OUTPUT_DIR = Path(__file__).resolve().parent / "output"

# Common preamble to every agent prompt: explains where the report should go
# and that the autocheck expects EXACTLY this format.
PROMPT_PREAMBLE = (
    "You are helping me prepare a submission report for an `autocheck` system. "
    "Inspect my current project workspace and create a file named `report.md` "
    "in the project root with EXACTLY the structure shown below. "
    "Replace bracketed placeholders with real values from my project. "
    "Do not add extra sections, do not omit sections, do not invent data. "
    "If a value is genuinely unknown or missing, write `N/A`."
)


def build_section(subject: str, agent_prompt_body: str, criteria_lines: list[str]) -> str:
    """Build the full replacement submission section."""
    # Indent the agent prompt body by 3 spaces so it stays inside list item 1.
    prompt_block = "\n".join(
        ("   " + line).rstrip() for line in agent_prompt_body.splitlines()
    )
    criteria_block = "\n".join(f"   {line}" for line in criteria_lines)
    return (
        f"**Submit your `report.md` for automated check:**\n"
        "\n"
        "1. In your AI agent (`Copilot` / `Cursor` / `Claude Code`), open your project workspace and run the prompt below. The agent will inspect your project and create a `report.md` file in the project root, in the exact format the `autocheck` expects:\n"
        "\n"
        "   ````markdown\n"
        f"{prompt_block}\n"
        "   ````\n"
        "\n"
        "2. Submit `report.md` to the `autocheck` system (the submission endpoint is being set up in parallel; instructions for accessing it will be shared once it is available).\n"
        "3. The `autocheck` system will check that:\n"
        f"{criteria_block}\n"
    )


# Per-module specifications. Key = filename stem.
MODULES: dict[str, dict] = {
    "module-08-clarifying-requirements.md": {
        "agent_prompt": dedent(f"""\
            {PROMPT_PREAMBLE}

            Source: the specification file I created and committed during Module 08 — Clarifying Requirements (typical names: `specification.md`, `project_spec.md`, or similar in the repository root or `docs/`). Locate it, read it, then write `report.md` in this exact format:

            # Specification Report
            - Module: 08 — Clarifying Requirements
            - Specification file: `[relative/path/to/file]`
            - Repository: `[git remote URL or local path]`
            - Commit: `[short SHA of HEAD]`
            - Language: `[English | Other]`

            ## Automation Goal
            [One paragraph stating the automation goal in plain English, copied or summarized faithfully from the file.]

            ## Key Requirements
            - [Requirement 1, as it appears in the file]
            - [Requirement 2]
            - [Requirement 3]
            - [... list ALL requirements surfaced during the AI interview, one per bullet]

            ## Structure
            - Top-level section count: [N]
            - Top-level section names: [comma-separated list]
            - Single-paragraph free text: [Yes | No]
            """),
        "criteria": [
            "- Covers the automation goal clearly",
            "- Includes at least the key requirements surfaced during the AI interview",
            "- Is written in English",
            "- Is structured (not a single paragraph of free text)",
        ],
    },
    "module-09-agent-memory-management.md": {
        "agent_prompt": dedent(f"""\
            {PROMPT_PREAMBLE}

            Source: the files `project_spec.md` and `backlog.md` in my repository (Module 09 — Agent Memory Management). Locate both, read them, then write `report.md` in this exact format:

            # Memory Files Report
            - Module: 09 — Agent Memory Management
            - Repository: `[git remote URL or local path]`
            - Commit: `[short SHA of HEAD]`
            - Language: `[English | Other]`

            ## project_spec.md
            - Path: `[relative/path/to/project_spec.md]`
            - Automation goal: [one sentence quoted or summarized from the file]
            - Requirements stated: [Yes | No]
            - Quality standards stated: [Yes | No]

            ## backlog.md
            - Path: `[relative/path/to/backlog.md]`
            - Phase count: [N]
            - Total tasks: [N]
            - Tasks use checkboxes (`- [ ]`): [Yes | No]
            - Tasks are actionable (specific verbs, not vague goals): [Yes | No]

            ## Phases
            - [Phase 1 name] — [task count]
            - [Phase 2 name] — [task count]
            - [...]
            """),
        "criteria": [
            "- `project_spec.md` clearly states the automation goal, requirements, and quality standards.",
            "- `backlog.md` breaks the work into phases with checkboxes and specific, actionable tasks.",
            "- Both files are written in English and are committed to your repository.",
        ],
    },
    "module-10-custom-instructions.md": {
        "agent_prompt": dedent(f"""\
            {PROMPT_PREAMBLE}

            Source: the instruction files in `instructions/` (created during Pages 4–5 of Module 10), the catalog `instructions/main.agent.md`, and the entry-point file (`.github/copilot-instructions.md` for VS Code or `.cursor/rules/main.mdc` for Cursor). Locate them, then write `report.md`:

            # Instructions Report
            - Module: 10 — Custom Instructions
            - Repository: `[git remote URL or local path]`
            - Commit: `[short SHA of HEAD]`
            - Entry-point file: `[.github/copilot-instructions.md | .cursor/rules/main.mdc | N/A]`
            - Catalog file: `[instructions/main.agent.md | N/A]`

            ## Instruction Files
            - `[instructions/verb-subject.agent.md]` — [one-sentence purpose]
            - `[instructions/verb-subject.agent.md]` — [one-sentence purpose]
            - [... list every file in `instructions/`]

            ## Naming Convention Check
            - Files following `[verb]-[subject].agent.md` pattern: [N of M]
            - Files NOT following the pattern: [list filenames or `none`]

            ## Catalog Check
            - Each instruction file listed in catalog with description: [Yes | No]
            - Entry-point file references the catalog: [Yes | No]
            """),
        "criteria": [
            "- Uses the `[verb]-[subject].agent.md` naming convention for each instruction file.",
            "- Each instruction covers a single workflow (no catch-all files).",
            "- All instructions are listed with descriptions in `instructions/main.agent.md`.",
            "- The entry point file (`.github/copilot-instructions.md` or `.cursor/rules/main.mdc`) exists and references the catalog.",
            "- All files are committed to your repository.",
        ],
    },
    "module-11-learning-from-hallucinations.md": {
        "agent_prompt": dedent(f"""\
            {PROMPT_PREAMBLE}

            Source: the `instruction` file I updated as a result of a real `hallucination` I encountered during Module 11. Locate it (most recently changed file under `instructions/`), then write `report.md`:

            # Hallucination-Driven Instruction Update Report
            - Module: 11 — Learning From Hallucinations
            - Repository: `[git remote URL or local path]`
            - Commit: `[short SHA of HEAD]`
            - Updated instruction file: `[relative/path/to/instructions/file.agent.md]`

            ## Hallucination
            [Two to four sentences describing the specific, real unexpected behavior I observed: what I asked, what the AI produced, why it was wrong.]

            ## Root Cause
            [One or two sentences explaining which `instruction` rule was missing, ambiguous, or wrong — the underlying gap, not just the symptom.]

            ## Instruction Fix
            - Rule added or changed: `[concise description of the new/edited rule]`
            - Location in file: `[heading or section the rule lives in]`
            - Why this prevents recurrence: [one sentence]

            ## Diff Summary
            - Lines added: [N]
            - Lines removed: [N]
            """),
        "criteria": [
            "- A specific, real `hallucination` is described (not a hypothetical example).",
            "- The `instruction` fix targets the root cause, not just the symptom.",
            "- The updated `instruction` has a rule that prevents the `hallucination` from recurring.",
            "- The file is committed to your repository.",
        ],
    },
    "module-12-ai-skills-tools-creation.md": {
        "agent_prompt": dedent(f"""\
            {PROMPT_PREAMBLE}

            Source: the instruction file and the corresponding tool/script I created during Module 12 — AI Skills & Tools Creation (typically `instructions/[name].agent.md` plus a script in the project). Locate both, then write `report.md`:

            # Skill & Tool Report
            - Module: 12 — AI Skills / Tools Creation
            - Repository: `[git remote URL or local path]`
            - Commit: `[short SHA of HEAD]`
            - Instruction file: `[relative/path/to/instructions/[name].agent.md]`
            - Tool / script file: `[relative/path/to/script]`
            - Tool language / runtime: `[Python | Node.js | Bash | ...]`

            ## Task Justification
            [Two to three sentences explaining why this task genuinely requires precision (calculation, API query, deterministic data operation) and would be unreliable if done by the LLM directly.]

            ## Invocation Rule
            [Quote or paraphrase the rule from the instruction file that tells the AI WHEN to call the tool and HOW to pass arguments.]

            ## Parameters
            - Parameter `[name]`: [type, what it controls]
            - Parameter `[name]`: [type, what it controls]
            - [... list every parameter the tool accepts]
            - Hardcoded inputs in the tool: [None | list them]
            """),
        "criteria": [
            "- The task genuinely requires precision (calculation, API query, or data operation).",
            "- The instruction clearly specifies when and how to invoke the tool.",
            "- The tool accepts parameters - nothing is hardcoded.",
            "- Both files are committed to your repository.",
        ],
    },
    "module-13-mcp-model-context-protocol.md": {
        "agent_prompt": dedent(f"""\
            {PROMPT_PREAMBLE}

            Source: my `MCP` configuration file — `.vscode/mcp.json` (VS Code) or `.cursor/mcp.json` (Cursor). Locate it, then write `report.md`. CRITICAL: do NOT include any real `tokens`, `API keys`, or secrets — replace any such value with `[REDACTED]`.

            # MCP Configuration Report
            - Module: 13 — MCP (Model Context Protocol)
            - Repository: `[git remote URL or local path]`
            - Commit: `[short SHA of HEAD]`
            - Config file: `[.vscode/mcp.json | .cursor/mcp.json]`

            ## Servers
            - `[server_name]` — command: `[command]`, status: `[functional | not tested]`
            - [... list every configured server]

            ## Enabled Tools (per server)
            - `[server_name]`:
              - `[tool_name]` — purpose: [one sentence, why it is relevant to my project]
              - `[tool_name]` — purpose: [...]

            ## Secrets Audit
            - Any `tokens` / `API keys` present in plain text: [Yes | No]
            - If yes, file path and field name: [list or `N/A`]
            """),
        "criteria": [
            "- At least one `MCP` server is configured and functional.",
            "- Only tools relevant to your project are enabled.",
            "- The configuration file is committed to your repository with no credentials or `tokens` included.",
        ],
    },
    "module-14-mcp-github-integration-issues.md": {
        "agent_prompt": dedent(f"""\
            {PROMPT_PREAMBLE}

            Source: the `backlog.md` I updated with `GitHub` issue references during Module 14. Locate it, then write `report.md`:

            # Backlog ↔ GitHub Issues Report
            - Module: 14 — MCP `GitHub` Integration / Issues
            - Repository: `[git remote URL or local path]`
            - Commit: `[short SHA of HEAD]`
            - Backlog file: `[relative/path/to/backlog.md]`

            ## Linked Tasks
            - [Task title]: `[#issue-number or full URL]`
            - [Task title]: `[#issue-number or full URL]`
            - [Task title]: `[#issue-number or full URL]`
            - [... list every backlog task that has a `GitHub` issue link]

            ## Counts
            - Backlog tasks total: [N]
            - Backlog tasks with `GitHub` issue links: [N]

            ## Creation Method
            - Issues were created from the AI chat using the `GitHub` `MCP` server: [Yes | No]
            - Evidence: [one sentence describing the chat command or workflow used]
            """),
        "criteria": [
            "- At least 3 backlog tasks have corresponding `GitHub` issue numbers or URLs added.",
            "- Issues were created from the AI chat using the `GitHub` `MCP` server (not manually through the web interface).",
            "- The updated `backlog.md` is committed to your repository.",
        ],
    },
    "module-15-bulk-file-processing.md": {
        "agent_prompt": dedent(f"""\
            {PROMPT_PREAMBLE}

            Source: either the bulk processing script I created OR a brief note about the non-script approach I used during Module 15. Locate the script (if any) under the project, then write `report.md`:

            # Bulk Processing Report
            - Module: 15 — Bulk File Processing
            - Repository: `[git remote URL or local path]`
            - Commit: `[short SHA of HEAD]`
            - Approach used: `[single-request | iterative | script]`
            - Script file (if any): `[relative/path/to/script | N/A]`

            ## Files Processed
            - Total files: [N]
            - File type / extension: `[.md | .json | ...]`
            - Source folder: `[relative/path]`

            ## Justification
            [Two to three sentences: why this batch size and consistency requirement led to the chosen approach. If iterative or script: explain how each file got its own context window. If single-request: explain why batching was safe.]

            ## Per-File Context Isolation
            - Each file processed in a separate `context window`: [Yes | No | N/A — single request]
            - Mechanism: [e.g., script loops and calls the agent once per file, OR new chat per file, OR N/A]
            """),
        "criteria": [
            "- The approach matches the batch size and consistency requirements from the module.",
            "- If a script was used, each file is processed in a separate `context window`.",
            "- The choice of approach is clearly justified.",
        ],
    },
    "module-16-development-environment-setup.md": {
        "agent_prompt": dedent(f"""\
            {PROMPT_PREAMBLE}

            Source: the local development environment on this machine. Run each version command in a terminal and capture the output. Then write `report.md`:

            # Environment Check Report
            - Module: 16 — Development Environment Setup
            - OS: `[Windows | macOS | Linux] [version]`
            - Shell: `[pwsh | bash | zsh | ...]`

            ## Tool Versions
            - Node.js: `[output of `node --version`]`
            - npm: `[output of `npm --version`]`
            - nvm: `[output of `nvm --version` — or `not installed`]`
            - Docker: `[output of `docker --version` — or `not installed`]`

            ## Checks
            - All four tools return a version: [Yes | No]
            - `Node.js` version is 20 or higher: [Yes | No]
            - `Docker` is installed (does not need to be running): [Yes | No]
            """),
        "criteria": [
            "- All four tools are installed and return a version number.",
            "- `Node.js` version is 20 or higher (LTS recommended).",
            "- `Docker` is installed and returns a version (it does not need to be running).",
        ],
    },
    "module-17-rapid-prototyping-speckit.md": {
        "agent_prompt": dedent(f"""\
            {PROMPT_PREAMBLE}

            Source: the `specification.md` (or equivalent spec file) created during the `SpecKit` workflow in Module 17, the task list used for implementation, and the commits demonstrating that at least one task was implemented. Locate everything, then write `report.md`:

            # SpecKit Prototype Report
            - Module: 17 — Rapid Prototyping with `SpecKit`
            - Repository: `[git remote URL or local path]`
            - Commit: `[short SHA of HEAD]`
            - Specification file: `[relative/path/to/specification.md]`
            - Task list file: `[relative/path/to/task-list.md or N/A]`

            ## Use Case
            [Two to three sentences describing the real use case from my project that the spec covers — not a placeholder example.]

            ## Tasks
            - [Task 1 name] — acceptance criteria: [one sentence] — status: `[done | in-progress | not started]`
            - [Task 2 name] — acceptance criteria: [one sentence] — status: `[done | in-progress | not started]`
            - [... list all tasks from the task list, in order]

            ## Implemented Task Evidence
            - Implemented task: `[task name]`
            - Commit SHA(s): `[short SHA(s) where the implementation was committed]`
            - Verification method: [one sentence — test run, manual check, etc.]
            """),
        "criteria": [
            "- The specification describes a real use case from your project (not a placeholder example).",
            "- Tasks are broken into baby steps with clear acceptance criteria.",
            "- At least one task was implemented, verified, and committed.",
            "- A repository URL or commit reference demonstrates working code was produced.",
        ],
    },
    "module-18-chrome-devtools-mcp-qa.md": {
        "agent_prompt": dedent(f"""\
            {PROMPT_PREAMBLE}

            Source: the QA report file generated during Module 18 (typically a markdown file produced by the `Chrome DevTools` `MCP` QA workflow). Locate it, read it, then write `report.md`:

            # QA Report Summary
            - Module: 18 — Chrome DevTools `MCP` QA
            - Repository: `[git remote URL or local path]`
            - Commit: `[short SHA of HEAD]`
            - QA report file: `[relative/path/to/qa-report.md]`

            ## Scenarios Tested
            - [Scenario 1 name] — [one-sentence description]
            - [Scenario 2 name] — [one-sentence description]
            - [Scenario 3 name] — [one-sentence description]
            - [... list every distinct UI scenario covered]

            ## Bugs Found
            - [Bug 1 short title] — fix commit: `[short SHA | N/A]`
            - [Bug 2 short title] — fix commit: `[short SHA | N/A]`
            - [... list every bug, or write `None`]

            ## Final State
            - All bugs fixed and committed before finalization: [Yes | No]
            - Prototype passed QA in its final state: [Yes | No]
            """),
        "criteria": [
            "- The report covers at least 3 distinct UI scenarios (e.g., page navigation, form submission, error handling).",
            "- Found bugs are documented with descriptions.",
            "- All bugs found were fixed and committed before the report was finalized.",
            "- The report confirms the prototype passed QA in its final state.",
        ],
    },
    "module-19-github-coding-agent-delegation.md": {
        "agent_prompt": dedent(f"""\
            {PROMPT_PREAMBLE}

            Source: the `GitHub` issue I assigned to the coding agent during Module 19, and the pull request the agent created. Use the `GitHub` `MCP` server (if available) or `gh` CLI to fetch the data. Then write `report.md`:

            # Coding Agent Delegation Report
            - Module: 19 — `GitHub` Coding Agent Delegation
            - Repository: `[owner/repo]`

            ## Issue
            - Number: `#[N]`
            - URL: `[full URL]`
            - Title: `[issue title]`
            - Description quality: [one sentence — does it have a clear description with acceptance criteria? Yes/No + brief reason.]

            ## Pull Request
            - Number: `#[N]`
            - URL: `[full URL]`
            - Title: `[PR title]`
            - Created at: `[ISO date]`
            - Status: `[open | closed | merged]`
            - Author: `[bot/agent username]`
            - Created by the coding `agent` (not manually committed): [Yes | No]

            ## Review Workflow
            - Review comments submitted all at once (single review batch): [Yes | No]
            - Total review comments: [N]
            - `Agent` mistakes treated as `instruction` improvement opportunities: [Yes | No]
            - Instruction file(s) updated as a result: `[list paths or N/A]`
            """),
        "criteria": [
            "- The `GitHub` issue has a clear description with acceptance criteria.",
            "- The PR was created by the coding `agent` (not manually committed).",
            "- You submitted all review comments at once (not one by one).",
            "- Any `agent` mistakes were treated as `instruction` improvement opportunities.",
        ],
    },
    "module-20-dial-api-key-curl-access.md": {
        "agent_prompt": dedent(f"""\
            {PROMPT_PREAMBLE}

            Source: a `cURL` request I run against the `DIAL` `API` and the `JSON` response I capture. Run the request, capture both the command and the response, then write `report.md`. CRITICAL: replace the real `API key` value in the command with `[REDACTED]` — do NOT include the actual key.

            # DIAL API Interaction Report
            - Module: 20 — `DIAL` `API` Key & `cURL` Access
            - Endpoint URL: `[full URL of the request]`
            - Project use case context: [two to three sentences describing why this `API` call is relevant to my project]

            ## cURL Command
            ```bash
            [paste the exact command here, with the `API key` value replaced by [REDACTED]]
            ```

            ## Parameters Used
            - model: `[model name]`
            - temperature: `[value]`
            - max_tokens: `[value]`

            ## Response
            - Status: `[HTTP status, e.g., 200]`
            - Valid `JSON`: [Yes | No]
            - Response body (full):
            ```json
            [paste the JSON response here]
            ```
            """),
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
            subject=filename,
            agent_prompt_body=spec["agent_prompt"].rstrip(),
            criteria_lines=spec["criteria"],
        )

        # Replace from the heading to end of file (every existing block goes
        # to EOF, verified beforehand).
        updated = SUBMIT_HEADING_RE.sub(lambda _m: new_section, original)
        # Ensure file ends with a single newline.
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
