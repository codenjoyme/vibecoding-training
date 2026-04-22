<follow>
iterative-prompt.agent.md
</follow>

## UPD1

Давай в quickstart добавим пререквизит что надо использовать Claude Sonnet 4.6 модель использовать стоить и агентный режим. go 

### RESULT

- `quickstart.md` — added a **Prerequisites** section at the top recommending Claude Sonnet 4.6 model and Agent Mode.

## UPD2

Можно ли переключить модель программно?

### RESULT

- `github.copilot.chat.defaultModel` в `settings.json` не работает — VS Code показывает "Unknown Configuration Setting"
- В `.prompt.md` файлах можно указать модель в YAML frontmatter: `model: claude-sonnet-4-6` — это поддерживаемый способ
- В текущих `.prompt.md` файлах проекта `model:` не задан, только `mode: agent`

## UPD3

Смотри что я нашел как ошибка 
`The 'mode' attribute has been deprecated. Please rename it to 'agent'.`
Надо пофиксить инструкцию по созданию инструкций, чтобы там было `agent: agent` для промптов. Пофиксить промпты. 

А так же сделай в `quickstart.md` чтобы он был промптом с именем `quickstart.prompt.md` и там уже указать `agent: agent` и `model: Claude Sonnet 4.6`. Go

### RESULT

- `.github/prompts/*.prompt.md` (7 files) — replaced deprecated `mode: agent` with `agent: agent`
- `instructions/creating-instructions.agent.md` — updated VSCode prompt template: `mode: agent` → `agent: agent`
- `quickstart.prompt.md` — created new prompt file with `agent: agent` and `model: Claude Sonnet 4.6` frontmatter, same content as `quickstart.md`

## UPD4

Я удалил `quickstart.prompt.md` - не сработало как ожидалось. Давай в папке .github/prompts/ сделаем `quickstart.prompt.md` с `agent: agent` и `model: Claude Sonnet 4.6` в YAML frontmatter и одной ссылкой на `quickstart.md` внутри. 

Порисерчи, что есть для курсора по этой теме. Тоже должен быть какой-то такой способ запуска. 

И третье, надо нам создать инфрастуктуру для клода надо для  `quickstart.md` с включением агентного режиме и модели сделать. go

### RESULT

- `.github/prompts/quickstart.prompt.md` — created GitHub Copilot prompt with `agent: agent` and `model: Claude Sonnet 4.6` and link to `quickstart.md`
- `.cursor/rules/quickstart.mdc` — created Cursor rule for quickstart with description and reference to `quickstart.md`
- `.claude/commands/quickstart.md` — created Claude Code command for quickstart with reference to `quickstart.md`
- `.claude/CLAUDE.md` — created Claude project memory file with instructions to follow `main.agent.md`

## UPD5

Так же я хочу еще один мануал в корне `for-authors.md` суть которой будет такая же как в `quickstart.md`, но с фокусом на авторов инструкций. Для этого файла надо так же в трех вариациях: claude, cursor и copilot сделать ярлыки с переключением модели и агентного режима. Но в самой инструкции надо пеерчислить вот такие важные моменты:
- Смотрите папку [requests](..) там много примеров того как я создаю модули и другие правки через iterative prompt подход.
- Смотрите инструкцию [text](../../instructions/iterative-prompt.agent.md) она расскажет как работает iterative prompt подход.
- Когда вы просите создать модуль, то используется инструкция [text](../../instructions/create-training-module.agent.md).
- Когда вы просите пройти модуль, то инструкция [text](../../instructions/training-mode.agent.md).
  + Опционально, если хочется секономить токены то инструкция [text](../../instructions/training-mode-iterative-prompt.agent.md) добавляет вомзможность пройти тренинг в iterative prompt режиме.
- А в инструкции [text](../../instructions/creating-instructions.agent.md) описана архитектура при которой агент добирается до инструкций через: 
  + [Github Copilot](../../.github/copilot-instructions.md)
  + [Claude](../../CLAUDE.md)
  + [Cursor](../../.cursor/rules/core-instructions.mdc)
  + [Другие](../../AGENT.md)
  + Через [text](../../instructions/main.agent.md)
  + К инструкциям в папке [text](../../instructions) 
go

### RESULT

- `for-authors.md` — created comprehensive guide for content authors with Prerequisites section, Essential Resources linking to all key instruction files, Workflow Tips, and Common Tasks
- `.github/prompts/for-authors.prompt.md` — created GitHub Copilot prompt with `agent: agent` and `model: Claude Sonnet 4.6` and link to `for-authors.md`
- `.cursor/rules/for-authors.mdc` — created Cursor rule for authors guide with description and reference to `for-authors.md`
- `.claude/commands/for-authors.md` — created Claude Code command for authors with reference to `for-authors.md`