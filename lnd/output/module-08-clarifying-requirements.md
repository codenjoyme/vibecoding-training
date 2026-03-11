Module 8: Clarifying Requirements Before Start

Background
You have a general idea — "I want to automate my weekly status reports" — but when you sit down to write a prompt, you get stuck after two sentences. You know you need more details, but you cannot think of what to specify. Your head feels empty.

This is the most common blocker for non-developers starting an automation project. The good news: the AI itself can solve this problem. Instead of asking the AI to implement something immediately, you ask it to interview you first. Through that conversation, the AI extracts the details you did not know you had.

In this module, you will learn the interview technique and use it to create a Technical Specification (ТЗ) for your Jira/Confluence automation project — the central artifact for the rest of the course.

Page 1: The Empty Head Problem
Background
When you start writing a detailed prompt, you often reach a point where you run out of things to specify. This happens for three reasons:

1. You are not an expert in everything — you may not know all the technical decisions that need to be made, what edge cases exist, or what best practices apply.
2. You have implicit assumptions — things that seem obvious to you but need to be stated explicitly for the AI.
3. You are starting from scratch — an empty project without context means you need to define everything, and it is hard to know where to begin.

This is not a personal failure. Professionals across all fields face this — requirements elicitation is an entire discipline in software engineering.

Steps
1. Open a text editor or your AI chat.
2. Try writing a detailed prompt for this task: "Automate my weekly status report."
3. Write as many specific statements as you can.
4. Notice where you get stuck. What questions arise that you cannot answer? (Format? Source of data? Who receives it? What sections? How often?) Write them down — you will use them later.

✅ Result
You have experienced the "empty head" problem firsthand and identified questions you could not answer on your own.

Page 2: The Interview Mode Pattern
Background
The solution is a single phrase that transforms the AI from an implementer into a requirements analyst:

"Before we start, ask me clarifying questions."

When you add this to the end of even a minimal prompt, the AI stops and interviews you. Instead of guessing and generating something immediately, it asks the questions you should have thought of but did not.

Why this works:
- The AI knows what information is needed for implementation (it has seen thousands of similar projects in its training data).
- The AI can identify gaps in your requirements.
- Your answers fill in the missing details naturally.
- The context window accumulates precise information through dialogue rather than through guessing.

Steps
1. Open your AI chat in Agent Mode.
2. Type a minimal prompt:
   "I want to automate my weekly status report for stakeholders. Before we start, ask me clarifying questions."
3. Send it. The AI will ask several questions — about format, data sources, audience, frequency, sections, and so on.
4. Answer the questions honestly. If you do not know the answer, say so — the AI will suggest options.
5. After answering, type: "Are there any more questions?"
6. Repeat until the AI says it has enough information.

✅ Result
You have used the interview technique to transform a vague idea into a set of specific requirements.

Page 3: Controlling the Interview
Background
You are not just a passive interviewee — you control how the AI asks questions and what it focuses on.

You can specify:
- How to ask: "Ask one question at a time" or "Give me all questions at once."
- What to focus on: "Focus on the data format and delivery method" or "Ask about edge cases."
- When to stop: "Ask questions until you can implement without any assumptions."
- How to explain: "If I do not understand a question, explain the options and their tradeoffs."

You can also ask your own questions during the interview:
- "What is the difference between a REST API and a webhook?"
- "Which format would you recommend for my use case?"
- "What are the tradeoffs between these options?"

The AI will answer your question and then return to the interview.

Steps
1. Start a new chat and try this enhanced prompt:
   "I want to build a Jira dashboard that shows my team's sprint progress. Before we start, interview me to understand the requirements. Ask one question at a time. If I am unsure about an answer, explain the options and recommend one."
2. Go through the interview process, answering questions and asking your own when needed.
3. After the interview, ask the AI: "Summarize what we discussed as a requirements document."
4. Review the summary — it should capture everything you discussed.

✅ Result
You can control the interview process — setting the pace, focus, and depth of questions.

