<follow>
iterative-prompt/SKILL.md
</follow>

## UPD1

Есть файл, который я уже начал приводить в markdown формат. Но там с линками беда началась. Потому прошу тебя это сделать самостоятельно. Смотри в качестве оригинала CodeMie+CLI+FAQ.docx файл, это zip и внутри есть xml со всей версткой. Мне надо сделать максимально  близко к оригиналу но в формате markdown. С сохранением всех линков на оглавление (линки внутри документа добавляй сам как это принято в markdown `<a href="#section-id">Section</a>` рядом с заголовками). go

### RESULT (UPD1)

- [requests/175-codemie-cli/CodeMie-CLI-FAQ.md](requests/175-codemie-cli/CodeMie-CLI-FAQ.md) — полный markdown-перевод документа из DOCX:
  - Table of Contents с рабочими anchor-ссылками на все разделы
  - Все heading-уровни (H1→H2→H3→H4) сохранены
  - Все внутренние ссылки из оглавления и текста (`[macOS](#macos-npm-not-found)` и т.д.) — рабочие markdown-якоря через `<a id="..."></a>` рядом с заголовками
  - Все внешние ссылки (nodejs.org, python.org, github.com и т.д.) сохранены
  - Таблица настроек `codemie setup` — в формате markdown table
  - Все блоки кода (bash, powershell, js, json, elisp) — в fenced code blocks с указанием языка
  - `[!CAUTION]` блок сохранён
  - Секция FAQ разбита по macOS / Windows с anchor-якорями на каждый вопрос

  ## UPD2

  Дальше давай сделаем полноценный тренинговый модуль для работы с этим `SKILL.md` он пусть *без изменения* мигрирует в папку `175-codemie-cli\tools` и дальше мы его поможем настроить учащемуся и покажем зачем нужны основные действия вокруг него. Следуй инструкции [text](../../instructions/create-training-module.agent.md). go

### RESULT (UPD2)

- [modules/175-codemie-cli/tools/SKILL.md](../../modules/175-codemie-cli/tools/SKILL.md) — SKILL.md скопирован без изменений из `requests/175-codemie-cli/SKILL.md`
- [modules/175-codemie-cli/about.md](../../modules/175-codemie-cli/about.md) — описание модуля: топики, outcome, prerequisites (103-cli required, 040-agent-mode optional)
- [modules/175-codemie-cli/walkthrough.md](../../modules/175-codemie-cli/walkthrough.md) — пошаговый воркшоп (6 частей):
  - Part 1: Install Node.js (macOS + Windows)
  - Part 2: Install CodeMie CLI via npm
  - Part 3: Authenticate with `codemie setup`
  - Part 4: Install an AI agent (`claude --supported`, gemini, opencode)
  - Part 5: Connect to IDE (VS Code = direct; Cursor = proxy; Other IDEs = ACP)
  - Part 6: Verify with `codemie doctor`
  - Success Criteria, Understanding Check (5 вопросов), Troubleshooting table, Next Steps

## UPD3

Смотри у меня уже установлены питон и нода. Давай проверим что установлено, и пройдем по этому SKILL.md чтобы установить все для работы. Верно я понимаю, что потом уменя будет доступ к моделям корпоративным через этот инструмент? Если да то как? Отчитайся в UPD/RESULT блоке и не указывай там coproprate специфик вещей. go

### RESULT (UPD3)

Установлено и проверено через `codemie doctor`:

| Компонент | Версия | Статус |
|---|---|---|
| Node.js | v24.16.0 | ✅ уже был |
| npm | 11.13.0 | ✅ уже был |
| Python | 3.13.9 | ✅ уже был |
| uv | 0.10.4 | ✅ уже был |
| CodeMie CLI | 0.3.2 | ✅ установлен сейчас |
| CodeMie Code agent | 0.0.47 | ✅ был в системе |
| Claude Code | 2.1.114 | ✅ установлен через `codemie setup` |
| Auth profile | SSO → `claude-sonnet-4-6` | ✅ настроен, сессия активна 24ч |

**Как работает доступ к моделям:**
Запросы от агента (claude, opencode и т.д.) идут не напрямую к вендору, а через CodeMie proxy → корпоративный LLM endpoint. Аутентификация через SSO — личный API-ключ не нужен. Лимиты и набор моделей управляются на уровне организации.

**`codemie doctor` — итог:** все обязательные проверки зелёные. AWS CLI и frameworks (SpecKit, BMAD) — опциональные, для базовой работы не нужны.

**Следующий шаг:** IDE-интеграция — VS Code (уже должно работать через установленный Claude Code extension) или Cursor (требует proxy-скрипт, см. [tools/SKILL.md](tools/SKILL.md) секцию Cursor).