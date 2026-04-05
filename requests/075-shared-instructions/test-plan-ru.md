# План тестирования: Skills CLI — Модуль 076

**Модуль:** `076-skills-management-system`
**Инструмент:** `skills` CLI (бинарник Go)
**Тестовое окружение:** `work/076-task/`
**Дата:** 2026-04-05

---

## Структура тестового окружения

```
work/076-task/
├── skills-repo/          ← центральный Git-репозиторий навыков (локальный)
│   ├── .manifest/
│   │   ├── _global.json
│   │   ├── _agents.json
│   │   ├── project-alpha.json
│   │   ├── project-beta.json
│   │   └── security.json
│   ├── code-review-base/
│   ├── security-guidelines/
│   ├── style-guidelines/
│   ├── test-writing/
│   ├── creating-instructions/  ← глобальный навык
│   └── iterative-prompting/    ← глобальный навык
├── project-alpha/        ← рабочая папка проекта Alpha
└── project-beta/         ← рабочая папка проекта Beta
```

**Распределение по группам:**
- `_global.json`: `creating-instructions`, `iterative-prompting`
- `project-alpha.json`: `code-review-base`, `style-guidelines`, `security-guidelines` + саб-конфиг `security`
- `project-beta.json`: `code-review-base`, `test-writing`
- `security.json` (саб-конфиг): `security-guidelines`

**Пересечение:** оба проекта включают `code-review-base` + оба глобальных навыка.

---

## TC-001: Базовый сценарий — инициализация одной группы

**Команда:**
```bash
cd work/076-task/project-alpha
skills init --repo ../skills-repo --groups project-alpha
```

**Ожидаемый результат:**
- `instructions/` склонировано из `../skills-repo` (содержит `.git`)
- Sparse checkout применён: `.manifest`, `code-review-base`, `style-guidelines`, `security-guidelines`, `creating-instructions`, `iterative-prompting` присутствуют локально
- Директория `test-writing` НЕ присутствует локально (не входит в группу project-alpha)
- Создан `instructions/.manifest/config.json` с корректными `repo_url`, `groups`, `skills`
- Код завершения 0, сообщение об успехе

---

## TC-002: Базовый сценарий — инициализация нескольких групп

**Команда:**
```bash
cd work/076-task/project-alpha
# (предварительно удалить instructions/ из TC-001)
skills init --repo ../skills-repo --groups project-alpha,security
```

**Ожидаемый результат:**
- Навыки из `project-alpha.json` и `security.json` объединены (union)
- Нет дублирующихся навыков в итоговом списке
- В `instructions/.manifest/config.json` перечислены обе группы

---

## TC-003: Базовый сценарий — получение обновлений

**Подготовка:** изменить файл навыка в `skills-repo` и закоммитить.

**Команда:**
```bash
cd work/076-task/project-alpha
skills pull
```

**Ожидаемый результат:**
- `git pull` выполнен успешно в `instructions/`
- Обновлённый файл виден в `instructions/<имя-навыка>/SKILL.md`
- Код завершения 0

---

## TC-004: Базовый сценарий — список навыков

**Команда:**
```bash
cd work/076-task/project-alpha
skills list
```

**Ожидаемый результат:**
- Все директории навыков из репозитория перечислены (через `git ls-tree`)
- Активные навыки (в группах project-alpha) отмечены ✅
- Неактивные навыки (например, `test-writing`) отмечены ○
- Показаны счётчики: `Active: N | Total: M`

---

## TC-005: Базовый сценарий — публикация изменений навыка

**Подготовка:** отредактировать `instructions/code-review-base/SKILL.md` в рабочей папке project-alpha.

**Команда:**
```bash
cd work/076-task/project-alpha
skills push code-review-base
```

**Ожидаемый результат:**
- Создана ветка `feature/code-review-base-update` в `instructions/`
- Изменения добавлены в индекс и закоммичены
- Ветка запушена в origin (`../skills-repo`)
- Сообщение об успехе
- Для локального репозитория: сообщение "local repository — request a review" (URL для PR не генерируется)

**Проверка:**
```bash
cd work/076-task/skills-repo
git branch
# должна отображаться: feature/code-review-base-update
```

---

## TC-006: Команда help

**Команды:**
```bash
skills help
skills --help
skills -h
skills         # без аргументов
```

**Ожидаемый результат:**
- Отображается справка со списком всех команд
- `skills eval` показан как `(coming soon)`
- Код завершения 0

---

## TC-007: Команда eval (скоро будет)

**Команда:**
```bash
skills eval code-review-base
```

**Ожидаемый результат:**
- Выведено сообщение "coming soon"
- Код завершения 0 (не ошибочное состояние)

---

## TC-008: Проверка sparse checkout

**После TC-001:**

**Ожидаемое состояние директорий:**
```
instructions/
├── .manifest/           ✅ присутствует (всегда включается)
├── code-review-base/    ✅ присутствует
├── style-guidelines/    ✅ присутствует
├── security-guidelines/ ✅ присутствует
├── creating-instructions/ ✅ присутствует
├── iterative-prompting/ ✅ присутствует
└── test-writing/        ❌ ОТСУТСТВУЕТ (не входит в project-alpha)
```

**Проверка:**
```bash
ls work/076-task/project-alpha/instructions/
# test-writing НЕ должен отображаться
```

---

## TC-009: Глобальные навыки всегда включаются

**Подготовка:** инициализировать project-beta, не перечисляя глобальные навыки явно.

**Команда:**
```bash
cd work/076-task/project-beta
skills init --repo ../skills-repo --groups project-beta
```

