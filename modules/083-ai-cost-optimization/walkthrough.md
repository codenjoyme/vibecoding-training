# AI Cost Optimization & Token Economics - Hands-on Walkthrough

In this module you will learn how AI API costs are calculated, check your own usage dashboard, and apply practical techniques to reduce spending — without sacrificing quality. By the end you will have a budget template and a decision matrix for model selection.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Cover

- **Token economics** — the unit of currency for every AI call
- **Usage dashboards** — where to check what you're spending
- **Cost reduction playbook** — five techniques you can apply today
- **Model routing** — matching task complexity to model price tier
- **Budget template** — a spreadsheet formula for team cost estimation

---

## Part 1: Token Economics 101

### What we'll do

Understand what a "token" is and why it determines your bill.

### What is a token?

A token is roughly 3–4 characters, or about ¾ of a word. Every AI request is metered in tokens:

- **Input tokens** — everything you send: system prompt + conversation history + your message
- **Output tokens** — everything the model generates back

Pricing is per 1 000 000 tokens (MTok). Example rates as of early 2026:

| Model | Input ($/MTok) | Output ($/MTok) |
|---|---|---|
| GPT-4o | $2.50 | $10.00 |
| Claude Sonnet 4.5 | $3.00 | $15.00 |
| GPT-4o mini | $0.15 | $0.60 |
| Claude Haiku | $0.25 | $1.25 |

### Why this matters

A 10 000-token system prompt costs **20× more** to run than a 500-token one — on every single request.

### Hands-on

