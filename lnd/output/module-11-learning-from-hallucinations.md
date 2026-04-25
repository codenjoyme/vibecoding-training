# Module 11: Learning from Hallucinations

### Background
You created a custom instruction in the previous module, and the AI followed it — mostly. But the quiz questions it generated have five answer options instead of three. Or the report format has an extra section you never asked for. Or the function has type hints when you explicitly said "no type hints."

These are not bugs. They are `hallucinations` — creative interpretations of ambiguous `instructions`. And they are the most valuable feedback you will ever receive, because each `hallucination` reveals a gap in your `instructions` that you can fix.

In this module, you will learn to treat `hallucinations` as a systematic improvement tool: observe the deviation, delegate the fix to the AI, and verify the result. You will apply this technique to improve the `Jira`/`Confluence` workflow `instructions` you created in `Module 10`.

Upon completion of this module, you will be able to:
- Interpret AI `hallucinations` as feedback about ambiguous or missing constraints in your `instructions`.
- Apply the Run → Observe → Delegate fix → Verify cycle to iteratively improve `instructions`.
- Delegate `instruction` corrections to the AI instead of editing files manually.
- Diagnose the interference problem when combining multiple `instructions`.

## Page 1: Hallucinations Are Feedback
### Background
When the AI produces unexpected output, the natural reaction is frustration. But a `hallucination` is simply the AI filling in gaps you left in your `instructions`. If you said "generate quiz questions" without specifying the number of answer options, the AI chose 5 because that seemed reasonable based on its training data.

This reframing is important:
- A `hallucination` is not the AI being wrong — it is the AI interpreting ambiguity.
- Every `hallucination` reveals a missing or unclear constraint in your `instruction`.
- Fixing the `instruction` prevents the same `hallucination` from ever happening again.
- Over time, your `instructions` become so precise that `hallucinations` become rare.

The continuous improvement cycle:
1. Run the `agent` using your `instruction`.
2. Observe the output — spot where it deviates from your expectations.
3. Stop the `agent` at the point of deviation.
4. Ask the `agent` to fix the `instruction` — describe what went wrong and what you expected.
5. Rerun from the previous step — verify the fix works.
6. Repeat until the `instruction` produces consistent output.

**Why `hallucinations` are inevitable — the dreaming mind analogy**

Think about how dreams work. When you dream, your mind replays fragments of today, last week, childhood — mixed together with things that never happened and could never happen: a stranger with three fingers, a building that bends, your childhood home in a city you've never visited. Dreams do not distinguish between memory and invention. Everything feels equally real.

A language model works the same way. When it generates text, it "dreams" that text — drawing on traces of everything it read during training. Those original texts no longer exist as discrete documents; they dissolved into the `model's` weights and parameters, the way memories dissolve into neural connections. What remains is a probability landscape shaped by billions of words. When you give the `model` a `prompt`, it dreams a response — a stream of `tokens` that feels statistically plausible, assembled from patterns absorbed during training, not from direct recall.

This is why `hallucinations` are not bugs — they are the nature of generation. Everything a `model` produces is, in a sense, one large `hallucination`: a dream shaped by `context`. Your task, through increasingly precise `instructions`, is to guide that dreaming into something you will call useful.

### ✅ Result
You understand that `hallucinations` are feedback about `instruction` gaps, not AI failures.

## Page 2: Delegate the Fix — Do Not Edit Manually
### Background
The key technique in this module is counterintuitive: when the AI produces unexpected output, you ask the AI itself to fix the `instruction`. You do not open the `instruction` file and edit it manually.

Why delegate?
- The AI maintains consistency with the existing `instruction` style.
- The AI understands the `context` of what went wrong better than a manual edit.
- The process of self-correction makes `instructions` more precise.
- You learn what was ambiguous by seeing how the AI interprets the fix.

