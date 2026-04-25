"""Extract Tier-1 shortlist skills with their proficiency descriptions, in compact form,
to skills-tier1-detail.txt for level-mapping decisions."""
from pathlib import Path
import openpyxl

HERE = Path(__file__).parent
SRC = HERE / "graph.xlsx"
SHORT = HERE / "skills-shortlist.txt"
OUT = HERE / "skills-tier1-detail.txt"

names = set(SHORT.read_text(encoding="utf-8").splitlines())
names.discard("")

wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
ws = wb.active
rows = ws.iter_rows(values_only=True)
next(rows)

I_NAME, I_TYPE, I_EDID, I_PATH, I_DESC = 9, 10, 11, 12, 16
I_NOVICE, I_INTER, I_ADV, I_EXPERT = 36, 37, 38, 39

def short(text, n=400):
    if not text:
        return ""
    s = str(text).strip().replace("\r", " ").replace("\n", " ")
    return s if len(s) <= n else s[:n] + "…"

found = {}
for r in rows:
    if r[I_TYPE] != "Skill":
        continue
    name = (r[I_NAME] or "").strip()
    if name in names and name not in found:
        found[name] = r

with OUT.open("w", encoding="utf-8") as f:
    f.write(f"# Tier-1 shortlist — {len(found)} skills with proficiency descriptions\n\n")
    for name in sorted(names, key=str.lower):
        r = found.get(name)
        if not r:
            f.write(f"--- {name} (NOT FOUND) ---\n\n")
            continue
        f.write(f"--- {name} ---\n")
        f.write(f"EDID: {r[I_EDID] or ''}\n")
        f.write(f"PATH: {r[I_PATH] or ''}\n")
        d = short(r[I_DESC], 300)
        if d: f.write(f"DESC: {d}\n")
        for lbl, idx in [("N", I_NOVICE), ("I", I_INTER), ("A", I_ADV), ("E", I_EXPERT)]:
            v = short(r[idx], 350)
            if v: f.write(f"{lbl}: {v}\n")
        f.write("\n")

print(f"wrote {len(found)}/{len(names)} -> {OUT} ({OUT.stat().st_size:,} bytes)")
