# Module 11: Learning from Hallucinations

### Background
You created a custom instruction in the previous module, and the AI followed it — mostly. But the quiz questions it generated have five answer options instead of three. Or the report format has an extra section you never asked for. Or the function has type hints when you explicitly said "no type hints."

These are not bugs. They are hallucinations — creative interpretations of ambiguous instructions. And they are the most valuable feedback you will ever receive, because each hallucination reveals a gap in your instructions that you can fix.

In this module, you will learn to treat hallucinations as a systematic improvement tool: observe the deviation, delegate the fix to the AI, and verify the result. You will apply this technique to improve the Jira/Confluence workflow instructions you created in Module 10.

Upon completion of this module, you will be able to:
- Interpret AI hallucinations as feedback about ambiguous or missing constraints in your instructions.
- Apply the Run → Observe → Delegate fix → Verify cycle to iteratively improve instructions.
- Delegate instruction corrections to the AI instead of editing files manually.
- Diagnose the interference problem when combining multiple instructions.

## Page 1: Hallucinations Are Feedback
### Background
When the AI produces unexpected output, the natural reaction is frustration. But a hallucination is simply the AI filling in gaps you left in your instructions. If you said "generate quiz questions" without specifying the number of answer options, the AI chose 5 because that seemed reasonable based on its training data.

This reframing is important:
- A hallucination is not the AI being wrong — it is the AI interpreting ambiguity.
- Every hallucination reveals a missing or unclear constraint in your instruction.
- Fixing the instruction prevents the same hallucination from ever happening again.
- Over time, your instructions become so precise that hallucinations become rare.

The continuous improvement cycle:
1. Run the agent using your instruction.
2. Observe the output — spot where it deviates from your expectations.
3. Stop the agent at the point of deviation.
4. Ask the agent to fix the instruction — describe what went wrong and what you expected.
5. Rerun from the previous step — verify the fix works.
6. Repeat until the instruction produces consistent output.

### ✅ Result
You understand that hallucinations are feedback about instruction gaps, not AI failures.

## Page 2: Delegate the Fix — Do Not Edit Manually
### Background
The key technique in this module is counterintuitive: when the AI produces unexpected output, you ask the AI itself to fix the instruction. You do not open the instruction file and edit it manually.

Why delegate?
- The AI maintains consistency with the existing instruction style.
- The AI understands the context of what went wrong better than a manual edit.
- The process of self-correction makes instructions more precise.
- You learn what was ambiguous by seeing how the AI interprets the fix.

The workflow:
1. Run the instruction and observe the deviation.
2. Describe the problem to the AI: "The quiz questions have 5 options, but I need exactly 3 options."
3. Ask the AI to update the instruction file: "Update ./instructions/generate-quiz.agent.md to specify exactly 3 answer options per question."
4. The AI reads the instruction, finds the ambiguity, and adds the constraint.
5. Rerun the instruction and verify the output now matches expectations.

### Steps
1. Open one of the instruction files you created in Module 10 (e.g., a Jira/Confluence workflow instruction).
2. Ask the AI to execute it: "Following ./instructions/[your-instruction].agent.md, [your task]."
3. Review the output carefully. Note anything that deviates from what you expected — format, content, structure, missing elements, extra elements.
4. If you find a deviation, do NOT edit the file manually. Instead, tell the AI: "I noticed [describe the deviation]. Please update ./instructions/[your-instruction].agent.md to prevent this in the future."
5. After the update, run the same task again and compare results.

### ✅ Result
You can delegate instruction fixes to the AI and verify the improvements.

## Page 3: The Interference Problem
### Background
When you combine multiple instructions together — or add your own prompt on top of an instruction — things can change in unexpected ways. This is the interference problem.

A single instruction works predictably in isolation. But when the AI context contains:
- Instruction A (generate report)
- Instruction B (format as table)
- Your additional prompt ("also include a summary")

...the AI must reconcile all three, and the result may differ from what any single instruction produces alone. Instructions are context-sensitive: the same instruction may behave differently depending on what else is active.

Types of instructions to be aware of:
1. Scenario instructions — step-by-step playbooks ("do this, then that").
2. Mode-switching instructions — put the agent into interactive mode ("interview me first").
3. Creation instructions — transform drafts into structured output.
4. Decorator instructions — small rules for specific corner cases.

Understanding which type you are building (or fixing) helps you keep each instruction focused.