The workflow:
1. Run the `instruction` and observe the deviation.
2. Describe the problem to the AI: `The quiz questions have 5 options, but I need exactly 3 options`.
3. Ask the AI to update the `instruction` file: `Update 'generate-quiz' instruction to specify exactly 3 answer options per question`
4. The AI reads the `instruction`, finds the ambiguity, and adds the constraint.
5. Rerun the `instruction` and verify the output now matches expectations.

### Steps
1. Open one of the `instruction` files you created in `Module 10` (e.g., a `Jira`/`Confluence` workflow `instruction`).
2. Ask the AI to execute it: `Following '[your-instruction]', do [your task]`
3. Review the output carefully. Note anything that deviates from what you expected — format, content, structure, missing elements, extra elements.
4. If you find a deviation, do NOT edit the file manually. Instead, tell the AI: `I noticed [describe the deviation]. Please update '[your-instruction]' to prevent this in the future`
5. Commit the updated `instruction` file immediately — before doing anything else. Use the same baby-steps commit pattern from `Module 3`. This step is critical: if you revert to an earlier `prompt` without committing first, the AI's undo mechanism may roll back the instruction file along with everything else, erasing the fix.
6. Return to the `prompt` that came just before the `hallucination` and re-run it. This is the same recovery technique from `Module 7`, but instead of editing the `prompt` itself, you fixed the `instruction`. The AI's `context` still contains the "memory" of the wrong interpretation — you need to clear it. Two ways to do this:
   - **Option A — edit and resend:** Go back one step in the chat history to the `prompt` before the `hallucination`, edit or resend it, and confirm that the updated `instruction` is loaded and the output is now correct.
   - **Option B — fresh `context`:** Open a new chat session and repeat the original request from scratch in a clean `context`. This guarantees no residual "memory" of the failed interpretation.

### ✅ Result
You can delegate instruction fixes to the AI and verify the improvements.

## Page 3: The Interference Problem
### Background
When you combine multiple `instructions` together — or add your own `prompt` on top of an `instruction` — things can change in unexpected ways. This is the interference problem.

A single instruction works predictably in isolation. But when the AI context contains:
- Instruction A (generate report)
- Instruction B (format as table)
- Your additional `prompt` ("also include a summary")

...the AI must reconcile all three, and the result may differ from what any single `instruction` produces alone. `Instructions` are context-sensitive: the same `instruction` may behave differently depending on what else is active.

Types of `instructions` to be aware of:
1. Scenario `instructions` — step-by-step playbooks ("do this, then that").
2. Mode-switching `instructions` — put the `agent` into interactive mode ("interview me first").
3. Creation `instructions` — transform drafts into structured output.
4. Decorator `instructions` — small rules for specific corner cases.

Understanding which type you are building (or fixing) helps you keep each instruction focused.

### Steps
1. Take two of your instruction files and try combining them in a single `prompt`: `Following '[instruction-a]' and '[instruction-b]', do [task].`. You can write it in simple: `Following instructions a and b, do some task`.
2. Compare the output to running each instruction separately.
3. If the combined result is unexpected, identify which `instruction's` rules were overridden.
4. Decide whether to adjust one instruction or keep them separate.

### ✅ Result
You understand the interference problem and can diagnose it when combining `instructions`.

## Page 4: Improve Your `Jira`/`Confluence` Instructions
### Background
Now you will apply the `hallucination`-fixing workflow to your practical project. In `Module 10`, you created `instruction` files for `Jira`/`Confluence` workflows. It is time to stress-test them and make them more robust.

### Steps
1. Pick one of your `Jira`/`Confluence` `instruction` files.
2. Ask the AI to execute it 3 times with slightly different inputs (e.g., different `Jira` project names, different date ranges, different report formats).
3. For each execution, note any deviations — output format, missing fields, unexpected sections, wrong data structure.
4. For each deviation, delegate the fix: `I ran this instruction with [input] and got [deviation]. Update the instruction to handle this correctly`
5. After all fixes, run the `instruction` once more and verify it produces consistent output across different inputs.
6. Commit the improved instruction files.

