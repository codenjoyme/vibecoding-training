# Onboarding New Team Members with AI - Hands-on Walkthrough

In this walkthrough, you'll build an AI-powered onboarding system for your project. You'll create an instruction that makes AI understand your codebase, test it by simulating a new joiner's questions, and measure how much better the answers are with the system than without it.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

By the end of this walkthrough you will have:

- **An onboarding instruction file** — `instructions/onboarding.agent.md` with project structure, conventions, key decisions, and common Q&A
- **A tested Q&A session** — 10 questions a new joiner would ask, with answers graded before and after activating the instruction
- **A SpecKit-grounded knowledge base** — the AI uses your actual documentation to answer "why" questions, not just "what" questions
- **A reproducible onboarding flow** — a step-by-step checklist any new team member follows on day one

---

## Step 1: Diagnose the onboarding problem

Before building anything, ask AI to help you articulate the problem:

```
I manage a team working on [describe your project briefly].
When new developers join, what are the top 10 questions they typically ask in the first week?

For each question, estimate:
- How long it typically takes to get an answer (minutes/hours/days)
- Whether the answer exists in documentation or only in someone's head
- How accurate AI would be answering it WITHOUT any project-specific context

Organise the list by: "AI can answer well right now" vs. "AI needs context to answer well" vs. "AI cannot answer this".
```

This diagnostic shows you exactly where the onboarding instruction will add the most value.

---

## Step 2: Create the onboarding instruction

**What we're about to do:** Write an instruction file that gives AI everything it needs to answer new-joiner questions accurately — project structure, conventions, key decisions, and the location of important files.

Ask AI to help you draft it, then fill in the specifics yourself:

```
Create a VS Code Copilot onboarding instruction file for a new team member.

The instruction should tell the agent:
1. Project overview: [describe your project — what it does, who uses it, main tech stack]
2. Repository structure: [list top-level folders and their purpose]
3. Key conventions: [naming rules, branching strategy, code style]
4. Important decisions and their rationale: [why was technology X chosen, why is Y structured this way]
5. Where to find things: [config files, main entry points, test setup, documentation]
6. Common gotchas: [things that confuse everyone at first]
7. Who to ask: [team roles and what each person owns — use roles, not names]

When a new joiner asks a question, the agent should:
- Answer directly from this context when possible
- Cite which file or folder is relevant
- Admit when the answer is uncertain and suggest who to ask

Format as .agent.md.
```

Save to `instructions/onboarding.agent.md`.

**Windows:** `c:/workspace/hello-genai/instructions/onboarding.agent.md`  
**macOS/Linux:** `~/workspace/hello-genai/instructions/onboarding.agent.md`

---

## Step 3: Connect your SpecKit documentation

**What we're about to do:** Add your SpecKit documentation (from module 125) as the grounded knowledge base so AI can answer "why" questions with real decisions, not guesses.

If you completed module 125, you have a `specs/` folder with project documentation. Tell the onboarding agent about it:

Open `instructions/onboarding.agent.md` and add a section:

```markdown
## Documentation Sources

When answering questions about architecture, design decisions, or requirements, use these documents as primary sources:

- `specs/overview.md` — high-level project description and goals
- `specs/architecture.md` — system design and component relationships
- `specs/decisions/` — Architecture Decision Records (why key choices were made)
- `README.md` — setup and getting started guide

If the documentation contradicts this instruction, trust the documentation — it is more recent.
```

Ask AI to test whether it can use the docs to answer a question:

```
[Attach instructions/onboarding.agent.md]
[Attach specs/overview.md]

I'm a new developer joining this project. My first question is:
"Why did the team choose [key technology] instead of [alternative]?"

Answer based only on the documentation provided. If the answer is not in the docs, say so.
```

Compare: does the answer with docs differ from the answer without docs? That difference is the value of the grounded knowledge base.

---

## Step 4: Simulate the 30-minute onboarding

**What we're about to do:** Roleplay being a new joiner for 30 minutes. Ask 10 real questions a new team member would ask. Grade each answer.

Open a new AI chat, attach `instructions/onboarding.agent.md`, enable Agent Mode. Then ask these questions (adapted to your project):

1. "What does this project do and who are its users?"
2. "How do I set up my local development environment from scratch?"
3. "What's the branching strategy — should I work directly on main or create feature branches?"
4. "Where is the main entry point of the application?"
5. "How do I run the tests?"
6. "What does the `[your most confusing folder name]` folder contain?"
7. "Why was [key architectural decision] made this way?"
8. "If I need to add a new API endpoint, where do I start?"
9. "Who owns the authentication/payment/[critical area] part of the codebase?"
10. "What were the main challenges this project faced in its first 6 months?"

After each answer, grade it: ✅ Accurate and useful / ⚠️ Partially correct / ❌ Wrong or missing.

**What just happened:** You've stress-tested your onboarding instruction. Low-scoring questions reveal gaps — either in the instruction or in your documentation.

---

## Step 5: Fix the gaps

For every ⚠️ or ❌ answer from Step 4:

