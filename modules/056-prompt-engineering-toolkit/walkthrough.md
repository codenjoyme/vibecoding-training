# Prompt Engineering Toolkit — Hands-on Walkthrough

In this walkthrough, you'll build a personal toolkit of 15 prompting techniques — and more importantly, develop the intuition for **when** each one matters. We'll use a single abstract task throughout: *"I want to improve team communication."* This deliberately vague goal will let you see how each technique reshapes what AI tells you — and which hidden knowledge it unlocks.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

---

## Two Core Metaphors

Before we dive into techniques, two metaphors will frame everything in this module. They explain **why** the same person can get wildly different results from the same AI model.

### The Mirror

AI is a mirror. It reflects back to you the language, framing, and expertise level that you bring to it.

- If you speak like an architect, it answers like it's talking to an architect — with systems thinking, trade-offs, and design patterns.
- If you speak like a junior, it answers like it's talking to a junior — with toy examples, simplified explanations, and safe defaults.
- It's not being condescending or elitist. It's calibrating to **your signal**.

This means: **your words don't just describe the problem — they select which corpus of knowledge the model draws from.** The same question phrased differently lands in a completely different region of the model's training data.

"How do I make my team communicate better?" → self-help, generic tips.
"What communication frameworks reduce coordination overhead in cross-functional product teams?" → organizational design, Conway's Law, team topologies.

Same intent. Different mirrors. Different worlds of answers.

### The Room of Requirement

From Harry Potter: a magical room that gives you exactly what you need — but only if you **know what to ask for**. If you walk past it without knowing what you need, the door doesn't appear.

This is the fundamental problem with AI for newcomers: **you don't know what you don't know.** You can't ask for "team topologies" if you've never heard the term. You can't request "a RACI matrix" if you don't know it exists.

The techniques in this module are **keys to rooms you didn't know existed.** Each one is a way to make the model reveal territory beyond your current map.

---

## The Running Task

Throughout all 15 Parts, we'll work with the same deliberately vague task:

> **"I want to improve team communication."**

This is intentionally abstract. It could mean anything — Slack channels, meeting cadence, documentation, conflict resolution, feedback culture, async vs sync communication, tooling, rituals, team topologies...

Watch how each technique pulls a completely different response from the model — from the same starting point.

> **🌍 Localization Note for Trainers:** When presenting examples in chat, **localize all explanatory text and example responses** to the user's language. Only the **prompt templates** should stay in English (since models respond best to English prompts). The goal is that the user's understanding is built in their native language, while prompt crafting skills are practiced in English. If there's more English than the user's language in a chat message — you're doing it wrong.

---

## Step-by-Step Instructions

### Part 1: Role Assignment — "You Are an Expert In..."

**The Technique:**

Assign the model a specific professional role before asking your question. This shifts which knowledge corpus the model draws from.

**Why It Matters:**

Remember the Mirror metaphor — the model calibrates to your signal. When you say "You are an organizational psychologist," you're not role-playing. You're **pointing the mirror at a specific bookshelf** in the model's training data.

**The Exercise:**

Try this prompt in your AI chat:

```
You are an experienced organizational psychologist who specializes in team dynamics.
I want to improve team communication. What should I focus on?
```

Observe the response. Then try a different role:

```
You are a senior engineering manager at a FAANG company who has led distributed teams of 50+ engineers.
I want to improve team communication. What should I focus on?
```

**What to Notice:**

- The organizational psychologist will talk about psychological safety, feedback loops, conflict styles, group dynamics
- The engineering manager will talk about standups, async communication, documentation culture, PR reviews, incident retrospectives
- Same question. Different expert lens. Different universe of answers.

**The Key Insight:**

You don't need to BE an expert to get expert-level answers. You just need to know that the expert **exists** and name who should answer.

### Part 2: Audience Framing — "Explain as If I'm..."

**The Technique:**

Tell the model who you are — your background, expertise level, and context. This adjusts the depth, vocabulary, and assumptions in the response.

**Why It Matters:**

The Mirror works in both directions. Role assignment points it at the expert. Audience framing points it at **you** — telling the model how deep to go and what to assume you already know.

