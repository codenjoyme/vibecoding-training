# LangGraph & Advanced Agent Frameworks — Hands-on Walkthrough

In this module, you'll move beyond simple multi-agent patterns and build a **stateful agent pipeline** using LangGraph. You'll create a graph where a coder agent writes code, a reviewer agent evaluates it, and a fixer agent corrects issues — with conditional routing, human approval gates, and persistent state. This is how production AI applications handle complex, multi-step workflows.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

- **LangGraph installation** — Add langgraph to your Python environment
- **Minimal graph** — A simple input → process → output pipeline to understand nodes and edges
- **Conditional router** — A quality gate that decides whether to pass forward or retry
- **Three-agent pipeline** — Coder → Reviewer → Fixer with feedback loops
- **Human-in-the-loop** — A pause point where the graph waits for human approval
- **State persistence** — Save and resume workflow state between runs

## What We'll Install

| Component | Purpose | Size |
|-----------|---------|------|
| `langgraph` | Graph-based agent orchestration framework | ~5 MB |
| `langchain-core` | Core abstractions (should already be installed) | ~2 MB |

---

## Step 1: Why Frameworks Matter

In module 195 you learned multi-agent patterns: sequential, parallel, supervisor. But implementing those patterns with raw Langchain has limitations:

- **No state management** — each call is independent, no memory of what happened before
- **No error recovery** — if an agent fails, you start over
- **No conditional routing** — you can't say "if quality < 80%, retry"
- **No persistence** — close the terminal and all progress is lost

LangGraph solves all of these. It models your workflow as a **directed graph** where:
- **Nodes** = functions that do work (call an LLM, run code, evaluate quality)
- **Edges** = connections between nodes (including conditional ones)
- **State** = a shared dictionary that flows through the graph and accumulates results

Think of it as a flowchart that actually runs.

---

## Step 2: Set Up the Environment

1. Navigate to your workspace:
   ```
   cd ./workspace/hello-genai/
   ```
   Use `c:/workspace/hello-genai/` (Windows) or `~/workspace/hello-genai/` (macOS/Linux).

