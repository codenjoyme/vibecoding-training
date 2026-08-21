---
name: skills-management-python
description: Manage shared AI instruction skills with the Python Skills CLI and Git sparse checkout.
version: 1.0.0
---

# Skills Management System - Python Edition

This file is both a human guide and an AI skill. It describes the Python implementation of the Skills Management System, its command contract, and the workflow an AI agent should follow when setting it up or operating it.

## What This System Does

The system keeps AI instructions in a central Git repository and gives each project only the skills selected by its manifests. The Python CLI preserves the Go and Node.js interface while using Python's standard library and the system `git` executable.

| Capability | Implementation |
|---|---|
| Shared source of truth | Central Git repository containing one folder per skill |
| Project selection | `.manifest/` JSON files with global, group, and sub-config entries |
| Minimal local checkout | Git cone-mode sparse checkout |
| Team contribution | Feature branch, commits, push, and review/PR URL |
| Project customization | `skills.json` with groups, extra skills, and exclusions |
| AI support | `skills ai-help` prints `SKILL-CLI.md` |

## Port Layout

The `tools_py/` folder contains `pyproject.toml`, `skills.py`, this `SKILL.md`, `SKILL-CLI.md`, `README.md`, `go-node-differences.md`, the `skills_cli/` package, and `tests/`. The package has `commands/` for `root`, `help`, `init`, `pull`, `push`, `list`, `create`, `toggle`, `aihelp`, and `initrepo`; `lib/` contains `config`, `manifest`, `gitops`, and `errors`.

The direct `skills.py` launcher supports isolated portable Python distributions. A regular Python installation can also use `python -m skills_cli`.

## Prerequisites

- Python 3.10 or newer.
- Git 2.25 or newer with a configured user identity.
- Access to the central skills repository.
- A GitHub/GitLab token or SSH key when pushing to a remote host.

Check `python --version` and `git --version` before setup.

## Installation and Launch

From `tools_py/`, run `python .\skills.py help` on Windows or `python3 ./skills.py help` on macOS/Linux. On a regular Python installation, `python -m skills_cli help` is also supported.

To install a local `skills` command, run `python -m pip install .` and then `skills help`. Use `python -m pip install --editable .` for development. The runtime has no third-party dependencies. Git arguments are passed as an argument list, never through a shell command string.

## Central Repository Structure

```text
central-skills-repo/
├── .manifest/
│   ├── _global.json
│   ├── _agents.json
│   ├── <group-name>.json
│   └── <sub-config>.json
├── code-review-base/
│   ├── SKILL.md
│   └── info.json
└── ...
```

`_global.json` applies skills to every workspace. Group files list skills and reference reusable `sub-configs`. Each skill is a top-level folder with `SKILL.md`; `info.json` is recommended for metadata. Its fields are only `description` and `owner`.

## Resolution Rules

The resolver applies `_global.json` skills, selected group skills, recursively referenced `sub-configs`, deduplication and sorting, `extra_skills`, and finally `excluded_skills`. Exclusions override every other source. Sub-config traversal has cycle protection. A missing explicitly selected group is an error; a missing nested sub-config is warned about and skipped.

## Workspace Configuration

`skills init` writes `skills.json` in the project root with `repo_url`, `groups`, `extra_skills`, and `excluded_skills`. Active skills are resolved dynamically from the cloned manifests; the CLI does not persist a second `skills` list.

## Command Reference

### `skills init`

Use `skills init --repo <url-or-path> [--groups <group1>[,<group2>...]] [group...]` to clone into `instructions/`, resolve manifests, configure sparse checkout, and write `skills.json`. Groups are optional; without them only `_global.json` is used. If `skills.json` exists and `--repo` is omitted, the command reclones from the saved configuration.

### `skills pull`

Use `skills pull` to check out the detected default branch and run `git pull origin <branch>`.

### `skills push`

Use `skills push <skill-name> [--groups <group1> <group2> ...]`. The command creates or recreates `feature/<skill-name>-update`, commits the skill changes, optionally creates or updates group manifests and commits them on the same branch, pushes to `origin`, and prints a GitHub/GitLab PR URL when supported. The local clone returns to its default branch.

### `skills list`

Use `skills list`, `skills list --verbose`, or `skills list --json`. The command lists top-level skills from Git and marks active skills. `--verbose` shows metadata from `info.json`. `--json` emits an indented array with `name`, `active`, `description`, and `owner` when available. Sparse-excluded metadata is read with `git show`.

### `skills create`

Use `skills create <skill-name>` to create `instructions/<skill-name>/SKILL.md` and `info.json`, register the skill in `extra_skills`, and extend sparse checkout. Edit the files, then use `skills push <skill-name>`.

### `skills enable`

Use `skills enable group <group-name>` to append a group to `groups`, or `skills enable <skill-name>` to append an individual skill to `extra_skills`. If the individual skill is excluded, enable removes it from `excluded_skills`. Sparse checkout is reapplied immediately.

### `skills disable`

Use `skills disable group <group-name>` to remove a group, or `skills disable <skill-name>` to add an individual skill to `excluded_skills`. Uncommitted changes block removal. `--force` stashes tracked and untracked files with `git stash push -u`, then reapplies sparse checkout.

### `skills init-repo`

Use `skills init-repo <folder-name>` to create `.manifest/_global.json`, `.manifest/group-1.json`, `.manifest/sub-group.json`, a `skills-cli/` starter skill containing the compact CLI reference, its `info.json`, and `.gitignore`. It does not run Git initialization. In the new folder, run `git init`, `git add .`, and `git commit -m "init: skills repository"`.

### `skills ai-help` and `skills help`

Use `skills ai-help` to print `SKILL-CLI.md`, or `skills help` to print the command list, flags, and examples.

## AI Agent Workflow

When an agent reads this skill, it should check Python, Git, and CLI availability; detect the operating system; ask for the repository URL/path and groups if unknown; run `skills init --repo ...` from the project root; explain active skills with `skills list --verbose`; use `skills pull` for updates and `skills push <name>` for reviewed changes; and never print credentials, tokens, or secret-bearing URLs.

## Testing

Run `python tests/run.py` from `tools_py/`. The included launcher is recommended because some portable Python distributions use an isolated import path. The Docker smoke test is built with `docker build -t skills-python-smoke -f test/Dockerfile .`, run with `docker run --rm -v ./test:/app/test skills-python-smoke`, and reviewed with `git diff test/commands.md`. The smoke runner treats `test/commands.md` as both command source and output snapshot, replacing only output fences on rerun.

## Compatibility

The port preserves command names, flags, JSON fields, commit messages, folder names, and user-facing workflow from the Go and Node.js editions. Differences found while comparing them are recorded in [`go-node-differences.md`](./go-node-differences.md).
