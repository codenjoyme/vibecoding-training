Module 6: Agent Mode — How AI Works Under the Hood

Background
When you click "Send" in your AI chat, what actually happens? Most people treat AI assistants as magic — type a question, get an answer. But understanding the mechanics behind agent mode transforms you from a passive user into someone who can predict, troubleshoot, and control AI behavior.

In this module, you will build a mental model of how AI coding assistants work behind the scenes: how text is generated, who the key players are, and how the agent orchestrates tools on your behalf. This knowledge is the foundation for everything that follows in the course.

Page 1: How AI Generates Text — Token by Token
Background
AI models are sophisticated text prediction engines. They do not "think" or "understand" the way humans do — they predict the most likely next word based on everything they have seen so far. This single concept explains most AI behavior you will observe.

Key concepts:
- A token is roughly one word (sometimes part of a word, sometimes punctuation).
- The model generates text one token at a time: it sees all previous text, predicts the next token, appends it, and repeats.
- Example: given "Write a function to calculate," the model might generate "the" → "sum" → "of" → and so on.
- The model was trained on massive text datasets — code, documentation, books, articles — and learned patterns of how words and concepts relate.
- Temperature (randomness) means the same prompt can produce slightly different outputs each time. All outputs are valid — just varied in expression.

Steps
1. Open your AI chat (Copilot Chat or Cursor Chat).
2. Type the same simple prompt twice, for example: "Write a one-sentence definition of project management."
3. Compare the two responses. Notice they say the same thing in different words — this is temperature at work.
4. Try a very specific prompt: "Define project management in exactly 10 words." Notice the variability is much lower because you constrained the output.

✅ Result
You understand that AI generates text token by token and that temperature causes natural variation in responses.

Page 2: The Four Players in Agent Mode
Background
When you use AI in Agent Mode, four participants collaborate behind the scenes. Understanding their roles helps you predict behavior and troubleshoot problems.

The four players:
1. You (User) — type prompts, see responses, make decisions.
2. AI Model — generates text token by token on a shared "canvas."
3. Agent System — the orchestrator built into your IDE (VS Code or Cursor) that coordinates everything.
4. Tools — functions that can read files, edit code, run terminal commands, search the codebase, and more.

The shared canvas (context window):
- Imagine an invisible shared document where all four players write.
- The AI Model sees everything on this canvas.
- You see only the high-level summary — technical details (tool calls, system prompts) are hidden from you.
- The Agent System manages who writes what and when.

Steps
1. Open Agent Mode in your AI chat.
2. Ask the AI to create a simple file: "Create a file called hello.txt with the text 'Hello World' inside."
3. Watch the response. From your perspective — you asked, and a file appeared.
4. Now think about what happened behind the scenes: You wrote on the canvas → Agent System added tool descriptions → Model generated a tool call → Agent System executed it → Model confirmed to you.

✅ Result
You can name the four players (User, Model, Agent System, Tools) and explain how they interact on the shared canvas.

Page 3: How the Agent Orchestrates Tool Use
Background
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

Steps
1. Give the AI a multi-step prompt: "Create a folder called 'calculator', then inside it create two files: operations.py with add and subtract functions, and main.py that imports operations and uses both functions."
2. Watch the agent work — notice multiple status updates as it makes several tool calls in sequence.
3. Each step follows the pattern: Model suggests → Agent executes → Model sees result → Model continues.
4. Verify the folder and files were created correctly.

✅ Result
You can explain the orchestration process: prompt → hidden context → tool call → execution → result → response.

Page 4: What the Model Sees vs What You See
Background
One of the most important insights is the difference between what appears on your screen and what the AI model works with internally. The canvas contains far more information than you see.

What you see (simplified):
- Your message: "Create a file called math_helper.py with an add function."
- AI response: "I have created the file math_helper.py with an add function."

What the model sees (full canvas):
- System context with all available tools and their parameters.
- Current workspace path and file listing.
- Your message.
- The tool call it generated (create_file with path and content).
- The tool execution result ("File created successfully").
- Its response to you.

The Agent System manages this entire flow: injecting tool descriptions, detecting tool calls, executing tools, filtering what you see, and passing control between participants.

Steps
1. Ask the AI a question about a file in your workspace: "What files are in the current directory?"
2. The AI will use a tool to list files, but you will only see the summary answer.
3. Reflect: the model made a tool call, received a result, and then summarized it for you — all on the canvas you cannot see directly.

✅ Result
You understand that the AI model works with a richer context than what appears in your chat window.

Page 5: Why This Matters for Your Work
Background
Understanding the agent architecture has practical consequences for how effectively you use AI assistants:

1. The Model does not "think" — it generates text. What looks like reasoning is pattern matching from training data. This explains unexpected choices and why specificity matters.
2. Agent Mode extends capabilities. Without it, the model can only chat. With it, the model triggers real actions through tools.
3. Everything is sequential. The model generates one token at a time and cannot "go back." Each tool call requires a round trip: Model → Agent → Tool → Result → Model. Complex tasks take longer because of these sequential steps.
4. Context is everything. The model sees all previous text on the canvas. More context means better responses, but too much context can slow down or confuse the model.
5. Temperature explains variability. Same prompt, different results — this is normal and expected. If you need consistency, be more specific.

Steps
1. Think about a recent AI interaction that surprised you (unexpected result, slow response, or inconsistent behavior).
2. Using what you learned in this module, identify which mechanism explains that behavior (temperature? sequential tool calls? context overload?).
3. Commit any files you created during this module's exercises using the git workflow from Module 3.

✅ Result
You have a mental model of AI agent behavior that helps you predict and troubleshoot issues.

Summary
In this module, you learned how AI coding assistants work under the hood. The AI model generates text one token at a time, predicting each word from all previous context. In Agent Mode, four players collaborate: You, the Model, the Agent System, and Tools. The Agent System orchestrates tool calls invisibly, showing you only the high-level results while the model works with a richer shared canvas.

Key takeaways:
- AI models predict text — they do not think or plan.
- Agent Mode enables real actions (file creation, code execution) through tool orchestration.
- The shared canvas (context window) contains more information than you see in the chat.
- Temperature causes natural variation in responses — this is normal, not a bug.
- Understanding these mechanics makes you a more effective AI user.

Quiz
1. What is the role of the Agent System in agent mode?
   a) It generates the text responses you see in the chat
   b) It orchestrates communication between you, the AI model, and the tools — intercepting tool calls and executing them
   c) It stores your conversation history permanently
   Correct answer: b. The Agent System is the invisible coordinator that detects when the model wants to use a tool, executes the tool, and returns the result to the model.

2. Why does the same prompt sometimes produce different results?
   a) The AI model is unreliable and makes random errors
   b) The model has built-in randomness (temperature) that causes natural variation — all outputs are valid, just expressed differently
   c) Your internet connection affects the quality of responses
   Correct answer: b. Temperature is a built-in feature that introduces slight randomness in token selection, producing varied but equivalent responses.

3. Why do complex multi-step tasks take longer for the AI agent to complete?
   a) The AI model needs to rest between tasks
   b) Each tool call requires a sequential round trip: model generates a request, agent executes the tool, result returns to model, and the model continues — this happens for every step
   c) The agent is downloading additional data from the internet
   Correct answer: b. Agent mode tasks are sequential. Each tool use involves multiple steps, and the model cannot parallelize them — it generates one token at a time.