**The Exercise:**

Try this prompt:

```
I'm a non-technical project manager with 2 years of experience.
I want to improve team communication. Give me actionable advice.
```

Now try the same question with a different audience frame:

```
I'm a CTO of a 200-person engineering organization dealing with cross-team coordination problems.
I want to improve team communication. Give me actionable advice.
```

**What to Notice:**

- The PM gets: concrete rituals, meeting templates, stakeholder update formats, simple frameworks
- The CTO gets: organizational structure, team topologies, platform teams vs stream-aligned teams, RFC processes, architecture decision records
- The model isn't dumbing down or showing off — it's **calibrating depth to your stated context**

**The Key Insight:**

If you feel AI gives you "shallow" answers, it might be because you haven't told it who you are. State your context explicitly, and the depth follows.

**Bonus Insight — De Bono's Six Thinking Hats:**

Role Assignment and Audience Framing are essentially **Edward de Bono's Six Thinking Hats** applied to AI prompting. De Bono's core idea: you can't wear two hats at once. The Critic and the Dreamer interfere with each other. Same with prompts — if you ask the model to "brainstorm ideas AND critique them" in one prompt, the output gets muddled. Better to separate: first one role, then another.

Similarly, **Walt Disney's Creative Strategy** (Dreamer → Realist → Critic) works as a prompting workflow: first ask the model as a Dreamer ("give me wild ideas"), then as a Realist ("which of these are feasible?"), then as a Critic ("what could go wrong?"). Each pass through a different lens sharpens the result — just like switching hats in de Bono's framework.

The practical takeaway: **don't ask the model to be everything at once.** Assign one perspective per prompt, get the output, then switch hats and run another pass.

### Part 3: Chain of Thought — "Think Step by Step"

**The Technique:**

Ask the model to reason through the problem step by step instead of jumping to the answer. This forces structured, deeper analysis.

**Why It Matters:**

Without this instruction, the model tends to pattern-match to the most common answer. "Think step by step" forces it to actually decompose the problem — and decomposition often reveals aspects you hadn't considered.

**The Exercise:**

Try this prompt:

```
I want to improve team communication. Think step by step:
first diagnose what could be wrong, then suggest solutions for each diagnosis.
```

**What to Notice:**

- Instead of a flat list of tips, you get a structured analysis
- The model first identifies potential problems: information silos, unclear ownership, meeting overload, no async culture...
- Then maps solutions to each diagnosis
- This is closer to how a consultant would actually approach the problem

**The Key Insight:**

"Think step by step" is not just about getting a longer answer. It's about forcing the model to **show its reasoning** — and reasoning reveals structure that a quick answer hides.

### Part 4: Output Format Specification — "Answer as a Table / List / JSON"

**The Technique:**

Specify the exact format you want the response in. Tables, numbered lists, markdown, JSON, comparison matrices — the format shapes the content.

**Why It Matters:**

Format isn't cosmetic. A table forces the model to create comparable categories. A comparison matrix forces it to evaluate trade-offs. The format you request **restructures the thinking**.

**The Exercise:**

Try this prompt:

```
I want to improve team communication.
Give me a comparison table with columns:
| Problem | Symptom | Quick Fix | Deep Fix | Time to Impact |
```

**What to Notice:**

- The table format forces the model to think in structured categories
- "Quick Fix vs Deep Fix" creates a dimension the model wouldn't produce in a freeform answer
- "Time to Impact" adds a practical lens that's missing from generic advice
- You get a decision-making tool, not just a list

**The Key Insight:**

The format you request is a thinking tool. When you ask for a table, you're not just asking for pretty output — you're asking the model to organize knowledge along the axes **you** define.

### Part 5: Constraints and Scoping — "In 3 Sentences / Only About X"

**The Technique:**

Set explicit constraints: length limits, topic scope, or exclusion rules. Force the model to prioritize and compress.

**Why It Matters:**

Without constraints, the model gives you everything it can think of, weighted by frequency in training data. Constraints force it to **prioritize** — and priorities reveal what the model considers most important.

**The Exercise:**

Try this prompt:

