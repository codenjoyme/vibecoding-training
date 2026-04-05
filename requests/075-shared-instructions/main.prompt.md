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

## UPD4

Давай так же сделаем `_global.json` и `_agents.json` для того, чтобы они были сразу видны в списке первыми.

Так же в названии cli команды `instructions init ...` я хотел бы использовать слово `skills` вместо `instrunctions` потому что долго печатать.

Вместо ключа `--projects` наверное лучше указать `--groups` с перечнем всех групп, проекты это или сабгруппы. 

В разделе `## Компоновка промпта` надо просто указать, что агент сам дотянется до нужных скилов и объединит их, это уже не наша задача думать как эта компановка делается.

В разделе `## Модель совместной работы` просто информация рекомендательная, она не влияет на имплементацию. Такая информация нужна будет на этапе создания Skills для работы c CLI.

Везде пиши `SKILL.md` а не `skill.md` - такая конвенция. 

Еще мне нужна комада `skills help` дающая ответ как чем пользоваться.

Наверное пока что пометь `skills eval` как что-то что будет потом реализовано. Сейчас не надо. 

Так же у тебя есть вопросы в [text](session-summary-ru.md):

> **Вопрос:** Мы редизайним это для технической аудитории, или нужно сохранить доступность для не-инженеров? Или разбить на два уровня?
> **Ответ:** Нет, тренинг уже далеко не для менеджеров. Он для всех. Потому исправь во всем проекте упоминания что этот тренинг для всех. Даже неопытных разработчиков. Но как они решат технически все, что мы делаем тут? Будет описан SKILL.md с описанием установки CLI подхода. Как скомпилировать решение, как развернуть его в команде, как менеджить. И агент прочитавший єтот скилл впервіе поможет юзеру с сетапом. 

> **Вопрос:** CLI должен быть:
> **Ответ** (a) **Реальным инструментом**, который мы создаём и публикуем как часть курса?
> Более того, тут в модуле тренинговом будет папка `tools` в котормо будет находиться production ready проект CLI, который можно будет скачать и использовать. И в SKILL.md будет инструкция по его использованию. Я пока решил разместить его тут и не создавать отдельного репозитория для солюшена.

> **Вопрос:** Сейчас модуль 075 рассчитан на 15 минут и охватывает базовую структуру общего репозитория + Git-воркфлоу.
>
> **Ответ:** Цель:
> ### Вариант C — Разбивка на два модуля (высокие затраты)
> - Модуль **075** остаётся вводным (текущий контент, лёгкое обновление) — для менеджеров
> - Модуль **076** становится продвинутой системой (манифест, sparse checkout, концепция CLI, evals) — для техлидов

> **Вопрос:** `evals.json` — включать или нет?
> **Ответ:** Пока не включать, оставить как "coming soon" в SKILL.md и в research. Нет мы не будем обучать тестированию инструкций в этом модуле. 

> **Вопрос:** Ядро системы из исследования не привязано к IDE. Текущий модуль 075 упоминает совместимость с VSCode и Cursor, но не углубляется. Стоит ли включить раздел о том, как центральные `skill.md`-файлы соотносятся с IDE-специфичными форматами обёрток (`.github/prompts/`, `.cursor/rules/`)?
> **Ответ:** Мы рекомендуем использование tools agnostic подхода описанного в `instructions/creating-instructions.agent.md` то есть все инструкции независимо от Агентной системы и IDE хранятся в отдельной папке как простые markdown файлы. А конкретная агентная система имеет свои ссылки-адаптеры привычные ей на эти файлы. 

### RESULT

Обновлены все 6 документов:

**`research.md` + `research-ru.md`:**
- `global.json` → `_global.json`, `agents.json` → `_agents.json` (префикс для приоритетной сортировки)
- `skill.md` → `SKILL.md` везде (конвенция)
- CLI бинарник `instructions` → `skills`; флаг `--project` → `--groups`
- Раздел «Компоновка промпта» упрощён: агент сам собирает нужные скилы
- Раздел «Модель совместной работы» помечен как рекомендательный (не влияет на имплементацию)
- `evals.json` помечен как `coming soon`
- Добавлена команда `skills help`; `skills eval` помечена как `coming soon`
- Дистрибуция: `skills.exe` / `skills`

**`session-summary.md` + `session-summary-ru.md`:**
- Раздел «Уточняющие вопросы» заменён на «Принятые решения» со всеми 5 ответами
- Аудитория: все разработчики, включая начинающих
- CLI → реальный инструмент в `tools/`; Вариант C (075 + 076); evals → coming soon; tools-agnostic подход

**`existing-module-review.md` + `existing-module-review-ru.md`:**
- Аудитория обновлена: «managers / non-engineers» → «all developers including beginners»
- Раздел рекомендаций заменён: варианты A/B/C → подтверждённое решение «Вариант C выбран»
- `skill.md` → `SKILL.md`; `evals.json` помечен как `coming soon`