**Ожидаемый результат:**
- `creating-instructions` и `iterative-prompting` присутствуют локально (из `_global.json`)
- `code-review-base` и `test-writing` присутствуют (из `project-beta.json`)
- `style-guidelines` и `security-guidelines` ОТСУТСТВУЮТ (не входят в группы project-beta)

---

## TC-010: Ошибка — повторная инициализация

**Команда (после TC-001):**
```bash
cd work/076-task/project-alpha
skills init --repo ../skills-repo --groups project-alpha
```

**Ожидаемый результат:**
- Сообщение об ошибке: "workspace already initialized (instructions/.manifest/config.json exists)"
- Подсказка: "Run `skills pull` to update, or delete instructions/ to re-initialize"
- Код завершения 1
- Существующее окружение не изменено

---

## TC-011: Ошибка — несуществующая группа

**Команда:**
```bash
skills init --repo ../skills-repo --groups non-existent-group
```

**Ожидаемый результат:**
- Клонирование проходит успешно
- Ошибка при разборе манифеста: `group "non-existent-group": manifest not found`
- Код завершения 1

---

## TC-012: Инициализация без `_global.json`

**Подготовка:** временно удалить `_global.json` из skills-repo.

**Команда:**
```bash
skills init --repo ../skills-repo --groups project-alpha
```

**Ожидаемый результат:**
- Нет сбоя — ошибка загрузки глобальных навыков обрабатывается молча
- Разрешаются только навыки из project-alpha
- Предупреждение или тихий откат (задокументировать поведение)

---

## TC-013: Ошибка — pull/push/list без инициализации

**Команды (в чистой директории):**
```bash
mkdir temp-project && cd temp-project
skills pull
skills push code-review-base
skills list
```

**Ожидаемый результат:**
- Ошибка: "not a skills workspace — run `skills init` first"
- Код завершения 1 для всех трёх команд

---

## TC-014: Ошибка — push без изменений

**Подготовка:** файлы навыка не изменены с момента последнего коммита.

**Команда:**
```bash
skills push code-review-base
```

**Ожидаемый результат:**
- Ветка создана
- `git commit` возвращает "nothing to commit"
- Понятное сообщение об ошибке (без сбоя приложения)
- Код завершения 1

---

## TC-015: Ошибка — неверный путь к репозиторию

**Команда:**
```bash
skills init --repo /nonexistent/path --groups project-alpha
```

**Ожидаемый результат:**
- Клонирование завершается с понятной ошибкой: "clone failed: ..."
- Код завершения 1
- Директория `instructions/` не создаётся

---

## TC-016: Два независимых рабочих окружения

**Подготовка:** project-alpha и project-beta оба инициализированы из одного skills-repo.

**Проверка:**
- `project-alpha/instructions/` содержит навыки alpha + глобальные, НЕ содержит `test-writing`
- `project-beta/instructions/` содержит навыки beta + глобальные, НЕ содержит `style-guidelines`
- Изменения в одном окружении не влияют на другое

---

## TC-017: Разрешение саб-конфига

**Контекст:** `project-alpha.json` ссылается на саб-конфиг `security`.

**Проверка после TC-001:**
- Навыки из `security.json` (`security-guidelines`) включены в разрешённый список
- Аналогично прямому указанию в `project-alpha.json`

---

## TC-018: Отсутствующий саб-конфиг (обработка с предупреждением)

**Подготовка:** добавить ссылку на несуществующий саб-конфиг в `project-alpha.json`:
```json
{ "skills": ["code-review-base"], "sub-configs": ["nonexistent"] }
```

**Команда:**
```bash
skills init --repo ../skills-repo --groups project-alpha
```

**Ожидаемый результат:**
- Предупреждение: "Warning: sub-config "nonexistent" not found, skipping"
- Инициализация продолжается с доступными навыками
- Код завершения 0

---

## TC-019: Инициализация с URL удалённого репозитория (опционально, требует сеть)

**Команда:**
```bash
skills init --repo https://github.com/example/skills-repo --groups backend
```

**Ожидаемый результат:**
- Клонирование с GitHub (требуется сеть)
- Поведение аналогично локальному репозиторию после клонирования

---

## Сводная таблица результатов

| ТК | Сценарий | Ожидаемый результат |
|---|---|---|
| TC-001 | Инициализация одной группы | ✅ Пройдет |
| TC-002 | Инициализация нескольких групп | ✅ Пройдет |
| TC-003 | Получение обновлений | ✅ Пройдет |
| TC-004 | Список навыков | ✅ Пройдет |
| TC-005 | Публикация изменений | ✅ Пройдет |
| TC-006 | Команда help | ✅ Пройдет |
| TC-007 | Команда eval (скоро) | ✅ Пройдет |
| TC-008 | Проверка sparse checkout | ✅ Пройдет |
| TC-009 | Глобальные навыки включены | ✅ Пройдет |
| TC-010 | Повторная инициализация | ✅ Пройдет |
| TC-011 | Несуществующая группа | ✅ Пройдет |
| TC-012 | Отсутствует _global.json | ✅ Пройдет |
| TC-013 | Команды без инициализации | ✅ Пройдет |
| TC-014 | Push без изменений | ✅ Пройдет |
| TC-015 | Неверный путь к репо | ✅ Пройдет |
| TC-016 | Два независимых окружения | ✅ Пройдет |
| TC-017 | Разрешение саб-конфига | ✅ Пройдет |
| TC-018 | Отсутствующий саб-конфиг | ✅ Пройдет |
| TC-019 | URL удалённого репо (опционально) | 🔲 Опционально |
