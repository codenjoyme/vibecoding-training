# Python Skills CLI - Test Report

## Scope

The Python port was compared with the current Go and Node.js implementations and tested on Windows with Docker Desktop available. The tests use only temporary repositories or the isolated `work/076-task/` area.

## Executed Checks

| Check | Result | Coverage |
|---|---|---|
| Python bytecode compilation | PASS | All package and test modules compile with `python -m compileall -q .` |
| Python unit and integration tests | PASS: 8/8 | Config defaults/errors, recursive manifests, cycles, init, global-only init, list metadata fallback, toggles, force stash, create, init-repo, push, repeated branch recreation, merge, pull, re-init |
| Python package build/install | PASS | `pip install --target` builds a wheel; console package includes `SKILL-CLI.md` |
| Python Docker image build | PASS | Clean `python:3.12-slim` image with Git |
| Python Docker smoke test | PASS | 57 command lines covering help, init, list, metadata, toggles, create, push with groups, merge/pull, repeated push, force stash, re-init, init-repo, and negative cases |
| Go Docker baseline | PASS | Existing 14-phase smoke suite, 166 command lines |
| Node.js Docker baseline | PASS | Existing 14-phase smoke suite, 168 command lines |
| Workspace diagnostics | PASS | No errors reported for `tools_py/` |

## Python Smoke Scenarios

- Fresh fixture repository with `_global.json`, two groups, a nested security sub-config, and five skills.
- Grouped initialization and sparse checkout verification.
- Global-only initialization without `--groups`.
- Plain, verbose, and JSON skill listing.
- Metadata lookup for both checked-out and sparse-excluded skills.
- Group and individual enable/disable with immediate sparse-checkout reapplication.
- Refusal to disable a dirty skill and `--force` stash of an untracked file.
- New skill templates and `extra_skills` registration.
- Push with multiple new/existing group manifests.
- Merge, pull, and a second push that recreates an existing feature branch.
- Re-initialization from `skills.json`.
- `init-repo` structure and pretty-printed JSON.
- Expected failures for an unknown command and an uninitialized workspace.

## Portability Fixes Found During Testing

1. Portable Windows Python did not include the script directory in `sys.path`; `skills.py` now inserts its own directory and is the documented launcher.
2. Windows `charmap` output could not encode the CLI status markers; the entry point now configures UTF-8 output with replacement handling.
3. Windows Git object files can be read-only; re-initialization removes them with a read-only recovery callback.
4. The first Docker smoke image missed `/workspace`, which made every command silently run nowhere; the Dockerfile now creates the runner's workspace.
5. Installed `ai-help` needs its reference inside the wheel; `skills_cli/SKILL-CLI.md` is packaged and resolved before source-tree fallbacks.

## Expected Negative Output

The smoke snapshot intentionally contains:

- `Error: not a skills workspace - run 'skills init' first` with `exit=1`.
- Dirty-change refusal before the forced disable.
- `Error: unknown command "unknown-command"`.

These lines are assertions of error handling, not failed test runs.

## Go/Node Research

The cross-implementation findings are recorded in [`../tools_py/go-node-differences.md`](go-node-differences.md), including recursive sub-config resolution, output differences, documentation drift, and the Node branch-recreation stderr leak observed in the baseline smoke run.