1. Activate your virtual environment:
   ```
   # Windows
   .venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

1. Install LangGraph:
   ```
   pip install langgraph
   ```

1. Verify installation:
   ```python
   python -c "import langgraph; print('LangGraph version:', langgraph.__version__)"
   ```
   You should see the version number printed without errors.

---

## Step 3: Build a Minimal Graph

Let's start with the simplest possible graph — one node that processes input and returns output.

1. Create a file `graph_basic.py`:

   ```python
   from langgraph.graph import StateGraph, START, END
   from typing import TypedDict

   # Define the state schema — what data flows through the graph
   class GraphState(TypedDict):
       task: str
       result: str

   # Define a node — a function that takes state and returns updates
   def process_task(state: GraphState) -> dict:
       task = state["task"]
       return {"result": f"Processed: {task}"}

   # Build the graph
   graph = StateGraph(GraphState)
   graph.add_node("process", process_task)
   graph.add_edge(START, "process")
   graph.add_edge("process", END)

   # Compile and run
   app = graph.compile()
   result = app.invoke({"task": "Write a hello world function", "result": ""})
   print(result)
   ```

1. Run it:
   ```
   python graph_basic.py
   ```

**What just happened:** You created a graph with one node (`process`) connected from `START` to `END`. The state dictionary `{"task": ..., "result": ...}` flows through the graph. Each node receives the full state and returns only the fields it wants to update.

---

## Step 4: Add an LLM Node

Now let's replace the dummy processing with an actual LLM call.

1. Create a file `graph_llm.py`:

   ```python
   import os
   from dotenv import load_dotenv
   from langgraph.graph import StateGraph, START, END
   from langchain_openai import AzureChatOpenAI
   from langchain_core.messages import HumanMessage
   from typing import TypedDict

   load_dotenv()

   llm = AzureChatOpenAI(
       azure_deployment=os.getenv("AZURE_DEPLOYMENT", "gpt-4o-mini"),
       api_version=os.getenv("AZURE_API_VERSION", "2024-08-01-preview"),
       temperature=0,
   )

   class GraphState(TypedDict):
       task: str
       code: str
       review: str

   def coder(state: GraphState) -> dict:
       response = llm.invoke([
           HumanMessage(content=f"Write Python code for this task. Return ONLY code, no explanation.\n\nTask: {state['task']}")
       ])
       return {"code": response.content}

   def reviewer(state: GraphState) -> dict:
       response = llm.invoke([
           HumanMessage(content=f"Review this code. Rate quality 1-10 and explain issues.\n\nCode:\n{state['code']}")
       ])
       return {"review": response.content}

   # Build the graph
   graph = StateGraph(GraphState)
   graph.add_node("coder", coder)
   graph.add_node("reviewer", reviewer)

   graph.add_edge(START, "coder")
   graph.add_edge("coder", "reviewer")
   graph.add_edge("reviewer", END)

   app = graph.compile()
   result = app.invoke({
       "task": "Function that checks if a string is a palindrome",
       "code": "",
       "review": ""
   })

   print("=== CODE ===")
   print(result["code"])
   print("\n=== REVIEW ===")
   print(result["review"])
   ```

1. Run it:
   ```
   python graph_llm.py
   ```

**What just happened:** You built a two-node pipeline: Coder writes code → Reviewer evaluates it. This is the sequential pattern from module 195, but now implemented as a proper graph with typed state.

---

## Step 5: Add Conditional Routing

The reviewer gave feedback — but nothing happens with it. Let's add a **conditional edge**: if the review score is low, send back to the coder for a fix.

1. Create `graph_conditional.py`:

   ```python
   import os
   import re
   from dotenv import load_dotenv
   from langgraph.graph import StateGraph, START, END
   from langchain_openai import AzureChatOpenAI
   from langchain_core.messages import HumanMessage
   from typing import TypedDict

   load_dotenv()

   llm = AzureChatOpenAI(
       azure_deployment=os.getenv("AZURE_DEPLOYMENT", "gpt-4o-mini"),
       api_version=os.getenv("AZURE_API_VERSION", "2024-08-01-preview"),
       temperature=0,
   )

   class GraphState(TypedDict):
       task: str
       code: str
       review: str
       score: int
       attempts: int

   def coder(state: GraphState) -> dict:
       feedback = state.get("review", "")
       prompt = f"Write Python code for this task. Return ONLY code.\n\nTask: {state['task']}"
       if feedback:
           prompt += f"\n\nPrevious review feedback (fix these issues):\n{feedback}"

       response = llm.invoke([HumanMessage(content=prompt)])
       return {"code": response.content, "attempts": state.get("attempts", 0) + 1}

   def reviewer(state: GraphState) -> dict:
       response = llm.invoke([
           HumanMessage(content=(
               f"Review this code. First line must be 'SCORE: X' where X is 1-10.\n"
               f"Then explain issues.\n\nCode:\n{state['code']}"
           ))
       ])
       content = response.content
       score_match = re.search(r"SCORE:\s*(\d+)", content)
       score = int(score_match.group(1)) if score_match else 5
       return {"review": content, "score": score}

   def should_retry(state: GraphState) -> str:
       """Conditional edge: retry if score < 8 and attempts < 3"""
       if state["score"] >= 8:
           return "accept"
       if state["attempts"] >= 3:
           return "accept"  # Give up after 3 attempts
       return "retry"

   # Build the graph
   graph = StateGraph(GraphState)
   graph.add_node("coder", coder)
   graph.add_node("reviewer", reviewer)

   graph.add_edge(START, "coder")
   graph.add_edge("coder", "reviewer")
   graph.add_conditional_edges("reviewer", should_retry, {
       "retry": "coder",
       "accept": END,
   })

   app = graph.compile()
   result = app.invoke({
       "task": "Function that finds the longest common subsequence of two strings",
       "code": "", "review": "", "score": 0, "attempts": 0
   })

   print(f"=== FINAL CODE (after {result['attempts']} attempts, score: {result['score']}) ===")
   print(result["code"])
   print(f"\n=== FINAL REVIEW ===")
   print(result["review"])
   ```

1. Run it:
   ```
   python graph_conditional.py
   ```

**What just happened:** The graph now has a **loop**. After the reviewer scores the code, the `should_retry` function decides: score >= 8 → accept and finish; score < 8 → send back to coder with review feedback. The coder sees the feedback and improves. Maximum 3 attempts to prevent infinite loops.

This is the **core power of LangGraph** — conditional edges that create intelligent retry logic.

---

## Step 6: Human-in-the-Loop

Sometimes you want a human to approve before the pipeline continues. LangGraph supports **interrupts** — the graph pauses at a node and waits.

1. Create `graph_human.py`:

   ```python
   import os
   import re
   from dotenv import load_dotenv
   from langgraph.graph import StateGraph, START, END
   from langchain_openai import AzureChatOpenAI
   from langchain_core.messages import HumanMessage
   from typing import TypedDict

   load_dotenv()

   llm = AzureChatOpenAI(
       azure_deployment=os.getenv("AZURE_DEPLOYMENT", "gpt-4o-mini"),
       api_version=os.getenv("AZURE_API_VERSION", "2024-08-01-preview"),
       temperature=0,
   )

   class GraphState(TypedDict):
       task: str
       code: str
       approved: bool

   def coder(state: GraphState) -> dict:
       response = llm.invoke([
           HumanMessage(content=f"Write Python code for: {state['task']}. Return ONLY code.")
       ])
       return {"code": response.content}

   def human_review(state: GraphState) -> dict:
       print("\n" + "=" * 50)
       print("HUMAN REVIEW REQUIRED")
       print("=" * 50)
       print(f"\nGenerated code:\n{state['code']}")
       print("\n" + "=" * 50)
       answer = input("Approve this code? (yes/no): ").strip().lower()
       return {"approved": answer in ("yes", "y")}

   def finalize(state: GraphState) -> dict:
       if state["approved"]:
           print("\n✅ Code approved and ready for deployment!")
       else:
           print("\n❌ Code rejected. Pipeline stopped.")
       return {}

   graph = StateGraph(GraphState)
   graph.add_node("coder", coder)
   graph.add_node("human_review", human_review)
   graph.add_node("finalize", finalize)

   graph.add_edge(START, "coder")
   graph.add_edge("coder", "human_review")
   graph.add_edge("human_review", "finalize")
   graph.add_edge("finalize", END)

   app = graph.compile()
   result = app.invoke({"task": "Fibonacci sequence generator", "code": "", "approved": False})
   ```

1. Run it:
   ```
   python graph_human.py
   ```

The pipeline will **pause** and ask you to approve the generated code in the terminal. This is the human-in-the-loop pattern — critical for production workflows where AI-generated output needs human sign-off.

---

## Step 7: State Persistence

With LangGraph's checkpointer, you can save graph state and resume later — even after restarting Python.

1. Create `graph_persistent.py`:

   ```python
   import os
   from dotenv import load_dotenv
   from langgraph.graph import StateGraph, START, END
   from langgraph.checkpoint.memory import MemorySaver
   from langchain_openai import AzureChatOpenAI
   from langchain_core.messages import HumanMessage
   from typing import TypedDict

   load_dotenv()

   llm = AzureChatOpenAI(
       azure_deployment=os.getenv("AZURE_DEPLOYMENT", "gpt-4o-mini"),
       api_version=os.getenv("AZURE_API_VERSION", "2024-08-01-preview"),
       temperature=0,
   )

   class GraphState(TypedDict):
       task: str
       code: str
       iteration: int

   def coder(state: GraphState) -> dict:
       iteration = state.get("iteration", 0) + 1
       response = llm.invoke([
           HumanMessage(content=f"Write Python code for: {state['task']}. Iteration {iteration}. Return ONLY code.")
       ])
       print(f"  [Coder] Iteration {iteration} complete")
       return {"code": response.content, "iteration": iteration}

   # Build graph with persistence
   graph = StateGraph(GraphState)
   graph.add_node("coder", coder)
   graph.add_edge(START, "coder")
   graph.add_edge("coder", END)

   # Add memory-based checkpointer
   memory = MemorySaver()
   app = graph.compile(checkpointer=memory)

   # Run with a thread ID — this enables state tracking
   config = {"configurable": {"thread_id": "my-project-1"}}

   result = app.invoke(
       {"task": "Binary search function", "code": "", "iteration": 0},
       config=config
   )
   print(f"Result: iteration {result['iteration']}")

   # You can inspect the saved state
   saved_state = app.get_state(config)
   print(f"Saved state keys: {list(saved_state.values.keys())}")
   print(f"Saved iteration: {saved_state.values['iteration']}")
   ```

1. Run it:
   ```
   python graph_persistent.py
   ```

**What just happened:** The `MemorySaver` checkpointer saves every state transition. In production, you'd use `SqliteSaver` or `PostgresSaver` for durable persistence. This means you can:
- Resume interrupted workflows
- Audit what happened at each step
- Roll back to a previous state

---

## Step 8: Framework Comparison

LangGraph is not the only option. Here's when to use what:

| Framework | Best For | State Management | Learning Curve |
|-----------|----------|-------------------|---------------|
| **LangGraph** | Complex conditional workflows, production pipelines | Built-in, typed | Medium |
| **CrewAI** | Role-based agent teams, "crew" metaphor | Automatic | Low |
| **AutoGen** | Research, multi-turn agent conversations | Message-based | Medium-High |
| **Raw Langchain** | Simple sequential chains, quick prototypes | Manual | Low |

**Decision guide:**
- Need conditional routing or loops? → **LangGraph**
- Want quick role-based setup without coding graphs? → **CrewAI**
- Doing research with conversational agents? → **AutoGen**
- Just chaining 2-3 calls linearly? → **Raw Langchain** (module 195 patterns)

---

## Success Criteria

- ✅ LangGraph installed and working in your Python environment
- ✅ Built and ran a minimal graph with typed state
- ✅ Connected LLM calls as graph nodes
- ✅ Implemented conditional routing with retry logic (score-based)
- ✅ Added human-in-the-loop approval gate
- ✅ Used MemorySaver for state persistence
- ✅ Can explain when to use LangGraph vs CrewAI vs raw Langchain

## Understanding Check

1. **What are the three core concepts of LangGraph?**
   Nodes (functions that do work), Edges (connections between nodes, including conditional), and State (typed dictionary that flows through the graph and accumulates results).

2. **How does a conditional edge differ from a regular edge?**
   A regular edge always goes to the same next node. A conditional edge calls a function that inspects the current state and returns a string key that maps to different target nodes (e.g., "retry" → coder, "accept" → END).

3. **Why do we limit retry attempts in the conditional routing example?**
   To prevent infinite loops. Without a maximum attempts check, a low-quality-scoring cycle could loop forever between coder and reviewer, consuming tokens and time.

4. **What does the checkpointer do and why is it important for production?**
   The checkpointer saves graph state at every transition. This enables: resuming interrupted workflows, auditing what happened at each step, and rolling back to a previous state. In production, you'd use a durable backend like SQLite or PostgreSQL instead of in-memory.

5. **When would you choose CrewAI over LangGraph?**
   When you want a quick role-based setup without explicitly coding graph structures. CrewAI uses a "crew" metaphor where you define agent roles and tasks, and it handles orchestration automatically. Better for simpler, role-based scenarios.

6. **What is the human-in-the-loop pattern and when do you need it?**
   The graph pauses at a specific node and waits for human input before continuing. You need it when AI-generated output requires human approval before proceeding — e.g., code review before deployment, content approval before publishing.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: langgraph` | Run `pip install langgraph` in your activated virtual environment |
| `ImportError: cannot import MemorySaver` | Update langgraph: `pip install --upgrade langgraph`. MemorySaver was added in newer versions |
| Graph runs but produces empty state | Check that your node functions return a dictionary with the state keys they want to update |
| Conditional edge always goes to the same branch | Debug by printing the state before the routing function. Check that the score/flag field is actually being set by the previous node |
| `AZURE_DEPLOYMENT` not found | Ensure `.env` file exists with correct variables (see module 170) |
| Graph hangs on human_review node | This is expected — it's waiting for your terminal input. Type `yes` or `no` and press Enter |

## Next Steps

You've built stateful agent pipelines with LangGraph. Next, explore:
- [195 — Multi-Agent Orchestration](../195-multi-agent-orchestration/about.md) for conceptual patterns behind these frameworks
- [197 — Onboarding New Team Members with AI](../197-onboarding-new-team-members-with-ai/about.md) for applying multi-agent patterns to a real use case
