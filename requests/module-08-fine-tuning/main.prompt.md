<follow>
iterative-prompt.agent.md
</follow>

## UPD1

```
Why this works:
- The AI "knows" what information is needed for implementation (it has seen thousands of similar projects in its training data).
- The AI can identify gaps in your requirements.
- Your answers fill in the missing details naturally.
- The `context window` accumulates precise information through dialogue rather than through guessing.
```

Скажи тут, что помните "что весь текст который написан до сих пор в чате: ваш изначальный промпт, уточняющите вопросы AI ваши ответі на єту тему - все это является новым промптом для текста который генерируется дальше. По сути контекстное окно - это промпт для текста который генерируется в нем. Потмоу если не знаете чем наполнить контекст, разогрейте его small talk в той доменной области в которой вы хотите получить велью" go

### RESULT
- `lnd/output/module-08-clarifying-requirements.md` — added a callout block after the "Why this works" bullets explaining that all chat text (prompt + AI questions + answers) forms the prompt for what the AI generates next; the context window is the prompt for the text within it; warm it up with domain small talk if unsure what to put there.

## UPD2

Слушай в модуле есть `ТЗ` во всему тексту. Это сокращение от техническое задание. А у нас весь текст на английском. Давай вместо `ТЗ` использовать `requirements` или `specification`, так чтобы оно было консистентно всему тексту. go 

### RESULT
- `lnd/output/module-08-clarifying-requirements.md` — replaced all 5 occurrences of `ТЗ` with `specification` for consistency with the English text (lines 95, 134, 146, 147, 162).

## UPD3

В 149й строчке написано 
```
[MG]: Вот уже начиная отсюда, где студент начинает генерить какие-то файлы по инструкциям, предлагаю переходить от квизов к практическим задачам, формата "загрузите файл такой-то в аудитора, он должен соответствовать критериям таким-то".
```
Надо сделать блок практического задания после квиза, где предложить студенту засабмитать полученный файл specification к нам. Давайте пока укажем `Name_Surname@example.com` в качестве получателя. Квиз оставь. Комментарий ревьюера удаляй. go

### RESULT

- `lnd/output/module-08-clarifying-requirements.md` — removed the `[MG]:` reviewer comment between Summary and Quiz; added `## Practical Task` section after the Quiz with instructions to email the specification to `Name_Surname@example.com`, including subject line and review criteria.

## UPD4

Переключись на файл [text](../module-09-fine-tuning/main.prompt.md) и следи уже за ним. go

### RESULT
- Switched monitoring to `requests/module-09-fine-tuning/main.prompt.md`. All future UPD blocks should be added there.