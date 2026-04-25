<follow>
iterative-prompt.agent.md
</follow>

## UPD1

В 9 и 10 модулях встречается название файла `BACKLOG.md`. Капслоком как-то сильно громко получается, может просто `backlog.md`? go

### RESULT

- `lnd/output/module-09-agent-memory-management.md` — replaced 13 occurrences of `BACKLOG.md` with `backlog.md`.
- `lnd/output/module-10-custom-instructions.md` — replaced 1 occurrence of `BACKLOG.md` with `backlog.md`.

## UPD2

Следуя инструкции [text](../../instructions/lnd/organize-module-images.agent.md) обслужи картинки что я добавил толкьо что. Дальше я буду только говорить `обработай картинки`. go

### RESULT

- `lnd/output/image-1.png` → moved to `lnd/output/img/module-09/04-using-at-mention.png`
- `lnd/output/image.png` → moved to `lnd/output/img/module-09/05-move-file-to-chat.png`
- `lnd/output/module-09-agent-memory-management.md` — updated references to use new paths.

## UPD3

В модуле 08 и 09 (и возможно в последующих) есть упоминание `PROJECT_SPEC.md` опять же слишком капслоксно. Давай просто `project_spec.md`?

Так же обрати внимание если в каком-то модуле есть ссылка на модуль в формате `Module NN` то надо брать его в кавычки '`'.

Сделай это двумя разными коммитами. go

### RESULT

- **Commit 1:** `lnd/output/module-08-clarifying-requirements.md`, `lnd/output/module-09-agent-memory-management.md` — replaced all `PROJECT_SPEC.md` with `project_spec.md`.
- **Commit 2:** 14 module files updated — wrapped bare `Module N` references (in prose, not headings) in backticks.

## UPD4

Там была инструкция, которая говорила что если есть какой-то термин технический, то его надо брать в кавычки. Про модули туда тоже добавь упоминание. go

### RESULT

- `instructions/lnd/generate-lnd-modules.agent.md` — added a cross-module references rule after the "Technical terms and modes" bullet: when referring to another module by number in prose (e.g. "you created this in Module 8"), wrap it in backticks: `` `Module 8` ``; headings are exempt.

## UPD5

Смотри по тексту я снова нахожу `ТЗ` вместо `specification`. Давай еще раз поищем и заменим во всех модулях. go

### RESULT

- `lnd/output/module-09-agent-memory-management.md` — replaced 1 remaining `ТЗ` with `specification`.
- `lnd/output/module-17-rapid-prototyping-speckit.md` — replaced 5 `ТЗ` occurrences with `specification`, removed `[MG]:` reviewer comment, fixed inline prompt to backtick format.
- `lnd/output/module-16-development-environment-setup.md` — replaced 1 `ТЗ`, removed `[MG]:` reviewer comment, fixed inline prompt to backtick format.

## UPD6

В этом модуле перед 143 строчкой `### ✅ Result` давай добавим такой блок: Важно понимать, что ты не ограничен конкретно двумя этими файлами. Ты можешь создавать любые файлы, которые нужны для реализации, и заполнять их любым содержимым, которое поможет тебе реализовать функциональность. Эти два файла — просто примеры того, как можно структурировать информацию. Пожалуйста будь креативным в этом процессе и автоматизируй это так, чтобы тебе было максимально удобно. Цель этого модуля сообщить о том, что тебе стоит позаботиться о том, как между сессиями переносить информацию. Ты отвечаешь за долгосрочную память агента. Иначе он будет кук рыбка Дорри, у которой беда с краткосрочной памятью. go  

### RESULT

- `lnd/output/module-09-agent-memory-management.md` — added a callout block before the `### ✅ Result` on "Tips" page explaining that students are not limited to two files, they own the agent's long-term memory, and a Dory analogy for sessions without persistent context.

## UPD7

В этом модуле так же есть упоминание `[MG]: Здесть тоже можно просить загрузить файл вместо квиза` Давай так же добавим после модуля практическое задание отправить нам файл с реализацией как в прошлом модулей. Сохрани структуру єтого раздела. 

Так же посмотри на квиз. Мне надо кодревью его, все ли там адекватно и консистентно. 

And когда будешь готов, создай мне iterative prompt для следующего модуля как заготовку и переключись на polling него. go

### RESULT
**Quiz review:** Looks good — 3 consistent questions with 3 options each, labeled correct answers, and clear explanations for all. No issues found.

**Changes:**
- `lnd/output/module-09-agent-memory-management.md` — removed `[MG]:` reviewer comment before Quiz; added `## Practical Task` section after Quiz (submit `project_spec.md` + `backlog.md` to `Oleksandr_Baglai@epam.com` with review criteria).
- `requests/module-10-fine-tuning/main.prompt.md` — created starter iterative prompt file. Switching monitoring to it now.

## UPD8

Посмотри на текст моделя и предложи какие0-то правки которіе тебе кажется уместніми. go

### RESULT

- `lnd/output/module-09-agent-memory-management.md` — three edits:
  1. "Three approaches to external memory:" → "Three approaches to managing agent memory:" — built-in todo tool is not external memory, so the heading was misleading.
  2. "from `Module 10` till `Module 20`" → "from `Module 10` through `Module 20`" — "till" is too informal; "through" is standard.
  3. "Reference both your specification and the interview technique:" → "Reference your specification and apply the interview technique:" — you apply a technique, not "reference" it; also removed awkward "both … and" phrasing.

## UPD9

А еще переведи на немецкий. go

### RESULT

Не могу — по правилам проекта весь контент модулей должен быть только на английском (`instructions/main.agent.md` → "All project content must be written in English only").