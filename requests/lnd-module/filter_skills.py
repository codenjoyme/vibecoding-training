"""Filter graph.xlsx Skill rows to candidates relevant to vibe-coding-for-managers training,
and produce two outputs:
  - skills-candidates-full.txt : full block (name, EDID, path, desc, levels) per candidate
  - skills-shortlist.txt       : tighter shortlist (names only) hand-curated by keyword tiers
"""
from pathlib import Path
import openpyxl
import re

HERE = Path(__file__).parent
SRC = HERE / "graph.xlsx"
OUT_FULL = HERE / "skills-candidates-full.txt"
OUT_SHORT = HERE / "skills-shortlist.txt"

# Tier 1: very specific to course content (must contain one of these phrases)
TIER1 = [
    r"\bGenAI\b", r"\bGen AI\b", r"\bGenerative AI\b",
    r"GitHub Copilot", r"\bCopilot\b",
    r"\bCursor\b", r"Claude Code", r"\bClaude\b",
    r"\bChatGPT\b", r"\bLLM\b", r"Large Language Model",
    r"prompt engineer", r"prompting",
    r"\bAI agent", r"agent[ic]+", r"agentic",
    r"vibe coding", r"vibe[- ]code",
    r"\bMCP\b", r"Model Context Protocol",
    r"Spec[- ]?Kit",
    r"no[- ]code", r"low[- ]code",
    r"hallucinat",
    r"AI[- ]assist", r"AI[- ]powered",
    r"AI literacy", r"AI fluency",
    r"AI ethics", r"responsible AI", r"AI governance",
    r"AI for managers", r"AI for leaders",
    r"prompt", 
]

# Tier 2: foundational tech the course touches (broader, requires combining with context)
TIER2 = [
    r"\bGit\b", r"\bGitHub\b", r"version control", r"pull request", r"code review",
    r"\bIDE\b", r"VS ?Code", r"Visual Studio Code",
    r"\bAPI\b", r"REST API", r"\bcURL\b",
    r"\bCLI\b", r"command line", r"terminal",
    r"\bNode\.?js\b", r"\bnpm\b", r"\bDocker\b", r"\bPython\b",
    r"\bJSON\b", r"\bYAML\b", r"\bMarkdown\b",
    r"specification", r"requirement",
    r"rapid prototyp", r"prototyping",
    r"automation", r"script(ing)?",
    r"browser automation", r"Playwright", r"DevTools",
    r"debugging", r"testing", r"QA",
    r"environment setup", r"developer environment",
]

# Tier 3: managerial / soft-skill angle (target audience)
TIER3 = [
    r"delivery manage", r"project manage", r"engineering manage",
    r"product manage", r"product owner",
    r"leadership", r"coaching", r"mentoring", r"mentorship",
    r"stakeholder", r"presales", r"pre[- ]?sales", r"consulting",
    r"change management", r"team lead",
    r"backlog", r"estimation", r"planning",
    r"communication", r"presentation", r"feedback",
    r"workflow", r"process improvement",
    r"learning and development", r"\bL&D\b", r"training design",
]

ALL = TIER1 + TIER2 + TIER3
PAT = re.compile("|".join(ALL), re.IGNORECASE)
PAT_TIER1 = re.compile("|".join(TIER1), re.IGNORECASE)

I_NAME, I_TYPE, I_EDID, I_PATH, I_DESC = 9, 10, 11, 12, 16
I_NOVICE, I_INTER, I_ADV, I_EXPERT = 36, 37, 38, 39

wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
ws = wb.active
rows = ws.iter_rows(values_only=True)
next(rows)

candidates = []
shortlist = []
for r in rows:
    if r[I_TYPE] != "Skill":
        continue
    name = (r[I_NAME] or "").strip()
    if not name:
        continue
    if PAT.search(name):
        candidates.append(r)
        if PAT_TIER1.search(name):
            shortlist.append(name)

SEP = "\n" + ("=" * 100) + "\n"
with OUT_FULL.open("w", encoding="utf-8") as f:
    f.write(f"# Filtered candidate Skills ({len(candidates)} rows)\n")
    f.write(f"# Source: {SRC.name}\n")
    for r in candidates:
        f.write(SEP)
        f.write(f"NAME: {r[I_NAME]}\n")
        f.write(f"EDID: {r[I_EDID] or ''}\n")
        f.write(f"PATH: {r[I_PATH] or ''}\n")
        desc = (r[I_DESC] or "").strip()
        if desc:
            f.write(f"DESCRIPTION:\n{desc}\n")
        for lbl, idx in [("NOVICE", I_NOVICE), ("INTERMEDIATE", I_INTER),
                         ("ADVANCED", I_ADV), ("EXPERT", I_EXPERT)]:
            v = r[idx]
            if v:
                f.write(f"{lbl}:\n{str(v).strip()}\n")

shortlist = sorted(set(shortlist), key=str.lower)
OUT_SHORT.write_text("\n".join(shortlist) + "\n", encoding="utf-8")

print(f"candidates: {len(candidates)} -> {OUT_FULL} ({OUT_FULL.stat().st_size:,} bytes)")
print(f"tier1 shortlist: {len(shortlist)} -> {OUT_SHORT} ({OUT_SHORT.stat().st_size:,} bytes)")
