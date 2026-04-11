# Module 6: `Agent Mode` — How AI Works Under the Hood

### Background
When you click `Send` in your AI chat, what actually happens? Most people treat AI assistants as magic — type a question, get an answer. But understanding the mechanics behind agent mode transforms you from a passive user into someone who can predict, troubleshoot, and control AI behavior.

In this module, you will build a mental model of how AI coding assistants work behind the scenes: how text is generated, who the key players are, and how the agent orchestrates tools on your behalf. This knowledge is the foundation for everything that follows in the course.

Upon completion of this module, you will be able to:
- Describe how AI models generate text `token` by `token` and explain the role of temperature.
- Identify the four participants in `Agent Mode` (`User`, `Model`, `Agent System`, `Tools`) and their interactions.
- Trace the orchestration flow from `prompt` to `tool` execution to response.
- Explain why the AI `model's` context (the canvas) contains more information than what you see in the chat.

## Page 1: How AI Generates Text — Token by Token
### Background
AI `models` are sophisticated text prediction engines. They do not `think` or `understand` the way humans do — they predict the most likely next word (`token`) based on everything they have seen so far. This single concept explains most AI behavior you will observe.

Key concepts:
- A `token` is roughly one word (sometimes part of a word, sometimes punctuation).
- The `model` generates text one `token` at a time: it sees all previous text, predicts the next `token`, appends it, and repeats.
- Critically, each new `token` is predicted based on the **entire text so far** — the original user prompt plus every `token` already generated. This is why the output stays coherent and on-topic.
- All text the model can see at any moment is called the **context window** (or simply the **context**). Its size is finite — once it fills up, older content is dropped.
- Example: given `Write a function to calculate,` the model might generate `the` → `sum` → `of` → and so on.
- The `model` was trained on massive text datasets — code, documentation, books, articles — and learned patterns of how words and concepts relate.
- `Temperature` (randomness) means the same `prompt` can produce slightly different outputs each time. All outputs are valid — just varied in expression.

### Steps
1. Open your AI chat (`Copilot` or `Cursor` Chat).
2. Type the same simple prompt twice, for example: `Write a one-sentence definition of project management`
3. Compare the two responses. Notice they say the same thing in different words — this is `temperature` at work.

![Temperature at work](img/module-06/01-temperature-at-work.png)

4. Try a very specific prompt: `Define project management in exactly 10 words.` Notice the variability is much lower because you constrained the output.

### ✅ Result
You understand that AI generates text token by token and that `temperature` causes natural variation in responses.

## Page 2: The Four Players in `Agent Mode`
### Background
When you use AI in `Agent Mode`, four participants collaborate behind the scenes. Understanding their roles helps you predict behavior and troubleshoot problems.

The four players:
1. `You (User)` — type prompts, see responses, make decisions.
2. `AI Model` — (for example `Claude Sonnet 4.6`) generates text `token` by `token` on a shared canvas named `context`.
3. `Agent System` — the orchestrator built into your IDE (`VS Code` `Github Copilot` plugin or `Cursor`) that coordinates everything.
4. `Tools` — functions that can read files, edit code, run terminal commands, search the codebase, and more.

The shared canvas (`context window`):
- Imagine an invisible shared document where all four players write.
- You see only the high-level summary — technical details (tool calls, system prompts) are hidden from you.
![What user can see](image.png)
- The AI `model` sees everything on this canvas — and that text is far larger than it might seem.
![All the context](11111.png)
- In practice, the canvas already contains a lot of hidden content before you type a single word: the agent's identity and behavioral rules, a list of things it can and cannot do, and the full descriptions of every available `tool`. In the screenshot above only 9 `tools` are shown, but real projects often expose more than 50 — each with its own name, description, and parameter list taking up space in the `context window`.
- The `Agent System` manages who writes what and when.

### Steps
1. Open `Agent Mode` in your AI chat.
2. Ask the AI to create a simple file: "Create a file called `hello.txt` with the text 'Hello World' inside."
3. Watch the response. From your perspective — you asked, and a file appeared.
4. Now think about what happened behind the scenes: You wrote on the canvas → Agent System added tool descriptions → Model generated a tool call → Agent System executed it → Model confirmed to you.

### ✅ Result
You can name the four players (User, Model, Agent System, Tools) and explain how they interact on the shared canvas.

## Page 3: How the Agent Orchestrates Tool Use
### Background
The magic of agent mode is that the AI can do real things — create files, run commands, search code — not just chat. Here is the step-by-step orchestration process:

1. You write a prompt (goes on the canvas).
2. Agent System adds hidden context: available tools, workspace structure, file system capabilities.
3. Model starts generating tokens. When it "decides" a tool is needed, it writes a tool invocation in a special format.
4. Agent System intercepts the tool call (you do not see this syntax).
5. Agent System executes the tool (e.g., creates a file, runs a command).
6. The result is written back on the canvas ("File created successfully").
7. Model sees the result and continues generating its response to you.

From your perspective: you asked for a file, and it appeared.
From the Model's perspective: it suggested using a tool, saw it worked, and confirmed to you.
From the Agent System's perspective: it coordinated between you, the Model, and the tools.

### Steps
1. Give the AI a multi-step prompt: "Create a folder called 'calculator', then inside it create two files: `operations.py` with add and subtract functions, and `main.py` that imports operations and uses both functions."
2. Watch the agent work — notice multiple status updates as it makes several tool calls in sequence.

![Tools at work](img/module-06/02-tools-at-work.png)

3. Each step follows the pattern: Model suggests → Agent executes → Model sees result → Model continues.
4. Verify the folder and files were created correctly.

### ✅ Result
You can explain the orchestration process: prompt → hidden context → tool call → execution → result → response.