### Steps
1. Take two of your instruction files and try combining them in a single prompt: "Following ./instructions/A.agent.md and ./instructions/B.agent.md, do [task]."
2. Compare the output to running each instruction separately.
3. If the combined result is unexpected, identify which instruction's rules were overridden.
4. Decide whether to adjust one instruction or keep them separate.

### ✅ Result
You understand the interference problem and can diagnose it when combining instructions.

## Page 4: Improve Your Jira/Confluence Instructions
### Background
Now you will apply the hallucination-fixing workflow to your practical project. In Module 10, you created instruction files for Jira/Confluence workflows. It is time to stress-test them and make them more robust.

### Steps
1. Pick one of your Jira/Confluence instruction files.
2. Ask the AI to execute it 3 times with slightly different inputs (e.g., different Jira project names, different date ranges, different report formats).
3. For each execution, note any deviations — output format, missing fields, unexpected sections, wrong data structure.
4. For each deviation, delegate the fix: "I ran this instruction with [input] and got [deviation]. Update the instruction to handle this correctly."
5. After all fixes, run the instruction once more and verify it produces consistent output across different inputs.
6. Document what you learned in a brief note in the instruction file itself or in a separate CHANGELOG section.
7. Commit the improved instruction files.

### ✅ Result
Your Jira/Confluence workflow instructions are refined through real-world testing and hallucination fixing.

## Page 5: Building Progressive Trust
### Background
As your instructions improve through iterative refinement, you start trusting the AI more. At first, you review every output line by line. After 10 consecutive runs that produce correct results, you begin to trust the process.

This trust is earned — built on:
- Precise, battle-tested instructions refined through real failures.
- Consistent results across many runs with different inputs.
- A self-correcting system where hallucinations lead to instruction improvements.

The end goal is delegation: you delegate entire workflow segments to the AI with confidence, only stepping in when the task or context changes significantly. This is the real productivity multiplier — not using AI as a chat tool, but building a reliable instruction-driven partnership.

### Steps
1. Review all your instruction files. For each one, ask yourself: "Would I trust this instruction to run without review?"
2. If the answer is "not yet," plan one more round of testing and fixing.
3. If the answer is "yes," mark it as battle-tested in your instruction catalog (main.agent.md).
4. Commit your changes.

### ✅ Result
You have a process for building trust in your instructions through iterative improvement.

## Summary
Remember the quiz with five answer options instead of three? Or the report format with that extra section you never asked for? Those surprises are no longer frustrating mysteries — they are improvement signals. Each hallucination told you exactly what was missing from your instruction, and by delegating the fix to the AI, you closed the gap permanently.

Key takeaways:
- Hallucinations are feedback, not failures. Each one reveals an ambiguity in your instruction.
- Delegate fixes to the AI — do not edit instructions manually. The AI maintains consistency.
- The improvement cycle: Run → Observe → Delegate fix → Verify → Repeat.
- Be aware of the interference problem when combining multiple instructions.
- Progressive trust is earned through iterative testing and refinement.

[MG]: Тоже можно вместо квиза сделать практическую проверку обновленного файла Instrctuions.
## Quiz
1. What does a hallucination typically reveal about your instructions?
   a) That your instruction has an ambiguity or gap that the AI filled in with its own interpretation
   b) That the AI model’s training data is outdated and it needs to be retrained on newer examples
   c) That the instruction file is too long and the AI stopped reading it before reaching the relevant rule
   Correct answer: a.
   - (a) is correct because hallucinations occur when the AI encounters ambiguity in your instructions and fills the gap with a reasonable but unintended interpretation. Fixing the ambiguity prevents the hallucination from recurring.
   - (b) is incorrect because hallucinations are not caused by stale training data. They happen because the instruction did not specify a constraint, so the AI chose a default from its general knowledge — retraining would not help.
   - (c) is incorrect because AI models do not stop reading mid-file due to length (unless the file exceeds the context window). The issue is ambiguity in the instruction, not the AI skipping content.

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
   c) When you add your own prompt alongside an instruction, the AI treats your prompt as a correction and rewrites the instruction file
   Correct answer: a.
   - (a) is correct because instructions are context-sensitive. Combining multiple instructions or adding extra prompts changes how the AI interprets each instruction, potentially producing unexpected results.
   - (b) is incorrect because referenced instructions do not override the original. Both sets of rules are active simultaneously, which is precisely what causes the reconciliation challenge.
   - (c) is incorrect because adding a prompt alongside an instruction does not rewrite the instruction file. The AI treats both as input for the current task, but the instruction file on disk remains unchanged.
