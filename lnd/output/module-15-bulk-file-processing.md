# Module 15: Bulk File Processing with AI

### Background
You need to review 20 `Markdown` files for formatting issues. Or extract action items from 50 meeting notes. Or validate 30 configuration files against a checklist. You open the AI chat and paste your `prompt` — it works beautifully for the first 5 files, then the quality drops. By file 15, the AI is hallucinating information that was never in the source files.

This is called context drift, and it is the core problem of bulk file processing with AI. In this module, you will learn why it happens, experience three different approaches to bulk processing, and implement the most efficient solution that scales to any number of files.

**Learning Objectives**

Upon completion of this module, you will be able to:
- Explain what context drift is and why it degrades quality during bulk AI processing.
- Compare three approaches to bulk file processing (single request, iterative re-reading, script automation) and their tradeoffs.
- Implement script-based automation that processes each file in a fresh context.
- Choose the appropriate approach for a given batch task based on file count, quality requirements, and repeatability.

## Page 1: Approach 1 — Single Request (Context Drift)
### Background
The simplest approach: ask the AI to process all files at once in a single conversation.

What happens:
- The AI processes the first 3-5 files accurately.
- As the conversation grows, the `context window` fills with previous responses.
- Quality degrades: later files get generic responses or hallucinated information.
- By file 15-20, the model has lost focus on the original instruction.

This is context drift — as conversation history accumulates, the model's attention to your original instructions decays. The `context window` has a fixed size, and older information gets pushed out or diluted.

When to use this approach:
- Quick checks on 3-5 files.
- Acceptable quality loss is tolerable.
- No automation needed.

### Steps
1. Open your AI chat in `Agent Mode`.
2. Ask: "Review all `walkthrough.md` files in the `modules/` directory. For each file, check if it has a Summary section and a Quiz section. List any files that are missing either."
3. Watch the agent work. If you have many modules, notice how the quality of analysis changes between the first files and the last files.
4. Note at which point the analysis becomes less detailed or starts repeating generic observations.

### ✅ Result
You have experienced context drift firsthand and understand its cause.

## Page 2: Approach 2 — Iterative Re-reading (`Token` Waste)
### Background
A smarter approach: tell the AI to re-read the instruction for each file, resetting its focus.

The `prompt` looks like this: "For each file: 1) Re-read the validation rules. 2) Read the file. 3) Check against rules. 4) Report issues. 5) Move to next file. 6) Repeat from step 1."

What happens:
- Quality improves because the instruction is refreshed for each file.
- But the AI re-reads the same instruction file every time — wasting `tokens`.
- For 20 files with a 500-word instruction, you pay for 10,000+ words of redundant instruction reading.
- Slower and more expensive than necessary.

When to use this approach:
- 10-15 files where quality is critical.
- One-time operation (cost is acceptable).
- No time to write an automation script.

### Steps
1. Create a validation rules file (e.g., `validation-rules.md`) with 5-6 specific checks for any file type you work with.
2. Ask the AI to process files iteratively with re-reading: "For each `walkthrough.md` in `modules/`: 1) Read `validation-rules.md`. 2) Read the file. 3) Check against rules. 4) Report issues. 5) Move to next file."
3. Compare the quality of analysis with Approach 1. Is it more consistent across files?
4. Think about the `token` cost: the instruction was read N times instead of once.

### ✅ Result
You understand the tradeoff between quality and `token` cost in iterative processing.

## Page 3: Approach 3 — Script-Based Automation (Best Practice)
### Background
The optimal approach: write a script that calls the AI separately for each file with a fresh context. Each file is processed independently — no accumulated conversation history, no context drift, no `token` waste from re-reading.

The pattern:
1. A script (`Python`, `PowerShell`, or `Bash`) iterates over all target files.
2. For each file, the script calls the AI `CLI` tool (like `GitHub Copilot` `CLI`) with the instruction file and the target file.
3. Each call starts with a clean context — no history from previous files.
4. Results are saved to individual output files.

