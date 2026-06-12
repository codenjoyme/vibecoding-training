<follow>
iterative-prompt/SKILL.md
</follow>

## UPD1

Следуя инструкции по созданию инструкций, создай мне скилл, который на входе будет принимать ссылку на docx файл шаблона, а на выходе будет файл который мы держим. Также на вход должен передаваться properties файл, который будет иметь ключ-значение, а ключи есть в том шаблоне как плейсхолдеры (посмотри в шаблон [work/test-docx/Template.docx](../../work/test-docx/Template.docx) сам). Старый шаблон не изменяется, новый файл создаётся копированием шаблона.

go

### RESULT (UPD1)

**Новые файлы:**
- [instructions/demo/fill-docx-template/SKILL.md](../../instructions/demo/fill-docx-template/SKILL.md) — инструкции для скилла
- [instructions/demo/fill-docx-template/scripts/fill_docx_template.py](../../instructions/demo/fill-docx-template/scripts/fill_docx_template.py) — Python скрипт
- [.github/prompts/to-fill-docx-template.prompt.md](../../.github/prompts/to-fill-docx-template.prompt.md) — VSCode обёртка
- [work/test-docx/data.properties](../../work/test-docx/data.properties) — пример properties файла

**Обновлено:**
- [instructions/main.agent.md](../../instructions/main.agent.md) — добавлена запись в каталог

**Результат теста** — шаблон не изменился, в Filled.docx все плейсхолдеры `<data1>`–`<data6>` заменены значениями из data.properties

## UPD2

Давай сделаем такой эксперимент — я хочу чтобы ты спрашивал меня через Ask questions на каждый плейсхолдер. Сделай скилл таким, который будет доставать плейсхолдеры через CLI, и вариант будет не через properties файл, а через Ask_questions тул.

go

### RESULT (UPD2)

**Новый файл:**
- [instructions/demo/fill-docx-template/scripts/extract_placeholders.py](../../instructions/demo/fill-docx-template/scripts/extract_placeholders.py) — извлекает плейсхолдеры из DOCX через ZIP/XML (даже если разбиты между XML-рунами)

**Обновлённые файлы:**
- [instructions/demo/fill-docx-template/SKILL.md](../../instructions/demo/fill-docx-template/SKILL.md) — полностью переписан под интерактивный workflow
- [instructions/demo/fill-docx-template/scripts/fill_docx_template.py](../../instructions/demo/fill-docx-template/scripts/fill_docx_template.py) — `--properties` теперь опциональный, добавлен `--set key=value` (повторяемый)

**Как выглядит новый flow:**
1. Агент запускает `extract_placeholders.py --template Template.docx` → получает список: `data1, data2 ...data6`
2. Агент вызывает `vscode_askQuestions` — одно вопрос на плейсхолдер, все в одном вызове
3. Агент запускает `fill_docx_template.py --set data1="..." --set data2="..."` с ответами
4. Сообщает о готовом файле

## UPD3

Давай потестируем.

go

### RESULT (UPD3)

Результат в [work/test-docx/FilledTest.docx](../../work/test-docx/FilledTest.docx):

| Плейсхолдер | Значение |
|---|---|
| `<data1>` | value1 |
| `<data2>` | value2 |
| `<data3>` | value3 |
| `<data4>` | value4 |
| `<data5>` | value5 |
| `<data6>` | value6 |

Flow отработал полностью: extract → ask → fill. Оригинальный [work/test-docx/Template.docx](../../work/test-docx/Template.docx) не изменён.

## UPD4

Давай создадим iterative prompt файл со всеми моими вопросами тут как UPD и твои ответы отсюда как RESULT в папке requests про common demo cases которые я показываю людям. В него входят так же calculate-trig-table, fill-docx-template. Давай для них сделаем подпапку instructions/demo и туда переместим все эти ценные только для демок инструкции. И ссылку в main каталоге инструкций поправь. И ещё мне надо в промпт файл реквеста унести всё слово в слово отсюда, только на русском а не на украинском. RESULT UPD чтобы соответствовали этой сессии. И моё новое сообщение это туда тоже.

go

### RESULT (UPD4)

**Переезд инструкций:**
- `instructions/calculate-trig-table/` → [instructions/demo/calculate-trig-table/](../../instructions/demo/calculate-trig-table/)
- `instructions/fill-docx-template/` → [instructions/demo/fill-docx-template/](../../instructions/demo/fill-docx-template/)

**Обновлены ссылки:**
- [instructions/main.agent.md](../../instructions/main.agent.md) — оба скилла теперь указывают на `./demo/...`

**Создан prompt файл:**
- [requests/demo-cases/main.prompt.md](main.prompt.md) — вся сессия в формате UPD1–UPD4 на русском, RESULT'ы соответствуют тому что реально было сделано
