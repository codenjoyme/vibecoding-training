````markdown
# AI Skills & Tools Creation - Hands-on Walkthrough

Large Language Models are amazing at generating text, but they can hallucinate when asked to perform precise calculations or operations. The solution? Don't ask the AI to calculate—ask it to create a tool that calculates, then provide instructions on how to use it. This combination of **instruction + tool = skill** makes AI reliable for tasks beyond text generation.

## Prerequisites

- Complete [Learning from Hallucinations](../080-learning-from-hallucinations/about.md) module
- Familiar with creating and refining instruction files
- Basic understanding of scripting (Python, PowerShell, or Bash)

## Exercise Overview

You'll witness AI hallucinating simple math calculations, then create a proper tool (Python script) with instructions to handle calculations reliably. Finally, you'll learn about the emerging AgentSkills.io standard for packaging reusable skills—though using this format is optional.

## Practice Steps

1. **Create a workspace folder for this exercise**
   
   Create a new folder: `c:/workspace/hello-genai/work/090-task/` (Windows) or `~/workspace/hello-genai/work/090-task/` (macOS/Linux)
   
   Inside, create two folders:
   - `instructions/` for instruction files
   - `tools/` for your scripts

2. **Test AI's calculation abilities (observe hallucination)**
   
   Open your AI assistant (enable Agent Mode if using Claude Sonnet 4.5) and ask:
   
   ```
   Calculate the compound interest for:
   - Principal: $15,847
   - Annual interest rate: 7.34%
   - Compounded monthly
   - Time period: 8 years and 7 months
   
   Show the final amount and total interest earned.
   ```
   
   The AI will generate an answer. **Don't trust it yet.**

3. **Verify the result manually (or with a calculator)**
   
   Use a financial calculator or spreadsheet to check the result. You'll likely find the AI's answer is close but not precise—this is a hallucination. The model "dreams" plausible numbers instead of computing exact values.
   
   **Key insight:** LLMs don't calculate; they generate text that looks like calculations.

4. **Ask AI to create a calculation tool instead**
   
   Now take a different approach—delegate tool creation:
   
   ```
   Create a Python script at ./tools/compound_interest.py that calculates compound interest.
   
   Requirements:
   - Accept principal, annual_rate, compounds_per_year, and years as command-line arguments
   - Calculate final amount and interest earned
   - Print results in clear format
   - Make it reusable—no hardcoded values
   - Include usage example in comments
   ```
   
   AI will generate a parameterized Python script that performs accurate calculations.

5. **Create an instruction for using the tool**
   
   Ask AI to document how to use this tool:
   
   ```
   Following ./instructions/creating-instructions.agent.md pattern,
   create an instruction file at ./instructions/calculate-compound-interest.agent.md
   
   The instruction should describe:
   - When to use the compound interest calculator tool
   - How to invoke ./tools/compound_interest.py with proper parameters
   - Format for presenting results to the user
   - Examples of common use cases
   ```
   
   This creates the "instruction" part of the skill. The instruction tells AI **when** and **how** to use the tool.

6. **Test the skill (instruction + tool)**
   
   Now ask the same calculation question from step 2, but reference your instruction:
   
   ```
   Following ./instructions/calculate-compound-interest.agent.md,
   calculate the compound interest for:
   - Principal: $15,847
   - Annual interest rate: 7.34%
   - Compounded monthly
   - Time period: 8 years and 7 months
   ```
   
   AI will now:
   - Read the instruction file
   - Understand it should use the Python tool
   - Run the script with correct parameters
   - Present the accurate result
   
   **No hallucination—just facts.**

7. **Refine the instruction if needed**
   
   If AI doesn't use the tool correctly (e.g., passes wrong parameters), this is another hallucination moment:
   
   ```
   The tool was called incorrectly—months should be converted to years as decimal (8.583 years, not 8).
   
   Update ./instructions/calculate-compound-interest.agent.md to clarify that time period must be converted to years if given in mixed format.
   ```
   
   Let AI fix its own instruction. Then test again at step 6.