Why this wins:
- No context drift — each file gets a fresh `context window`.
- `Token` efficient — the instruction is read once per file by the `CLI`, not accumulated in conversation history.
- Deterministic — the same instruction is applied consistently to every file.
- Scalable — works for 100+ files.
- Auditable — each result is saved in a separate file for review.

### Steps
1. If you have `GitHub Copilot` `CLI` installed (or another AI `CLI` tool), test it with a single file:
   "copilot -p '@validation-rules.md Validate this file: @modules/010-installing-vscode-github-copilot/`walkthrough.md`' --allow-all -s"
2. If you do not have a `CLI` tool, create a simple `Python` script that:
   - Lists all target files.
   - For each file, invokes the AI (via API or `CLI`) with the instruction + file content.
   - Saves the result to an output file.
3. Run the script on your target files.
4. Compare results with Approach 1 and 2: is the quality consistent across all files?

### ✅ Result
You can implement script-based bulk processing for consistent, scalable results.

## Page 4: Comparison and Decision Framework
### Background
Here is a comparison of the three approaches:

| Aspect | Single Request | Iterative Re-read | Script Automation |
|--------|---------------|-------------------|-------------------|
| Files | 3-5 max | 10-15 | Unlimited |
| Quality | Degrades | Good | Excellent |
| `Token` cost | Low | High | Optimal |
| Speed | Fast initially | Slow | Fast |
| Setup time | None | None | Script required |
| Context drift | Yes | Reduced | None |

Decision framework:
- Need a quick answer for a few files? → Approach 1.
- One-time high-quality check, no time for scripting? → Approach 2.
- Repeatable operation, many files, consistency matters? → Approach 3.

For your `Jira`/`Confluence` project, any batch operation (processing meeting notes, validating documentation, generating reports from multiple data sources) should use Approach 3.

### Steps
1. Think about the batch operations in your `BACKLOG.md`. Which ones involve processing multiple files or data items?
2. For each, decide which approach is most appropriate based on the comparison table.
3. Document your decision in `BACKLOG.md` (add a note: "Approach 1/2/3" next to relevant tasks).
4. Commit the updated file.

### ✅ Result
You have a decision framework for choosing the right bulk processing approach.

## Page 5: Practical Application — Process Project Files
### Background
Apply the best approach to a real task in your project. Choose one of these scenarios (or create your own):
- Process all instruction files in `instructions/` to verify they follow the Single Responsibility Principle.
- Analyze meeting notes or project documents to extract action items.
- Validate all `Markdown` files in your project for consistent formatting.

### Steps
1. Define the task: what files, what check, what output format.
2. Create a validation or processing instruction file (e.g., instructions/validate-instructions.agent.md).
3. If using Approach 3 (recommended), create a script that processes each file individually.
4. If using Approach 2, write the iterative `prompt`.
5. Run the processing and review results.
6. If any results are inconsistent, review the instruction file and refine it.
7. Commit the script and results.

### ✅ Result
You have applied bulk processing to a real project task and can reuse the pattern for future batch operations.

## Summary
Remember the scenario from the introduction — 20 `Markdown` files to review, and by file 15 the AI is hallucinating content that was never there? That is context drift in action, and now you have three tools to handle it.

Single-request processing works for quick checks on 3-5 files. Iterative re-reading improves consistency but multiplies `token` cost. Script-based automation eliminates context drift entirely by giving each file a fresh `context window` — making it the best choice for repeatable operations at scale.

Key takeaways:
- Context drift causes quality degradation when processing many files in one conversation.
- Single requests work for 3-5 files; iterative re-reading works for 10-15; scripts scale to unlimited.
- Script-based automation provides consistent quality and optimal `token` usage.
- Each file processed in a fresh context = no accumulated history = no drift.
- Use the decision framework to choose the right approach for each batch task.

