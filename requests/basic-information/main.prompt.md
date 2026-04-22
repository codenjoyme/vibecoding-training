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