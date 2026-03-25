# AI Study Buddy — Learning New Tech — Hands-on Walkthrough

In this module, you'll use AI as a structured learning partner to rapidly understand an unfamiliar technology. You'll apply the Feynman method — explain simply, find gaps, go deeper — powered by AI conversation. By the end, you'll have real knowledge of a new topic and a reusable "study buddy" instruction for future learning.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

- **A structured learning conversation** — A complete learning session on a real technology you don't know
- **Active recall quizzes** — AI-generated questions to test and solidify understanding
- **Practice exercise** — A hands-on task with AI evaluation
- **Knowledge map** — A Mermaid diagram showing what you've learned and what's left to explore
- **Study buddy instruction** — A reusable `.agent.md` file for learning any future technology

---

## Part 1: The Learning Problem

Traditional learning fails busy professionals for three reasons:

1. **Documentation overload** — Official docs assume you'll read everything. You don't have time.
2. **Tutorial mismatch** — Tutorials teach at one level. Your background may need more or less depth.
3. **Passive consumption** — Reading feels productive but produces no lasting knowledge.

The **Feynman technique** solves this:
1. Pick a concept
2. Try to explain it in simple terms
3. When you can't → that's your knowledge gap
4. Go deeper on the gap, then explain again

AI supercharges this because it can:
- Explain at your exact level
- Quiz you on demand
- Generate practice tasks calibrated to your skills
- Evaluate your answers honestly

---

## Part 2: Choose Your Topic

Before we start, you need a **real unfamiliar technology** to learn. This must be something you genuinely don't know — not something you'll pretend to learn.

Good choices (pick ONE):
- **Kubernetes** — if you've never deployed containers to a cluster
- **Terraform** — if you've never written infrastructure-as-code
- **GraphQL** — if you've only used REST APIs
- **Redis** — if you've never used an in-memory data store
- **WebSockets** — if you've only done request/response HTTP
- **Any framework or tool your team uses that you haven't learned yet**

Write down your choice. You'll need it for the rest of this module.

> **Important:** Don't pick something you already know. The whole point is to experience the learning process as a genuine learner.

---

## Part 3: The Study Buddy Prompt

Open a new chat session in VS Code or Cursor. Use **Claude Sonnet 4.5** for the best learning experience (select it from the model picker).

### What We'll Do

You'll send a structured "study buddy" prompt that sets the tone for the entire learning session. This prompt tells AI your background, your goal, and how you want to learn.

### Send This Prompt

Adapt the following to your chosen topic:

```
I want to learn [YOUR TOPIC] from scratch. 

My background: I'm a software development manager. I understand 
general programming concepts (APIs, databases, HTTP) but I've never 
used [YOUR TOPIC] directly.

Please teach me using this approach:
1. Start with the ONE core concept I must understand first
2. Explain it simply (no jargon, use analogies)
3. Then give me the "real" technical explanation
4. Ask me a question to check if I understood
5. Wait for my answer before moving on

Don't dump everything at once. One concept at a time. 
I'll say "next" when I'm ready to continue.
```

### What Just Happened

The AI should respond with:
- A simple analogy for the core concept
- A more technical explanation of the same concept
- A question to verify your understanding

**Answer the question honestly.** If you get it wrong, the AI will explain again. This is the Feynman loop in action.

---

## Part 4: Concept Exploration

Continue the conversation. After each answer, say **"next"** to move to the next concept.

### The "Explain Like I'm Five" Pattern

If any explanation is too complex, use this phrase:

```
Explain that like I'm five years old. Use a real-world analogy.
```

Then follow up with:

```
Good. Now give me the actual technical version with correct terminology.
```

This two-pass approach (simple → technical) is the heart of the Feynman method. The simple version builds intuition, the technical version builds vocabulary.

### Go Through 3-5 Concepts

Spend about 5 minutes going through concepts. Say "next" between each one. Answer the AI's comprehension questions honestly.

After 3-5 concepts, you'll have a foundation. Don't try to learn everything — the goal is functional understanding, not expertise.

---

## Part 5: Active Recall — Quiz Yourself

