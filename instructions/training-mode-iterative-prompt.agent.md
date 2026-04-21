# Training Mode: Iterative Prompt Approach

This file describes an **alternative way to run training sessions** using the `iterative prompt` pattern.
It is an extension of `training-mode.agent.md` — all rules from that file apply here unless explicitly overridden.

**When to activate this mode:** User explicitly requests to go through training using the `iterative prompt` approach, or mentions wanting to save premium requests.

---

## Why Use This Mode

Under the current GitHub Copilot billing model, every response from a premium model (e.g. Claude Opus) costs exactly **1 premium request** — regardless of input/output token count. In a standard chat-based training session, each piece of feedback, each "next", and each small clarification fires a new request.

The **iterative prompt** approach eliminates most of these back-and-forth charges by keeping the agent working autonomously inside a single long loop, while you communicate via a versioned file that stays in `git`.

Additional benefits (regardless of billing):
- The entire session is preserved as a file in version control — colleagues and future AI sessions can see what was done and how
- The prompt file acts as a running summary of the module coverage — no lost context even after `compact conversation`
- You work at your own pace: write an update, append `go`, the agent picks it up automatically

---

## Activating Iterative Prompt Training Mode

When a user requests training with the iterative prompt approach, **before loading the module**, do the following:

### Step 1 — Brief User Onboarding

Explain the mechanics in a few short points (localize to user's language):

```
🗂️ We'll run this training session in **iterative prompt mode**.

Here's how it works:
1. I'll create a `main.prompt.md` file in `work/NNN-[module-name]/main.prompt.md`
2. All module content and your responses go into that file — not in this chat
3. You communicate with me by appending `## UPD[N]` blocks to that file
4. When you're ready for me to act, write `go` at the end of your UPD block
5. I'll process it, write a `### RESULT` block, then sleep 60 seconds waiting for your next update
6. You can write your next UPD at any pace — I'll pick it up automatically

This saves premium requests: while I'm sleeping I consume no quota.
The file stays in git alongside the generated content — your full session history.
```

### Step 2 — Create the Prompt File

Create the file `work/NNN-[module-name]/main.prompt.md` (where NNN matches the module number):

```markdown
<follow>
iterative-prompt.agent.md
training-mode.agent.md
training-mode-iterative-prompt.agent.md
</follow>

## Context

Module: [module-id] — [Module Name]
Training progress file: ../../training-progress.md

---

## UPD1

Start the training module: [module-id] — [Module Name].
Follow the Part-by-Part progression from training-mode.agent.md.
Present Part 1, then wait for my response in UPD2.
go
```

Replace `[module-id]` and `[Module Name]` with the actual values.

### Step 3 — Hand Off to the File

Tell the user:

```
✅ Created: work/NNN-[module-name]/main.prompt.md

Open that file in VS Code. You'll see a ▶ Run button at the top — click it to start the agent loop.
From now on, write your replies and requests as new `## UPD[N]` blocks at the bottom of the file.
Append `go` when you're done writing an update and want me to act on it.
This chat window stays open in the background — that's fine, it's just the engine.
```

---

## How Training Flows Inside the Prompt File

Once the agent is running inside the iterative prompt loop, the training proceeds exactly as described in `training-mode.agent.md` — Part-by-Part, one idea at a time, with discussion and engagement checks.

The only difference is the **communication channel**: instead of chat messages, each exchange becomes a `## UPD[N]` / `### RESULT` pair in the file.

### Typical Session Structure

```markdown
## UPD1
Start module 040 — Agent Mode Under the Hood.
go

### RESULT
- Started module 040
- Presented Part 1: What Is Agent Mode

## UPD2
Interesting! I've seen the agent loop before but didn't think about the token cycle.
In my team we always interrupt it. Is that a problem?
go

### RESULT
- Discussed interruption impact on agent context
- Answered question about mid-loop interruptions

## UPD3
Ok that makes sense. Ready for Part 2.
go

### RESULT
- Presented Part 2: Tool Use and Permissions

## UPD4
Done with the hands-on step. Output was: [paste output here]
go

### RESULT
- Reviewed output, confirmed correct behavior
- Explained what the output means

## UPD5
All good. Mark module complete and let's check progress.
go

### RESULT
- Updated training-progress.md: [x] 040-agent-mode-under-the-hood
- Module completed with feedback saved
```

---

## Rules for Agent Inside the Iterative Prompt Loop

These rules apply when conducting training inside a `main.prompt.md` file:

1. **All training-mode.agent.md rules apply** — Part-by-Part progression, engagement checks, Fun Mode, feedback collection, etc.

2. **One UPD = One interaction cycle** — Process each `## UPD[N]` and append `### RESULT`. Do not skip ahead.

3. **Wait for `go` before acting** — If an `## UPD[N]` block exists but does not end with `go`, the user is still typing. Sleep and check again.

4. **Polling loop** — After writing `### RESULT` for the last UPD:
   - Run `Start-Sleep -Seconds 60` (Windows) or `sleep 60` (Linux/macOS) in **sync** mode
   - Re-read the full `main.prompt.md`
   - Check for new `## UPD` blocks ending with `go`
   - If found → process immediately, write `### RESULT`, commit, then return to sleep
   - If not found → sleep again
   - **Never stop the loop** — keep it alive until user explicitly closes the agent

5. **Commit after each RESULT** — Follow the project git workflow. Each UPD cycle = one commit. This builds a clean history of the training session.

6. **Update training-progress.md as usual** — Module completion, feedback, deep engagement reminders — all go into `training-progress.md` as described in `training-mode.agent.md`. The progress file is the source of truth; the prompt file is the session log.

7. **Keep RESULT blocks concise** — This is a changelog, not documentation:
   - ✅ Good: `- Presented Part 2: Tool Use and Permissions`
   - ❌ Bad: `- I have just presented Part 2 which covers the topic of Tool Use and Permissions in GitHub Copilot Agent Mode, explaining how the agent requests permission to use tools...`

8. **Discussion still happens** — Don't skip the 4-5 exchange minimum per Part just because the medium changed. Each UPD from the user is one exchange. Build depth across multiple UPD cycles. Do not rush to the next Part after one UPD exchange.

---

## UPD Format Reference (for User)

| What to write | Example |
|---|---|
| Start or continue training | `Start module 040. go` |
| Respond to a question | `My team usually interrupts loops when they take too long. go` |
| Move to next Part | `Ready for Part 2. go` |
| Paste command output | `Output was: [paste here]. go` |
| Ask a question mid-module | `Why does the agent need 2500 max requests? Can it be lower? go` |
| Mark complete and move on | `All criteria done. Mark complete and suggest next module. go` |
| Pause (no `go`) | Write your draft UPD without `go` — agent will wait |

---

## Switching Back to Chat Mode

If the user wants to return to normal chat-based training mid-session:

1. Note the current module and last completed Part in `training-progress.md`
2. Tell the user: "Switch back to chat mode confirmed. Continue in this chat — tell me the last Part you finished and we'll pick up from there."
3. Resume `training-mode.agent.md` flow in the chat window normally
