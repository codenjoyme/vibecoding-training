<follow>
iterative-prompt.agent.md
</follow>

## UPD1

Давай в этом модуле термин `hallucination` тоже возьмем в кавычки и добавим его в инструкцию по стилю. Сразу поправь все модуля. 

Стой ты делаешь двойные кавычки, а надо `` как указано в инструкции по lnd мсодулям. 

Стой стой, я откатил все. Мне надо чтобы ты правил не модуля программы, а модуля lnd тренинга. go

### RESULT

- Added style rule to `instructions/lnd/generate-lnd-modules.agent.md`: wrap `hallucination`/`hallucinations` in backticks in LND module prose (exceptions: compound forms like "hallucination-fixing", headings).
- Applied backtick wrapping to all `hallucination`/`hallucinations` occurrences in:
  - `lnd/output/module-11-learning-from-hallucinations.md` (all prose, quiz, practical task sections)
  - `lnd/output/module-12-ai-skills-tools-creation.md` (lines 29, 82, 152, 155; compound forms on 103/116 left intact)
  - `lnd/output/module-17-rapid-prototyping-speckit.md` (lines 16, 161)

## UPD2

То же для слова `instructions`, `agent` и так далее все специафические тремины которые появляются с изучением этого курса. Во всех модулях lnd поправь и инструкцию по стилю модуля. [text](../../instructions/lnd/generate-lnd-modules.agent.md) go

### RESULT

- Added two new style rules to `instructions/lnd/generate-lnd-modules.agent.md`:
  - `` `instructions` ``/`` `instruction` `` — wrap in backticks when referring to AI instruction files (.agent.md). Not for generic use.
  - `` `agent` `` — wrap in backticks when referring to an AI agent acting autonomously. Not for generic use.
- Applied backtick wrapping to `instructions`/`instruction` and `agent` prose occurrences in:
  - `lnd/output/module-11-learning-from-hallucinations.md` (all pages, quiz, practical task)
  - `lnd/output/module-12-ai-skills-tools-creation.md` (skill formula, page instructions, quiz)
  - `lnd/output/module-06-agent-mode-under-the-hood.md` (intro, page 3 header, steps, result, summary)
  - `lnd/output/module-19-github-coding-agent-delegation.md` (background, when to use, all pages, quiz, practical task)

## UPD3

Перед резалт блоком в 34й строчке надо сделать следующее. Приведи метафору, что когда человеку снится сон, то он видит там все в перемешку - что происходило сегодня, на прошлой неделе, в детстве вместе с нереальными фактами которых никогда небыло и не могло быть - например человек с тремя пальцами. Модель работает так же - когда она генерирует текст, он ей "снится" на базе тех текстов что она когда-то читала (пока обучалась). Тех текстов уже нет, они растворены в ее синапсах/весовых коефициентах нейросетей внутри нее. И сейчас ей снится текст на тему заданного в сесии контекста. Потому галлюцинации неизбежны. Все что она генерирует есть одна большая галлюцинация, но наша задача через указагнием все более четких инструкицй привести их в русло, которое мы будем считать полезным. go

### RESULT

- Added dream metaphor paragraph **"Why `hallucinations` are inevitable — the dreaming mind analogy"** to `lnd/output/module-11-learning-from-hallucinations.md`, inserted between step 6 of the improvement cycle and the `### ✅ Result` block on page 1 (line 34 area).
- The metaphor: dreams mix real memory with invented facts (person with three fingers); a language model works the same — it "dreams" text from training data dissolved into weights/parameters; this is why `hallucinations` are inevitable, and precise `instructions` channel that dreaming into useful output.

## UPD4

В 67й строчке надо указать следующее вместо `5. After the update, run the same task again and compare results.`. надо сказать что после изменения инструкции ее надо закоммитить, а потом в новом пункте: вернуться к запросу, который предшествовал галлюцинации и запустить его снова, как мы делали в модуле 07, но там мы правили промпт, а тут вместо промпта была исправлена инструкция, и теперь нам надо удалить воспоминания об ошибке и неверного истолкования инструкции из контекста, и сделать это можно вернувшись на 1 промпт до галлюцинации, отредактировав его и проследив что инструкция загрузилась и что теперь поведение ожидаемое. Можно так же открыть новую сессию и попробовать сделать запрос в чистом контексте. Важно! Если вы не закомиитите инструкцию тут, то откат к предыдущему промпту может повлечь к отмене всех произведенных действий в файле, потому надо закомиитить. go 

### RESULT

- Replaced step 5 of the Page 2 Steps section in `lnd/output/module-11-learning-from-hallucinations.md` with two new steps:
  - Step 5: Commit the updated `instruction` file immediately (before reverting), with a warning that reverting without committing may erase the fix.
  - Step 6: Return to the pre-hallucination `prompt` and re-run it — Option A (edit/resend in chat history), Option B (fresh `context` in new session). Cross-references `Module 7` and `Module 3`.

## UPD5

И подгрузи в контекст [text](../../instructions/lnd/generate-lnd-modules.agent.md) чтобы стилистику понимать, а то я снова вижу что специфические термины не берутся в кавычки ``. Посмотри все модули что мы уже отработали, пойми что там брали в кавычки и обнови эту инстркцию. Мне нужно все термины которые относятся в genAI чтобі тоже брались. Промпт. Модель. Контекст. Галлюцинация. Скилл. Тулл. И так далее. go

### RESULT

- Updated `instructions/lnd/generate-lnd-modules.agent.md` with four new style rules:
  - `` `model` `` — wrap when referring to the AI language model concept (not product names or compound phrases like "mental model").
  - `` `skill` `` — wrap when referring to the course-specific instruction+tool capability pair (Module 12 pattern). Not for generic human skills.
  - `` `tool` `` — wrap when referring to scripts/programs invoked by an AI agent. Not for generic "useful tool" usage.
  - (`` `hallucination` ``, `` `instruction` ``, `` `agent` `` were added in earlier UPDs.)
- Applied new rules across:
  - `lnd/output/module-12-ai-skills-tools-creation.md` — wrapped all `skill`, `tool`, `model` occurrences throughout (background, pages 1-5, summary, quiz, practical task).
  - `lnd/output/module-06-agent-mode-under-the-hood.md` — fixed remaining unquoted `model` in prose (lines 22-23, 97, 129, 151) and unquoted `prompt` in summary.