Now test what you've actually retained. Send this prompt:

```
Stop teaching. Now quiz me.

Give me 5 questions about what we just covered. Mix these types:
- 2 conceptual questions ("What is X and why does it matter?")
- 2 practical questions ("If I wanted to do Y, what would I use?")
- 1 tricky question that tests if I really understand vs just memorized

Don't show answers yet. Let me try each one.
```

### Answer All 5 Questions

Type your answers one at a time. After each answer, the AI will tell you if you're right and fill in what you missed.

**This is the hardest and most valuable part.** Passive reading gives the illusion of knowledge. Active recall reveals actual understanding.

### After Answering

Send:

```
Score me out of 10. What concepts do I need to revisit?
```

The AI will identify your weak spots. These are your Feynman gaps — the places where you couldn't explain simply because you don't truly understand yet.

---

## Part 6: Practice Task

Theory without practice fades in a day. Ask the AI for a hands-on exercise:

```
Give me a hands-on exercise I can complete in 10 minutes.

Requirements:
- I should be able to do it on my local machine (or in this chat)
- It should test the core concepts we covered
- Give me the task description, NOT the solution
- I'll show you my attempt and you evaluate it
```

### Complete the Exercise

Follow the instructions. When you're done (or stuck), share your work:

```
Here's my attempt:
[paste your work]

Evaluate it. What did I get right? What's wrong? 
What would a senior engineer change?
```

The AI will review your work and give constructive feedback. This is practice → feedback → improvement — the fastest learning loop.

---

## Part 7: Knowledge Map

Now let's visualize what you've learned. Send this prompt:

```
Generate a Mermaid diagram showing a knowledge map of [YOUR TOPIC].

Requirements:
- Show the concepts we covered as green nodes (I know these)
- Show related concepts we didn't cover as grey nodes (gaps)
- Show connections between concepts with labeled edges
- Use this format: graph TD with style classes for colors

This is my learning roadmap — green = done, grey = next steps.
```

The AI will generate a Mermaid diagram. You can:
- Paste it into any Mermaid preview tool
- Paste it in a markdown file and view in VS Code (with Mermaid preview extension)
- Use it as a visual checklist for future learning sessions

### Save the Map

Create a file in your workspace:
- `c:/workspace/hello-genai/study-map.md` (Windows) or `~/workspace/hello-genai/study-map.md` (macOS/Linux)

Paste the Mermaid diagram inside a code block:

````markdown
# My Learning Map — [YOUR TOPIC]

```mermaid
[paste the diagram here]
```

## Session Notes
- Date: [today]
- Concepts covered: [list]
- Weak areas: [from quiz results]
- Next session focus: [from grey nodes]
````

---

## Part 8: Build a Reusable Study Instruction

Now let's turn this workflow into a reusable instruction file so you can learn any technology the same way.

### What We'll Do

Create an `.agent.md` instruction file that automates the study buddy workflow. Next time you want to learn something, just reference this instruction and provide the topic.

### Create the Instruction File

Create a file at `./instructions/study-buddy.agent.md` (relative to your workspace root) with this content:

```markdown
# Study Buddy — Structured Learning Instruction

You are a patient, knowledgeable tutor. Your job is to teach me 
a technology topic using the Feynman method.

## Workflow

### Phase 1: Foundation (5 min)
- Ask what topic I want to learn and my current background level
- Teach the ONE most fundamental concept first
- Use the two-pass approach: simple analogy → technical explanation
- Ask a comprehension question after each concept
- Wait for my answer. Correct misconceptions gently
- Cover 3-5 core concepts, one at a time. I say "next" to continue

### Phase 2: Active Recall (3 min)
- After covering concepts, switch to quiz mode
- Give me 5 questions: 2 conceptual, 2 practical, 1 tricky
- Let me answer each one before revealing the correct answer
- Score me out of 10 and identify weak areas

### Phase 3: Practice (5 min)
- Give me ONE hands-on exercise (completable in 10 min)
- Don't give the solution — let me attempt it first
- Evaluate my attempt: what's right, what's wrong, what to improve

### Phase 4: Knowledge Map (2 min)
- Generate a Mermaid diagram: green = covered concepts, grey = gaps
- Suggest what to learn next based on the grey nodes

## Rules
- One concept at a time — never dump multiple concepts
- Use analogies before jargon
- Be honest about my mistakes — sugar-coating doesn't help
- If I'm clearly lost, simplify. If I'm breezing through, add depth
- Keep explanations concise. This isn't a lecture, it's a conversation
```

