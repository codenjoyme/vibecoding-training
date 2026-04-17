# How Your IDE's AI Assistant Actually Works: A Coaching Session Breakdown

> A detailed breakdown of two GenAI coaching sessions on practical use of GitHub Copilot and language models. What happens under the hood, why models "hallucinate," and how to turn one from a junior into a reliable assistant.

---

## Introduction

Two individual coaching sessions on generative AI took place. The format: live demonstrations in VS Code with GitHub Copilot, real case analysis, and looking "under the hood" of agent mode. The participants were specialists with initial experience using ChatGPT and Copilot who wanted to build a systematic understanding.

This article isn't a transcript — it's a structured distillation of key insights with examples and practical recommendations.

---

## Part 1: How Models Generate Text — And Why Understanding This Matters

### Token by Token

A language model is neither a search engine nor a database. It **generates text one word** (token) at a time, re-evaluating the entire previous context each time.

Simple analogy: T9 on your phone. You type "the sun shines on" — and the phone suggests the next word. If you just keep tapping suggestions, you get nonsense, because T9 only sees the previous 2–3 words.

Large language models do the same thing, but instead of 3 words, they see **200,000 words simultaneously**. Imagine walking into a huge hall with walls covered in newspapers. In a single glance, you read every article, see the connections between them, and understand the chronology and context. That's how the model "thinks."

### The Context Window

The context window is the total volume of text the model sees at once. For current models, that's 200,000 tokens (roughly words). Everything in your chat — your questions, model responses, tool call results, loaded files — all sits in one context.

Every new word is generated taking into account this entire "canvas." The model sees all the text, senses all connections, and generates the next token to be maximally coherent with everything before it.

> **Practical takeaway:** Everything you type in the chat becomes part of the "problem statement." If you wrote something extraneous or false — that also affects the result.

### Temperature: Why Answers Are Always Different

Model developers deliberately added a "temperature" parameter. At zero temperature, the model would choose the most probable word — and the answer would be (nearly) identical every time. But temperature introduces randomness: from the range of most probable words, one is chosen at random.

This is intentional — so that:
- You can extract different information from different runs
- The model isn't "locked" into a single response pattern
- You can get creative solutions

> **Practical takeaway:** Three people — a junior, a senior, and an architect — will ask the same question using different words. The model senses each person's level and responds accordingly. For the junior — a simple solution; for the architect — a systemic one. That's why instructions matter: they standardize the "level" of communication.

---

## Part 2: Why You Should Never Argue With the Model

### Context as Your Specification

Each message in the chat isn't a separate question. It's a **continuation of one large specification**. When you write your third message, the model sees:

1. Your first question
2. Its first answer
3. Your clarification
4. Its second answer
5. Your third message

And generates the next response based on all of this text.

### The Problem of "Polluted Context"

Imagine giving a task to a developer like this: "We need a web application... no, not web. Mobile... actually no. Don't write it in C#. And not C++ either. We'll write it in..." — by this point, the developer is confused. They see a pile of negations and contradictions.

The same thing happens with the model when you argue:

```
You: Write a sort function
Model: [writes in Python]
You: No, in JavaScript
Model: [writes JavaScript with usage examples]
You: Without examples
Model: [writes quicksort]
You: Not quicksort, bubble sort
Model: [writes it, but with comments]
You: Without comments
```

Now the context is a **mess** of Python, JavaScript, quicksort, bubblesort, with and without examples. The model sees all of this simultaneously and tries to generate an answer from this chaos.

### The Right Approach: Edit the Prompt

Instead of going further down and arguing — **go back to the original message and edit it**. In VS Code and ChatGPT, you can click on your message and hit "Edit." Everything below gets cut. The context stays clean.

Iteratively, you assemble one precise prompt:

```
Write a bubble sort function in JavaScript.
Name it bubbleSort.
No usage examples.
No comments.
Clean code.
In a markdown code block with a language tag.
```

This prompt can be run multiple times — and the result will be stable 99% of the time.

> **Practical takeaway:** Don't go further down until you've gotten what you need at the current level. One well-crafted prompt is better than ten iterations of arguing.

---

## Part 3: The Model's Memory — Or Lack Thereof

### Short-Term vs. Long-Term Memory

Humans have short-term memory (limited — 5–7 items) and long-term memory (formed during sleep, through consolidation).

For the model:
- **Short-term memory** = the context window. Huge (200K words) but temporary — only lasts for the session.
- **There is no long-term memory.** The model doesn't "go to sleep." Its short-term experience doesn't convert to long-term.

When you close the chat and open a new one — the model remembers absolutely nothing. It's like Dory the fish: every time — "Hi! Who are you? What are we talking about?"

