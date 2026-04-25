"""Dump all 'Skill' rows from graph.xlsx to a text file."""
from pathlib import Path
import openpyxl

HERE = Path(__file__).parent
SRC = HERE / "graph.xlsx"
OUT = HERE / "skills.txt"

wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
ws = wb.active
rows = ws.iter_rows(values_only=True)
hdr = list(next(rows))

# Indexes
I_NAME = 9
I_TYPE = 10
I_EDID = 11
I_PATH = 12
I_DESC = 16
I_NOVICE = 36
I_INTER = 37
I_ADV = 38
I_EXPERT = 39

SEP = "\n" + ("=" * 100) + "\n"

count = 0
with OUT.open("w", encoding="utf-8") as f:
    f.write(f"# Skills dump from {SRC.name}\n")
    f.write(f"# Format: one block per Skill, separated by ====\n")
    for r in rows:
        if r[I_TYPE] != "Skill":
            continue
        name = (r[I_NAME] or "").strip()
        if not name:
            continue
        count += 1
        f.write(SEP)
        f.write(f"NAME: {name}\n")
        f.write(f"EDID: {r[I_EDID] or ''}\n")
        f.write(f"PATH: {r[I_PATH] or ''}\n")
        desc = (r[I_DESC] or "").strip()
        if desc:
            f.write(f"DESCRIPTION:\n{desc}\n")
        for label, idx in [("NOVICE", I_NOVICE), ("INTERMEDIATE", I_INTER),
                           ("ADVANCED", I_ADV), ("EXPERT", I_EXPERT)]:
            v = r[idx]
            if v:
                f.write(f"{label}:\n{str(v).strip()}\n")

print(f"Wrote {count} skills to {OUT}")
print(f"Size: {OUT.stat().st_size:,} bytes")
