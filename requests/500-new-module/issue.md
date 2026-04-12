# GitHub Issue #3: New Module 310 → Repurposed as Module 500

**Repository:** codenjoyme/vibecoding-training  
**Issue Number:** 3  
**State:** OPEN  
**Author:** IvanLapunka  
**Created:** 2026-03-11  
**URL:** https://github.com/codenjoyme/vibecoding-training/issues/3  

---

## Title

New Module 310: AI Workflow Decision Guide — Daily Tasks with the Right Tools

---

## Body

## Module Overview

**Module Number:** 310  
**Folder:** `310-ai-workflow-decision-guide`  
**Placement:** After Module 300 (DMtools Agent Skill) — capstone/final module  

**Skill:** Know exactly which AI tools to use, when to use them, and how to combine them for any daily development task — eliminating "what should I do here?" uncertainty.

---

## Problem This Module Solves

After completing all prior modules, learners have many AI tools available but may not have a mental model for *which tool fits which situation*. This module provides that decision clarity through scenario-based practice.

---

## Topics to Cover

- AI tool selection framework: when to use chat vs. MCP vs. CLI vs. agent delegation
- Scenario 1: **Vague feature request** — clarify with AI interview → spec → GitHub issue → delegate to coding agent
- Scenario 2: **Bug report** — describe symptom → AI locates cause → fix → commit with baby steps
- Scenario 3: **Onboard a new developer** — AI reads codebase → generates structured onboarding docs
- Scenario 4: **Legacy project feature** — SpecKit reverse-docs project → AI proposes safe insertion points → implement
- Scenario 5: **Bulk file processing** — process 50 config/log files with AI agent automation
- Scenario 6: **Prototype an idea in 2 hours** — SpecKit from idea to working full-stack PoC
- Scenario 7: **Review what AI did across sessions** — export & search chat history → build knowledge base
- Scenario 8: **Repetitive weekly task** — identify pattern → build CLI skill → automate it
- Scenario 9: **Web UI bug hunting** — Chrome DevTools MCP → AI emulates user actions → reports issues
- Scenario 10: **Sprint planning** — AI interview about features → creates prioritized GitHub issues backlog

---

## Learning Outcome

Learners can independently identify the right AI tool(s) for any daily task and execute the workflow without hesitation. No more "what should I do here?" — they have a clear, practiced decision framework.

---

## Prerequisites

### Required Modules
All prior modules (010–300) are prerequisites — this is a capstone module that assumes familiarity with all tools covered in the course.

Key modules directly used:
- 055 — Clarifying Requirements with AI
- 060 — Version Control with Git
- 100 — Model Context Protocol (MCP)
- 103 — CLI Command Line Interface
- 105 — MCP GitHub Integration
- 120/125 — SpecKit Rapid Prototyping
- 130 — Chrome DevTools MCP
- 150 — GitHub Coding Agent Delegation
- 160 — Bulk File Processing with AI
- 250 — Export Chat Session
- 300 — DMtools Agent Skill

### Required Skills & Tools
- All tools installed from previous modules
- GitHub account connected
- Active GitHub Copilot subscription

---

## Hands-on Steps

1. Introduce the **AI Tool Decision Framework** — a simple flowchart: task type → recommended tool(s)
2. For each of the 10 scenarios:
   - Present the situation (1-2 sentence problem statement)
   - Guide learner to identify which tools apply
   - Walk through the actual workflow step by step
   - Checkpoint: verify output (issue created, code committed, file processed, etc.)
3. Final exercise: learner picks a real task from their own work and applies the framework independently

---

## Implementation Notes

- Module is scenario-driven, not theory-driven — each scenario should be hands-on
- The Decision Framework visual (flowchart or table) should be the centerpiece of `about.md`
- `walkthrough.md` can be structured as 10 numbered sections (one per scenario)
- Scenarios can reference earlier modules' walkthroughs rather than repeating steps
- Estimated duration: 45-60 minutes (longest module in the course)