### How to Create "Long-Term Memory"

The only way is to **actively extract** useful results from the session into files:

1. You worked in the chat, got a good result
2. You say: "Extract an instruction from this session describing how we did this"
3. The model creates a file with key rules and approaches
4. In the next chat, you provide this instruction — and the model "remembers" your experience

It's like taking meeting notes. Don't write them down — you'll forget.

> **Practical takeaway:** Before closing a chat — ask yourself: "Is there something here worth saving?" If yes — tell the model to create an instruction.

### What Happens in ChatGPT, Which "Has Memory"

ChatGPT creates a summary of each session and stores it separately. When you start a new chat, the agent has a tool to "check summaries of previous sessions." That's why it "remembers" your job and food preferences.

IDE-based tools (VS Code + Copilot) don't have this mechanism. Here, you manage memory yourself — through instruction files.

---

## Part 4: What Happens Under the Hood

### The System Prompt

Before your very first word, the model already sees a massive amount of text:

1. **Descriptions of 150+ tools** — how to create files, search, edit, run terminal commands. Each tool is described: name, parameters, call format.

2. **System prompt** — behavioral rules: "You are GitHub Copilot, using Claude Sonnet 4.6, following Microsoft content policies, not generating harmful content..."

3. **User instructions** — the `.github/copilot-instructions.md` file and its links to other instructions.

4. **Project context** — OS, open folder, file structure, last terminal command.

5. **And only then — your request.**

During the demonstration, a simple question "What is this project about?" used **7% of the context window** (about 14,000 words). The user request was 3 words. Everything else was infrastructure.

### How Agent Mode Works

The model itself **only prints text**. It cannot open a file, run a command, or browse the internet.

But its context describes tools. And when the model decides it needs to read a file — it doesn't read it. It **prints**: "I want to call the read_file tool with parameter path=..."

At this moment, **agent mode** (part of the Copilot plugin):
1. Notices the model "wants" to call a tool
2. Stops generation
3. Executes the actual tool call
4. Inserts the result back into the context
5. Returns control to the model

The model sees the result and continues generating **as if it did it itself**. In reality — the agent did it for the model.

It's a cycle of four participants: **You → Model → Agent → Tools**. The model is the brain, the agent is the hands, the tools are the real actions.

> **Practical takeaway:** Every time you see "Reading file..." or "Running command..." — the model printed an intention, and the agent executed it. Understanding this mechanism removes the sense of magic.

---

## Part 5: Instructions, Skills, Agents

### Instruction — One "Exercise"

An instruction is a text file (usually markdown) describing how to perform one specific operation. For example:
- How to compare two CSV files and find discrepancies
- How to write test cases in a specific format
- How to respond in a particular style

Instructions are written in human language — because the model was trained on human languages. A good instruction for a new employee = a good instruction for the model.

### Skill — Instruction + Code

Sometimes text directions aren't enough. For example, the model **is bad at math** — it's not a calculator, it "dreams" about mathematics. Solution: write a Python script for calculations and an instruction describing how to run it.

During the session, a calculator skill was created:
- `calculator.py` — a Python script for precise calculations
- `SKILL.md` — instruction: "When you need to calculate — never calculate yourself, always run this script in the terminal"

After this, for any computation the model runs the script and returns an **exact** result, not a hallucination.

### Agent — A Process of Multiple Instructions

An agent is when several instructions are linked into a process: "Get data from here (instruction 1), process it this way (instruction 2), put the result there (instruction 3)."

Technically under the hood — it's still just text in the context. The model simply sees the description of the entire process and executes it step by step.

> **Practical takeaway:** Separate different aspects of work into different instructions (single responsibility principle). This allows you to combine and reuse them.

---

## Part 6: Iterative Instruction Improvement

### Hallucination = Feedback

The model hallucinated and did the wrong thing? That's not a bug — it's a **corner case** your instruction didn't cover. Actions:

1. Don't argue: "You did it wrong!"
2. Say: "You did X, but it should have been Y. Fix the instruction so this doesn't happen in the future."
3. The model updates the instruction, adding the new case.
4. You open a new session with the updated instruction and verify.

### Instruction Evolution

- **After 1 session:** primitive, 100 lines, covers the basic case
- **After 5 sessions:** 200 lines, handles main corner cases
- **After 15–20 sessions:** 400–500 lines, a "senior" instruction, minimal hallucinations

Recommendation: no more than 700 lines per instruction. If it's longer — time to split.

### Example With a Real Task

A real case from the session: a specialist needed to compare profession lists from different markets against a superset, find discrepancies, and generate a table for the WordPress team.

