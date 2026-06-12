<follow>
iterative-prompt/SKILL.md
</follow>

## UPD1

Следуя инструкции по созданию инструкций, создай мне скилл, который на входе будет принимать ссылку на docx файл шаблона, а на выходе будет файл который мы держим. Также на вход должен передаваться properties файл, который будет иметь ключ-значение, а ключи есть в том шаблоне как плейсхолдеры (посмотри в шаблон [work/test-docx/Template.docx](../../work/test-docx/Template.docx) сам). Старый шаблон не изменяется, новый файл создаётся копированием шаблона.

go

### RESULT (UPD1)

- Создан [instructions/demo/fill-docx-template/SKILL.md](../../instructions/demo/fill-docx-template/SKILL.md) — описание скилла: входы, формат плейсхолдеров, формат properties файла, как запускать
- Создан [instructions/demo/fill-docx-template/scripts/fill_docx_template.py](../../instructions/demo/fill-docx-template/scripts/fill_docx_template.py) — Python скрипт: копирует шаблон, заменяет `<key>` токены, обрабатывает split-runs
- Создан [.github/prompts/to-fill-docx-template.prompt.md](../../.github/prompts/to-fill-docx-template.prompt.md) — VSCode обёртка для Copilot
- Создан [work/test-docx/data.properties](../../work/test-docx/data.properties) — пример properties файла для Template.docx
- Обновлён [instructions/main.agent.md](../../instructions/main.agent.md) — добавлена запись в каталог
- Протестировано: оригинальный Template.docx не изменился, Filled.docx содержит подставленные значения

## UPD2

Давай сделаем такой эксперимент — я хочу чтобы ты спрашивал меня через Ask questions на каждый плейсхолдер. Сделай скилл таким, который будет доставать плейсхолдеры через CLI, и вариант будет не через properties файл, а через Ask_questions тул.

go

### RESULT (UPD2)

- Создан [instructions/demo/fill-docx-template/scripts/extract_placeholders.py](../../instructions/demo/fill-docx-template/scripts/extract_placeholders.py) — извлекает имена плейсхолдеров из DOCX через ZIP/XML, печатает по одному на строку
- Обновлён [instructions/demo/fill-docx-template/scripts/fill_docx_template.py](../../instructions/demo/fill-docx-template/scripts/fill_docx_template.py) — `--properties` теперь опциональный, добавлен `--set key=value` (повторяемый аргумент)
- Переписан [instructions/demo/fill-docx-template/SKILL.md](../../instructions/demo/fill-docx-template/SKILL.md) — полный интерактивный workflow: Step 1 получить пути → Step 2 extract placeholders via CLI → Step 3 `vscode_askQuestions` (все вопросы одним вызовом) → Step 4 fill via `--set` → Step 5 подтвердить

## UPD3

Давай потестируем.

go

### RESULT (UPD3)

- Запущен `extract_placeholders.py` на [work/test-docx/Template.docx](../../work/test-docx/Template.docx) → получены: `data1 data2 data3 data4 data5 data6`
- Вызван `vscode_askQuestions` с 6 вопросами одним батчем (по одному на плейсхолдер)
- Запущен `fill_docx_template.py` с `--set` аргументами из ответов
- Создан [work/test-docx/FilledTest.docx](../../work/test-docx/FilledTest.docx) — все плейсхолдеры заменены, оригинал не тронут
- Flow отработал полностью: extract → ask → fill ✅

## UPD4

Давай создадим iterative prompt файл со всеми моими вопросами тут как UPD и твои ответы отсюда как RESULT в папке requests про common demo cases которые я показываю людям. В него входят так же calculate-trig-table, fill-docx-template. Давай для них сделаем подпапку instructions/demo и туда переместим все эти ценные только для демок инструкции. И ссылку в main каталоге инструкций поправь. И ещё мне надо в промпт файл реквеста унести всё слово в слово отсюда, только на русском а не на украинском. RESULT UPD чтобы соответствовали этой сессии. И моё новое сообщение это туда тоже.

go

### RESULT (UPD4)

- Создана папка `instructions/demo/` — подпапка для инструкций используемых только в демках
- Перемещён `instructions/calculate-trig-table/` → [instructions/demo/calculate-trig-table/](../../instructions/demo/calculate-trig-table/)
- Перемещён `instructions/fill-docx-template/` → [instructions/demo/fill-docx-template/](../../instructions/demo/fill-docx-template/)
- Обновлён [instructions/main.agent.md](../../instructions/main.agent.md) — исправлены пути для обоих скиллов на `./demo/...`
- Создан [requests/demo-cases/main.prompt.md](main.prompt.md) — этот файл, полная история сессии в формате UPD/RESULT на русском языке