## Quiz
1. What is context drift and why does it matter for bulk file processing?
   a) The AI model gradually shifts its interpretation of instructions as conversation history accumulates, reducing accuracy for later files
   b) As conversation history grows, the AI's attention to original instructions decays — causing quality degradation for later files in a long conversation
   c) The AI slows down because each successive file takes longer to read into memory
   Correct answer: b.
   - (a) Incorrect. This describes a plausible-sounding mechanism, but context drift is about the `context window` filling with previous responses, not about the model reinterpreting instructions. The original instructions get diluted, not reinterpreted.
   - (b) Correct. Context drift occurs because the `context window` fills with previous responses, diluting the model's focus on the original instruction. Later files receive less accurate analysis as a result.
   - (c) Incorrect. Context drift is not about processing speed. The AI does not slow down noticeably — it continues to respond quickly, but the quality of responses degrades because earlier conversation consumes context space.

2. Why is script-based automation (Approach 3) the most efficient for processing many files?
   a) The script caches the AI's responses and reuses them for similar files, reducing `token` cost
   b) Each file is processed in a fresh context with no accumulated history, eliminating context drift and providing consistent quality without wasting `tokens` on re-reading instructions
   c) The script splits large files into smaller chunks so they fit within the `context window`
   Correct answer: b.
   - (a) Incorrect. Script automation does not cache or reuse responses — each file is processed independently with a fresh AI call. The efficiency comes from clean contexts, not from caching.
   - (b) Correct. Script automation gives each file a clean context window, avoiding both context drift (Approach 1's problem) and redundant instruction reading (Approach 2's problem).
   - (c) Incorrect. The script processes each file as a whole in its own context, not by splitting files into chunks. The key advantage is isolating each file's processing from previous files.

3. When is it acceptable to use the single-request approach (Approach 1)?
   a) When the files are well-structured and follow a consistent template
   b) When processing 3-5 files for a quick ad-hoc check where some quality loss is acceptable
   c) When the AI model has a large enough `context window` to hold all files simultaneously
   Correct answer: b.
   - (a) Incorrect. File structure does not prevent context drift. Even well-structured files cause the conversation to grow, and the AI's attention to original instructions still decays after several files.
   - (b) Correct. The single-request approach works for small batches where perfect consistency is not critical. Beyond 5 files, context drift makes the results unreliable.
   - (c) Incorrect. `Context window` size helps but does not eliminate drift. Even with large `context windows`, the model's attention distribution shifts as more content accumulates, reducing focus on the original instructions.

## Practical Task

You have processed a set of project files in bulk using an appropriate approach for your batch size.

**Submit your `report.md` for automated check:**

1. In your AI agent (`Copilot` / `Cursor` / `Claude Code`), open your project workspace and run the prompt below. The agent will inspect your project and create a `report.md` file in the project root, in the exact format the `autocheck` expects:

   ````markdown
   You are helping me prepare a submission report for an `autocheck` system. Inspect my current project workspace and create a file named `report.md` in the project root with EXACTLY the structure shown below. Replace bracketed placeholders with real values from my project. Do not add extra sections, do not omit sections, do not invent data. If a value is genuinely unknown or missing, write `N/A`.

   Source: either the bulk processing script I created OR a brief note about the non-script approach I used during Module 15. Locate the script (if any) under the project, then write `report.md`:

   # Bulk Processing Report
   - Module: 15 — Bulk File Processing
   - Repository: `[git remote URL or local path]`
   - Commit: `[short SHA of HEAD]`
   - Approach used: `[single-request | iterative | script]`
   - Script file (if any): `[relative/path/to/script | N/A]`

   ## Files Processed
   - Total files: [N]
   - File type / extension: `[.md | .json | ...]`
   - Source folder: `[relative/path]`

   ## Justification
   [Two to three sentences: why this batch size and consistency requirement led to the chosen approach. If iterative or script: explain how each file got its own context window. If single-request: explain why batching was safe.]

   ## Per-File Context Isolation
   - Each file processed in a separate `context window`: [Yes | No | N/A — single request]
   - Mechanism: [e.g., script loops and calls the agent once per file, OR new chat per file, OR N/A]
   ````

2. Submit `report.md` to the `autocheck` system (the submission endpoint is being set up in parallel; instructions for accessing it will be shared once it is available).
3. The `autocheck` system will check that:
   - The approach matches the batch size and consistency requirements from the module.
   - If a script was used, each file is processed in a separate `context window`.
   - The choice of approach is clearly justified.
