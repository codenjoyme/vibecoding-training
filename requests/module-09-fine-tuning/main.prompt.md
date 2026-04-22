<follow>
iterative-prompt.agent.md
</follow>

## UPD1

В 9 и 10 модулях встречается название файла `BACKLOG.md`. Капслоком как-то сильно громко получается, может просто `backlog.md`? go

### RESULT

- `lnd/output/module-09-agent-memory-management.md` — replaced 13 occurrences of `BACKLOG.md` with `backlog.md`.
- `lnd/output/module-10-custom-instructions.md` — replaced 1 occurrence of `BACKLOG.md` with `backlog.md`.

## UPD2

Следуя инструкции [text](../../instructions/organize-module-images.agent.md) обслужи картинки что я добавил толкьо что. Дальше я буду только говорить `обработай картинки`. go

### RESULT
- `lnd/output/image-1.png` → moved to `lnd/output/img/module-09/04-using-at-mention.png`
- `lnd/output/image.png` → moved to `lnd/output/img/module-09/05-move-file-to-chat.png`
- `lnd/output/module-09-agent-memory-management.md` — updated references to use new paths.

## UPD3

В модуле 08 и 09 (и возможно в последующих) есть упоминание `PROJECT_SPEC.md` опять же слишком капслоксно. Давай просто `project_spec.md`?

Так же обрати внимание если в каком-то модуле есть ссылка на модуль в формате `Module NN` то надо брать его в кавычки '`'.

Сделай это двумя разными коммитами. go

### RESULT
- **Commit 1:** `lnd/output/module-08-clarifying-requirements.md`, `lnd/output/module-09-agent-memory-management.md` — replaced all `PROJECT_SPEC.md` with `project_spec.md`.
- **Commit 2:** 14 module files updated — wrapped bare `Module N` references (in prose, not headings) in backticks.