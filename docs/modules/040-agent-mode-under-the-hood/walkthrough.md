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

### Part 4: Understanding Temperature and Prompt Precision

Before we practice, let's understand two critical concepts that affect AI behavior.

**Temperature: The Source of Variability**

1. Remember that the model has built-in randomness called "temperature"

1. This means the **same prompt will produce different results** each time

1. Temperature can be both helpful and problematic:
   - **Helpful:** Gives you creative variations and alternative approaches
   - **Problematic:** Can cause hallucinations and inconsistent results
   - **Important:** You can control this by how you write your prompts!

**The Artist Metaphor:**

Imagine you ask 10 world-class artists to paint a still life:

1. **Very abstract prompt:** "Paint a still life"
   - Result: 10 completely different masterpieces
   - Each is professional, but wildly different subjects, styles, compositions
   - This is like asking AI: "Write a function"

1. **Slightly more specific:** "Paint a still life with a vase of flowers and a fruit on the left"
   - Result: 10 paintings with similarities, but each artist chooses different flowers and fruits
   - Some paint roses with an apple, others tulips with an orange
   - This is like: "Write a sorting function in Python"

1. **Very specific:** "Paint a still life with a vase of lilacs and a pear on the left, on a wooden table, with soft morning light"
   - Result: 10 very similar paintings - nearly identical compositions
   - Minor variations in brushstroke style, but recognizably the same scene
   - This is like: "Write a bubble sort function in Python that takes a list of integers, sorts in-place, and returns None"

**The Power of Statements:**

1. When you write a prompt, structure it as **statements** - one sentence per requirement

1. Each statement adds one specific aspect of what you want:
   - Statement 1: What to create (function, file, class)
   - Statement 2: What it should do (sort, calculate, parse)
   - Statement 3: Technical details (algorithm, language)
   - Statement 4: Constraints (no comments, specific format)
   - Statement 5: Edge cases or examples

1. **More statements = more precise results = less variability**

**Language and Terms Matter:**

1. You can write prompts in any language - English, Russian, even with typos
   - Model understands: "напиши функцыю сортування" = "write sorting function"
   - Model handles Surzhyk, misspellings, informal language

1. BUT specific **technical terms have huge impact:**
   - "Python" vs "Java" → completely different code
   - "bubble sort" vs "quicksort" → different algorithms
   - "function" vs "class" → different code structure

1. **When model seems "dumb", you're probably being too abstract**
   - Model is incredibly smart, but needs specificity
   - Vague prompts → diverse results (high temperature effect)
   - Specific prompts → consistent results (controlled temperature)

### Part 5: Practical Exercise - Controlling Model Output

Let's practice controlling the model's variability through prompt refinement.

**The Iterative Refinement Technique:**

1. Open VS Code or Cursor with your `./workspace/hello-genai/` workspace

1. Open the AI chat panel

1. Make sure Agent Mode is enabled (see Module 030 if needed)

**Round 1: Abstract Prompt**

1. Type this very abstract prompt:
   ```
   Create a file with sorting function
   ```

1. Press Enter and wait for the model to complete

1. Observe the result - check what file was created and what's inside

1. **What you'll see:**
   - Model might choose any language (Python, JavaScript, Java)
   - Model might use any sorting algorithm (quicksort, merge sort, bubble sort)
   - Model might add tests, examples, comments
   - **This is temperature at work - maximum variability**

**Round 2: Edit the Original Prompt**

1. **Important:** Don't write a new message - go back and EDIT your first message

1. Change it to:
   ```
   Create a file with bubble sort function
   ```

1. Press Enter again

1. **What happens:**
   - Agent deletes the old file
   - Agent creates a new file with new content
   - This is the key skill - editing prompts to regenerate results

1. Observe the new result - still variability in language, structure, extras

**Round 3: Continue Refining**

1. Edit the prompt again:
   ```
   Create a file with bubble sort function in Python
   ```

1. Press Enter, observe the result

1. Notice: Results getting more consistent, but still variations in:
   - Variable names
   - Comments and docstrings
   - Test code inclusion
   - Type hints

**Round 4: Add More Constraints**

1. Edit the prompt again:
   ```
   Create a Python file with bubble sort function. Only the function, no tests, no examples.
   ```

1. Press Enter, observe the result

1. Getting closer, but might still have:
   - Docstrings
   - Type hints
   - Different function signatures

**Round 5: Maximum Precision**

1. Edit the prompt one more time:
   ```
   Create a Python file named bubble_sort.py with a bubble sort function. 
   Function name: bubble_sort
   Parameter: numbers (list of integers)
   Return: sorted list
   No docstrings, no type hints, no comments.
   ```

1. Press Enter, observe the result

1. **Now try this experiment:**
   - Delete the file manually
   - Run the SAME precise prompt again
   - Compare results - they should be nearly identical!

**Round 6: Test Consistency**

1. Repeat the precise prompt 2-3 more times

1. Each time, compare the generated code

1. You should see:
   - Same file name
   - Same function name
   - Same basic algorithm structure
   - Minor variations in variable names (i, j vs idx, jdx)
   - But essentially the same code

**Key Observations:**

1. **Abstract prompts → High variability**
   - "sorting function" could be anything
   - Model's temperature creates diverse solutions

1. **Specific prompts → Low variability**
   - Detailed statements constrain the model
   - Less room for temperature to affect outcome

1. **Editing prompts vs new messages**
   - Editing: Forces fresh start, clean slate
   - New messages: Builds on previous context (different behavior)
   - For precise control: Edit the original prompt

1. **Each word matters**
   - "bubble sort" locks algorithm choice
   - "Python" locks language choice
   - "no comments" removes extra text
   - Every statement reduces variability

### Part 6: Understanding the Conversation Canvas

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

### Part 8: Advanced Exercise - Multi-Step Orchestration

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
✅ You've practiced iterative prompt refinement technique  
✅ You understand that abstract prompts cause variability, specific prompts give consistency  
✅ You know the power of statements - one sentence per requirement  
✅ You've learned to EDIT prompts instead of sending new messages for precise control  
✅ You understand why Agent Mode enables real actions vs just chat  
✅ You have a mental model of what happens behind the scenes

## Troubleshooting

**Agent seems slow or stuck?**
- Model is generating tokens one by one
- Complex tasks require multiple tool calls in sequence
- Each tool call adds time (Model → Agent → Tool → Result → Model)
- This is normal - agent is working, not stuck

****You're probably being too abstract** - add more specific statements
- Remember: model doesn't "understand" intent, it predicts text patterns
- Solution: Edit your prompt with more constraints and try again

**Getting different results each time?**
- This is temperature working - built-in randomness
- **Solution: Add more specific statements to your prompt**
- More details = less room for variability
- Use the "artist painting still life" mental model
- Each additional constraint narrows the solution space
- Based on training patterns, that sequence seemed appropriate
- Try rephrasing your prompt or being more specific
- Remember: model doesn't "understand" intent, it predicts text patterns

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

Now that you understand how AI works under the hood, you're ready to learn advanced prompting techniques to communicate more effectively with AI in the next module!