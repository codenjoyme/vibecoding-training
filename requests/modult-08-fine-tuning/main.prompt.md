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