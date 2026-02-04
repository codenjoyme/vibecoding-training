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
   
   Create a new folder to practice in: `c:/workspace/instruction-refinement/` (Windows) or `~/workspace/instruction-refinement/` (macOS/Linux)
   
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