Either:
1. **Add the missing information to `instructions/onboarding.agent.md`** — if the answer exists but wasn't in the instruction
2. **Create a documentation file** — if the answer doesn't exist anywhere (`specs/decisions/why-X.md`)
3. **Accept the gap** — some knowledge only lives in people's heads; note these as "ask [role]" in the instruction

Re-run the failing questions. The goal: 8 out of 10 answers should be ✅ after the fix pass.

---

## Step 6: Create the day-one checklist

**What we're about to do:** Package the onboarding setup into a simple checklist a new team member follows on their first day — independent of anyone being available to guide them.

Ask AI:

```
Based on the onboarding instruction and documentation I have, create a Day One checklist for a new developer joining this project.

The checklist should:
1. Start with setup (clone repo, install dependencies, run locally)
2. Include: open the onboarding instruction in VS Code, enable Agent Mode, do the 10-question self-test
3. List 5 files/folders to read in the first hour (with brief reason why)
4. End with: "You're ready if you can answer these 5 questions without AI help: [list questions]"

Format as a Markdown checklist with checkboxes.
```

Save as `docs/day-one-checklist.md`. Commit all new files to Git.

---

## Success Criteria

- ✅ `instructions/onboarding.agent.md` created with project context, conventions, and key decisions
- ✅ SpecKit documentation linked as a knowledge source in the instruction
- ✅ 10-question simulation completed with answers graded
- ✅ At least 8 out of 10 questions received ✅ Accurate answers
- ✅ Gaps identified and addressed (instruction updated or docs created)
- ✅ `docs/day-one-checklist.md` created and committed
- ✅ You can estimate how much onboarding time the AI system saves vs. traditional wikis

---

## Understanding Check

1. **Why does AI give better onboarding answers with a project-specific instruction than without one?**
   > Without context, AI answers based on general best practices and guesses about your project. With an onboarding instruction, AI has the actual facts: your folder structure, your tech choices, your naming conventions. The instruction is the difference between "here's how teams typically structure this" and "here's how YOUR team structures this".

2. **What is the relationship between documentation quality and onboarding AI quality?**
   > AI can only answer accurately from what's written down. If a decision was made verbally and never documented, the AI cannot answer "why was X chosen?" — it will guess or say it doesn't know. Better documentation directly improves AI onboarding quality. This creates a virtuous cycle: the onboarding system exposes documentation gaps that are worth filling.

3. **Why should the onboarding instruction say "trust the documentation over this instruction" when they conflict?**
   > Instructions are written once and tend to accumulate drift — the project changes but the instruction isn't always updated. Documentation (especially SpecKit docs with dates) is more likely to reflect the current state. This fallback rule prevents the instruction from confidently giving outdated answers.

4. **What types of questions can AI-powered onboarding NOT answer well, even with a perfect instruction?**
   > Questions requiring real-time information (current sprint state, recent incidents), interpersonal context (why two team members disagree on approach), implicit tribal knowledge never written down, and questions requiring judgment about the future (should we change X?). These remain "ask a human" questions — and that's fine. Good onboarding identifies which questions are which.

5. **How does the day-one checklist change the onboarding experience for a remote team member joining from a different time zone?**
   > A remote team member in a different time zone may have zero overlap with senior team members in the first day. Without a checklist + AI system, they're blocked waiting for answers. With it, they can be productive immediately — explore the codebase, understand the structure, and ask AI for context — without depending on synchronous communication.

6. **What metric would tell you the onboarding system is actually working after 3 months of use?**
   > Time from "first commit" to "merged meaningful contribution" (time-to-first-contribution). Or: number of "how do I X?" Slack/Teams messages sent to senior developers in the first two weeks (should decrease). Or: new joiner self-assessment score on project understanding after day one (should increase). Pick one, measure it before and after.

---

## Troubleshooting

**AI answers are correct but too generic — not specific to our project**
> The instruction is too abstract. Replace general statements with specifics: instead of "we follow REST API conventions", write "our API endpoints are in `src/api/`, use snake_case names, and every endpoint must have an OpenAPI docstring". Concrete beats abstract every time.

**New joiner says AI gave wrong answers about recent changes**
> Instructions go stale. Add a last-updated date to the instruction header and a reminder to update it after significant architectural changes. Consider adding an "Ask AI to check if this instruction is still accurate" step to your team's quarterly process.

**The 10-question simulation gives mostly ⚠️ answers**
> The instruction is missing content, not wrong. For each partial answer, ask AI: "What information was missing from my instruction that prevented you from answering this well?" Use the response as a to-do list for filling in the instruction.

**Instruction file is getting very long (100+ lines)**
> Split into multiple files: `instructions/onboarding-structure.agent.md`, `instructions/onboarding-decisions.agent.md`. Attach the relevant one based on the question type. Alternatively, link to documentation files instead of duplicating their content in the instruction.

---

## Next Steps

You've applied AI to team-level knowledge sharing. Complete the advanced track:

**→ [Module 200 — AI for Data Analysis & Reporting](../200-ai-data-analysis-reporting/about.md)**

Take the AI fluency you've built and apply it to the data your team generates daily — sprint reports, test results, usage metrics — and turn them into actionable insights automatically.
