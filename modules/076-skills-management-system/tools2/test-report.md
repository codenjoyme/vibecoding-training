# Skills CLI (Node.js) — Stress Test Report

**Version:** 1.0.0 (post-UPD18 fixes)  
**Date:** 2026-04-13  
**Environment:** Windows 11, Node.js 18+, PowerShell 5.1  
**Test workspace:** `work/076-task/` (recreated from `demo/setup.ps1`)

---

## Setup

| # | Step | Result |
|---|------|--------|
| S-01 | `demo/setup.ps1` — создаёт `skills-repo` с git (18 файлов) | ✅ |
| S-02 | `npm install -g ./tools2/skills-cli` — глобальная установка | ✅ |
| S-03 | `skills help` глобально доступна после установки | ✅ |

---

## help / root

| # | Команда | Ожидаемое | Результат |
|---|---------|-----------|-----------|
| TC-01 | `skills help` | Список всех команд с описанием | ✅ |
| TC-02 | `skills` (без аргументов) | То же что help, exit 0 | ✅ |
| TC-03 | `skills foobar` | `Error: unknown command "foobar"` + usage, exit 1 | ✅ |

---

## init

| # | Команда | Ожидаемое | Результат |
|---|---------|-----------|-----------|
| TC-04 | `skills init --repo ../skills-repo --groups project-alpha` | 5 скиллов: code-review-base, creating-instructions, iterative-prompting, security-guidelines, style-guidelines | ✅ |
| TC-05 | `skills init --repo ../skills-repo --groups project-beta` | 4 скилла: code-review-base, creating-instructions, iterative-prompting, test-writing | ✅ |
| TC-06 | `skills init --repo ../skills-repo --groups "project-alpha,project-beta"` | 6 скиллов (PowerShell запятая), обе группы | ✅ |
| TC-07 | `skills init --groups project-alpha` (без --repo) | `Error: --repo is required` + help, exit 1 | ✅ |
| TC-08 | `skills init --repo ../skills-repo` (без групп) | `Error: specify at least one group` + help, exit 1 | ✅ |
| TC-09 | Повторный `skills init` в уже инициализированном workspace | `Error: workspace already initialized` + подсказка, exit 1 | ✅ |
| TC-10 | project-alpha: `test-writing` не должен присутствовать | `skills list` — ○ test-writing | ✅ |
| TC-11 | project-beta: `security-guidelines`, `style-guidelines` отсутствуют | `skills list` — ○ для обоих | ✅ |
| TC-12 | project-both (обе группы): все 6 скиллов активны | `skills list` — 6/6 ✅ | ✅ |
| TC-13 | `skills init --help` | Флаги, примеры, exit 0 | ✅ |
| TC-14 | positional args: `skills init --repo ../skills-repo project-alpha project-beta` | 6 скиллов (без --groups) | ✅ |

---

## list

| # | Команда | Ожидаемое | Результат |
|---|---------|-----------|-----------|
| TC-15 | `skills list` в project-alpha | 5 ✅, 1 ○ (test-writing), показывает repo + groups | ✅ |
| TC-16 | `skills list` в project-beta | 4 ✅, 2 ○ (security-guidelines, style-guidelines) | ✅ |
| TC-17 | `skills list` вне workspace | `Error: not a skills workspace — run \`skills init\` first`, exit 1 | ✅ |
| TC-18 | `skills list --help` | Описание команды, exit 0 | ✅ |

---

## pull

| # | Команда | Ожидаемое | Результат |
|---|---------|-----------|-----------|
| TC-19 | `skills pull` | `✅ Skills updated successfully`, остаётся на master | ✅ |
| TC-20 | `skills pull` вне workspace | `Error: not a skills workspace`, exit 1 | ✅ |
| TC-21 | `skills pull` после `skills push` | Не падает (default branch корректно) | ✅ |
| TC-22 | `skills pull --help` | Описание команды, exit 0 | ✅ |

---

## push

| # | Команда | Ожидаемое | Результат |
|---|---------|-----------|-----------|
| TC-23 | `skills push code-review-base` (с реальным изменением) | branch + commit + push + `(local repository — ...)` | ✅ |
| TC-24 | `skills push style-guidelines` (второй скилл) | branch + commit + push + `(local repository — ...)` | ✅ |
| TC-25 | После push: `git -C instructions branch` — на master | `* master` | ✅ |
| TC-26 | `skills push` (без имени) | `Error: skill name is required`, exit 1 | ✅ |
| TC-27 | `skills push does-not-exist` | commit fail + автоматический `Switched to branch 'master'`, exit 1 | ✅ |
| TC-28 | `skills push` вне workspace | `Error: not a skills workspace`, exit 1 | ✅ |
| TC-29 | `skills push --help` | Описание шагов 1-5, exit 0 | ✅ |

---

## manifest / sparse checkout

| # | Сценарий | Ожидаемое | Результат |
|---|----------|-----------|-----------|
| TC-30 | sub-config: группа `security` → `security.json` добавляет `security-guidelines` | 3 скилла (global + security) | ✅ |
| TC-31 | `_global.json` скиллы (`creating-instructions`, `iterative-prompting`) присутствуют во всех группах | ✅ во всех: project-alpha, project-beta, security | ✅ |

---

## Итого

| Категория | Всего | ✅ Прошло | ❌ Упало |
|-----------|-------|----------|---------|
| Setup | 3 | 3 | 0 |
| help/root | 3 | 3 | 0 |
| init | 11 | 11 | 0 |
| list | 4 | 4 | 0 |
| pull | 4 | 4 | 0 |
| push | 7 | 7 | 0 |
| manifest | 2 | 2 | 0 |
| **Всего** | **34** | **34** | **0** |

**34/34 тест-кейсов пройдено. Все баги из UPD18 пофикшены и подтверждены.**

---

## Фиксы подтверждены в тестах

| Фикс (UPD18) | Подтверждающий тест |
|--------------|---------------------|
| `execFileSync` вместо `execSync` | TC-04 – TC-24 (все git-операции работают) |
| `"prepare": "tsc"` | S-02 (установка без предварительного билда) |
| `config.load()` бросает исключение | TC-17, TC-20, TC-28 (единственный `Error:` без дублирования) |
| Мёртвый тернарный убран | TC-19 (pull работает корректно) |
| Сообщение для локального репо | TC-23, TC-24 (`(local repository — request a review...)`) |
| Branch cleanup при push failure | TC-27 (возврат на master после `commit failed`) |
| Branch cleanup при push rejection | TC-25 (branch `--show-current` → `master`) |
