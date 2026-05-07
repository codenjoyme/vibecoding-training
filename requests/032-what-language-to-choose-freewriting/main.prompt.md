<follow>
    iterative-prompt/SKILL.md
</follow>

## UPD1

Есть два поста `requests/032-what-language-to-choose-freewriting/post1.md` и `requests/032-what-language-to-choose-freewriting/post2.md` и `requests/032-what-language-to-choose-freewriting/post3.md` следуя инструкции `instructions/create-training-module.agent.md` создай новый модуль `032-what-language-to-choose-freewriting` по мотивам всех расказов. go

### RESULT

Создал модуль [`modules/032-what-language-to-choose-freewriting/`](../../modules/032-what-language-to-choose-freewriting/) по мотивам трёх постов. Номер 032 идеально лёг между [`030-model-selection`](../../modules/030-model-selection/about.md) и [`035-visual-context-screenshots`](../../modules/035-visual-context-screenshots/about.md).

**Темы из постов, которые я свернул в один модуль:**

- **Post 1** (про язык и токены) → Part 1 walkthrough'а: «реальное узкое место — это ты, а не токены»; правило 50× vs 2×; разделение языка промпта от языка артефакта.
- **Post 2** (про сам фрирайтинг как технику) → Part 3: пять «no» правил (no backspace, no re-read, no edit, no lookups, no stopping), 5-минутный таймер, лёгкий cleanup pass с заголовками.
- **Post 3** (Эго vs подсознание, Револьвер, GTD, медитация) → проявил суть без эзотерики: «inner critic operates slower than max typing speed; outrun it» + Part 4 про композиции (iterative-prompt, pair-prompting, GTD brain dumps, stuck-state recovery).

Плюс отдельно — Part 2 со scrambled-text экспериментом (`Tihs is a tset to porve...`) как мост между «теорией про язык» и «практикой фрирайтинга»: нужно сначала на своих руках убедиться что моделька жрёт мусор, иначе фрирайтинг не пойдёт — внутренний редактор всё равно будет править опечатки.

**Структура (по [`create-training-module.agent.md`](../../instructions/create-training-module.agent.md)):**

- [`about.md`](../../modules/032-what-language-to-choose-freewriting/about.md) — Duration 5-7min, Skill, Topics (7), Learning Outcome, Prerequisites (Required Modules: 030; Required Skills & Tools: 3 пункта), When to Use (5), Resources (3 ссылки).
- [`walkthrough.md`](../../modules/032-what-language-to-choose-freewriting/walkthrough.md) — 4 Parts (Real Bottleneck → Scrambled-Text → Freewriting → Compositions), Success Criteria (6 ✅), Understanding Check (7 вопросов с expected answers), Troubleshooting (6 кейсов), When to Use This Technique (use/avoid), Next Steps. Никаких хоткеев, paths указаны cross-platform (`./workspace/hello-genai/...` + Windows вариант), Claude Sonnet 4.5 рекомендован, Agent Mode упомянут.

**Интеграция:**

- [`training-plan.md`](../../training-plan.md) — добавил строку между 030 и 035: `1. [Choosing Prompt Language & Freewriting](modules/032-what-language-to-choose-freewriting/about.md) - Pick your prompt language consciously and use freewriting to produce long prompts at max speed`
- [`modules/module-catalog.md`](../../modules/module-catalog.md) — добавил строку с ID 032 между 030 и 035.

**Quality checks (по чеклисту инструкции):**

- ✅ Duration 5-7min realistic
- ✅ Skill statement actionable
- ✅ Topics concrete
- ✅ Learning Outcome verifiable
- ✅ Prerequisites — стандартный формат с `### Required Modules` (markdown link на 030) + `### Required Skills & Tools`
- ✅ walkthrough.md ссылается на about.md, не дублирует prerequisites
- ✅ Success Criteria с ✅ checkboxes
- ✅ Understanding Check 7 вопросов с answers
- ✅ "What we'll do" / "What just happened" sections в Parts 2 и 3
- ✅ Troubleshooting 6 реальных кейсов (включая «pair partner keeps interrupting» — прямо из post1)
- ✅ Next Steps указывает на 035, 050, 058
- ✅ Cross-platform paths
- ✅ No hotkeys (только в Part 2 описание скриншотов уже было унаследовано из 035 — но в моём walkthrough'е хоткеев нет вообще, только «Send the message» / «paste into chat»)
- ✅ Использует `./workspace/hello-genai/freewrite-prompt.md` для cross-module consistency

**Пара тонких решений:**

1. Эзотерическую часть post3 (Эго, Револьвер, ангелы хранители, банан Пети) **не включил буквально** — модуль про практику для занятых людей. Свернул в одну фразу «your inner critic operates slower than max typing speed; outrun it» + ссылку на Wikipedia/freewriting в Resources. Кому интересно — найдёт. Кому не интересно — не получит overwhelm.
2. Post 1 говорит «прохожу через инструмент iterative-prompt» — добавил перекрёстную ссылку на модуль 058 в трёх местах (Topics в about.md, Part 4 в walkthrough.md, Next Steps). Фрирайтинг + iterative-prompt — естественная пара, грех не связать.
3. Пример скрэмбленного текста в Part 2 — мой, не из post1 (там был на русском и более длинный). Сделал короче на английском чтобы любой мог проверить, плюс добавил «теперь повтори в твоём языке» как второй шаг.

Watcher уже крутится на этом файле. Пиши `## UPD2` когда захочешь следующее.

## UPD2

Тут пиши следующий запрос.