# Agent Mode Under the Hood - Hands-on Walkthrough

In this walkthrough, you'll build a mental model of how AI coding assistants actually work behind the scenes. Understanding this will help you work more effectively with AI and troubleshoot unexpected behavior.

## Prerequisites

- Completed Module 030 (Model Selection)
- Experience using AI assistant for basic coding tasks
- Basic understanding of how AI chat interfaces work

---

## Step-by-Step Instructions

### Part 1: How the AI Model Generates Text

Let's start by understanding the fundamental mechanism of how AI models work.

**The Token-by-Token Generation:**

1. Think of AI models as highly sophisticated text prediction engines

1. The model generates text one "token" at a time
   - A token is roughly equivalent to one word (but can be part of a word, punctuation, or formatting)
   - For simplicity, think: **1 token ≈ 1 word**

1. Here's how it works in practice:
   - Model sees: "Write a function to calculate"
   - Model generates: "the" (first token)
   - Model sees: "Write a function to calculate the"
   - Model generates: "sum" (second token)
   - Model sees: "Write a function to calculate the sum"
   - Model generates: "of" (third token)
   - And so on...

1. The model sees **all previous text** every time it generates the next token

1. This is why responses take time - each word depends on analyzing all previous words

**Why the Model "Knows" What to Write:**

1. The model was trained on massive text datasets
   - Essentially everything humanity had in digital form at training time
   - Code repositories, documentation, books, articles, conversations

1. During training, the model learned how words and concepts relate to each other

1. When generating text, the model "feels" which word should come next based on patterns from training

1. The model has **temperature** (randomness/variability):
   - Same input text can produce slightly different outputs
   - Outputs are always similar in meaning, just varied in expression
   - This is why asking the same question twice gives different but equivalent answers

### Part 2: The Four Players in Agent Mode

Now let's understand who's involved when you use AI in Agent Mode.

**The Four Key Players:**

1. **You (User)** - You type prompts and see responses

1. **AI Model** - Generates text token by token on a shared "canvas"

1. **Agent System** - The orchestrator built into your IDE (VS Code or Cursor)

1. **Tools** - Functions that can read files, edit code, run commands, search, etc.

**The Shared Canvas:**

1. Imagine there's an invisible shared document - the "canvas of narrative"

1. All four players take turns writing text on this canvas

1. The AI Model sees **everything** on the canvas

1. You (User) see only **part** of what's on the canvas - the meaningful high-level information

1. Low-level technical details are hidden from you but visible to the model

### Part 3: How Agent System Orchestrates Tool Use

This is where the magic happens - how your prompt becomes actual file edits or code execution.

**The Orchestration Process:**

1. **Step 1: You write a prompt**
   - Example: "Create a Python file that prints Hello World"
   - This goes on the canvas

1. **Step 2: Agent System adds hidden context**
   - Agent System writes on the canvas (invisible to you):
     * Available tools and how to use them
     * Current workspace structure
     * File system capabilities
     * Terminal access
   - The Model sees all this additional context

1. **Step 3: Model starts generating response**
   - Model generates tokens one by one
   - Model might "decide" to use a tool based on your request
   - Model writes tool invocation syntax on the canvas

1. **Step 4: Agent System intercepts tool use**
   - Agent System recognizes the Model is trying to use a tool
   - Agent System doesn't show you this technical syntax
   - Agent System executes the tool on behalf of the Model

1. **Step 5: Tool execution result returns**
   - Tool executes (e.g., creates the file)
   - Result is written on the canvas: "File created successfully at path/to/file.py"
   - Model sees this result

1. **Step 6: Model continues generation**
   - Model sees the tool execution was successful
   - Model continues generating its response to you
   - Model writes: "I've created a Python file with a Hello World program"
   - You see this final message

**Key Insight:**

- From your perspective: You asked for a file, and it appeared
- From the Model's perspective: It suggested using a tool, saw it worked, confirmed to you
- From Agent System's perspective: It coordinated between you, the Model, and tools

### Part 4: Understanding the Conversation Canvas

Let's visualize what the canvas looks like from different perspectives.

**What YOU see (simplified):**

```
You: Create a new file called math_helper.py with a function to add two numbers

AI: I've created the file math_helper.py with an add function.
```

**What the MODEL sees (full canvas):**

```
[System Context - Available Tools]
Tool: create_file
Parameters: filePath, content
Description: Creates a new file with specified content

Tool: read_file  
Parameters: filePath
Description: Reads content of existing file

[Current Workspace]
Path: c:/workspace/hello-genai/
Files: [empty directory]

[User Message]
Create a new file called math_helper.py with a function to add two numbers

[Agent System - Tool Execution Request]
<tool_call>
  <tool>create_file</tool>
  <filePath>c:/workspace/hello-genai/math_helper.py</filePath>
  <content>
def add(a, b):
    """Add two numbers and return the result."""
    return a + b
  </content>
</tool_call>

[Agent System - Tool Result]
✓ File created successfully: math_helper.py

[Model Response to User]
I've created the file math_helper.py with an add function.
```

