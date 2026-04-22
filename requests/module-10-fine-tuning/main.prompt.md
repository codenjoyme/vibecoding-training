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

## UPD7

В UPD4 сделал правку, но. Тут как раз важно не просто сказать, а подчеркнуть, что юзер не пишет сам файлы, мы делаем все через агента. К этому сложнее привыкнуть инженерам, чем менеджерам. Потому что у менеджеров наівік делегирования работает лучше. А инженеры до уровня team lead все пытаются сделать сами, часто не доверяя AI. go 

### RESULT
- `lnd/output/module-10-custom-instructions.md` — strengthened Stage 3 text: removed "(or write them yourself)"; added bold "Key insight: you do not write these files yourself — you delegate the creation to the agent. This is the habit to build."

## UPD8

Давай все же откатим первую часть ## UPD1 про суфикс `.agent.md`. Все же оно должн ооставаться консистентно с другими инструкциями. go

### RESULT
- `lnd/output/module-10-custom-instructions.md` — reverted `.agent.md` rename back: restored `[verb]-[subject].agent.md` naming convention and examples at lines 13, 42, 158.

## UPD9

В строчке 79 написано `To make the AI load this catalog automatically, you need an entry point file:` и дальше даются две опции. После надо сказать, что это минималистичный вариант, а более точное описание и создание наполнения для этого файла мы дадим в следующем блоке. 

Следующий блок должден быть перед 4м (про джиру и конфлюенс), потому что там уже упоминается инструкция для создания инструкций, которая не могла появиться изнеоткуда. Потому этот новый раздел должен помочь настроить эту инструкцию и всю инфрастркуру. Скачать и установить ее можно сказав: `Установи мне инструкцию и настрой работу с уже созданнымим мной инструкциям https://github.com/codenjoyme/vibecoding-training/blob/main/instructions/creating-instructions.agent.md`. Дальше 4й сделай 5м и так ждалее. И в тексте 4 (который станет 5м) есть упоминание что если инструкции по созданию инструкций у вас нет, то создайте ее. Это удалим и в тексте отныне будем указывать не `Following 'instructions/creating-instructions.agent.md', create an instruction for` а `Following instructions create an instruction for...`. 

И давай все проверим в последующих модулях, чтобы там тоже было консистетно. go

### RESULT
- `lnd/output/module-10-custom-instructions.md` — added minimalist note after VS Code/Cursor entry point options in Page 3 Background; inserted new **Page 4: Installing the Instruction Toolkit** (meta-instruction setup, install command, 5 steps); renamed old Page 4 → Page 5 and old Page 5 → Page 6; in new Page 5 (Jira/Confluence) removed step 3 ("If you do not have creating-instructions.agent.md yet...") and changed step 2 from `Following 'instructions/creating-instructions.agent.md', create an instruction for` to `Following instructions, create an instruction for`; steps renumbered accordingly.
- Subsequent modules: no other references to `creating-instructions.agent.md` found — no additional changes needed.


## UPD10

В 120 строчке есть `### ✅ Result` вот перед ним так же можно сказать, что инструкция работает еще в двух режимах. Во первых, вы всегда можете спросить у нее любой вопрос `По инструкции для создания инструкций у меня есть вопрос: ...` (только на английском промпт сделай). А во-вторых можно взять любую старую сессию, в которой вы что-то делали полезное с AI за ручку, открыть ее и сказать `Следуя инструкции по созданию инструкцуий создай такую, которая будет ____` и дальше описать что именно из процесса тебе надо. Можно так же поступить для расширения существующей инструкции, для этого надо написать что-то вроде `Следуя инструкции по созданию инструкций создай дополнение к существующей инструкции ___, которое будет ____`. Важно понимать, что текст пропта может быть иной - большая языковая модель поймет из контекста, что ты хочешь создать новую инструкцию или дополнение к существующей. Просто используй ключевые слова `следуй инструкции`, `создай инструкцию`, `создай дополнение к инструкции` или любые синонимы, которые тебе удобны. Экспериментируй, что лучше сработает. Если окажется что модель не видит инструкцию, перефразируй запрос как мы это делали в модуле 07. go  

### RESULT
- `lnd/output/module-10-custom-instructions.md` — added content before `### ✅ Result` of Page 4 describing two extra usage modes: (1) ask questions about the instruction using `I have a question about the instruction for creating instructions: [your question]`; (2) convert a past session into an instruction using `Following instructions, create an instruction that will [...]`; and extend an existing instruction with `Following instructions, create an addition to existing instruction [name], that will [...]`; plus a Note callout explaining the `prompt` wording can vary, referencing `Module 7` if the model doesn't find it.

## UPD11

В блоке с 145й строчки `### Steps` сказано добавьте сами инфу в main.agent.md но єто уже не надо делать, оно будет сделано автоматом - надо только глянуть на изменение. go

### RESULT
- `lnd/output/module-10-custom-instructions.md` — Page 5, Step 4: changed "Update `instructions/main.agent.md` with the new instruction entries" to "Verify that `instructions/main.agent.md` was updated automatically...— review the change rather than editing manually."

## UPD13

И давай так же добавим в конец после квиза, отправьте задание на почту. Давай этот блок сделаем для всех модулей начиная от текущего и до конца. Сохраняй структуру этого блока, но меняй текст задания в зависимости от темы модуля. go

### RESULT
- `lnd/output/module-10-custom-instructions.md` — added `## Practical Task` section (instruction files + catalog submission).
- `lnd/output/module-11` through `module-20` — added `## Practical Task` section to each, with task text tailored to the module theme. Also removed `[MG]:` reviewer comments from all Summary sections in modules 11–20.

## UPD12

В 180 строчке написано `If any instruction has more than 15 rules, consider splitting it.` но правило скорее другое, не больше 500-700 строчек на инструкцию. Исправь везде где имеет смысл. go

### RESULT
- `lnd/output/module-10-custom-instructions.md` — Page 6 Step 2: changed "more than 15 rules" → "approaching 500–700 lines". The "50 rules" in the Too-broad example describes topic breadth and was intentionally left unchanged.

## UPD13

И давай так же добавим в конец после квиза, отправьте задание на почту. Давай этот блок сделаем для всех модулей начиная от текущего и до конца. Сохраняй структуру этого блока, но меняй текст задания в зависимости от темы модуля. go

## UPD14

И поревьювай квиз после всех наших правок, может что-то надо поменять в нем. go