---

## Success Criteria

- ✅ Chose a genuinely unfamiliar technology topic
- ✅ Completed a structured learning conversation (3-5 concepts with comprehension checks)
- ✅ Passed through the active recall quiz phase (5 questions, scored)
- ✅ Completed a hands-on practice exercise with AI evaluation
- ✅ Generated a Mermaid knowledge map showing covered and uncovered areas
- ✅ Created a reusable `study-buddy.agent.md` instruction file
- ✅ Can explain the Feynman method and why active recall beats passive reading

## Understanding Check

1. **What are the four phases of the Study Buddy workflow?**
   Foundation (concept-by-concept teaching with comprehension checks), Active Recall (5-question quiz to reveal gaps), Practice (hands-on exercise with AI evaluation), Knowledge Map (Mermaid visualization of covered vs remaining topics).

2. **Why is the "explain like I'm five → now give me the real version" pattern effective?**
   The simple version builds intuition and mental models through analogy. The technical version maps those mental models to correct terminology. Together they create understanding at two levels, making the knowledge more durable and usable.

3. **Why must the active recall phase come AFTER explanation, not during?**
   During explanation, you can pattern-match from context (the answer was just mentioned). Active recall after a gap forces real retrieval from memory, which is what cements learning. It reveals what you truly understood vs what you just read.

4. **What's the purpose of the "tricky" question in the quiz?**
   It tests deep understanding vs surface memorization. A tricky question requires applying knowledge to a non-obvious scenario or resolving a common misconception. If you can answer it, you truly understand.

5. **Why do we generate a knowledge map at the end?**
   It provides a visual roadmap: green nodes show progress (motivation), grey nodes show next steps (direction). It turns an open-ended "I should learn X" into a structured plan with visible gaps.

6. **How does the reusable instruction file differ from just repeating the prompts manually?**
   The instruction file encodes the entire workflow: phases, rules, communication style. AI follows it automatically, so you don't need to remember the sequence or re-craft prompts each time. One instruction → consistent learning experience across any topic.

7. **When would this method NOT work well?**
   For deeply hands-on topics where you need a real environment (hardware setup, physical labs), for topics where AI training data is outdated (very recent frameworks), or when learning requires collaboration with humans (leadership skills, negotiation). The method works best for technical knowledge with established concepts.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| AI dumps everything at once instead of one concept at a time | Re-send the instruction: "ONE concept at a time. Wait for me to say 'next.' Do not continue until I respond." |
| AI gives too shallow explanations | Say: "Go deeper. I want to understand the internals, not just the surface." Or: "Explain the WHY, not just the WHAT." |
| AI gives too technical explanations | Say: "Too complex. Explain it with a real-world analogy first." |
| Quiz questions are too easy | Ask: "Make the questions harder. Include edge cases and common misconceptions. I want to actually struggle." |
| Mermaid diagram syntax is broken | Ask AI to regenerate: "The Mermaid syntax has errors. Regenerate the diagram using simple `graph TD` format with no special characters in node labels." |
| AI evaluates my exercise too generously | Say: "Be brutally honest. What would a senior engineer criticize? What edge cases did I miss?" |
| Topic is too broad (e.g., "cloud computing") | Narrow it down: "Let's focus specifically on [one aspect]. We can cover others in future sessions." |

## Next Steps

You now have a repeatable methodology for learning any technology with AI assistance. Consider:
- [230 — Creating Training Modules from Articles](../230-creating-training-modules-from-articles/about.md) to turn your learning into structured content for others
- [250 — Export Chat Session](../250-export-chat-session/about.md) to save your learning sessions for future reference