## Page 4: What the Model Sees vs What You See
### Background
One of the most important insights is the difference between what appears on your screen and what the AI model works with internally. The canvas contains far more information than you see.

What you see (simplified):
- Your message: "Create a file called `math_helper.py` with an add function."
- AI response: "I have created the file `math_helper.py` with an add function."

What the model sees (full canvas):
- System context with all available tools and their parameters.
- Current workspace path and file listing.
- Your message.
- The tool call it generated (create_file with path and content).
- The tool execution result ("File created successfully").
- Its response to you.

The Agent System manages this entire flow: injecting tool descriptions, detecting tool calls, executing tools, filtering what you see, and passing control between participants.

### Steps
1. Ask the AI a question about a file in your workspace: "What files are in the current directory?"
2. The AI will use a tool to list files, but you will only see the summary answer.

![More tools at work](img/module-06/03-more-tools-at-work.png)

3. Reflect: the model made a tool call, received a result, and then summarized it for you — all on the canvas you cannot see directly.

### ✅ Result
You understand that the AI model works with a richer context than what appears in your chat window.

## Page 5: Why This Matters for Your Work
### Background
Understanding the agent architecture has practical consequences for how effectively you use AI assistants:

1. The Model does not "think" — it generates text. What looks like reasoning is pattern matching from training data. This explains unexpected choices and why specificity matters.
2. `Agent Mode` extends capabilities. Without it, the model can only chat. With it, the model triggers real actions through tools.
3. Everything is sequential. The model generates one token at a time and cannot "go back." Each tool call requires a round trip: Model → Agent → Tool → Result → Model. Complex tasks take longer because of these sequential steps.
4. Context is everything. The model sees all previous text on the canvas. More context means better responses, but too much context can slow down or confuse the model.
5. Temperature explains variability. Same prompt, different results — this is normal and expected. If you need consistency, be more specific.

`Agent Mode` can: read and write files in your workspace, search for code patterns, execute terminal commands (when you approve), create directories, and refactor code across multiple files.

`Agent Mode` cannot: access files outside your workspace without permission, run commands that require elevated privileges, modify system settings, access the internet (unless you configure specific tools like `MCP`), or remember previous conversations — each session starts fresh.

### Steps
1. Think about a recent AI interaction that surprised you (unexpected result, slow response, or inconsistent behavior).
2. Using what you learned in this module, identify which mechanism explains that behavior (temperature? sequential tool calls? context overload?).
3. Try a project-relevant exercise: ask the AI in `Agent Mode` — "Create a file called `PROJECT_IDEAS.md` with 3 possible `Jira`/Confluence automation ideas for a manager. For each idea, describe the problem it solves and what data it needs." Watch the agent mode cycle as it creates the file — notice the tool calls, the sequential generation, the canvas at work.

![Generation at work](img/module-06/04-generation-at-work.png)

4. Commit any files you created during this module's exercises using the git workflow from Module 3.

### ✅ Result
You have a mental model of AI agent behavior that helps you predict and troubleshoot issues. You also have a `PROJECT_IDEAS.md` file that will feed into your project planning in Module 08.

## Summary
So — what actually happens when you click "Send"? Now you know. Your prompt lands on a shared canvas, the Agent System injects tool descriptions, the model predicts one token at a time, and when it "decides" a tool is needed, the Agent System intercepts and executes it. The result goes back to the canvas, and the model continues generating its response to you.

Key takeaways:
- AI models predict text — they do not think or plan.
- `Agent Mode` enables real actions (file creation, code execution) through tool orchestration.
- The shared canvas (context window) contains more information than you see in the chat.
- Temperature causes natural variation in responses — this is normal, not a bug.
- Understanding these mechanics makes you a more effective AI user.

## Quiz
1. What is the role of the Agent System in agent mode?
   a) It generates the text responses you see in the chat
   b) It orchestrates communication between you, the AI model, and the tools — intercepting tool calls and executing them
   c) It selects which AI model to use for each request based on task complexity
   Correct answer: b.
   - (a) is incorrect because text generation is the AI model's job, not the Agent System's. The model predicts tokens; the Agent System coordinates tool execution.
   - (b) is correct because the Agent System is the invisible coordinator that detects when the model wants to use a tool, executes the tool, and returns the result to the model.
   - (c) is incorrect because model selection is a user setting, not something the Agent System decides dynamically. You choose the model in your IDE configuration.

2. Why does the same prompt sometimes produce different results?
   a) The AI model has built-in randomness (temperature) that causes natural variation — all outputs are valid, just expressed differently
   b) The Agent System caches previous responses and returns slightly modified versions to save processing time
   c) The model's training data is updated between requests, leading to different knowledge each time
   Correct answer: a.
   - (a) is correct because temperature is a built-in feature that introduces slight randomness in token selection, producing varied but semantically equivalent responses.
   - (b) is incorrect because the Agent System does not cache or reuse previous outputs — each request triggers fresh token generation from the model.
   - (c) is incorrect because the model's training data is fixed at training time and does not change between requests. The variation comes from randomness in token selection, not from updated knowledge.

3. Why do complex multi-step tasks take longer for the AI agent to complete?
   a) Each tool call requires a sequential round trip: model generates a request, agent executes the tool, result returns to model, and the model continues — this happens for every step
   b) The model pauses to verify each step's output against its training data before proceeding
   c) The Agent System queues all tool calls and processes them in a separate background thread
   Correct answer: a.
   - (a) is correct because agent mode tasks are sequential. Each tool use involves multiple steps (model → agent → tool → result → model), and the model cannot proceed until each round trip completes.
   - (b) is incorrect because the model does not verify outputs against training data. It sees the tool result as new text on the canvas and generates the next token based on the full context.
   - (c) is incorrect because tool calls are executed in sequence, not in a background queue. The model waits for each tool result before generating the next step.