```
I want to improve team communication.
Give me exactly 3 recommendations. For each one, explain in exactly 2 sentences: what to do and why it works.
No generic advice like "communicate more" — only specific, actionable changes.
```

**What to Notice:**

- Tight constraints force the model to pick its strongest recommendations
- "No generic advice" acts as a quality filter — pushes past surface-level answers
- The 2-sentence limit forces precision and eliminates fluff
- You get the model's **top 3**, not its exhaustive list

**The Key Insight:**

Constraints are not limitations — they're **sharpening tools**. The tighter the constraint, the more the model has to think about what actually matters.

### Part 6: Requesting Alternatives — "Give Me 3 Different Approaches"

**The Technique:**

Explicitly ask for multiple distinct approaches to the same problem. Force the model to explore different directions, not just variations of one.

**Why It Matters:**

By default, the model gives you one answer — the most probable one. But the most probable answer isn't always the best for your situation. Requesting alternatives **forces the model off the beaten path** into less obvious territory.

**The Exercise:**

Try this prompt:

```
I want to improve team communication.
Give me 3 fundamentally different approaches — not variations of the same idea.
For each approach, name the philosophy behind it.
```

**What to Notice:**

- You might get: a process-heavy approach (ceremonies, rituals), a tool-centric approach (async-first, documentation), and a culture approach (psychological safety, feedback norms)
- Each one comes from a different school of thought
- The "name the philosophy" instruction forces the model to be explicit about the underlying worldview
- This maps the solution space — you see **categories** of solutions, not just a list

**The Key Insight:**

One answer is a point. Three different answers show you the **landscape**. Requesting alternatives is how you discover approaches you didn't know existed.

### Part 7: Few-Shot Examples — "Here's What I Mean, Do More Like This"

**The Technique:**

Provide 1-2 examples of the output you want. The model matches the style, structure, depth, and tone of your examples.

**Why It Matters:**

Sometimes words can't describe what you want, but an example makes it instantly clear. Few-shot examples are the most reliable way to get the exact format, tone, and depth you need.

**The Exercise:**

Try this prompt:

```
I want to improve team communication. Give me recommendations in this format:

Example:
🔴 Problem: Decisions get lost in Slack threads and no one remembers what was agreed
💡 Fix: Create a #decisions channel. After any significant decision, post a one-liner summary with date, who decided, and link to context
⏱️ Time to see results: 1-2 weeks
📊 Effort: Low

Now give me 5 more recommendations in exactly this format.
```

**What to Notice:**

- The model precisely mirrors your format: emoji markers, categories, tone, length
- The example sets the bar for specificity — "create a #decisions channel" is concrete, so all recommendations will be concrete
- If your example were vague, all outputs would be vague too
- The example is your quality standard — the model aims to match it

**The Key Insight:**

One good example teaches the model more than a paragraph of instructions. Show, don't tell. The example **is** the spec.

**Bonus Insight — The Boilerplate Parallel:**

If you're a developer, you already use few-shot thinking every day. A boilerplate template says: "Here's the structure — fill it with your content." You don't explain to a new developer in words how a service should look — you hand them a boilerplate and say "follow the pattern."

Few-shot prompting works identically: your example is a boilerplate for the model. It sees the structure and replicates it with new content. And just like in code — the quality of the boilerplate determines the quality of everything built from it. A bad boilerplate breeds bad code. A good one sets the standard.

So the highest-ROI investment in few-shot prompting is **crafting one great example.** Spend 2 minutes on one perfect example, and you'll get 10 outputs at the same quality level.

### Part 8: Adversarial Critique — "Poke Holes in This"

**The Technique:**

Ask the model to critique, attack, or find weaknesses in a plan, idea, or its own previous answer. Adversarial mode activates a different reasoning pattern.

**Why It Matters:**

AI, like humans, has a confirmation bias in its default mode — it tends to agree and build upon what you say. Adversarial critique flips that. It forces the model to look for **what's missing, what could fail, and what you're not seeing**.

**The Exercise:**

First, get a plan:

```
I want to improve team communication by introducing daily standups, a shared Confluence wiki, and monthly retrospectives. This is my plan.
```

