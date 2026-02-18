# Learning from Hallucinations - Hands-on Walkthrough

When AI generates something unexpected, it's not always an error—it's often a creative interpretation of ambiguous instructions. Instead of manually fixing instructions every time, you'll learn to leverage AI itself to improve its own guidance documents. This approach ensures consistency and saves time while building a self-improving instruction system.

## Prerequisites

- Complete [Custom Instructions](../070-custom-instructions/about.md) module
- Familiar with creating and organizing instruction files
- Understanding of how AI agents work with instructions

## Exercise Overview

You'll create a new instruction file for generating quiz questions, discover where the AI interpretation diverges from your intent, then delegate to the AI to fix its own instruction—without manual editing. This mirrors real-world scenarios where instructions need refinement based on actual usage.

## Practice Steps

1. **Create a workspace folder for this exercise**
   
   Create a new folder to practice in: `c:/workspace/hello-genai/work/080-task/` (Windows) or `~/workspace/hello-genai/work/080-task/` (macOS/Linux)
   
   Inside, create an `instructions/` folder for your instruction files.

2. **Ask AI to generate a quiz creation instruction**
   
   Open your AI assistant (enable Agent Mode if using Claude Sonnet 4.5) and prompt:
   
   ```
   Following the instruction for creating instructions at ./instructions/creating-instructions.agent.md,
   create a new instruction for generating multiple-choice quiz questions on technical topics.
   The instruction should be saved in ./instructions/generate-quiz.agent.md
   ```
   
   AI will read the creating-instructions pattern and generate a new instruction file.

3. **Test the newly created instruction**
   
   Now ask AI to use its own instruction:
   
   ```
   Following ./instructions/generate-quiz.agent.md, create 3 quiz questions about Git branching strategies.
   ```
   
   Review the output carefully. Look for:
   - Are there exactly 3 questions?
   - Is the format consistent?
   - Are the answer explanations included?
   - Is the difficulty level appropriate?

4. **Identify the hallucination/deviation**
   
   You'll likely notice something unexpected. Common deviations:
   - AI might include 4-5 answer options when you wanted 3
   - Questions might be too basic or too advanced
   - Format might not match your expectations
   - Missing elements like point values or time estimates
   
   **Stop here.** This is your "hallucination moment"—the AI interpreted the instruction differently than you intended.

5. **Delegate the fix to the AI agent**
   
   Instead of editing `generate-quiz.agent.md` manually, ask the AI:
   
   ```
   I noticed the quiz questions include 5 answer options, but I need exactly 4 options per question
   with one correct answer. Also, each question should include a point value (1-3 points based on difficulty).
   
   Please update ./instructions/generate-quiz.agent.md to clarify these requirements so this won't happen again.
   ```
   
   The AI will read its own instruction, identify where ambiguity exists, and add specific constraints.

6. **Verify the fix by regenerating**
   
   Return to step 3 and run the same quiz generation request again:
   
   ```
   Following ./instructions/generate-quiz.agent.md, create 3 quiz questions about Git branching strategies.
   ```
   
   Compare the new output with the previous attempt. The format should now match your expectations precisely.

7. **Refine further if needed**
   
   If you spot another deviation:
   - Point it out to the AI
   - Ask it to update the instruction file again
   - Regenerate and verify
   
   This iterative refinement builds robust instructions without manual editing.

8. **Check instruction consistency**
   
   Ask AI to compare the updated instruction with the original creating-instructions pattern:
   
   ```
   Does ./instructions/generate-quiz.agent.md follow the same style and structure as ./instructions/creating-instructions.agent.md?
   If not, please align them.
   ```
   
   This ensures all your instructions maintain a consistent format—important when you have dozens of instruction files.

## Success Criteria

✅ Created a new instruction file using AI delegation  
✅ Identified where AI output deviated from expectations  
✅ Delegated instruction correction to the AI agent (no manual edits)  
✅ Verified that regenerated output matches requirements  
✅ Ensured instruction follows consistent style from creating-instructions pattern  

## Key Insights

- **Hallucinations are feedback:** Every unexpected output reveals ambiguity in your instructions
- **Delegate, don't edit:** Let AI improve its own instructions using the creating-instructions pattern as reference
- **Iterate rapidly:** Test → Identify deviation → Delegate fix → Retest
- **Maintain consistency:** Always reference your creating-instructions file to keep style uniform
- **Build once, use forever:** Refined instructions work reliably across all future requests

## Deep Dive: Instructions as a Programming Paradigm

Understanding how instructions really work will fundamentally change your approach to AI-assisted development. This section covers the conceptual framework that makes instruction-driven workflows powerful.

### Instructions Are Like Classes and Functions

Think of an instruction file as a **class or function in a programming language**. It stores context and produces repeatable results. Just like functions in code, instructions follow the **Single Responsibility Principle** — each instruction does one thing well. When an instruction handles a single responsibility effectively, it becomes reliable and predictable.

### The Interference Problem

When 3 separate instructions each work independently, they each function as one isolated process and behave predictably. However, when you **combine them together** and add your own prompt on top, everything can change fundamentally. Your prompt acts as a modifier that can shift how the agent interprets each instruction.

