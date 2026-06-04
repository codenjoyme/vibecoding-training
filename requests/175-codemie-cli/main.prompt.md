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