Page 4: Create Your Technical Specification
Background
Now you will apply the interview technique to a real task: creating a Technical Specification (ТЗ) for your Jira/Confluence automation project. This ТЗ will be the foundation for all practical work in the remaining modules.

Choose your automation idea (pick one or propose your own):
- Weekly status report generator that pulls data from Jira and formats it for stakeholders.
- Change Request (CR) registry that tracks and summarizes CRs across projects.
- Contributor analytics dashboard showing team activity from Jira and Confluence.
- Meeting notes processor that extracts action items and creates Jira tickets.

Steps
1. Open your AI chat in Agent Mode.
2. Write your initial prompt:
   "I want to build [your chosen automation idea]. This is for my role as [your role] managing [team size] people working on [project type]. Before we start building anything, interview me to understand the full requirements. After the interview, create a structured Technical Specification in markdown format. Save it as PROJECT_SPEC.md in the project root."
3. Go through the interview (2-3 rounds of questions).
4. When the AI creates PROJECT_SPEC.md, review it carefully.
5. If anything is missing or incorrect, tell the AI directly (e.g., "Add a section about data refresh frequency — it should be daily.").
6. When you are satisfied, commit the file: use the git workflow from Module 3.

✅ Result
You have a Technical Specification (ТЗ) for your practical project, committed to your repository.

Page 5: When to Use the Interview Technique
Background
The interview technique is not needed for every interaction. Use it strategically:

Use the interview when:
- Starting a new project or feature from scratch.
- You have a general idea but cannot articulate all the details.
- The task involves multiple technical decisions you are not sure about.
- You need to explore what questions you should be asking.

Skip the interview when:
- You already know exactly what you want (write specific statements directly).
- The task is simple and well-defined ("Create a .gitignore for Python").
- You are refining an existing feature with minor changes.

After the interview — two paths:
- Option A: Ask the AI to create a requirements document first (recommended for complex projects). Then use that document as reference for implementation.
- Option B: Proceed directly to implementation if the task is straightforward enough.

For this course, your ТЗ document is the reference artifact. You will revisit and refine it in future modules as you learn new techniques.

✅ Result
You know when to use the interview technique and when to skip it.

Summary
In this module, you learned the interview technique — a method for transforming vague ideas into clear, actionable requirements by asking the AI to interview you before implementing. You applied this technique to create a Technical Specification (ТЗ) for your Jira/Confluence automation project, which will serve as the foundation for all practical work in the remaining modules.

Key takeaways:
- When you cannot think of what to specify, ask the AI: "Before we start, ask me clarifying questions."
- The AI knows what information is needed and can identify gaps in your requirements.
- You control the interview — set the pace, focus, and depth.
- A structured ТЗ document is more valuable than jumping straight to implementation.
- Your ТЗ is now committed to the repository and will evolve as the course progresses.

Quiz
1. What is the main purpose of the interview technique?
   a) To test whether the AI understands your programming language
   b) To help you discover and articulate requirements you did not know you had, by letting the AI ask clarifying questions before implementation
   c) To teach the AI about your company's processes
   Correct answer: b. The interview technique transforms a vague idea into specific requirements through AI-guided questioning. The AI identifies gaps you would not have noticed on your own.

2. What should you do after the AI finishes asking clarifying questions?
   a) Delete the entire conversation and start over with a new prompt
   b) Ask the AI to create a structured requirements document (like a ТЗ), review it, and commit it to your repository
   c) Immediately start coding without documenting the requirements
   Correct answer: b. The interview produces valuable requirements that should be captured in a structured document. This document becomes the reference for all future implementation work.

3. When should you skip the interview technique and write specific statements directly?
   a) Always — the interview technique is only for beginners
   b) When you already know exactly what you want and can articulate all the details in your prompt
   c) When the task is complex and has many unknowns
   Correct answer: b. If you already have a clear picture of the requirements, writing specific statements directly is more efficient. The interview technique is most valuable when you have gaps in your understanding.
