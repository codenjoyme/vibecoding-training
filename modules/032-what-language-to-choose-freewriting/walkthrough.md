# Choosing Prompt Language & Freewriting - Hands-on Walkthrough

In this walkthrough you'll consciously pick the language you write prompts in, then practice **freewriting** — typing a prompt at maximum speed without backspace, without fixing typos, and without letting your inner critic edit you mid-sentence. By the end you'll have produced a long raw prompt faster than you've ever produced one before, and seen that the model still understands it perfectly.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

---

## What We'll Do

You'll work through three short experiments. Each one challenges an assumption that quietly slows you down:

1. **Token-cost reality check** — measure how much "expensive" a non-English prompt actually is, and weigh it against your own time
2. **Scrambled-text experiment** — paste a deliberately broken text and watch the model read it without complaint, proving you don't need clean prose
3. **Five-minute freewrite** — produce a complete, usable prompt in one sitting without editing yourself

Total time: ~7 minutes. Tools: just your AI chat window and a stopwatch in your head.

---

## Part 1: The Real Bottleneck

Before practicing the technique, get clear on **why** it works. The instinct "I should write prompts in English to save tokens" sounds rational but usually loses the math.

Three things to internalize:

1. **Tokens are cheap. Your time is not.** A model run that costs $0.05 in tokens replaces minutes of your reading and writing. The break-even point is almost always in your favor — even at a 2× token premium for non-English text.

2. **Mental tokens deplete too — and refill only with sleep.** Every word you weigh, every grammar correction you make, every typo you backspace over costs a slice of finite daily attention. Switching to a non-native language taxes that budget on **every prompt**, forever.

3. **Prompt language ≠ artifact language.** You can write your prompt in Russian, Ukrainian, Polish, Spanish — anything — and instruct the AI to produce code, docs, and commit messages in English. Most teams default to "everything in English" because they've never separated the two. They're separable.

**A useful rule of thumb:** Switch your prompt language only if a model becomes **50× cheaper** in another language, not 2×. Below that threshold, your reading/writing speed dominates the cost equation.

### Decide your prompt language now

Pick one to use for the rest of this module:

- The language you've read and written in for the most years (usually your native one)
- The language you can type fastest in
- The language you can express ambiguity and nuance in without searching for words

If those three answers point to the same language, that's your prompt language. Use it. Stop apologizing for it.

---

## Part 2: The Scrambled-Text Experiment

This experiment kills the belief that prompts need to be grammatically clean.

### What we'll do

Paste a sentence with intentionally scrambled letters into your AI chat and ask the model to summarize it. You'll see the model parse it correctly — meaning every minute you spend fixing typos and grammar in your own prompts is a minute spent on something the model didn't need.

### Steps

1. Open your AI assistant chat window (GitHub Copilot Chat in VSCode, or Cursor Chat). Make sure **Agent Mode** is enabled and the model is set to **Claude Sonnet 4.5** (recommended).

1. Paste this exact text into the chat (yes, in this order, with the typos):

   ```
   Tihs is a tset to porve taht you can raed wrods even wehn the mddile lettres are sacrmbled, as lnog as the frist and lsat lettres are crrocet. Pelase smumarzie waht you uderstnad form tihs sentnece in one line.
   ```

1. Send the message and read the model's response.

1. Now do the same in **your prompt language** (the one you picked in Part 1). Type a sentence quickly without correcting typos, scramble a couple of words on purpose if you need to, and ask the model to summarize.

### What just happened

The model summarized both correctly. It tolerates typos, scrambled middle letters, missing punctuation, and informal phrasing. That tolerance is your **permission slip**: stop fixing prose as you write. Get the meaning out first; the model will meet you halfway.

This is the foundation of freewriting — the technique only works if you trust the reader (in this case the model) to handle imperfect input.

---

## Part 3: Freewriting — DDoS Your Inner Critic