Then ask for critique:

```
Now act as a skeptical consultant who has seen this kind of initiative fail 100 times.
What are the 5 biggest risks and failure modes of my plan?
```

**What to Notice:**

- The model switches from supportive to critical
- You'll hear things like: "Standups become status reports that no one listens to," "Confluence becomes a graveyard of outdated pages," "Retrospectives without follow-through breed cynicism"
- These are real failure modes that the model wouldn't mention if you just asked "is this a good plan?"
- The adversarial frame **gave permission to be honest**

**The Key Insight:**

AI will agree with you by default. If you want honest analysis, you have to **explicitly request disagreement**. The adversarial frame is how you get the model to tell you what it would otherwise politely omit.

### Part 9: Asking What Was Omitted — "What Didn't You Tell Me?"

**The Technique:**

After getting a response, ask: "What did you leave out? What's important but wasn't mentioned?" This reveals the model's self-awareness of its own gaps.

**Why It Matters:**

Every response is a compression of everything the model knows. It picks what seems most relevant — but "most relevant" isn't always "most important." This technique surfaces the second layer of knowledge that didn't make the first cut.

**The Exercise:**

After any response about team communication, add:

```
What important aspects of team communication did you NOT mention in your answer?
What would an expert in this field say you missed?
```

**What to Notice:**

- The model will often surface genuinely different topics: power dynamics, remote vs co-located differences, cultural context, neurodiversity considerations, tooling fatigue
- These aren't just "more of the same" — they're often from a **different dimension** of the problem
- The model knew about them but filtered them out as "probably not what you wanted"
- You gave it permission to go wider

**The Key Insight:**

The model's first answer is its best guess at what you want. The omissions are often where the most interesting insights live. Asking "what didn't you say?" opens the door to the Room of Requirement you didn't know to ask for.

### Part 10: Meta-Learning — "What Do I Need to Know to Ask Better Questions?"

**The Technique:**

Instead of asking for answers, ask the model what knowledge or vocabulary you need to formulate better questions. This is the most powerful Room of Requirement key.

**Why It Matters:**

This directly attacks the "you don't know what you don't know" problem. You're asking the model to **draw you a map of the territory** before you decide where to go.

**The Exercise:**

Try this prompt:

```
I want to improve team communication, but I suspect I don't even know the right questions to ask.
What frameworks, concepts, and vocabulary should I learn about to think about this topic at a deeper level?
Don't give me solutions — give me a map of the knowledge landscape.
```

**What to Notice:**

- Instead of recommendations, you get: names of frameworks (Team Topologies, DORA metrics, Tuckman's stages), concepts (Conway's Law, cognitive load, information radiators), and vocabulary (async-first culture, decision logs, RACI matrix)
- Each of these terms is a **search key** — you can now ask about any of them specifically
- You went from "I want to improve communication" to having a map of 10+ specific areas to explore
- This one prompt potentially unlocked hours of productive conversation

**The Key Insight:**

This is the ultimate Room of Requirement key. You're not asking for the room — you're asking for the **map of all possible rooms**. Now you can walk to any door you want.

### Part 11: Reverse Prompting — "What Prompt Would Produce This Answer?"

**The Technique:**

Give the model an answer, outcome, or artifact you like — and ask it to generate the prompt that would have produced it. This teaches you how to write better prompts by working backwards.

**Why It Matters:**

It's often easier to recognize a good answer than to write the prompt that produces it. Reverse prompting lets you learn prompt engineering **from outputs you admire**.

**The Exercise:**

Try this prompt:

```
Here's a team communication improvement plan that I think is excellent:

"1. Replace daily standups with async check-ins in Slack using a bot that asks 3 questions at 9am.
2. Create an RFC (Request for Comments) process for any decision that affects more than one team.
3. Run bi-weekly 'friction logs' where each team member writes down their top 3 communication frustrations anonymously."

What prompt would I need to write to get an AI to produce a plan of this quality and specificity?
```

**What to Notice:**

