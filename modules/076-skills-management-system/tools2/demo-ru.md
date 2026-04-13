# Skills CLI — Быстрая демонстрация (Node.js Edition)

Пошаговое прохождение полного рабочего процесса: от установки до предложения изменения скилла через Pull Request.

---

## Шаг 1 — Установка CLI

```bash
npm install -g git+https://github.com/your-org/skills-cli.git
```

> Устанавливает команду `skills` глобально из приватного Git-репозитория.  
> После этого `skills` доступен в любой сессии терминала.

---

## Шаг 2 — Проверка установки

```bash
skills help
```

> Выводит список всех доступных команд. Используй `skills <команда> --help` для деталей.

---

## Шаг 3 — Создание папки проекта

```bash
mkdir my-project
cd my-project
```

> Это воркспейс разработчика, куда будут установлены скиллы.

---

## Шаг 4 — Инициализация воркспейса скиллов

```bash
skills init --repo https://github.com/your-org/skills-repo --groups backend
```

> Клонирует центральный репозиторий скиллов в `instructions/`, резолвит скиллы для группы `backend`  
> (объединяет `_global.json` + `backend.json` + любые sub-configs), применяет sparse checkout —  
> в локальном воркспейсе появляются только нужные скиллы. Записывает `instructions/.manifest/config.json`.

**Пример с локальным путём (для тестирования):**

```bash
skills init --repo ../skills-repo --groups project-alpha
```

**Несколько групп:**

```bash
skills init --repo ../skills-repo --groups backend,security
```

---

## Шаг 5 — Список доступных скиллов

```bash
skills list
```

> Показывает все скиллы в центральном репозитории.  
> Активные скиллы (подключённые для твоих групп) помечены ✅.  
> Скиллы, не входящие в твои группы, помечены ○.

**Пример вывода:**
```
Skills repository: ../skills-repo
Groups:           project-alpha

  ✅ code-review-base
  ✅ creating-instructions
  ✅ iterative-prompting
  ✅ security-guidelines
  ✅ style-guidelines
  ○  test-writing

Active: 5  |  Total: 6
```

---

## Шаг 6 — AI-агент читает скиллы

```
instructions/code-review-base/SKILL.md
instructions/creating-instructions/SKILL.md
instructions/security-guidelines/SKILL.md
...
```

> Дополнительная настройка не нужна. Агент сканирует `instructions/*/SKILL.md`  
> и автоматически загружает их как контекст.

---

## Шаг 7 — Обновление локальных скиллов

```bash
skills pull
```

> Запускает `git pull` в папке `instructions/`. Перед этим всегда переключается на ветку по умолчанию,  
> чтобы избежать проблем с трекингом после предыдущего `push`.

---

## Шаг 8 — Редактирование скилла

```bash
# Открой файл скилла в редакторе
code instructions/code-review-base/SKILL.md
```

> Вноси улучшения прямо в директории скилла.  
> Изменения остаются локальными до тех пор, пока ты не предложишь их через `skills push`.

---

## Шаг 9 — Предложить изменение через Pull Request

```bash
skills push code-review-base
```

> 1. Создаёт ветку `feature/code-review-base-update` в `instructions/`  
> 2. Стейджит все изменения в `instructions/code-review-base/`  
> 3. Делает коммит с сообщением `feat(code-review-base): update skill instructions`  
> 4. Пушит ветку в origin  
> 5. Выводит URL для создания PR (GitHub/GitLab)  
> 6. Автоматически возвращается на ветку по умолчанию

**Пример вывода:**
```
→ Creating branch feature/code-review-base-update ...
  ✓ Branch created
→ Staging and committing changes in code-review-base/ ...
  ✓ Changes committed
→ Pushing branch feature/code-review-base-update ...
  ✓ Branch pushed

✅ Skill "code-review-base" pushed for review
   Branch: feature/code-review-base-update
   Open PR: https://github.com/your-org/skills-repo/compare/feature/code-review-base-update?expand=1
```

---

## Шаг 10 — Обновление после мерджа PR

```bash
skills pull
```

> Синхронизирует все скиллы с последними изменениями из центрального репозитория.

---

## Итоговая таблица команд

| Команда | Что делает |
|---------|-----------|
| `skills help` | Показать все команды |
| `skills init --repo <url> --groups <группа>` | Клонировать репо, подключить нужные скиллы |
| `skills list` | Показать активные ✅ и неактивные ○ скиллы |
| `skills pull` | Получить последние изменения из центрального репо |
| `skills push <имя-скилла>` | Предложить изменение скилла через ветку + PR |
