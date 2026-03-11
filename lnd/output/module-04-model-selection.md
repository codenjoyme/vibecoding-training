Module 4: Model Selection

Background
Not all AI models are created equal — and not all tasks require the most powerful model. Choosing the right AI model is like choosing the right tool from a toolbox: a sledgehammer works for demolition, but you need a screwdriver for assembling furniture.

In this module, you will learn how AI model pricing works, how to select and switch models in your IDE, and a practical strategy for finding your go-to model. By the end, you will have your AI assistant configured with the optimal model and mode for productive work.

Page 1: Understanding Model Types and Pricing
Background
AI coding assistants offer multiple models with different capabilities and costs. Most IDEs use a tier system where each model interaction consumes a certain number of "premium requests" from your monthly quota. Understanding this system helps you make informed choices without worrying about unexpected costs.

Steps
1. Open your AI coding assistant (VS Code with Copilot or Cursor).
2. Navigate to Settings and find the Models or AI section.
3. Review the available models — you will typically see labels like:
   - 0x — Free tier models (no premium request cost).
   - 1x — Standard models (1 premium request per use).
   - 3x — Advanced models (3 premium requests per use).
4. The logic: higher multipliers consume quota faster but provide better quality responses.
5. Check your account settings to see your current premium request balance.

✅ Result
You can see the available models and understand the pricing tiers.

Page 2: Select Your Primary Model
Background
With many models available, it is tempting to switch constantly. Research shows this is counterproductive — each model has its own strengths and quirks, and you only learn them through sustained use. The recommended strategy is to start with the best available model and switch only when you encounter a real limitation.

Steps
1. Open the Command Palette in your IDE:
   - VS Code: Open the Copilot menu or search for "Copilot: Chat Model."
   - Cursor: Go to Settings > Models.
2. Review the available models. Recommended choices:
   - Claude Sonnet 4.5 — Best for coding tasks, excellent balance of price and quality.
   - GPT-4o — Strong general-purpose alternative.
3. Select Claude Sonnet 4.5 as your primary model.
4. Verify: The selected model should be displayed in your settings or status bar.

The practical strategy:
- Start with the best model available.
- Use it consistently while it works well.
- Switch only if it glitches, becomes unavailable, or underperforms on your tasks.
- Try the next best model, evaluate, and stay or move on.
- Most users settle on one or two models for 90% of their work.

✅ Result
Your AI assistant is configured with Claude Sonnet 4.5 (or your preferred model).

Page 3: Enable Agent Mode
Background
Your AI assistant can operate in two modes. Ask Mode is simple Q&A — it answers questions but does not take actions. Agent Mode is autonomous — it can read files, search your codebase, create files, run commands, and perform multi-step tasks. For this course, Agent Mode is essential because you will delegate real tasks to the AI.

Steps
1. In your AI assistant settings, look for mode selection (usually in the chat panel or settings).
2. Enable Agent Mode.
3. Verify by testing all three capabilities:
   - Test 1 — Ask a technical question:
     Explain the difference between async/await and promises in JavaScript
     You should receive a detailed, well-structured response.
   - Test 2 — Request code generation:
     Create a Python function that reads a CSV file and converts it to JSON
     The AI should generate working code with error handling.
   - Test 3 — Test autonomous file access:
     List the files in my current workspace and tell me what you see
     The AI should read the file system and report back (this proves Agent Mode works).

✅ Result
Agent Mode is enabled. Your AI assistant can answer questions, generate code, and interact with your file system autonomously.

Page 4: Understanding Real Costs
Background
Cost anxiety is the most common barrier to using AI coding assistants effectively. Knowing the real numbers helps you focus on productivity instead of watching a usage meter.

Real-world example from intensive usage:
- One month of daily AI-assisted work.
- Using Claude Sonnet 4.5 extensively — generating code every working day.
- Total cost: approximately $80 over the base subscription.
- That month of AI-assisted work produced more output than an entire previous year of manual work.

Most learners will not exhaust their free premium requests during this course. The productivity gain far exceeds any cost.

✅ Result
You understand real-world cost expectations and can focus on learning without cost anxiety.

Summary
In this module, you configured your AI assistant with an optimal model (Claude Sonnet 4.5) and enabled Agent Mode for autonomous task execution. You learned a practical strategy for model selection: start with the best, switch only when needed, and settle on what works for you.

Key takeaways:
- Start with the best available model (Claude Sonnet 4.5 recommended) and switch only when you hit a real limitation.
- Agent Mode is more powerful than Ask Mode — it can read files, create code, and perform multi-step tasks autonomously.
- Real costs are modest relative to productivity gains — do not let cost anxiety slow your learning.

Quiz
1. What is the recommended strategy for selecting an AI model?
   a) Switch models for every new task to find the best match
   b) Start with the best available model, use it consistently, and switch only when you encounter a real limitation
   c) Always use the cheapest model to save premium requests
   Correct answer: b. Consistent use of one model lets you learn its strengths and quirks, which is more productive than constant switching.

2. What is the difference between Ask Mode and Agent Mode?
   a) Ask Mode is slower, Agent Mode is faster
   b) Ask Mode answers questions only; Agent Mode can also read files, create code, and perform actions autonomously
   c) There is no difference — they are the same feature with different names
   Correct answer: b. Agent Mode extends the AI's capabilities beyond Q&A to include file system access, code generation, and multi-step task execution.

3. What happens when your premium request quota runs out?
   a) Your IDE stops working entirely
   b) You are limited to free-tier models or need to wait for monthly reset / purchase additional requests
   c) All your saved code is deleted
   Correct answer: b. Exhausting your quota restricts you to free models until the quota resets or is expanded.
