<follow>
iterative-prompt.agent.md
</follow>

## UPD1

Есть инструкция [text](../../work/project-merck/instructions/transform-meeting-transcript.agent.md) она помогает транскрибировать и структурировать встречи. Давай создадим у нас такую же инструкцию в папке `./instructions/transform-meeting-transcript.agent.md`. Если там есть информация про проект, то удаляем ее. 

Потом надо затранскрибировать митинг [text](<Call about teams.docx>) в той же папке давай сохраним результаты. 

Когда будешь делать саммари мне надо получить информацию о том, как собственно подключаться к тимзу. Выдели максимально инструцию для LLM. Я добавлю еще вводных из чата, и попробуем с тобой реализовать это подключение. Я вообще не очень понимаю как это делать, но ребята говорят что не сложно.

Так что давай в качестве ответа документ, который станет в основу будущего `Skill.md` и там мне инструкцию куда сходить и что сделать. Будем итеративно ее улучшать.

### RESULT

- Created `instructions/transform-meeting-transcript.agent.md` — generalized version of the project instruction (project-specific bits removed; added a generic "Meeting Summary" format alongside the coaching-session formats).
- Extracted `Call about teams.docx` → `requests/600-ms-teams-access/Call about teams.txt` using the in-house PowerShell .docx-to-text procedure.
- Wrote `requests/600-ms-teams-access/summary-2026-04-22.md` — full meeting summary (context, architecture, decisions, action items, open questions).
- Wrote `requests/600-ms-teams-access/skill-connect-to-teams.md` — draft v0.1 of the future `Skill.md`: Azure App Registration steps, env vars, Graph permissions, MSAL device-code flow, key Graph endpoints, container notes, verification checklist, and an "Open Items" section for iterative improvement.
- **Not committed** per user instruction. 