This is a critical insight: instructions are **context-sensitive**. The same instruction may produce different results depending on what other instructions or prompts are active at the same time. Be mindful of this when chaining multiple instructions together.

### Types of Instructions

In a mature instruction-driven system, you'll typically have several categories of instructions:

1. **Scenario instructions** — Step-by-step descriptions of actions. These are your "what to do" playbooks (e.g., a module walkthrough with concrete steps).
2. **Mode-switching instructions** — Instructions that put the agent into an interactive coaching or review mode, where it follows a scenario interactively rather than executing it all at once.
3. **Creation instructions** — Instructions that transform rough drafts, raw prompts, or semi-structured input into polished, structured output (e.g., turning notes into a complete training module).
4. **Decorator instructions** — Small, focused instructions for specific corner cases or formatting rules. They augment other instructions without replacing them.

Understanding which type you're building (or fixing) helps you keep each instruction focused and maintainable.

### The Continuous Improvement Cycle

The hallucination-fixing workflow is not a one-time trick — it's a **continuous improvement process** that makes your instructions better over time:

1. **Run** the agent using your instruction
2. **Observe** the output — spot where it deviates from your expectations
3. **Stop** the agent at the point of deviation
4. **Ask the agent to fix the instruction** — describe what went wrong and what you expected
5. **Rerun from the previous step** — verify the fix actually works at the exact point where it previously failed
6. **Repeat** until the instruction produces consistently correct output

Each cycle makes the instruction more precise. Over time, the agent becomes **more autonomous** in that part of the workflow because the instruction leaves less room for misinterpretation.

### Building Progressive Trust

As your instructions improve through iterative refinement, something interesting happens: you start **trusting the agent more and more**. At first, you carefully review every output. But after 10 consecutive code reviews that show nothing suspicious, you begin to trust the process.

This trust is earned — it's built on a foundation of:
- Precise, battle-tested instructions that have been refined through real failures
- Consistent results across many runs
- A track record of the agent self-correcting when given clear feedback

The end goal is a system where you can **delegate entire workflow segments** to the agent with confidence, only stepping in when the task or context changes significantly. This is the real productivity multiplier — not just using AI as a tool, but building a reliable, self-improving partnership.

## Understanding Check

1. **Why are instructions compared to classes or functions in programming?**
   - Because they store context, produce repeatable results, and follow the Single Responsibility Principle — each instruction handles one well-defined responsibility.

2. **What is the "interference problem" with instructions?**
   - When multiple instructions work independently they behave predictably, but combining them together with an additional prompt can fundamentally change how the agent interprets each one. Instructions are context-sensitive.

3. **Name the four types of instructions and their roles.**
   - **Scenario** — step-by-step action playbooks; **Mode-switching** — put the agent into interactive coaching mode; **Creation** — transform rough drafts into structured output; **Decorator** — small focused instructions for corner cases.

4. **What are the 6 steps of the continuous improvement cycle?**
   - Run → Observe → Stop → Ask agent to fix the instruction → Rerun from the failure point → Repeat until consistent.

5. **Why should you delegate instruction fixes to the agent instead of editing manually?**
   - The agent maintains consistency with existing instruction patterns, understands the context better, and the process of self-correction makes the instruction more precise while building your trust in autonomous workflows.

6. **How is progressive trust with the AI agent built?**
   - Through iterative refinement: as instructions get battle-tested through real failures and produce consistent results across many runs, you gradually trust the agent to handle larger workflow segments independently.

7. **What should you do when you notice a deviation in AI output?**
   - Stop the agent immediately, describe the deviation and expected behavior, ask the agent to update the instruction, then rerun from the previous step to verify the fix at the exact point of failure.

## Troubleshooting

**Problem:** AI says it can't read the instruction file  
**Solution:** Verify the file path is correct and the file exists. Use absolute paths if needed.

**Problem:** AI's fix doesn't fully resolve the issue  
**Solution:** Be more specific about what you need. Instead of "fix the format," say "each question must have exactly 4 options labeled A-D."

**Problem:** Updated instruction breaks other functionality  
**Solution:** Ask AI to review the change and ensure it doesn't conflict with other requirements. Request a rollback if needed.

**Problem:** Instruction file becomes too long and complex  
**Solution:** Ask AI to split it into multiple focused instructions following Single Responsibility Principle.

## When to Use This Approach

- Whenever AI output surprises you or diverges from expectations
- When building a library of reusable instruction files
- During team onboarding—capture tribal knowledge as instructions
- When the same type of mistake happens repeatedly
- To standardize outputs across different team members using AI

## Next Steps

Practice this with other scenarios:
- Create an instruction for code review comments
- Create an instruction for generating test cases
- Create an instruction for writing documentation

Each time you refine an instruction, you're building a more intelligent system. Your instruction library becomes a knowledge base that grows more precise with every use.

Move on to [AI Skills & Tools Creation](../090-ai-skills-tools-creation/about.md) to learn how to package instructions into reusable tools.
