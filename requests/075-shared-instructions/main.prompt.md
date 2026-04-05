<follow>
iterative-prompt.agent.md
</follow>

## UPD1

Какой модуль у меня про работу в команде с инструкциями? Обнови название этого файла поставив префикс номера после того как найдешь. 

Дальше я хочу чтобы ты почитал файл [text](research.txt) в нем есть саммари исследования, которое я провел в GPT чате пока ехал по делам. Не стоит воспринимать все там за руководство к действию, но стоит использовать как референс. Сделай из этого файла markdown со всем форматированием. Задай так же дополнительные вопросы и напиши саммари того что будем делать в отдельном файле в папке риквеста этого. 

Так же мне надо посмотреть на существующий модуль и сделать саммари рекомендаций, что там уже есть - так я ознакомлюсь приму решение что оставляем, а что будем заменять. Пока не трогай программу тренинга - этим мы займемся позже. 

### RESULT

- `requests/shared-instructions/` → renamed to `requests/075-shared-instructions/` (module number: 075)
- `requests/075-shared-instructions/research.md` — created: `research.txt` converted to full Markdown with headers, tables, and code blocks
- `requests/075-shared-instructions/session-summary.md` — created: summary of what we're working on + 5 clarifying questions before proceeding with the module update
- `requests/075-shared-instructions/existing-module-review.md` — created: part-by-part breakdown of current module 075 content, gap analysis vs. research, and 3 options (A/B/C) for how to proceed

## UPD2

Спасибо. А теперь переведи мне те файлы что ты создал слово в слово на русский язык. Создай рядом одноименные файлы с префиксом -ru. 

### RESULT

- `requests/075-shared-instructions/research-ru.md` — создан: дословный перевод `research.md` на русский язык
- `requests/075-shared-instructions/session-summary-ru.md` — создан: дословный перевод `session-summary.md` на русский язык
- `requests/075-shared-instructions/existing-module-review-ru.md` — создан: дословный перевод `existing-module-review.md` на русский язык

## UPD3

В документации есть упоминание `manifest.json` файла. Что мне в нем не нравится: 
- Во первых он один, и его будут менять все, а значит будут постояные конфликты. Потому я хотел бы, чтобы была папка с `.manifest` а в ней уже столько файлов сколько проектов нужно. Имя файла может быть `<project-name>.json`. 
- Так же пусть будет `global.json` для глобальных навыков, которые нужны всем.
- И еще один `agents.json` для различных сред разработки (VSCode, Copilot, Cursor и т.д.).
- Так же может быть любое количество дополнительных саб-кофигов, например `security.json` для навыков, связанных с безопасностью. Суть в них будет такая же как `<project-name>.json`. 
- В описании проекта, кроме инструкций будет так же указываться сабконфиги `<project-name>.json` на которые мы будем ссылаться.
- Так же можно будет при инициализации конфигов через CLI указывать не один несколько `project-name`. 

Делая изменения - вноси сразу во все версии документов, которые мы уже создали. 

### RESULT

- `research.md` + `research-ru.md` — updated repository structure: `manifest.json` replaced with `.manifest/` folder containing `global.json`, `agents.json`, `<project-name>.json`, and sub-configs (e.g., `security.json`)
- `research.md` + `research-ru.md` — Manifest Configuration section fully rewritten with new file layout table, per-file JSON examples, and updated rules
- `research.md` + `research-ru.md` — CLI init command changed from `--service <name>` to `--project <name> [<name-2> ...]` with multi-project support; manifest loader description updated
- `session-summary.md` + `session-summary-ru.md` — question 1 and manifest pattern step updated to reference `.manifest/` folder
- `existing-module-review.md` + `existing-module-review-ru.md` — gap table row updated to reflect new `.manifest/` structure