Open a token counter like [platform.openai.com/tokenizer](https://platform.openai.com/tokenizer) (Windows) or the equivalent at your AI provider. Paste a typical prompt you use. Count the tokens. Note the estimated cost per 1 000 calls.

**Verify:** You should see a token count and understand the difference between input and output cost.

---

## Part 2: Measure Your Usage

### What we'll do

Find your actual spending in the dashboard and identify the top cost drivers.

### Check your dashboards

**GitHub Copilot:**
1. Open github.com → Settings → Copilot → Usage
2. Note: monthly request count, completions vs. chat ratio

**EPAM AI DIAL:**
1. Open your organisation's DIAL portal
2. Navigate to Usage or Analytics section
3. Look for: tokens consumed per model, requests per day, cost breakdown

### Hands-on

Spend 5 minutes in your dashboard. Answer these questions:
- Which model consumes the most tokens?
- What is the input:output ratio?
- What time of day has the highest usage?

Write down three numbers: total tokens last 7 days, estimated cost, top model.

**Verify:** You can name a specific dollar amount your team spent on AI last week.

---

## Part 3: Cost Reduction Techniques

### What we'll do

Apply five concrete techniques that reduce cost without losing quality.

### Technique 1: Trim your context

Every message carries the full conversation history. Long chats are expensive.

- Start a new chat when switching topics
- Use the "Compact" feature in Claude or reset context in Copilot
- Keep system prompts under 500 tokens

### Technique 2: Compress prompts

Long prompts with polite filler cost money. Compare:

| Verbose | Compressed | Token savings |
|---|---|---|
| "Could you please help me by looking at the following code and telling me if there are any issues?" | "Review this code for issues:" | ~60% |

### Technique 3: Use the right model tier

Not every task needs GPT-4o or Claude Sonnet. Sort tasks by complexity:

| Task type | Recommended tier |
|---|---|
| Code completion, short answers | Mini / Haiku |
| Complex reasoning, architecture | Sonnet / GPT-4o |
| Document analysis, long context | Depends on doc length |

### Technique 4: Cache repeated prompts

If you run the same system prompt + static context repeatedly, some providers offer prompt caching (Anthropic, OpenAI). Cached input tokens cost 90% less.

### Technique 5: Batch offline tasks

Non-interactive tasks (bulk file processing, report generation) can use async Batch API at 50% discount. See module 160.

### Hands-on

Take your top 3 prompts from a recent project. Apply Technique 1 and 2 to each. Measure token reduction using the tokenizer from Step 1. Aim for 30%+ reduction.

**Verify:** At least one prompt is 30% shorter while delivering the same result.

---

## Part 4: Model Routing — Decision Matrix

### What we'll do

Build a personal routing matrix so you automatically pick the cheapest model that can handle the task.

### The matrix

| Complexity signal | Use this model tier | Example tasks |
|---|---|---|
| Single-step, factual | Mini / Haiku | "Summarise this paragraph", completions |
| Multi-step, code | Mid-tier (Sonnet, GPT-4o) | Debugging, refactoring, explanation |
| Long document, deep reasoning | Top-tier or long-context | Architecture review, legal analysis |
| Real-time user chat | Mid-tier with streaming | In-product AI assistants |

### Hands-on

Open VS Code. In your Copilot chat, switch models using the model picker. Redo the same task with a mini model first, then with a full model. Note quality difference. For the mini result: was it good enough?

Windows path: model selector is in the top of the Copilot chat panel.  
macOS path: same location.

**Verify:** You tried at least two model tiers and can articulate when the cheaper one is sufficient.

---

## Part 5: Budget Planning

### What we'll do

Produce a monthly cost estimate for a team of N developers.

### Budget formula

```
Monthly cost = N_devs × avg_requests_per_day × avg_tokens_per_request × price_per_token × 30
```

### Example calculation

- 10 developers
- 200 requests/dev/day (chat + completions)
- 2 500 tokens per request average (input + output combined)
- $3.00 per MTok (Sonnet mid-tier)

```
10 × 200 × 2500 × (3.00 / 1_000_000) × 30 = $450/month
```

### Hands-on

Fill in your own numbers. Use the formula above. Create a simple spreadsheet or markdown table:

```
| Variable | Value |
|---|---|
| Developers | ___ |
| Requests/dev/day | ___ |
| Avg tokens/request | ___ |
| Price/MTok ($) | ___ |
| Monthly estimate ($) | ___ |
```

Save this as `./workspace/hello-genai/ai-budget.md` (Windows: `c:/workspace/hello-genai/ai-budget.md`, macOS: `~/workspace/hello-genai/ai-budget.md`).

**Verify:** You have a concrete monthly estimate in a file you can share with your manager.

---

## Success Criteria

- ✅ You can explain what a token is and the difference between input and output cost
- ✅ You checked your actual usage dashboard and found a specific spending number
- ✅ You applied at least two cost reduction techniques and measured the token savings
- ✅ You have a model routing decision matrix you will use going forward
- ✅ You produced a monthly budget estimate for your team

---

## Understanding Check

1. **What determines whether you pay more for input or output tokens?** *(Answer: Output tokens cost more because they require the model to generate each token sequentially, while input is processed in parallel. For most models, output is 3–5× more expensive per token.)*

2. **Your chat conversation has grown to 50 messages. How does that affect cost?** *(Answer: Every message carries the full history, so each new message is exponentially more expensive as the context grows. Starting a new chat resets this.)*

3. **A developer asks you to review a PR summary. Which model tier do you route this to?** *(Answer: Mini/Haiku — it's a simple, factual, single-step task.)*

4. **What is prompt caching and when would you use it?** *(Answer: Caching re-uses processed input tokens across requests. Use it when the same system prompt or document appears in many calls — saves up to 90% on those tokens.)*

5. **You have 10 developers each making 100 requests/day at 3 000 tokens average using a $5/MTok model. What's the monthly cost?** *(Answer: 10 × 100 × 3000 × (5/1_000_000) × 30 = $450/month.)*

6. **Name two signals that indicate a task needs a top-tier model rather than a mini model.** *(Answer: Multi-step reasoning, long document input, code that requires architectural understanding, tasks where the first attempt quality is critical.)*

---

## Troubleshooting

**"I can't find my usage dashboard."**  
→ For GitHub Copilot: github.com → your avatar → Settings → Copilot → scroll to Usage.  
→ For DIAL: contact your organisation's AI platform admin for access.

**"My token count seems much higher than expected."**  
→ Check if you have a large system prompt or custom instructions file. Long `.instructions.md` files are prepended to every request.

**"The budget formula gives a number that seems too low."**  
→ Don't forget to account for bulk operations (160), automated CI pipelines (155), and agent mode multi-step tasks which can use 10–50× more tokens than a single chat message.

---

## Next Steps

Continue to [Module 040 — Agent Mode & AI Mechanics](../040-agent-mode-under-the-hood/about.md) where you'll see exactly how context windows and tool calls drive the token consumption you just learned to measure.
