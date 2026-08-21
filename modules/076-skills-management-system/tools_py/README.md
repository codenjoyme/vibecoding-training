# Skills CLI - Python Edition

This folder contains the Python port of the Skills Management System. It keeps the Go and Node.js command interface while using only the Python standard library at runtime.

## Run from the source checkout

```powershell
python scripts\main.py help
```

```bash
python3 ./scripts/main.py help
```

The direct launcher is useful on Windows portable Python distributions that do not add the current folder to `sys.path`. The source layout mirrors the Go edition:

```text
tools_py/
├── SKILL.md
├── SKILL-CLI.md
├── README.md
└── scripts/
	├── main.py
	├── cmd/
	├── internal/
	└── test/
```

On a regular Python installation, the package entry point also works:

```bash
python -m scripts.main help
```

## Optional installation

From the `tools_py/` project root, install the local project to expose the `skills` command:

```bash
python -m pip install .
skills help
```

The project metadata file is in `tools_py/`, not in `tools_py/scripts/`. If your terminal prompt ends with `tools_py\scripts>`, install the parent project instead:

```powershell
# Windows PowerShell, from tools_py/scripts/
python -m pip install ..
```

```bash
# macOS/Linux, from tools_py/scripts/
python3 -m pip install ..
```

The equivalent editable command is `python -m pip install --editable ..` (or `python3` on macOS/Linux). Running `python -m pip install .` from `scripts/` fails because that directory has no `pyproject.toml`.

The project has no runtime dependencies. It requires Python 3.10 or newer and a system `git` executable.

## Tests

Run the snapshot smoke test from the source checkout:

```bash
cd tools_py
docker build -t skills-python-smoke -f scripts/test/Dockerfile .
docker run --rm -v ./scripts/test:/app/test skills-python-smoke
git diff scripts/test/commands.md
```

The snapshot files in `scripts/test/` use the same four-file structure and 14-phase command layout as the Go and Node.js editions. There is no separate unit-test tree; validation is performed by reviewing the generated snapshot diff.

## Documentation

- `SKILL.md` is the full operator guide for an AI agent.
- `SKILL-CLI.md` is the compact reference printed by `python scripts/main.py ai-help`.
- The translated comparison and test reports are kept in `work/076-task/python/` with the development log.
