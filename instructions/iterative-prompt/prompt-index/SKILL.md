---
name: iterative-prompt-index
description: Index UPD/RESULT blocks in a large helm-log (*.prompt.md) file by line number, without loading the whole file into context
---

# Prompt-Index — a compact map of a helm-log file

A single `iterative-prompt` helm-log (`main.prompt.md`) can grow to several thousand lines after dozens of `## UPD[N]` cycles. Reading the whole file to find "where was that RESULT about X?" wastes context. `list_upds.py` scans the file with regex only (never loads it into the model's context) and prints a compact, plain-text index: one line per `## UPD[N]` block plus its `### RESULT` sub-blocks, each tagged with its exact line range and status. The model then uses `read_file` with the reported line range to drill into only the block it actually needs.

This is a sub-skill of [`../SKILL.md`](../SKILL.md) but is generic — it works on any file that follows the `## UPD[N]` / `### RESULT` convention, not just the active helm-log.

## Script

```
python instructions/iterative-prompt/prompt-index/scripts/list_upds.py <path-to-prompt-file> [options]
```

| Flag | Meaning |
|------|---------|
| `--last N` | Only show the last N UPD blocks (applied after `--pending`, if both given). |
| `--pending` | Only show UPD blocks that have no `### RESULT` yet. |
| `--no-results` | Suppress `+ RESULT (...)` sub-lines entirely — just UPD headers, ranges, status. |
| `--preview N` | Max characters of preview text per block (default `80`). `--preview 0` omits preview text — headers/ranges/status only. |

All flags are meant to be chosen by the model at call time depending on how much it needs — start compact (`--last 10 --preview 40`), widen if more context is needed.

### Output format

```
File: /abs/path/to/main.prompt.md (53 total UPD blocks, showing 3)
UPD blocks:
  - UPD51 (lines 1292-1307) [done] —
        "Смотри есть файл ... и он не создается автоматически..."
    + RESULT (lines 1298-1307)
        "Добавил в блок установки скила инструкцию создавать Copilot-агента..."
  - UPD52 (lines 1308-1346) [done] —
        "Давай сделаем CLI в этот скил iterative prompt на питоне..."
    + RESULT (lines 1312-1346)
        "Пользователь попросил задавать все вопросы прямо в этом файле..."
  - UPD53 (lines 1347-1407) [pending] —
        "Мои ответы: ..."
```

- `[done]` — the UPD block has at least one `### RESULT`. `[pending]` — no `### RESULT` yet (not yet processed, or still ends without `go`).
- A block can have **multiple `### RESULT` sub-blocks** (e.g. an intermediate result followed by a final one) — each gets its own line range.
- **UPD numbers are not assumed sequential or unique.** Blocks are parsed in file order (top to bottom), not sorted by number — a helm-log can contain gaps (e.g. `UPD55` right after `UPD2`) or merged/duplicated numbers from copy-pasted history. Always trust the **line range**, not the number, when jumping to a block.
- With `--no-results`, only UPD header lines are printed (no preview, no RESULT lines) — the most compact view for scanning scale.
- With `--preview 0`, preview text is omitted but the `—` marker and line ranges remain, so drill-down via `read_file` is still precise.

### Drill-down

The script never prints full block text. Once the model has the line range from the index (e.g. `UPD52 (lines 1308-1346)`), use `read_file` with that exact `startLine`/`endLine` to read only what's needed.

### When to use

- Before answering "what did we do in UPD30-40?" on a large helm-log.
- Before deciding whether an UPD is already processed (`--pending` to list only unprocessed ones).
- As a first pass on any helm-log with more than a few hundred lines, instead of `read_file` on the whole file.
