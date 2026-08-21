# Go and Node.js Differences Found During the Python Port

This is a research log for the Python port. It records differences observed in the current Go and Node.js source snapshots. These findings are deliberately documented here instead of changing the existing implementations as part of the port.

## Resolution behavior

| Area | Go implementation | Node.js implementation | Python choice |
|---|---|---|---|
| Nested `sub-configs` | Resolves the direct sub-configs of each selected group only | Recursively resolves sub-configs with a visited set | Follow Node's recursive, cycle-safe behavior |
| Missing selected group | Returns an error such as `group "name": manifest file not found` | Warns and skips the missing config | Fail for an explicitly selected top-level group so a typo cannot silently remove skills |
| Missing nested sub-config | Prints a warning and continues | Prints a warning and continues | Warn to stderr and continue |
| Missing `_global.json` | Silently skips it | Silently skips it | Silently skip it |
| Invalid `_global.json` | Treats load failure as absent | Propagates JSON parsing failure | Raise a manifest error |

## CLI parsing and output

| Area | Go implementation | Node.js implementation | Python choice |
|---|---|---|---|
| `--groups` parsing | Uses Go `flag` plus positional groups; repeated/comma values are supported | Manually accepts comma and whitespace-separated values | Accept comma-separated, `--groups=value`, and positional forms |
| Text group display | `%v` prints a Go slice with brackets | Joins names with commas | Use Node's comma-joined display for human output |
| PR URL | Supports selected HTTPS and SCP-style GitHub/GitLab URLs without GitHub `expand=1` | Normalizes additional SSH forms and adds `expand=1` for GitHub | Use Node's broader URL normalization |
| `list --json` metadata | Reads local metadata then falls back to `git show` | Same local-first and Git fallback | Same behavior, with two-space JSON indentation |

## Repository bootstrap

The Go `init-repo` help text says the target is Git-initialized, but the Go handler only creates files and prints a follow-up `git init` command. The Node implementation explicitly says it creates a folder and has the same follow-up. Python follows the actual behavior: it creates the folder and files but does not initialize Git.

## Git operation details

- Both implementations use the system Git executable rather than a Git library.
- Both include `.manifest` in sparse checkout even when no skills are selected.
- Both return to the detected default branch after a successful push.
- Both use `git stash push -u` for forced disable, preserving untracked files.
- Both create/recreate an existing feature branch before committing.
- Python uses `subprocess.run` with a list of arguments, equivalent to Node's `execFileSync` and Go's `exec.Command`; it does not pass Git arguments through a shell.

## Documentation drift observed

Some generated documentation in the Go and Node folders still contains older references to `instructions/.manifest/config.json`, says `--groups` is required, or describes `skills-cli` paths from an earlier layout. The Python guide describes the current source behavior (`skills.json` at project root, optional groups, and `tools_py`) and does not rewrite those historical files.

## Smoke-test evidence

The isolated Docker smoke runs use the same 14 phases in both editions. The Go snapshot contains 166 command lines; the Node snapshot contains 168 because Node also installs and uninstalls the npm package. Both snapshots contain the expected negative cases for missing groups, duplicate skills, and dirty disable.

During a normal second push of the same skill, Node prints `fatal: a branch named ... already exists` before deleting and recreating the branch. The command still succeeds. This comes from Node's `execFileSync` writing Git stderr before `createBranch` catches the error; Go's `CombinedOutput` captures it silently. Python captures combined output and follows the quiet Go behavior.