- The model reverse-engineers the implicit requirements: the plan is specific, actionable, uses named tools, addresses both sync and async, includes a feedback mechanism
- It generates a prompt template you can reuse for other topics
- You learn what made the good answer good — and how to replicate it
- This is meta-learning about prompting itself

**The Key Insight:**

Reverse prompting turns good examples into reusable prompt templates. Instead of guessing what prompt works, you start from what you know is a good answer and work backwards.

### Part 12: Iterative Refinement — "Same Thing, But..."

**The Technique:**

Take a response and ask for a modified version: shorter, for a different audience, in a different tone, more specific, more practical. Each iteration sharpens the output.

**Why It Matters:**

Perfection rarely comes on the first try. But unlike the "arguing" anti-pattern from Module 050, iterative refinement has a clear direction: you're steering, not complaining.

**The Exercise:**

Start with any response you've gotten about team communication. Then:

```
That's good. Now give me the same recommendations but:
- Written as a 5-minute pitch to a skeptical VP
- Focus on ROI and measurable outcomes
- Remove anything that sounds like HR jargon
```

**What to Notice:**

- The core content stays, but the framing completely changes
- "Psychological safety" becomes "reducing the cost of failed experiments"
- "Feedback culture" becomes "faster defect detection through peer review"
- Same knowledge, different lens — the Mirror reflects the new audience

**The Key Insight:**

Iterative refinement is not arguing with the model. Arguing says "you're wrong." Refinement says "you're right, now transform it." One pollutes context. The other builds on it.

### Part 13: Socratic Questioning — "Guide Me, Don't Tell Me"

**The Technique:**

Ask the model to lead you through the thinking process with questions instead of giving direct answers. This builds your own understanding instead of just delivering information.

**Why It Matters:**

When the model gives you an answer, you consume it. When it asks you questions, you **think**. Socratic mode is the difference between reading a textbook and having a conversation with a mentor.

**The Exercise:**

Try this prompt:

```
I want to improve team communication.
Don't give me recommendations. Instead, ask me a series of diagnostic questions — one at a time — to help me figure out what's actually broken and what to fix.
```

**What to Notice:**

- The model becomes a coach, not an encyclopedia
- Questions force you to examine your own situation: "What communication is working well?", "Where do things break down?", "What happens when someone disagrees?"
- Your answers contain the real data — the model uses it to guide you to insights that are specific to YOUR team
- By the end, the recommendations come from YOUR context, not generic best practices

**The Key Insight:**

Socratic questioning is the deepest form of AI-assisted thinking. You're not outsourcing the thinking — you're using AI as a **thinking partner** that asks the questions you forgot to ask yourself.

### Part 14: Persona Stacking — Combining Techniques

**The Technique:**

Stack multiple techniques in a single prompt: role + audience + format + constraints. Each technique layer narrows the output and increases precision.

**Why It Matters:**

Individual techniques are powerful. Combined, they become surgical. Each layer removes noise from a different angle.

**The Exercise:**

Try stacking several techniques:

```
You are a senior VP of Engineering at Spotify who has managed the transition from project-based teams to the Spotify model (tribes, squads, chapters, guilds).

I'm a Head of Engineering at a 50-person startup where communication is starting to break down as we scale.

Think step by step:
1. Diagnose the most likely communication breakdowns at our scale
2. For each, give a specific fix that worked at Spotify
3. Format as a table: | Breakdown | Spotify Fix | How to Implement in 50-Person Org | Timeline |

Keep it to top 5 breakdowns only.
```

**What to Notice:**

- Role assignment (Spotify VP) pulls from organizational design expertise
- Audience framing (50-person startup) constrains solutions to your scale
- Chain of thought (step by step + diagnose first) ensures structured analysis
- Output format (table) forces comparable, decision-ready output
- Constraints (top 5 only) force prioritization
- The result is hyper-specific, actionable, and tailored — all from one prompt

**The Key Insight:**

Techniques compose. Think of them like camera lenses — each one changes what's in focus. Stacking them puts exactly what you need into sharp relief.

### Part 15: Building Your Go-To Starter Kit

**The Technique:**

Now that you've experienced all 15 techniques, choose 3-5 that resonate most with you and create a personal "first prompt" kit for any new chat session.

