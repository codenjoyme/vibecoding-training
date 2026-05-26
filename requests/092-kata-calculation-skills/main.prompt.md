<follow>iterative-prompt/SKILL.md</follow>

## UPD1

Create a new training module following `instructions/create-training-module.agent.md`.

Use `requests/678-kata-calculation-skills/issue.md` as the source spec.

Produce the following artifacts:

- `modules/678-kata-calculation-skills/about.md`
- `modules/678-kata-calculation-skills/walkthrough.md`
- Update `training-plan.md` — insert module 678 after module 650 (WinAPI MCP Toolbox)

The walkthrough must:
- Follow the kata format: a repeating 5-step loop (describe → generate script → write SKILL.md → run → verify)
- Include a reference to `instructions/calculate-trig-table/SKILL.md` as the worked example to study first
- Show a concrete Round 1 example (Fibonacci sequence table) with exact CLI commands
- Provide a "pick your theme" menu for Round 2 and leave Round 3 open for user choice
- End with a debrief section and an optional Git commit step

### RESULT

Сделано Coding Agent и замержено.

## UPD2

Думаю что индекс этого модуля не совсем верный. Давай найдем ему более разумное место, где-то после того как скилы рассматриваются вообще. И переименуй риквест так же. go

### RESULT

- Renamed `modules/678-kata-calculation-skills/` → [modules/092-kata-calculation-skills/](../../modules/092-kata-calculation-skills/about.md)
- Renamed `requests/678-kata-calculation-skills/` → [requests/092-kata-calculation-skills/](.)
- Updated [training-plan.md](../../training-plan.md) — moved entry from after 650 to after 091 (CLI Snapshot Testing)
- Updated [walkthrough.md](../../modules/092-kata-calculation-skills/walkthrough.md) — replaced all `work/678-kata/` paths with `work/092-kata/`