Instruction creation process:
1. First attempt — model didn't account for column order
2. Added statement about column order → model didn't add placeholder
3. Added statement about placeholder → works
4. After 5 uses, the instruction covers all edge cases

Now for each new market: copy data from Confluence → feed it to the instruction → get a ready table.

---

## Part 7: Prompt Engineering — Going Beyond Your Own Knowledge

### The "Don't Know What I Don't Know" Problem

If you don't know the term "obfuscation," you'll never ask: "How do I obfuscate JavaScript code?" You'll ask: "How do I protect code from being copied in the browser?" — and the model may give a far-from-ideal answer.

### Technique: Terminology Reconnaissance

1. Name the domain: "Oil industry, stocks"
2. Ask: "Give me 10 key terms from this area"
3. The model responds: derivatives, hedging, futures, spot price...
4. Now this set of terms is part of your context
5. Subsequent questions will build on this enriched context

It's like going to a library and asking for the catalog of the relevant section before searching for a specific book.

### Technique: Context Switching

If the model refuses to answer ("I'm not a financial advisor"), you can reframe: "We're building an application that uses these terms. Answer in user story format."

The model is a tool. Like a hammer: you can drive nails, or you can do something else. It's about how you frame the task.

---

## Part 8: MCP and Connecting External Services

The sessions briefly touched on **MCP (Model Context Protocol)** — a way to connect external tools to the IDE agent:
- Access to Jira for creating tickets
- Access to Confluence for reading documentation
- Services for generating presentations
- Any API via MCP connectors

Important warning: through MCP, **your data goes to** the server of whoever created the connector. You need to understand how safe a specific MCP tool is.

> **Practical takeaway:** MCP extends agent capabilities beyond the IDE. But it requires a conscious approach to data security.

---

## Part 9: Practical Recommendations

### For Beginners

1. **Choose Claude Sonnet 4.6** in agent mode and don't switch
2. **Don't argue — edit** the original prompt
3. **Before closing a session** — extract useful things into an instruction
4. **Start with one instruction** for your everyday task

### For Practitioners

5. **Separate instructions** by single responsibility — one task = one file
6. **Use hallucinations** as feedback for improving instructions
7. **Create an instruction catalog** (main.agent.md) — so the model knows where to look
8. **Test instructions** in new sessions after every change

### For Advanced Users

9. **Create skills** for tasks requiring precision (calculations, formatting)
10. **Build agents** — chains of instructions describing a process
11. **Connect MCP** for access to external systems (with security in mind)
12. **Study the debug view** — see what the model sees under the hood

---

## Part 10: Version Control — Git as a Safety Net for AI

### Why Git Is Critical When Working With AI

An AI assistant is a wonderful code generator, but it has an unpleasant habit: it "improves" working code and breaks it. You asked for validation — and it also rewrote the sorting. Without Git, you lose 15–30 minutes of work. With Git — you roll back in a second.

### The Baby Steps Methodology

The idea is simple: take small steps and checkpoint each one.

1. Made one change — ran it, verified, works
2. `git add .` — saved checkpoint
3. Next change — verified — checkpointed
4. AI broke something? `git checkout .` — back to last checkpoint

One commit = one thought you can explain in one sentence. If you need two sentences — that's two commits.

### The Time Paradox

Three features via baby steps: 3 × 15 minutes = 45 minutes.
Three features simultaneously: 2–3 hours.

Why? Because the brain holds 7±2 items in working memory. When you're "juggling" three features, each new thought pushes out the previous one. You spend time not on code, but on context-switching between tasks.

Baby steps solve this: each 15-minute session is one task. All complexity fits in one commit.

> **Practical takeaway:** Git isn't a tool for developers. It's a tool for everyone working with AI. If AI can break your result — you need Git.

---

## Part 11: Team-Level Skills Management

### The Instruction Scaling Problem

You created 10 instructions. Then 30. Then 50. They're scattered across different projects in different formats. A colleague asks: "Where's the code review instruction?" — and you can't find it.

Even worse: you fixed a bug in an instruction in one project, but three others still have the old version. Result: three teams working by different rules.

### The Central Skills Repository

The solution — a Git repository where all instructions are stored centrally:

- **`.manifest/`** — like a restaurant menu. Global skills are "water" — available to everyone. Team skills are in sections. Team Alpha gets `style-guidelines`, Team Beta gets `test-writing`.
- **Sparse checkout** — each project pulls only its skills. Team Beta doesn't see Team Alpha's files — they don't clutter the workspace.
- **`skills` CLI** — a management utility: `skills init --groups project-alpha` pulls the right skills, `skills pull` updates, `skills push` sends changes for review.

