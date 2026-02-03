# Clarifying Requirements with AI - Hands-on Walkthrough

In this walkthrough, you'll learn how to use AI as an interviewer to transform vague ideas into clear, actionable requirements. This technique is invaluable when you know what you want but can't articulate all the details.

## Prerequisites

- Completed Module 050 (Effective Prompting Without Arguing)
- Understanding of how to write precise prompts with statements
- Basic experience with AI coding assistants

---

## Step-by-Step Instructions

### Part 1: The "Empty Head" Problem

Let's understand when and why this technique is valuable.

**The Common Situation:**

1. You have a general idea: "I need a sorting function"

1. You start writing a prompt with statements:
   - Statement 1: "Create a sorting function"
   - Statement 2: "Write it in Python"
   - Statement 3: "Use bubble sort algorithm"
   - Statement 4: "..."
   - Statement 5: "..."

1. **You get stuck** - what else should you specify?
   - You know you need more details
   - But you can't think of what to add
   - Your head feels "empty"

**Why This Happens:**

1. You're not an expert in everything:
   - You might not know all the technical decisions to make
   - You might not know what edge cases to consider
   - You might not know best practices

1. You have implicit assumptions:
   - Things that seem obvious to you
   - But need to be stated explicitly for AI
   - You don't realize they're missing

1. You're starting from scratch:
   - Empty project, no context
   - Need to define everything
   - Don't know where to begin

**When to Use This Technique:**

- Starting a new empty project without clear plan
- Adding a feature but unclear about implementation details
- Having a general idea but struggling to articulate requirements
- Need help breaking down a complex task
- Want to explore what questions you should be asking

### Part 2: The Interview Mode Pattern

Learn the magic phrase that transforms AI into your requirements analyst.

**The Core Technique:**

