# Отчёт о тестировании Python Skills CLI

## Область тестирования

Python-порт сравнивался с текущими реализациями Go и Node.js и тестировался в Windows с доступным Docker Desktop. Тесты используют только временные репозитории или изолированную область `work/076-task/`.

## Выполненные проверки

| Проверка | Результат | Покрытие |
|---|---|---|
| Компиляция Python bytecode | PASS | Все модули runtime компилируются с `python -m compileall -q .` |
| Сборка и установка Python-пакета | PASS | `pip install --target` собирает wheel; пакет содержит `SKILL-CLI.md` |
| Сборка Python Docker image | PASS | Чистый образ `python:3.12-slim` с Git |
| Python Docker smoke test | PASS | 14 фаз и 166 строк с командами: help, init, list, metadata, toggles, create, push с группами, merge/pull, повторный push, force stash, re-init, init-repo и negative cases |
| Docker baseline Go | PASS | Существующий smoke suite из 14 фаз и 166 строк с командами |
| Docker baseline Node.js | PASS | Существующий smoke suite из 14 фаз и 168 строк с командами |
| Диагностика workspace | PASS | Для `tools_py/` ошибок не обнаружено |

## Сценарии Python smoke-теста

- Свежий fixture-репозиторий с `_global.json`, двумя группами, вложенным security sub-config и пятью skills.
- Инициализация с группой и проверка sparse checkout.
- Инициализация только глобальных skills без `--groups`.
- Обычный, verbose- и JSON-вывод списка skills.
- Получение metadata для checked-out и sparse-excluded skills.
- Включение и отключение групп и отдельных skills с немедленным применением sparse checkout.
- Отказ отключать dirty skill и stash untracked-файла при использовании `--force`.
- Шаблоны нового skill и регистрация в `extra_skills`.
- Push с несколькими новыми и существующими group manifests.
- Merge, pull и второй push с пересозданием существующей feature-ветки.
- Повторная инициализация из `skills.json`.
- Структура `init-repo` и pretty-printed JSON.
- Ожидаемые ошибки для неизвестной команды и workspace без инициализации.

## Исправления переносимости, найденные тестами

1. Portable Windows Python не включал каталог скрипта в `sys.path`; launcher `skills.py` добавлял его сам и использовался в документации.
2. Windows `charmap` не мог кодировать status-маркеры CLI; entry point настраивал UTF-8-вывод с обработкой неподдерживаемых символов.
3. Git-файлы в Windows могли быть read-only; re-initialization удаляла их с обработчиком восстановления read-only.
4. В первом Docker smoke image отсутствовал `/workspace`, поэтому команды незаметно выполнялись не там; Dockerfile создавал этот каталог.
5. Для установленного `ai-help` требовался reference внутри wheel; root `SKILL-CLI.md` теперь устанавливается как data-file, а дублирующий `skills_cli/SKILL-CLI.md` удалён.

## Ожидаемый отрицательный вывод

Snapshot намеренно содержит:

- `Error: not a skills workspace - run 'skills init' first` с `exit=1`.
- Отказ из-за dirty changes перед принудительным disable.
- `Error: unknown command "unknown-command"`.

Эти строки проверяют обработку ошибок и не означают падение тестового прогона.

## Исследование Go/Node.js

Сравнение реализаций записано в [go-node-differences.md](go-node-differences.md), включая рекурсивное разрешение sub-config, различия вывода, дрейф документации и утечку stderr Node.js при пересоздании ветки, обнаруженную в baseline smoke-тесте.
