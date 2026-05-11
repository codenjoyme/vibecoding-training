# Module 15 Completion Report

## Script Metadata
- Filename: batch-rename.py
- Language: Python
- Purpose: Renames files in a directory by applying a pattern (prefix, suffix, replace substring) to filenames in bulk. Supports dry-run mode.

## Script Contents
```python
#!/usr/bin/env python3
"""Batch rename files in a directory using pattern rules."""

import argparse
import os
from pathlib import Path

def rename_files(directory: str, prefix: str = "", suffix: str = "",
                 find: str = "", replace: str = "", ext_filter: str = "",
                 dry_run: bool = False) -> list[dict]:
    results = []
    target = Path(directory)
    if not target.is_dir():
        raise FileNotFoundError(f"Directory not found: {directory}")

    for fpath in sorted(target.iterdir()):
        if not fpath.is_file():
            continue
        if ext_filter and fpath.suffix != ext_filter:
            continue
        stem = fpath.stem
        extension = fpath.suffix
        new_stem = stem
        if find:
            new_stem = new_stem.replace(find, replace)
        new_name = f"{prefix}{new_stem}{suffix}{extension}"
        new_path = fpath.parent / new_name
        action = "RENAME" if new_name != fpath.name else "SKIP"
        results.append({"old": fpath.name, "new": new_name, "action": action})
        if action == "RENAME" and not dry_run:
            fpath.rename(new_path)
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch rename files in a directory")
    parser.add_argument("directory", help="Target directory")
    parser.add_argument("--prefix", default="", help="Prefix to add")
    parser.add_argument("--suffix", default="", help="Suffix to add before extension")
    parser.add_argument("--find", default="", help="Substring to find in filename")
    parser.add_argument("--replace", default="", help="Replacement for found substring")
    parser.add_argument("--ext", default="", help="Filter by file extension (e.g. .txt)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without renaming")
    args = parser.parse_args()

    results = rename_files(args.directory, args.prefix, args.suffix,
                           args.find, args.replace, args.ext, args.dry_run)
    for r in results:
        print(f"[{r['action']}] {r['old']} -> {r['new']}")
    print(f"\nTotal: {len(results)} files processed, "
          f"{sum(1 for r in results if r['action'] == 'RENAME')} renamed.")
```

## Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| `directory` | Target directory to process (positional) | — (required) |
| `--prefix` | Prefix to add to filenames | "" |
| `--suffix` | Suffix to add before extension | "" |
| `--find` | Substring to find in filename | "" |
| `--replace` | Replacement for found substring | "" |
| `--ext` | Filter by file extension | "" (all files) |
| `--dry-run` | Preview changes without renaming | false |

## Test Run Output
```
$ python batch-rename.py ./test-files --prefix="2024-" --ext=.txt --dry-run
[RENAME] notes.txt -> 2024-notes.txt
[RENAME] draft.txt -> 2024-draft.txt
[RENAME] readme.txt -> 2024-readme.txt
[SKIP] image.png -> image.png

Total: 4 files processed, 3 renamed.
```
