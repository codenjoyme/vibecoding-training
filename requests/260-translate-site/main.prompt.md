<follow>
iterative-prompt/SKILL.md
</follow>

## UPD1

Я хочу такую штуку. Вот тут `modules/130-chrome-devtools-mcp-qa-emulation` есть модуль про `chrome devtool mcp`. Дальше я хочу `skill.md` следуя инструкции по созданию `instructions/creating-instructions.agent.md` открыть в хроме любой сайт и он переведется на любой язык который язык попросит. Скил в папке модуля в `tools` следуя инструкции по созданию модулей `instructions/create-training-module.agent.md`. А в модуле будет рассказ того как этим пользоваться. go

### RESULT (UPD1)

- Создан [modules/130-chrome-devtools-mcp-qa-emulation/tools/translate-site/SKILL.md](../../modules/130-chrome-devtools-mcp-qa-emulation/tools/translate-site/SKILL.md)
- Скилл умеет: принять URL + язык → построить Google Translate redirect URL → открыть через `mcp_chrome-devtoo_navigate_page` → скриншот для подтверждения
- Поддержка 14 языков из коробки (en, ru, uk, fr, de, es, it, ja, zh-CN, pt, pl, ko, ar, ...)
- Fallback: `evaluate_script` + Google Cloud Translation API для сайтов с X-Frame-Options
- Следующий шаг: добавить Part в walkthrough.md модуля 130 с описанием как пользоваться скиллом?

## UPD2

Несовсем правильно. Мне надо подход было позаимстсвовать с 130, но скил надо разместить в 260 (Одноименная папка папке риквеста), и там модуль разработать тренинговый вокруг этого. 

### RESULT (UPD2)

- Перенесён [modules/260-translate-site/tools/translate-site/SKILL.md](../../modules/260-translate-site/tools/translate-site/SKILL.md) из модуля 130 в модуль 260 (удалена старая папка в 130)
- Создан [modules/260-translate-site/about.md](../../modules/260-translate-site/about.md) — описание модуля, prerequisites (зависимость от модуля 130), topics, learning outcome, when to use
- Создан [modules/260-translate-site/walkthrough.md](../../modules/260-translate-site/walkthrough.md) — 4 Parts: как работает скилл, перевод реального сайта, edge cases и troubleshooting, расширение workflow
- SKILL.md обновлён: версия 1.1.0, ссылка на модуль 130 как кликабельный markdown link