### ✅ Result
Your `Jira`/`Confluence` workflow `instructions` are refined through real-world testing and `hallucination` fixing.

## Page 5: Building Progressive Trust
### Background
As your `instructions` improve through iterative refinement, you start trusting the AI more. At first, you review every output line by line. After 10 consecutive runs that produce correct results, you begin to trust the process.

This trust is earned — built on:
- Precise, battle-tested `instructions` refined through real failures.
- Consistent results across many runs with different inputs.
- A self-correcting system where `hallucinations` lead to `instruction` improvements.

The end goal is delegation: you delegate entire workflow segments to the AI with confidence, only stepping in when the task or context changes significantly. This is the real productivity multiplier — not using AI as a chat tool, but building a reliable instruction-driven partnership.

### Steps
1. Review all your `instruction` files. For each one, ask yourself: "Would I trust this `instruction` to run without review?"
2. If the answer is "not yet," plan one more round of testing and fixing.
3. If the answer is "yes," mark it as battle-tested in your `instruction` catalog (`main.agent.md`).
4. Commit your changes.

### ✅ Result
You have a process for building trust in your instructions through iterative improvement.

## Summary
Remember the quiz with five answer options instead of three? Or the report format with that extra section you never asked for? Those surprises are no longer frustrating mysteries — they are improvement signals. Each `hallucination` told you exactly what was missing from your `instruction`, and by delegating the fix to the AI, you closed the gap permanently.

Key takeaways:
- `Hallucinations` are feedback, not failures. Each one reveals an ambiguity in your `instruction`.
- Delegate fixes to the AI — do not edit `instructions` manually. The AI maintains consistency.
- The improvement cycle: Run → Observe → Delegate fix → Verify → Repeat.
- Be aware of the interference problem when combining multiple `instructions`.
- Progressive trust is earned through iterative testing and refinement.

## Quiz
1. What does a `hallucination` typically reveal about your `instructions`?
   a) That your `instruction` has an ambiguity or gap that the AI filled in with its own interpretation
   b) That the AI model’s training data is outdated and it needs to be retrained on newer examples
   c) That the instruction file is too long and the AI stopped reading it before reaching the relevant rule
   Correct answer: a.
   - (a) is correct because `hallucinations` occur when the AI encounters ambiguity in your `instructions` and fills the gap with a reasonable but unintended interpretation. Fixing the ambiguity prevents the `hallucination` from recurring.
   - (b) is incorrect because `hallucinations` are not caused by stale training data. They happen because the `instruction` did not specify a constraint, so the AI chose a default from its general knowledge — retraining would not help.
   - (c) is incorrect because AI models do not stop reading mid-file due to length (unless the file exceeds the `context window`). The issue is ambiguity in the instruction, not the AI skipping content.

2. Why should you delegate instruction fixes to the AI instead of editing manually?
   a) Because the AI maintains consistency with the existing instruction style, understands the context of the failure, and produces more precise corrections
   b) Because manually edited instruction files are not recognized by the AI agent and must be re-indexed
   c) Because the AI records each fix in a change log so you can track the instruction’s evolution over time
   Correct answer: a.
   - (a) is correct because delegating fixes leverages the AI's understanding of both the instruction context and the failure, producing corrections that are consistent in style and precise in addressing the root cause.
   - (b) is incorrect because the AI reads instruction files the same way regardless of how they were edited. Manual changes are recognized just like AI-generated changes.
   - (c) is incorrect because the AI does not automatically maintain a change log unless you explicitly ask it to. The benefit of delegation is consistency and contextual awareness, not automatic logging.

