<follow>
iterative-prompt.agent.md
</follow>

## UPD1

В этом модуле указывается, название файла `[verb]-[subject].agent.md` но правильнее будет называть их просто `[verb]-[subject].md` так как они не всегда будут агентами. Поправь это во всех модулях.

Так же перед 8 абзацем `In this module, you will learn` надо указать, что это именно то что мы делали в Модуле 09, но там мы эксрактили из сесии ифнормацию о задаче, а тут мы сохраняем информацию о процессе, чтобы потом не объяснять агенту как у нас в проекте все устроено. Смысл тот же. go

### RESULT

- `lnd/output/module-10-custom-instructions.md` — replaced all 3 occurrences of `[verb]-[subject].agent.md` (and `[action-verb]-[subject].agent.md` / example filenames) with the non-.agent.md form; added a `> Connection to Module 9` callout before "In this module, you will learn"; removed `[MG]:` reviewer comment at the end of Summary.

## UPD2

В модуле сказано `- Apply the `Single Responsibility Principle` to keep instructions focused and maintainable.` А надо дать поясннеие, єто инженернЫй термин не понятный менеджерам. go

### RESULT
- `lnd/output/module-10-custom-instructions.md` — added plain-language explanation of `Single Responsibility Principle` at all 5 occurrences: "one instruction file = one workflow. Keep each file focused on a single task type."