**Why It Matters:**

You won't remember all 15 in the moment. But if you have 3-5 go-to openers that are second nature, you'll consistently get better results than someone who opens every chat with "help me with X."

**The Exercise:**

Reflect on the techniques you've tried. Then create your personal starter prompt. Here's an example scaffold:

```
You are [role relevant to my task].
I am [your actual context — role, experience, constraints].
I want to [task].

Before answering:
- Think step by step
- Ask me clarifying questions if anything is ambiguous
- After your answer, tell me what you left out

Format: [your preferred output format]
```

Customize this to your style. Some people always want tables. Some always want the critic. Some always start with meta-learning. There's no wrong combination — the right one is the one you'll actually use.

**What to Notice:**

- The starter kit takes 30 seconds to write but fundamentally changes the quality of every interaction
- It becomes muscle memory — like a pre-flight checklist
- You can adjust it per task, but the skeleton stays the same

**The Key Insight:**

The goal isn't to use all 15 techniques every time. The goal is to **have them available** so you can reach for the right one when you need it. The Room of Requirement has many doors. You only need to open one at a time — but you need to know they exist.

---

## The Full Toolkit — Quick Reference

| # | Technique | One-liner | When to Use |
|---|---|---|---|
| 1 | Role Assignment | "You are an expert in..." | When you need a specific knowledge domain |
| 2 | Audience Framing | "I am a [role] with [context]..." | When answers feel too shallow or too technical |
| 3 | Chain of Thought | "Think step by step" | When you need structured reasoning, not just answers |
| 4 | Output Format | "Answer as a table / list / JSON" | When you need structured, comparable output |
| 5 | Constraints | "In 3 sentences / only about X" | When you want prioritized, focused answers |
| 6 | Requesting Alternatives | "Give me 3 different approaches" | When you want to see the solution landscape |
| 7 | Few-Shot Examples | "Here's an example, do more like this" | When words can't describe what you want |
| 8 | Adversarial Critique | "Poke holes in this / be a skeptic" | When you need honest risk assessment |
| 9 | Asking What Was Omitted | "What didn't you tell me?" | When you suspect there's more to the story |
| 10 | Meta-Learning | "What do I need to know to ask better?" | When you're in an unfamiliar domain |
| 11 | Reverse Prompting | "What prompt would produce this?" | When you have a good example and want to replicate it |
| 12 | Iterative Refinement | "Same thing, but for [new context]" | When you need to adapt output to new requirements |
| 13 | Socratic Questioning | "Guide me with questions, don't just tell" | When you want to think, not just consume |
| 14 | Persona Stacking | Combine role + audience + format + constraints | When you need surgical precision |
| 15 | Starter Kit | Your personal opening template | Every new chat session |

---

## Success Criteria

Congratulations! You've successfully completed this module if:

✅ You can explain the Mirror metaphor — how your words select which knowledge corpus the model draws from  
✅ You can explain the Room of Requirement metaphor — why you can't ask for what you don't know exists  
✅ You've tried at least 10 of the 15 techniques with the team communication task  
✅ You've observed how different techniques produce fundamentally different responses from the same starting point  
✅ You understand when to use Role Assignment vs Audience Framing  
✅ You can use Meta-Learning to map an unfamiliar knowledge domain  
✅ You've experienced how Adversarial Critique reveals risks that supportive mode hides  
✅ You know how to stack multiple techniques in one prompt (Persona Stacking)  
✅ You've created your personal Starter Kit — a go-to prompt template for new sessions  
✅ You understand that choosing the right technique is more important than knowing all of them

## Understanding Check

> **Note for trainers:** These questions test understanding of **when and why** to use techniques — not recall of their names. Each technique is referenced with a short metaphor so the user can recognize it without memorizing terminology.

1. **The Mirror:** Why does the same question give a shallow answer to one person and a deep, systems-level answer to another? What exactly controls this?
   - *Key point:* The words, framing, and vocabulary you use signal your expertise level. The model calibrates its response depth, assumptions, and vocabulary to match. Your words select which "bookshelf" the model pulls from.

