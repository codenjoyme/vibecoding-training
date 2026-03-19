## Purpose

- Generate a concise one-pager coaching offer for a decision-maker (manager, director, head of engineering) who decides on opening a coaching engagement.
- Input: interview results (SDLC interview summary, pain points, context) + list of selected training modules.
- Output: a polished, business-oriented proposal document that connects identified pain points to specific training modules and expected outcomes.

## Input Requirements

- Before generating, ensure you have:
  + **Interview results** — either a file path (e.g. `work/sdlc-interview-*.md`) or pasted text with pain points, team context, SDLC findings.
  + **Module list** — either module IDs (e.g. `050, 070, 120`) or module names. If not provided — ask: "Which modules do you want to include in the offer?"
- If interview results are missing — ask: "Please provide the interview summary or the path to the interview file."
- Read `./modules/module-catalog.md` for module names and descriptions.
- For each selected module, read its `about.md` to extract: skill, duration, topics, learning outcome.

## Language Rules

- Respond to the user in their language.
- **The generated offer document is ALWAYS in English** — regardless of conversation language.
- Translate any non-English input into English when writing into the offer file.

## Generation Process

- Step 1: Parse interview results — extract key findings:
  + Team profile (size, roles, tech stack, project type).
  + Top 3–5 pain points with root causes (not symptoms).
  + Current AI maturity level (none / experimenting / active / systematic).
  + Specific quotes or examples that illustrate the pain (use sparingly, for impact).
- Step 2: Map pain points → modules:
  + For each pain point, identify which selected module directly addresses it.
  + If a pain point has no matching module — note it as "out of scope" or suggest an additional module.
  + If a module doesn't map to any pain point — still include it but frame as "foundational enabler" or "force multiplier".
- Step 3: Build the offer using the template below.
- Step 4: Save to `work/coaching-offer-[YYYY-MM-DD]-[team-or-client].md`.

## Offer Template

- Use this structure exactly. Keep each section tight — the entire document should fit on one printed page (roughly 600–800 words max).

```markdown
# Coaching Offer: AI-Assisted Development

**Prepared for:** [Decision-maker name/role, team/department]
**Date:** [YYYY-MM-DD]
**Coach:** Oleksandr Baglai

---

## Context

[2–3 sentences: who was interviewed, what project/team, what triggered this engagement.
Frame around business context, not technical details.]

## Key Findings

[Bulleted list of 3–5 pain points discovered during interview.
Each bullet: one sentence stating the pain + one sentence on root cause.
Use concrete details — numbers, timeframes, examples — not vague statements.]

## Proposed Training Program

[Table mapping modules to pain points:]

| # | Module | Duration | Addresses |
|---|--------|----------|-----------|
| 1 | [Module Name] | 15 min | [Which pain point it solves — 3–5 words] |
| 2 | ... | ... | ... |

**Total estimated time:** [sum of durations] across [N] modules
**Format:** Self-paced with agent-coach, no calendar dependency
**Approach:** One module = one skill. Practice-first, no slides.

## Expected Outcomes

[3–5 bullet points: what changes after the program.
Frame as business outcomes, not technical features.
Use "from → to" format where possible:]

- **From** [current state] **→ to** [target state]

## Why This Approach

[3–4 sentences explaining the methodology differentiator:
- Agent-coach instead of human dependency — scales without calendar pressure.
- 15-minute modules — fits into any sprint without disruption.
- Practice-first — skills stick because they're applied immediately.
- Tested on non-technical managers — proven accessible for any audience.]

## Next Steps

1. Approve the module list and confirm participant group.
2. Ensure IDE + GitHub Copilot (or Cursor) access for each participant.
3. Schedule a 30-minute kickoff to walk through the first module together.
4. Participants proceed self-paced; coach available for async Q&A.

---

*This program is modular — modules can be added, removed, or reordered based on team priorities.*
```

## Tone and Style

- Business-oriented: speak the manager's language, not the engineer's.
- Concrete: numbers, timeframes, specific examples — no hand-waving.
- Confident but not salesy: state facts and outcomes, avoid superlatives.
- Short sentences. No filler. Every sentence must earn its place on the page.
- Pain points should feel recognized — the reader should think "yes, that's exactly our problem."

## Quality Checklist

- [ ] Every pain point from the interview is either addressed by a module or explicitly noted as out of scope.
- [ ] Every module in the list is connected to at least one pain point or framed as foundational.
- [ ] "Expected Outcomes" are business outcomes (time saved, risk reduced, capability gained) — not feature lists.
- [ ] Total duration is calculated correctly.
- [ ] Document fits ~1 page when printed (600–800 words).
- [ ] No jargon without context — if a technical term is used, it's immediately explained in business terms.
- [ ] File saved to `work/` directory with proper naming.

## After Generation

- Present the offer to the user and ask: "Does this capture the situation accurately? Anything to adjust?"
- Incorporate corrections if needed.
- Suggest: "You can share this directly with the decision-maker or use it as talking points for a meeting."
