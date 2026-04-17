# GenAI Coaching: Key Session Topics

> A concise summary of GenAI coaching sessions on working with GitHub Copilot and large language models.

---

## 1. How Language Models Generate Text

The model doesn't "think" — it **predicts the next word** based on all the text it sees. Like T9 on your phone, but instead of looking at the previous 5 words, it sees 200,000 words simultaneously and senses all the connections between them.

**Why it matters:** Understanding the mechanism removes the magic and lets you consciously steer the result.

## 2. Context Window — The "Wall of Newspapers"

Imagine a huge screen covered in newspapers. The model reads every article in a single glance, sees the connections between them, and generates a coherent response. That's the context window — all the text the model sees at once.

**Why it matters:** Everything you write, every model response, every tool call — it all accumulates in one context and influences every next word.

## 3. The Model Has No Memory — It's "Dory the Fish"

Close the session — the model forgets everything. New chat = blank slate. The only "memory" is the project files and instructions you've prepared in advance.

**Why it matters:** To preserve knowledge between sessions, you need to **actively extract** useful results into instruction files. That's how you create "long-term memory" for the model.

## 4. Don't Argue — Edit Your Prompt

If the model gives the wrong result — **don't go further down**, don't argue. Go back to the original prompt, add the missing facts, refine the wording. Every argument pollutes the context with false statements, making the model hallucinate more.

**Why it matters:** Clean context = accurate answer. Polluted context = a mess of conflicting requirements.

## 5. Temperature and Non-Determinism

Models have built-in "temperature" — a randomness element when choosing the next word. That's why responses to the same prompt differ in form while staying similar in meaning.

**Why it matters:** You can't expect 100% reproducibility. But you can **narrow the range** of answers by adding specific statements to the prompt until the result becomes stable.

## 6. Instructions — Your "Knowledge Transfer"

A new session is a junior who knows nothing about your project. An instruction is a knowledge transfer for that junior. After 10–20 iterations of corrections, the instruction accumulates corner cases and becomes a senior-level agent.

**Why it matters:** Instructions = scalable experience. Describe it once, delegate forever.

## 7. Instruction → Skill → Agent

- **Instruction** — a text description of "how to do one exercise"
- **Skill** — instruction + code (e.g., a Python calculator for precise computations)
- **Agent** — a set of instructions linked by a process: "take from here, process with this, put it there"

**Why it matters:** Separation into levels lets you mix and match instructions and build complex automations.

## 8. Under the Hood: System Prompt, Tools, Agent Mode

Before your very first word, the model already sees: descriptions of 50+ tools, a system prompt with behavioral rules, the project structure, and user instructions. Your question is just a small part of the entire context.

**Why it matters:** Understanding what happens "behind the scenes" removes the sense of magic and gives you control over the model's behavior.

## 9. Prompt Engineering: Going Beyond Your Own Knowledge

If you don't know the right term — ask the model for 10 key terms on the topic. This "unlocks" the relevant section of its knowledge "library." Then you work within an enriched context.

**Why it matters:** You don't have to know everything. The model is a library without a catalog. Your job is to guide it to the right "shelf."

## 10. Iterative Improvement Through Hallucinations

A hallucination isn't a failure — it's a signal. Spot an error — tell the model: "fix the instruction so this doesn't happen again." Every corner case makes the instruction more reliable.

**Why it matters:** Hallucinations are feedback. Use them to evolve instructions, not as a reason to abandon the tool.

