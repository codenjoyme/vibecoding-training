<follow>
iterative-prompt.agent.md
</follow>

## UPD1

В этом модуле указывается, название файла `[verb]-[subject].agent.md` но правильнее будет называть их просто `[verb]-[subject].md` так как они не всегда будут агентами. Поправь это во всех модулях.

Так же перед 8 абзацем `In this module, you will learn` надо указать, что это именно то что мы делали в Модуле 09, но там мы эксрактили из сесии ифнормацию о задаче, а тут мы сохраняем информацию о процессе, чтобы потом не объяснять агенту как у нас в проекте все устроено. Смысл тот же. go

### RESULT

- `lnd/output/module-10-custom-instructions.md` — replaced all 3 occurrences of `[verb]-[subject].agent.md` (and `[action-verb]-[subject].agent.md` / example filenames) with the non-.agent.md form; added a `> Connection to Module 9` callout before "In this module, you will learn"; removed `[MG]:` reviewer comment at the end of Summary.

## UPD2

В модуле сказано `- Apply the `Single Responsibility Principle` to keep instructions focused and maintainable.` А надо дать поясннеие, єто инженернЫй термин не понятный менеджерам. go

### RESULT

- `lnd/output/module-10-custom-instructions.md` — added plain-language explanation of `Single Responsibility Principle` at all 5 occurrences: "one instruction file = one workflow. Keep each file focused on a single task type."

## UPD3

Смотри я заметил, что термины такие как `prompt` не взято в кавычки как это сказано в инструкции по стилю. Давай все последущие модули включая текущий посмотрим еще раз на наличие таких терминов и возьмем их в кавычки.  go

### RESULT
- Modules 10–20: wrapped bare `prompt`/`prompts`/`token`/`tokens` in backticks across all occurrences in prose text (8 files updated: module-10, 11, 12, 13, 14, 15, 19).

## UPD4

Так же в этом модуле сказано `Stage 3 — `Markdown` format: You create`. Тут надо дать пояснение. `You create` это не значит что ты пишешь, это значит, что ты просишь агента написать.  go

### RESULT
- `lnd/output/module-10-custom-instructions.md` — clarified Stage 3 description: changed "You create" to "You ask the AI to create... (or write them yourself)" so it's clear you can ask the agent to generate the files.

## UPD5

В 36й строчке написано `(stage 4)` но везде в заголовках указано `Page N`. Давай так же посмотрим каждый модуль начиная от самого первого, на наличие подобных нестыковок и поправим их.  go

### RESULT
- Scanned all modules — no genuine Page/stage inconsistencies found. The `(stage 4)` in module-10 line 36 correctly refers to the prompt maturity model stages (Stage 1-4 listed above it), not to a module page. Fixed capitalization to `(Stage 4)` for consistency with the model definition.

## UPD6

Каждый из послудующих апдейтов сделай отдельным коммитом и отчитайся отдельно. Так же сделай новый UPD в риквесте по изменению iterative prompt, чтобы эта идея отражалась там, и в самой инструкии. После закрытия ## UPD6 тут, закрой его и там и в инструкции. Мне важно, чтобы я мог создавать серию апдейтов, и работать с ними атомарно. То есть пока ты рабоатешь скажем над UPD3, я могу заканчивать 4й и начинать 5й. Но ты будешь последовательно из обрабатывать. И для начала каждого ты ожидаешь его собственный go. go   

### RESULT
- `instructions/iterative-prompt.agent.md` — updated "Non-stop loop" to explicitly state each UPD = one separate commit, UPDs without `go` are skipped, parallel writing is supported.
- `requests/iterative-prompt/main.prompt.md` — added UPD6 with RESULT documenting this change.
- Going forward: each UPD in this session gets its own commit and reports separately.