3. What is the interference problem with instructions?
   a) When multiple instructions are active together, they can interact unpredictably — the AI must reconcile them, and the result may differ from what each instruction produces in isolation
   b) When an instruction file references another instruction, the referenced file’s rules take complete priority and the original file’s rules are ignored
   c) When you add your own `prompt` alongside an instruction, the AI treats your `prompt` as a correction and rewrites the instruction file
   Correct answer: a.
   - (a) is correct because instructions are context-sensitive. Combining multiple instructions or adding extra `prompts` changes how the AI interprets each instruction, potentially producing unexpected results.
   - (b) is incorrect because referenced `instructions` do not override the original. Both sets of rules are active simultaneously, which is precisely what causes the reconciliation challenge.
   - (c) is incorrect because adding a `prompt` alongside an `instruction` does not rewrite the `instruction` file. The AI treats both as input for the current task, but the `instruction` file on disk remains unchanged.

## Practical Task

You have applied the `hallucination` improvement cycle: identified an unexpected AI output, traced it to a missing or ambiguous `instruction` rule, and delegated the fix to the AI.

**Submit your `report.md` for automated check:**

1. In your AI agent (`Copilot` / `Cursor` / `Claude Code`), open your project workspace and run the prompt below. The agent will collect raw artifacts from your project and write them into a `report.md` file in the project root. The server-side `autocheck` will read the raw data and decide whether the submission is acceptable — your local agent must NOT make judgments itself.

   ```markdown
   You are a data-collection agent. Your job is to gather RAW artifacts from my project workspace and write them into a file named `report.md` in the project root. Do NOT make judgments, do NOT summarize, do NOT add opinions. Paste file contents verbatim. Paste command outputs verbatim. If a value is genuinely missing, write `N/A`. Use tilde fences (`~~~`) for every inner code block so they don't conflict with the outer markdown fence. Replace any real `tokens`, `API keys`, passwords, or secrets with the literal text `[REDACTED]` everywhere they appear.

   Collect the following raw artifacts for Module 11 — Learning From Hallucinations. Write them into `report.md` in this exact structure:

   # Module 11 Submission — Raw Data
   - Module: 11 — Learning From Hallucinations
   - Repository remote URL: `[output of `git remote get-url origin` or `N/A`]`
   - Repository local path: `[absolute path to the project root]`
   - Current commit SHA: `[output of `git rev-parse HEAD`]`
   - Current branch: `[output of `git rev-parse --abbrev-ref HEAD`]`
   - Report generated at: `[ISO 8601 timestamp]`

   ## Updated Instruction File
   - Path: `[relative/path/to/instructions/file.agent.md]`
   - Size (bytes): `[N]`
   - Last modified: `[ISO 8601 timestamp]`

   ### Verbatim Contents (current version)
   ~~~markdown
   [Paste full current contents here, byte-for-byte.]
   ~~~

   ## Diff Against the Previous Commit
   Output of `git log -p -1 --follow [path/to/instruction/file]` (or `git diff HEAD~1 HEAD -- [path]`):
   ~~~diff
   [paste output verbatim]
   ~~~

   ## Hallucination Evidence
   If a chat transcript, conversation log, or notes file documenting the hallucination exists in the repository (e.g., under `requests/`, `chat-history/`, `notes/`, or similar), paste it verbatim below. Otherwise write `NO TRANSCRIPT FILE FOUND`.

   ### Source File
   - Path: `[relative/path | N/A]`

   ### Verbatim Contents
   ~~~
   [paste full contents OR `NO TRANSCRIPT FILE FOUND`]
   ~~~

   ## Recent Commits to Instructions Folder
   Output of `git log --oneline -10 -- instructions/`:
   ~~~
   [paste output verbatim]
   ~~~
   ```

2. Submit `report.md` to the `autocheck` system (the submission endpoint is being set up in parallel; instructions for accessing it will be shared once it is available).
3. The `autocheck` system will check that:
   - A specific, real `hallucination` is described (not a hypothetical example).
   - The `instruction` fix targets the root cause, not just the symptom.
   - The updated `instruction` has a rule that prevents the `hallucination` from recurring.
   - The file is committed to your repository.