**Freewriting** is a technique borrowed from creative writing practice (see [The Artist's Way's "Morning Pages"](https://en.wikipedia.org/wiki/Free_writing), David Allen's GTD brain dump, and similar). The mechanic is simple: **write continuously, at max speed, without backspace, without re-reading, without fixing anything**, until a timer runs out or the thought is fully out.

The reason it works is that your inner critic — the voice that says "no, that word is wrong, restructure that sentence, fix that typo" — operates slower than your maximum typing speed. If you outrun it, it can't intervene. What comes out is the raw, honest version of what you actually meant. Editing happens **later**, separately.

For prompting, this means: you produce a long, complete prompt in one continuous push. No stopping. No second-guessing. The model reads it fine (Part 2 proved that), and you've spent 5 minutes instead of 25.

### What we'll do

Write a real prompt for a real task using the freewriting rules. The task itself doesn't matter — what matters is the technique.

### Setup

1. Pick a task you've been putting off because writing the prompt feels like a chore. Examples:
   - "Refactor this messy function so it's testable"
   - "Explain this error stack trace and suggest three causes"
   - "Design a markdown spec for a feature I keep describing verbally"
   - "Write a personal retro of my last sprint and find three patterns"

1. Open your AI chat (or, better, a scratch file like `./workspace/hello-genai/freewrite-prompt.md` (Windows: `c:/workspace/hello-genai/freewrite-prompt.md`) and write into that — you'll paste it into the chat after).

1. Set yourself a **5-minute timer**. A real one. Phone, kitchen timer, browser tab — anything.

### Rules (read these once, then don't look back)

While the timer runs:

- **No backspace key.** If you mistype, leave it. The model handles typos (you proved this in Part 2).
- **No re-reading what you just wrote.** Keep moving forward. Don't scroll up.
- **No structural editing.** No "wait let me reorder this paragraph". Reorder later.
- **No looking up words.** If you can't think of the precise term, write the imprecise one and move on.
- **No stopping to think.** If your mind blanks, type "I don't know what to say next so I'm going to keep typing about" and your topic — until the next thought arrives. It will.
- **Write in your chosen prompt language** (Part 1).
- **Capture intent, not polish.** The goal is "get everything out", not "produce a finished document".

### Go

Start the timer. Write.

When the timer ends, **stop**.

### After the timer

Now — and only now — read what you wrote. You'll see three things:

1. **More content than you expected.** 5 minutes of unblocked typing is roughly 400-700 words depending on language. That's a substantial prompt.
2. **Some genuinely useful structure that "just appeared".** Your subconscious organized things while your critic was muted.
3. **Mess.** Typos, half-sentences, repetition. **That's fine.** The model doesn't care.

### Light cleanup pass (optional, 1 minute)

Before pasting into the chat, do a single quick pass:

1. Add `## Goal` at the top in one sentence — what you actually want from the model
1. Add `## Context` heading above your raw freewrite
1. Optionally add `## Constraints` or `## Output format` at the bottom
1. **Do not** rewrite paragraphs. Do not "improve" sentences. Do not fix typos. Just add structural headings.

Now paste it into the chat and send.

### What just happened

You produced a complete, contextual prompt in 5–6 minutes that would normally take 20+ if you were editing as you wrote. The model got more context than you usually give it, expressed in your most natural voice. Your inner critic stayed offline the whole time.

This is the pattern. Once you've done it once, you'll never go back to writing prompts character-by-character with a backspace finger ready.

---

## Part 4: When Freewriting Pairs With Other Patterns

Freewriting is a building block. It composes well with:

- **Iterative-prompt pattern** ([Module 058](../058-workspace-kickoff-iterative-prompt/about.md)) — every `## UPD[N]` block in a helm-log file is a freewrite. You append, the agent processes, repeat.
- **Pair-prompting sessions** — when working with a colleague, the person at the keyboard freewrites while the other person watches **silently** (no "did you mean…?", no grammar tips). Roles swap on the next prompt. This eliminates the "five minutes of typing-then-deleting" pattern that wastes everyone's time.
- **GTD brain dumps** — start a session by freewriting "everything bothering me about this project" into a markdown file, then ask the AI to cluster the items. You discover priorities you didn't know you had.
- **Stuck-state recovery** — when a chat conversation goes in circles, open a fresh scratch file, freewrite "what I actually wanted from this whole thread", paste it as a new prompt. The reset usually unsticks the model.

---

## Success Criteria

- ✅ You consciously chose a prompt language and can articulate why (Part 1)
- ✅ You verified the model reads scrambled / typo-laden text without trouble (Part 2)
- ✅ You completed a 5-minute freewrite without using backspace, without re-reading, and without editing mid-flow (Part 3)
- ✅ You added structural headings (`## Goal`, `## Context`) without rewriting the body
- ✅ You sent the freewritten prompt to the model and got a usable response
- ✅ You can name at least two situations where you'd reach for freewriting again

## Understanding Check

1. **Why is "save tokens by switching to English" usually a false economy?**  
   *Expected: Mental tokens are scarcer than LLM tokens. Time spent translating, looking up words, and editing your own prose costs more than the token-price difference unless the difference is roughly 50× or more.*

2. **What rule separates "prompt language" from "artifact language", and why does it matter?**  
   *Expected: The prompt is for you-to-AI communication. The artifact (code, docs, commits) is for your team and the world. They can be different. Most teams collapse them into one because they never asked the question.*

3. **Why does the scrambled-text experiment matter for prompting?**  
   *Expected: It proves the model tolerates messy input. That gives you permission to stop polishing prose mid-prompt — which removes the main cost of freewriting (the urge to edit).*

4. **What are the four "no" rules during a freewrite?**  
   *Expected: No backspace, no re-reading, no structural editing, no looking up words. (Plus: no stopping — fill silence by typing about the silence.)*

5. **Why does freewriting work? What is it bypassing?**  
   *Expected: Your inner critic / Ego / "Censor" operates slower than max typing speed. By outrunning it, you produce raw thought before it gets edited into something safer or more polished.*

6. **When is the right moment to add structure to a freewritten prompt?**  
   *Expected: After the timer ends, in a single 1-minute pass, by adding headings only — never by rewriting sentences. Polish is a separate step from generation.*

7. **Name two non-prompting practices that use the same mechanic as freewriting.**  
   *Expected: Morning Pages (The Artist's Way), GTD brain dumps, journaling, stream-of-consciousness writing, freeform brainstorming. Any "dump first, organize later" technique.*

## Troubleshooting

- **"I keep wanting to fix typos and it breaks my flow"**  
  → Cover the screen with a sticky note for the first minute. You can also turn off autocorrect — autocorrect itself is an inner-critic substitute. After 30 seconds your hands stop reaching for backspace.

- **"My freewrite is incoherent — the model can't make sense of it"**  
  → That's almost never true; usually the issue is that the freewrite has no `## Goal` heading at the top. Add one sentence: "I want X". The model handles the rest.

- **"I run out of things to say after 90 seconds"**  
  → Type the sentence "I don't know what to write so I'll keep typing about [topic] until something comes". This is part of the technique, not a failure of it. The next real thought usually arrives within 20–40 seconds.

- **"My native language isn't English and I'm worried the team won't understand my prompts"**  
  → Your prompts are not the deliverable. The artifact is. Add `Reply in English. Generate all code, comments and commit messages in English.` to your prompt or your custom instructions, and the team sees only English output.

- **"My pair partner keeps interrupting to suggest words"**  
  → Establish the rule explicitly before the session: "I'm freewriting for the next 5 minutes. Don't speak until the timer ends." Swap roles on the next prompt.

- **"I tried freewriting in English (non-native) and it didn't feel faster"**  
  → That's the diagnosis, not the failure. You just confirmed Part 1 with your own keyboard. Switch to your native language and try again.

## When to Use This Technique

Reach for freewriting when:

- You've stared at an empty prompt for more than 30 seconds
- You're starting a new task and don't know yet what to ask for
- You're processing a frustrating debugging session and want to vent + ask for help in one shot
- You're kicking off an [iterative-prompt](../058-workspace-kickoff-iterative-prompt/about.md) helm-log
- You're pair-prompting and want to model the technique for your partner
- You're tired and your "polished writing" mode is too expensive right now

Avoid freewriting when:

- The prompt has to land in a strict format (e.g., a function signature, a regex). Use a template instead.
- You're already in the middle of a productive iterative dialogue with the model. Don't reset.
- You only need a one-line follow-up like "now in TypeScript please".

## Next Steps

You now have a deliberate prompt language and a technique for producing prompts at maximum speed. Pair this with the iterative-prompt pattern to make every prompt part of a versioned, reviewable log:

- Continue to [Module 035 — Visual Context with Screenshots](../035-visual-context-screenshots/about.md) — when words run out, send images
- Or jump ahead to [Module 050 — Effective Prompting](../050-effective-prompting-without-arguing/about.md) — the iterate-don't-argue mindset that consumes freewritten prompts
- Or apply both together in [Module 058 — Workspace Kickoff with Iterative Prompt](../058-workspace-kickoff-iterative-prompt/about.md) — every UPD block in a helm-log is a freewrite waiting to happen