1. Write your initial prompt (even if it's just 3-4 statements)

1. Add one simple question at the end:
   ```
   Before we start, ask me clarifying questions?
   ```

1. That's it! This single sentence changes everything

**What Happens:**

1. Instead of immediately generating code, the AI switches to interview mode

1. AI starts asking you questions:
   - About technical details you didn't specify
   - About edge cases you didn't consider
   - About requirements you didn't know you had

1. You answer the questions one by one

1. Through this dialogue, the context gets filled with precise information

**Why This Works:**

1. AI knows what information is needed for implementation

1. AI can identify gaps in your requirements

1. AI asks the questions you should have asked yourself

1. Your answers provide the missing statements automatically

### Part 3: Controlling the Interaction Style

Understanding that you can define HOW the AI should work with you.

**You Can Specify:**

1. **How to answer:**
   - "Give detailed explanations"
   - "Keep answers concise"
   - "Show code examples"
   - "Use analogies to explain"

1. **What to ask:**
   - "Focus on technical implementation details"
   - "Ask about edge cases"
   - "Help me understand performance implications"
   - "Question my architectural decisions"

1. **When to stop:**
   - "Ask questions until you have complete requirements"
   - "Stop when you can implement without assumptions"
   - "Keep asking until I say I'm ready"

**Example Patterns:**

```
"Before we start, ask me clarifying questions.
Keep questions focused on implementation details.
Ask one question at a time and wait for my answer."
```

```
"I'm not sure about all the requirements.
Interview me to understand what I need.
After each answer, ask follow-up questions if needed."
```

```
"Help me clarify this feature.
Ask questions about technical approach, edge cases, and performance.
When you have enough information, summarize what we discussed."
```

### Part 4: The Iterative Clarification Process

Learn the rhythm of the interview dialogue.

**The Flow:**

1. **You:** Write initial prompt + "ask me clarifying questions?"

1. **AI:** Asks 3-5 questions

1. **You:** Answer the questions (all at once or one by one)

1. **You:** Add the magic continuation phrase:
   ```
   Are there any more questions?
   ```

1. **AI:** Asks more questions (or says "no more questions")

1. Repeat steps 3-5 until AI says it has enough information

**Important Points:**

1. **You can ask questions too:**
   - "What do you mean by [term]?"
   - "What's the difference between [option A] and [option B]?"
   - "What would you recommend?"
   - Then return to answering AI's questions

1. **You can change your answers:**
   - "Actually, let me reconsider the previous answer..."
   - "I think I misunderstood the question..."
   - AI will adjust follow-up questions accordingly

1. **Keep asking "any more questions?"**
   - Don't assume AI is done after first round
   - Usually takes 2-3 iterations
   - AI will clearly say when it has enough information

**The End State:**

1. AI says something like:
   - "I have all the information I need"
   - "No more questions, I can proceed"
   - "I'm ready to implement based on our discussion"

1. Now you have two options:
   - **Option A:** Ask AI to create a markdown document summarizing requirements
   - **Option B:** Proceed directly to implementation

### Part 5: Practical Exercise - Sorting Function with Interview

Let's practice using the same sorting function example, but with the interview technique.

**Setup:**

1. Open VS Code or Cursor with your `./workspace/hello-genai/` workspace

1. Open the AI chat panel

1. Make sure Agent Mode is enabled

**Round 1: Initial Vague Prompt**

1. Type this minimal prompt:
   ```
   I need a sorting function in Python.
   Before we start, ask me clarifying questions?
   ```

1. Press Enter

1. **Observe what AI asks:**
   - AI will ask several questions
   - Questions might include:
     * What sorting algorithm should I use?
     * What data type will be sorted?
     * Should it sort in-place or return a new list?
     * Should it be ascending or descending?
     * How should it handle edge cases?
   - AI becomes your requirements analyst!

**Round 2: Answer the Questions**

1. Read all the questions carefully

1. Let's answer them (example answers):
   ```
   - Algorithm: bubble sort
   - Data type: list of integers
   - Should return a new sorted list
   - Ascending order
   - For empty list, return empty list
   ```

1. **Important:** After answering, ask:
   ```
   Are there any more questions?
   ```

1. Press Enter

**Round 3: Second Round of Questions**

1. AI might ask follow-up questions:
   - Should the function validate input?
   - What about duplicate numbers?
   - Should it have type hints?
   - Should it have docstrings?
   - What about comments?
   - Should it handle other iterables (tuples, sets)?

1. **Practice asking your own question:**
   ```
   Wait, what's the difference between in-place and returning new list?
   ```

1. Read AI's explanation

1. Then answer the questions:
   ```
   - No input validation needed
   - Duplicates are fine, keep them
   - No type hints
   - No docstrings
   - No comments
   - Only lists, not other iterables
   ```

1. Ask again:
   ```
   Are there any more questions?
   ```

**Round 4: Final Clarification**

1. AI might ask last few questions or say it's ready

1. If there are more questions, answer them

1. Keep asking "Are there any more questions?" until AI says no

1. When AI says it has enough information, you have two choices:

**Option A: Create Requirements Document**

1. Ask AI:
   ```
   Before implementing, create a markdown document with all requirements we discussed.
   Include function signature, behavior description, and all constraints.
   ```

1. AI creates a document like:
   ```markdown
   # Bubble Sort Function Requirements
   
   ## Function Signature
   - Name: bubble_sort
   - Parameter: numbers (list of integers)
   - Returns: new sorted list (ascending order)
   
   ## Behavior
   - Uses bubble sort algorithm
   - Returns new list (does not modify original)
   - Ascending order
   - Preserves duplicates
   
   ## Edge Cases
   - Empty list → returns empty list
   - Single element → returns single element list
   
   ## Code Style
   - No type hints
   - No docstrings
   - No comments
   - Only works with lists, not other iterables
   ```

1. Review the document

1. Now ask AI to implement:
   ```
   Please implement this function in a file named bubble_sort.py
   ```

**Option B: Direct Implementation**

1. After AI says it has enough information:
   ```
   Great! Please implement this function in a file named bubble_sort.py
   ```

1. AI creates the file with precise implementation

1. Check the result - it should match all your answers

**Round 5: Compare with Previous Module**

1. Think about what just happened:
   - **Previous module:** You had to think of all statements yourself
   - **This module:** AI asked questions, you just answered
   - Which was easier?

1. Look at the resulting code:
   - It should be very similar to what you got in Module 050 with 5+ statements
   - But you didn't have to think of everything upfront
   - AI guided you through the requirements

**Key Observations:**

1. **Initial prompt was minimal** (2 sentences)
   - Versus 5-7 statements in previous module
   - Much easier to start

1. **AI asked the right questions**
   - Questions you should have thought of
   - But didn't have to

1. **Iterative clarification**
   - Build understanding step by step
   - Can ask your own questions
   - Can change answers

1. **Final result is precise**
   - Just as specific as detailed prompt
   - But arrived through conversation

### Part 6: Advanced Patterns

Learn variations and advanced uses of this technique.

**Pattern 1: Exploration Mode**

When you don't even know what you want:

```
I want to build a web scraper, but I'm not sure what features it should have.
Interview me to understand my use case.
Ask questions about my goals, data sources, and constraints.
Help me discover what I actually need.
```

**Pattern 2: Options Discussion**

When you want to explore alternatives:

```
I need a caching mechanism for my application.
Before we choose an approach, ask me questions about:
- Scale and performance requirements
- Infrastructure constraints
- Maintenance considerations
Then recommend 2-3 options with pros/cons.
```

**Pattern 3: Learning While Clarifying**

When you want to learn during the process:

```
I need to implement authentication, but I'm not familiar with best practices.
As you ask clarifying questions, explain the implications of different choices.
Help me understand trade-offs so I can make informed decisions.
```

**Pattern 4: Architecture Discussion**

For complex features:

```
I want to add a notification system to my app.
Let's discuss architecture through questions:
1. Ask about functional requirements
2. Ask about technical constraints
3. Propose architecture options
4. Ask follow-up questions about my choice
When we align on approach, create detailed design document.
```

### Part 7: When to Use Each Approach

Understanding when interview mode is better than direct prompting.

**Use Interview Mode When:**

1. **Starting something new:**
   - Empty project
   - New feature you haven't built before
   - Unfamiliar technology

1. **Requirements are unclear:**
   - You have a general idea but not details
   - You're not sure what questions to ask
   - You need help breaking down the problem

1. **You want to learn:**
   - Understand implications of different choices
   - Explore best practices
   - Learn new concepts while planning

1. **Complex features:**
   - Many moving parts
   - Multiple technical decisions
   - Need to consider many factors

**Use Direct Detailed Prompts When:**

1. **You know exactly what you want:**
   - Clear requirements
   - Familiar pattern
   - Just need implementation

1. **Speed is important:**
   - Quick fix or adjustment
   - Simple, straightforward task
   - No need for discussion

1. **Consistency matters:**
   - Following established patterns
   - Matching existing code style
   - Repeating similar tasks

**The Hybrid Approach:**

1. Start with interview mode to clarify requirements

1. AI creates requirements document

1. Edit the document if needed

1. Use the document as a detailed prompt for implementation

1. Best of both worlds!

---

## Success Criteria

Congratulations! You've successfully completed this module if:

✅ You understand the "empty head" problem when writing prompts  
✅ You know the magic phrase: "ask me clarifying questions?"  
✅ You understand that you can control interaction style (how to answer, what to ask, when to stop)  
✅ You know the iterative pattern: answer → "any more questions?" → repeat  
✅ You've practiced asking your own questions during clarification  
✅ You understand you can request requirements document before implementation  
✅ You've completed the sorting function exercise using interview mode  
✅ You can compare interview mode vs direct detailed prompts  
✅ You know when to use each approach  
✅ You understand advanced patterns (exploration, options, learning, architecture)

## Troubleshooting

**AI goes straight to implementation instead of asking questions?**
- Make sure you phrased it as a question: "ask me clarifying questions?"
- Try more explicit: "Before implementing, ask me questions to clarify requirements"
- Emphasize: "Don't start coding yet, interview me first"

**AI asks too many questions?**
- Guide the focus: "Ask questions about [specific aspect]"
- Set a limit: "Ask your top 5 most important questions"
- You can start implementing after answering key questions, even if AI has more

**AI asks obvious questions?**
- Answer them briefly: "Standard approach is fine"
- Or challenge: "What would you recommend?"
- The questions help ensure nothing is missed

**Forgot to ask "any more questions?"**
- Just ask it in a new message
- AI will continue the interview
- Keep the clarification going until AI says it's done

**Want to change an answer?**
- Just say: "Actually, let me reconsider the [topic]..."
- Or: "I think I misunderstood. Let me clarify..."
- AI will adjust accordingly

**Not sure how to answer a question?**
- Ask AI: "What's the difference between the options?"
- Or: "What would you recommend and why?"
- Or: "What are the trade-offs?"
- Turn it into a learning conversation!

## Understanding the Benefits

**Cognitive Load Reduction:**
- Don't need to think of everything upfront
- AI guides you through necessary decisions
- Reduces mental effort to get started

**Knowledge Transfer:**
- Learn what questions matter for different types of tasks
- Over time, you'll internalize these questions
- Makes you better at requirement gathering

**Completeness:**
- Less likely to miss important aspects
- AI knows what information is needed
- Systematic coverage of requirements

**Documentation:**
- Interview transcript becomes requirements document
- Captures decisions and rationale
- Useful for future reference

**Flexibility:**
- Can explore options through questions
- Can change direction mid-conversation
- More interactive than one-shot prompting

## Next Steps

Now that you've mastered requirement clarification through AI interviews, you're ready to learn about version control and managing your code changes with Git in the next module!