### Governance: One Fixes, Everyone Gets

The workflow mirrors code: branch → PR → review → merge. One person updates a skill, opens a PR, the owner reviews and merges — and on the next `skills pull`, all teams get the update.

> **Practical takeaway:** If more than 5 people use AI instructions in your organization — you need a centralized skills repository. Otherwise, you get 50 different versions of "best practices."

---

## Part 12: AI Skills & Tools — When Text Isn't Enough

### The Experiment: Ask AI to Calculate

Ask the model: "Calculate compound interest for $15,847 at 7.34%, monthly compounding, 8 years 7 months." The model will produce a number — confidently, with the formula, with an explanation. Check it on a calculator — and you'll see the answer is **wrong**.

Why? Because the model doesn't calculate. It **generates text** that "looks like a correct answer." It's seen thousands of examples of financial calculations in training data and generates a "typical answer" — but with different numbers.

### The Formula: Instruction + Tool = Skill

Instead of asking AI to calculate — ask it to **create a calculator**:

1. "Write a Python script `compound_interest.py` with parameters: principal, rate, compounds_per_year, years"
2. The script uses `math` — real mathematics, not text generation
3. Instruction (SKILL.md): "When you need compound interest — **never calculate yourself**. Run the script in the terminal."

Now AI runs the script for any calculation and returns an **exact** result. The parameterized tool works with any input without modification.

### When You Need a Skill vs. Just an Instruction

- **Instruction** — for text tasks: response style, documentation format, test case template
- **Skill (instruction + code)** — for tasks requiring precision: calculations, data validation, formatting, conversion

> **Practical takeaway:** Don't ask AI to do — ask AI to **create a tool that does**. Build the calculator once — and it works forever, hallucination-free.

---

## Part 13: MCP — "USB for AI"

### The Problem: AI Is Trapped in the IDE

The model only sees what's in the context: project files, search results, terminal output. It can't go to Jira, read Confluence, query a database, or create a GitHub ticket.

### How MCP Solves This

MCP (Model Context Protocol) is an open standard from Anthropic. The analogy: before USB, every printer, scanner, and camera needed its own driver. USB standardized the connection. MCP does the same for AI:

- **GitHub MCP** — the agent creates repositories, issues, PRs through chat
- **Filesystem MCP** — the agent works with files outside the project
- **Database MCP** — the agent makes SQL queries through natural language
- **Jira, Confluence, Slack** — and 250+ more ready-made servers

Setup is simple: a JSON file with the MCP server address and authentication token. After that, the AI agent automatically "discovers" new tools and starts using them.

### Security

Every tool call goes through a confirmation dialog — you see which tool is being called with what data. You can expand details to see the raw JSON-RPC communication.

But remember: through MCP, data flows to the server of whoever created the connector. If you connected an MCP server from an unknown developer — **your data passes through their infrastructure**.

> **Practical takeaway:** MCP removes the wall between AI and your work systems. But every connection is a conscious decision about trusting the provider.

---

## Part 14: CLI — Direct Access Without Hallucinations

### The MCP Problem: AI in the Chain

When a tool returns a result through MCP, that result passes through the model. The model "regenerates" it — and can distort it. The server returned "42 × 17 = 714," but the model writes "Answer: 741." It didn't copy — it generated new text "similar to" the answer.

For creative tasks, this isn't a problem. For financial calculations, ETL pipelines, infrastructure scripts — it's a disaster.

### CLI: curl Directly to the Server

CLI (Command Line Interface) means calling REST APIs through the terminal using `curl`:

```bash
curl http://localhost:8080/calculate?expression=42*17
```

Server returned "714" — you get "714." No AI in the chain. No regeneration. No hallucination risk.

### When to Use What

| | MCP | CLI |
|---|---|---|
| **AI in chain** | Yes — reasons, chooses tools | No — direct call |
| **Tokens** | Spent on schema + reasoning | Zero |
| **Hallucinations** | Possible during regeneration | Impossible |
| **Binary files** | Base64 via JSON (+33% size) | `curl -F "file=@image.png"` directly |
| **Best for** | Exploration, decision-making | Automation, precise operations |

> **Practical takeaway:** Critical operations — through CLI. Exploratory — through MCP. Like manual vs. autopilot in a plane: autopilot is convenient, but you want manual control for landing in a storm.

---

## Part 15: GitHub MCP — Tasks Through AI Chat

### Traditional Workflow vs. MCP

**Without MCP:** Open browser → GitHub → create repo → copy URL → back to IDE → terminal → `git remote add` → open browser → create issue → type description → refresh page.

