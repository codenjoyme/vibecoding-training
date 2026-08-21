# Skills CLI (Python) - Docker Smoke Tests

This smoke test runs the Python CLI in a clean Linux container. It executes every command from `commands.md` and writes each command's output immediately below it. The same file is the test source and the golden output snapshot.

## Run

From `tools_py/`:

```bash
docker build -t skills-python-smoke -f test/Dockerfile .
docker run --rm -v ./test:/app/test skills-python-smoke
git diff test/commands.md
```

The container creates a fresh `/workspace/skills-repo` fixture and `/workspace/project-repo` for every run. The host repository is changed only through the bind-mounted `test/commands.md` snapshot.

## What is covered

- General and command-specific help.
- Fresh init with groups and global-only init.
- Pretty `skills.json` and dynamic `list` output.
- Verbose and JSON metadata, including Git fallback for inactive skills.
- Group and individual enable/disable with sparse checkout reapplication.
- `create` templates and extra-skill registration.
- `push --groups`, branch creation, manifest updates, merge, and pull.
- Refusal to remove uncommitted changes and `--force` stash behavior.
- Re-init from existing configuration.
- `init-repo` layout and pretty JSON.

## Re-running

The runner preserves headings and command lines, removes only old output fences, executes the commands again, and writes fresh fences. Review `git diff test/commands.md` before accepting a new snapshot.
