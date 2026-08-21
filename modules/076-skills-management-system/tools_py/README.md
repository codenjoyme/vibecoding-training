# Skills CLI - Python Edition

This folder contains the Python port of the Skills Management System. It keeps the Go and Node.js command interface while using only the Python standard library at runtime.

## Run from the source checkout

```powershell
python skills.py help
```

```bash
python skills.py help
```

The direct launcher is useful on Windows portable Python distributions that do not add the current folder to `sys.path`. On a regular Python installation, the package entry point also works:

```bash
python -m skills_cli help
```

## Optional installation

From this folder, install the local project to expose the `skills` command:

```bash
python -m pip install .
skills help
```

The project has no runtime dependencies. It requires Python 3.10 or newer and a system `git` executable.

## Tests

Run the standard-library unit and integration tests:

```bash
python tests/run.py
```

The included launcher is recommended because some portable Python distributions use an isolated import path.

The Docker smoke-test files in `test/` execute the same command-driven workflow used by the Go and Node.js editions.

## Documentation

- `SKILL.md` is the full operator guide for an AI agent.
- `SKILL-CLI.md` is the compact reference printed by `python skills.py ai-help`.
- `go-node-differences.md` records behavior differences found while comparing the source implementations.