2. **The Room of Requirement:** You want to explore a topic but you don't know the right terminology. You can't ask for what you don't know exists. What two things can you do — one BEFORE getting an answer, one AFTER?
   - *Hint:* Before = "Draw me a map of this territory" (Meta-Learning). After = "What did you NOT tell me?" (Asking What Was Omitted). Together they crack open unknown unknowns.

3. **Situations, not names:** Here are two situations. Which technique fits each?
   - **Situation A:** You have a ready plan and want to find out what could go wrong. → "Poke holes in this, be a skeptic" (Adversarial Critique)
   - **Situation B:** You don't have a plan. You're not even sure what the problem is. → "Don't give me answers — ask me questions to help me figure it out" (Socratic Questioning)
   - *Key point:* Critique validates what exists. Questions help discover from scratch.

4. **The compound lens:** What happens when you stack "You are [expert]" + "I am [my context]" + "Think step by step" + "Format as table" + "Top 5 only" in one prompt? Why is this more powerful than using them one at a time?
   - *Key point:* Each layer removes noise from a different angle — like stacking camera lenses. Role selects the knowledge domain, audience calibrates depth, chain-of-thought structures reasoning, format organizes output, constraints force prioritization. Together: surgical precision.

5. **Show, don't tell:** When is giving one example ("here's what I want, do more like this") more effective than writing a paragraph of instructions?
   - *Hint:* Think of it like a boilerplate in code — the template IS the spec.
   - *Key point:* When the desired output has a specific style, tone, structure, or level of specificity that's hard to put into words. One example sets the quality bar more reliably than a paragraph of description.

6. **Refactor, don't rewrite:** What's the difference between "No, that's wrong, try again" and "Good, now give me the same thing but for a different audience"? Why does one break things and the other improves them?
   - *Hint:* Think refactoring vs rewriting from scratch.
   - *Key point:* Arguing introduces negative examples, apologies, and confusion into context. Refinement builds on a good foundation and steers it. One adds noise, the other adds signal.

7. **The pre-flight checklist:** Why is a personal 3-5 technique starter template more practical than memorizing all 15 techniques?
   - *Key point:* You won't remember all 15 in the moment. A small, internalized kit becomes automatic — like a pre-flight checklist. You can always pull in more techniques when needed, but the kit ensures your baseline quality is consistently high.

## Troubleshooting

**Model ignores the role assignment and gives generic answers?**
- Make the role more specific: not just "expert" but "expert who has spent 15 years doing X at Y"
- Add concrete context: team size, industry, constraints
- Try stacking: add audience framing alongside role assignment

**Adversarial critique feels weak or surface-level?**
- Intensify the frame: "You've seen this exact plan fail 50 times. What goes wrong?"
- Ask for specific failure scenarios, not just "risks"
- Follow up: "What's the failure mode that's so obvious people overlook it?"

**Meta-learning returns obvious frameworks you already know?**
- Add your current knowledge: "I already know about X, Y, Z. What am I missing beyond those?"
- Ask for a specific level: "What would a PhD researcher in this field know that a practitioner wouldn't?"
- Request the "controversial" or "non-obvious" knowledge: "What do experts disagree about in this field?"

**Few-shot examples don't produce matching quality?**
- Your example might be too good — the model can't infer all the implicit quality criteria
- Add explicit instructions alongside the example: "Match this level of specificity and actionability"
- Provide 2-3 examples instead of one to establish a clearer pattern

**Socratic questioning feels aimless or circular?**
- Add direction: "Ask diagnostic questions focused on [specific area]"
- Set a goal: "Guide me to identify the root cause of [problem]"
- Limit scope: "Ask me 5 questions, then summarize what you've learned about my situation"

**Not sure which technique to use?**
- Start with Meta-Learning if you're in an unfamiliar domain
- Start with Role Assignment if you know the domain but want depth
- Start with Socratic Questioning if you don't know where to begin
- When in doubt, use your Starter Kit — it covers the basics

## Next Steps

Now that you have a prompt engineering toolkit, you're ready to learn about agent memory management — how to give AI persistent context across long, complex tasks using todo lists and structured notes!