8. **Create a skills.md file (optional standard)**
   
   The [AgentSkills.io](https://agentskills.io/specification) initiative proposes a standard format for packaging skills. While not mandatory, it's useful for sharing skills across tools and teams.
   
   Ask AI:
   
   ```
   Create a skills.md file at ./skills.md following the AgentSkills.io format.
   Include the compound interest calculation skill with:
   - Clear description
   - Link to instruction file
   - Link to tool script
   - Example usage
   - Tags: finance, calculations, tools
   ```
   
   This creates a discoverable catalog of your skills. Review the [AgentSkills.io specification](https://agentskills.io/specification) to understand the format, but don't feel obligated to use it—colocating instructions and tools is often sufficient.

9. **Test portability of your skill**
   
   Try using the skill for a different calculation:
   
   ```
   Following ./instructions/calculate-compound-interest.agent.md,
   calculate compound interest for a $50,000 investment at 5.5% annual rate,
   compounded quarterly, over 10 years.
   ```
   
   The AI should invoke the tool with new parameters without modification—this proves reusability.

10. **Extend the skill with related tools**
    
    Ask AI to add more financial calculation tools:
    
    ```
    Following the same pattern, create:
    - ./tools/simple_interest.py for simple interest calculations
    - ./tools/roi_calculator.py for return on investment
    
    Update ./instructions/calculate-compound-interest.agent.md to mention all three tools
    or create separate instruction files following the creating-instructions pattern.
    ```
    
    Notice how the pattern scales: each tool is parameterized, each instruction describes usage, and together they form a growing skill library.

## Success Criteria

✅ Observed AI hallucinating calculations without tools  
✅ Created a parameterized Python script that performs accurate calculations  
✅ Created an instruction file describing when and how to use the tool  
✅ Tested the skill (instruction + tool) and verified accurate results  
✅ Refined instruction based on usage feedback (if needed)  
✅ Documented the skill in skills.md format (optional)  
✅ Verified skill works for different input parameters (reusability)  

## Key Insights

- **LLMs generate, they don't compute:** Models "dream" plausible answers rather than calculating precise values
- **Tools extend AI capabilities:** Scripts, APIs, and executables give AI "hands" to perform actions
- **Instructions guide tool usage:** Without instructions, AI might read the entire script and guess—better to be explicit
- **Parameterization enables reusability:** Never hardcode values in tools; accept them as arguments
- **Skill = Instruction + Tool:** The instruction teaches when/how; the tool performs the action
- **Colocation matters:** Keep instructions and tools together (referenced in instruction file)
- **Standards are emerging:** AgentSkills.io format is promising but not required—use what works for your team

## The AgentSkills.io Standard (Optional)

The [AgentSkills.io](https://agentskills.io/) initiative provides a unified format for packaging AI skills:

- **What it is:** A specification for describing skills in machine-readable format
- **Why it matters:** Enables sharing skills across different AI tools and platforms
- **Format:** YAML-based skills.md file with metadata, instructions, and tool references
- **Status:** Emerging standard, still evolving—check [specification](https://agentskills.io/specification) for updates
- **Recommendation:** Explore it, but don't feel obligated to adopt immediately
- **Alternative:** Simply colocate your instructions and tools as shown in this exercise

The core principle remains the same whether you use AgentSkills.io or not: **package instructions with tools to create reliable, reusable skills**.

## Troubleshooting

**Problem:** AI still tries to calculate instead of using the tool  
**Solution:** Make the instruction more explicit: "You must use the Python script at ./tools/compound_interest.py. Do not attempt manual calculation."

**Problem:** Python script fails with "command not found"  
**Solution:** Ensure Python is installed and in your PATH. On Windows, use `python` or `py`; on macOS/Linux, use `python3`.

**Problem:** AI passes parameters in wrong order or format  
**Solution:** Update the instruction file to specify exact parameter names and order with an example command.

**Problem:** Tool works but instruction file becomes too complex  
**Solution:** Split into multiple focused instructions following Single Responsibility Principle from creating-instructions.

**Problem:** Unsure whether to use AgentSkills.io format  
**Solution:** Start without it. If you build many skills and need cross-tool compatibility, adopt the standard later.

## When to Use This Approach

- Anytime AI needs to perform precise calculations (finance, engineering, statistics)
- When integrating with external APIs or services
- For file processing that requires exact transformations
- When you need reproducible, auditable results (not AI-generated guesses)
- To build a library of reusable capabilities for your team
- When onboarding new team members—skills are discoverable and documented

## Next Steps

Expand your skill library:
- Create tools for date/time calculations (AI often gets timezone math wrong)
- Build tools for data validation and transformation
- Create API integration tools with authentication
- Package domain-specific calculations relevant to your work

Each skill you create makes AI more reliable and your workflows more efficient. Over time, you'll build a personal or team-wide toolkit that extends AI far beyond text generation.

Move on to [Model Context Protocol (MCP)](../100-mcp-model-context-protocol/about.md) to learn about the next-generation standard for connecting AI to external tools and data sources.

````