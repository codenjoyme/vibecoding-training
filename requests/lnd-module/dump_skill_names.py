"""Dump compact list of all 'Skill' names from graph.xlsx (one per line)."""
from pathlib import Path
import openpyxl

HERE = Path(__file__).parent
SRC = HERE / "graph.xlsx"
OUT = HERE / "skills-names.txt"

wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
ws = wb.active
rows = ws.iter_rows(values_only=True)
next(rows)

names = []
for r in rows:
    if r[10] != "Skill":
        continue
    name = (r[9] or "").strip()
    if name:
        names.append(name)

names.sort(key=str.lower)
OUT.write_text("\n".join(names) + "\n", encoding="utf-8")
print(f"Wrote {len(names)} skill names to {OUT}  ({OUT.stat().st_size:,} bytes)")