**What the AGENT SYSTEM manages:**

- Injecting tool descriptions into the canvas
- Detecting when Model wants to use a tool
- Executing tools and returning results
- Filtering what User sees vs what Model sees
- Passing control between User → Model → Tools → Model → User

### Part 7: Why This Matters for Effective Vibecoding

Understanding this architecture helps you work better with AI:

**1. The Model Doesn't "Think" - It Generates Text**

- The model doesn't have intentions or plans
- It predicts the next most likely token based on all previous tokens
- What looks like "reasoning" is actually pattern matching from training data
- This explains why AI sometimes makes unexpected choices

**2. Agent Mode = Extended Capabilities**

- Without Agent Mode: Model can only chat (generate text you see)
- With Agent Mode: Model can trigger real actions through tools
- Agent System is the bridge between text generation and actual file operations

**3. Everything is Sequential**

- Model generates one token at a time
- Model can't "go back" and revise (it can only generate new tokens that correct previous ones)
- Each tool use requires:
  1. Model generates tool request
  2. Agent executes tool
  3. Result goes back to Model
  4. Model continues generation
- This is why complex tasks take longer

**4. Context is Everything**

- Model sees ALL previous text on the canvas
- More context = better responses (but slower generation)
- This is why Agent System carefully manages what goes on the canvas
- Too much context can slow down or confuse the model

**5. Temperature Explains Variability**

- Same prompt can give different solutions
- All solutions are valid, just expressed differently
- If you don't like a response, try asking again - you'll get a variation
- Lower temperature = more predictable, higher = more creative

### Part 6: Advanced Exercise - Multi-Step Orchestration

Let's do a multi-step task to see the orchestration in action.

1. In VS Code/Cursor, open AI chat with Agent Mode enabled

1. Give this complex prompt:
   ```
   Create a folder called 'calculator', then inside it create two files:
   1. operations.py with add and subtract functions
   2. main.py that imports operations and uses both functions
   ```

1. **Watch the agent work:**
   - Notice multiple status updates
   - Agent is making multiple tool calls
   - Each tool call: Model suggests → Agent executes → Model sees result → Model continues

1. **Think about what's happening:**
   - Model sees your request
   - Model generates: "I'll create a directory using the create_directory tool..."
   - Agent intercepts and creates the directory
   - Model sees: "Directory created successfully"
   - Model generates: "Now I'll create the first file..."
   - Agent intercepts and creates operations.py
   - Model sees: "File created successfully"
   - Model generates: "Now I'll create the second file..."
   - Agent intercepts and creates main.py
   - Model sees: "File created successfully"
   - Model generates final message to you: "I've created the calculator folder with both files"

1. Verify the folder structure was created correctly

1. **Key observation:**
   - One prompt resulted in multiple tool calls
   - Each tool call was orchestrated by the Agent System
   - Model coordinated the sequence by seeing results of previous tools
   - You only saw the beginning and end, not the middle steps

---

## Success Criteria

Congratulations! You've successfully completed this module if:

✅ You understand that AI models generate text one token at a time  
✅ You know what "temperature" means and why responses vary  
✅ You can explain the four players: User, Model, Agent System, and Tools  
✅ You understand the "canvas" concept where all players interact  
✅ You know how Agent System orchestrates tool calls  
✅ You've observed multi-step orchestration in action  
✅ You understand why Agent Mode enables real actions vs just chat  
✅ You have a mental model of what happens behind the scenes

## Troubleshooting

**Agent seems slow or stuck?**
- Model is generating tokens one by one
- Complex tasks require multiple tool calls in sequence
- Each tool call adds time (Model → Agent → Tool → Result → Model)
- This is normal - agent is working, not stuck

**Agent does something unexpected?**
- Model predicted a different token sequence than you expected
- Based on training patterns, that sequence seemed appropriate
- Try rephrasing your prompt to be more specific
- Remember: model doesn't "understand" intent, it predicts text patterns
- You'll learn advanced prompting techniques in the next module

**Want to see what tools were actually called?**
- Some IDEs show tool call logs or execution history
- Check the output panel or logs in VS Code/Cursor
- This shows the "hidden" part of the canvas

**Results vary between attempts?**
- This is temperature at work - built-in randomness
- Model doesn't give identical outputs for identical inputs
- All variations should be valid solutions to your prompt

## Understanding Agent Limitations

**What Agent Mode CAN do:**
- Read and write files in your workspace
- Search for code patterns
- Execute terminal commands (when permitted)
- Create directories and manage file structure
- Refactor code across multiple files

**What Agent Mode CANNOT do:**
- Access files outside workspace without permission
- Run commands that require elevated privileges (unless you approve)
- Modify system settings
- Access the internet (unless using specific tools/MCP)
- "Remember" previous conversations (each session starts fresh)

## Next Steps

Now that you understand how AI works under the hood, you're ready to learn advanced prompting techniques to communicate more effectively with AI in the next module!5