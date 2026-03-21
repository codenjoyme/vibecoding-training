# LangGraph & Advanced Agent Frameworks

**Duration:** 15 minutes

**Skill:** Build a stateful multi-agent pipeline with conditional routing, persistence, and human-in-the-loop using LangGraph

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- LangGraph fundamentals: nodes, edges, state graphs
- Conditional routing and retry logic in agent pipelines
- Multi-agent graphs: Coder → Reviewer → Fixer with feedback loops
- Human-in-the-loop interrupts for approval workflows
- Graph state persistence and workflow resumption
- Framework comparison: LangGraph vs CrewAI vs AutoGen

## Learning Outcome

You will build a working LangGraph pipeline where three specialized agents (coder, reviewer, fixer) collaborate with conditional branching — the reviewer can send work back to the coder, the pipeline pauses for human approval, and state persists between runs. You will understand when to use stateful frameworks vs simple multi-agent patterns.

## Prerequisites

### Required Modules

- [180 — DIAL Integration with Python and Langchain](../180-dial-langchain-python-integration/about.md)
- [190 — RAG: Document Question Answering](../190-rag-document-question-answering/about.md)

### Required Skills & Tools

- Python 3.10+ with virtual environment
- Working DIAL API key (from module 170)
- Familiarity with Langchain basics (chains, prompts, models)
- Terminal/command line proficiency