**With MCP:** "Create a repo and an issue" → confirm tool calls → done. All context-switching disappears.

### The "Agent Delegation" Pattern

The most powerful pattern from this module:

1. An AI session conducts a **requirements interview**: asks clarifying questions, discovers details
2. Based on the interview, AI creates a **GitHub issue** with full context: what's needed, why, what constraints exist
3. In the next session (or another developer) opens the issue and **implements the task** — no re-asking, no lost context

This solves the key problem: different AI sessions don't know about each other. A GitHub issue becomes the "handoff mechanism" — a structured document preserving all context.

> **Practical takeaway:** Use GitHub issues as an asynchronous context handoff mechanism. One session gathers requirements, another implements. Information loss is minimal.

---

## Part 16: SpecKit — From Idea to Prototype Through Specification

### Spec-Driven Development

SpecKit is a methodology that forces you to describe **WHAT** and **WHY** before writing **HOW**. Eight sequential phases:

1. **Constitution** — project principles (like a country's constitution)
2. **Specify** — what exactly needs to be built
3. **Clarify** — refining acceptance criteria
4. **Plan** — architecture and tech stack
5. **Tasks** — decomposition into tasks
6. **Analyze** — checking the plan for conflicts
7. **Implement** — implementation by tasks
8. **Checklist** — result verification

The AI **refuses** to proceed to the next phase until the current one is complete. You can't start coding without an approved specification.

### Why This Works

- **Specification is separated from technology:** "User should log in securely" (spec) vs. "JWT + PostgreSQL + React" (plan). Non-technical stakeholders validate the spec; tech decisions can change without revisiting requirements.
- **Data model as investment:** SpecKit forces you to design the database schema before writing code. A mistake here costs minutes. A mistake during implementation — days of migrations.
- **Tasks as safeguard:** "Implement authentication" — that's asking AI to make 50 independent decisions. "Create a migration for the users table" — that's a specific, verifiable task.

> **Practical takeaway:** SpecKit transforms chaotic code generation into a managed process. The `specs/` folder becomes living documentation that helps future developers understand not just WHAT was built, but WHY.

---

## Part 17: Chrome DevTools MCP — AI Tests Your Application

### AI Gets "Eyes and Hands"

Chrome DevTools MCP lets the AI agent control the browser: inspect elements, click buttons, fill forms, take screenshots, read console errors. The agent **sees** your application — like a QA engineer sitting in front of the screen.

### The Self-Correcting Loop

Combined with hot reload (code changes instantly reflected in the browser), a powerful cycle emerges:

1. Agent implements a contact form
2. Changes instantly appear in the browser (hot reload)
3. Agent tests the form — sends empty data
4. Validation triggers incorrectly (screenshot)
5. Agent finds a bug in validation logic
6. Agent fixes the bug
7. Browser updates instantly
8. Agent re-tests — everything passes

The entire cycle — 2–3 minutes, without a single manual page refresh.

### Test Documentation as an Artifact

Instead of a manual QA checklist (which is never up to date), the agent generates test scenarios in markdown. This isn't just documentation — it's an **executable regression suite**. Run it anytime — and the agent verifies nothing is broken.

> **Practical takeaway:** QA shifts left — bugs are caught during development, not after release. For distributed teams, auto-generated markdown documentation becomes the specification of "correct behavior," eliminating ambiguity.

---

## Conclusion

A language model is not magic, and it's not artificial intelligence in the Hollywood sense. It's an incredibly powerful tool for working with text (and code, instructions, test cases, documentation — it's all text).

The key to effective use is **understanding the mechanism**:
- The model generates text one word at a time
- It sees the context as a whole
- It has no memory — you create it through instructions
- Instructions are your knowledge transfer for a "new junior" in each session
- Hallucinations are feedback for improving instructions

And beyond that — **tools that turn AI from a conversationalist into a working system**:
- Git baby steps — a safety net for safe iteration
- Skills Management — scaling knowledge across the entire team
- AI Skills & Tools — precision through code, not text generation
- MCP — connecting AI to the outside world through a unified standard
- CLI — direct access without hallucinations for critical operations
- GitHub MCP — task management and delegation between sessions
- SpecKit — the discipline of "specification first, code second"
- Chrome DevTools MCP — QA automation right during development

There will be more work, not less. But the nature of that work is changing: from manual execution to managing AI assistants, describing processes, and quality control. This is the foundational program, after which each participant moves to individual work — building specific agents for their SDLC.

Start with one instruction. Improve it over 10–20 iterations. When it becomes reliable — create your first skill. Connect MCP. Build an agent. And so, brick by brick, you'll assemble your "team" of AI assistants.