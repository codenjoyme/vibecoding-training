# Agent Memory Management - Hands-on Walkthrough

In this module, you'll learn how to give AI agents persistent memory for multi-step tasks. AI agents don't naturally remember what they planned to do - they process each message independently. By using todo lists (built-in or external), you create a "memory" that helps agents stay on track through complex workflows.

## Prerequisites

- Completed module 040 (Agent Mode basics)
- Completed module 050 (Effective Prompting)
- Completed module 055 (Clarifying Requirements)
- VS Code with GitHub Copilot installed OR Cursor IDE
- An empty test project or workspace folder

## What We'll Practice

You'll work through three memory management techniques:

1. **Built-in Todo Tool** - Native task tracking that appears above the chat
   - How to access built-in tools in your IDE
   - How to prompt AI to create and update todos
   - Visual progress tracking during task execution

2. **External Markdown Todo List** - File-based task tracking
   - Creating a structured todo list in a .md file
   - Referencing it with @-mentions in prompts
   - Having AI maintain and update the list as work progresses

3. **Project Planning Document** - High-level context document
   - Creating a project specification that AI references
   - Combining specs with todo lists for complex projects
   - Maintaining context across multiple chat sessions

---

## Exercise 1: Using Built-in Todo Tool

### What We'll Do

You'll prompt the AI agent to create a multi-step refactoring task and watch it automatically create a todo list above the chat window. The agent will mark items as it completes them, giving you visual progress tracking.

### Finding Built-in Tools

**In VS Code:**
1. Open GitHub Copilot Chat panel
2. Look at the chat input area at the bottom
3. Click the **wrench icon** (🔧) or **two keys icon** (🔑) next to the model name
4. You'll see a list of available built-in tools: `agent`, `askQuestions`, `edit`, `execute`, `read`, `search`, `todo`, `vscode`, `web`
5. These tools are automatically available - AI calls them when needed

**In Cursor:**
1. Open AI Chat panel
2. Look below the chat input area
3. Click the **tools icon** or **settings icon** near the model selector
4. You'll see available built-in tools similar to VS Code
5. Tools are enabled by default in Agent mode

### Step 1: Create a Test Project

Create a simple Python project with a few files to refactor:

```bash
mkdir c:/workspace/todo-test
cd c:/workspace/todo-test
```

Create `main.py`:
```python
def calculate(a, b, operation):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b

result = calculate(10, 5, "add")
print(result)
```

Create `utils.py`:
```python
def validate_input(value):
    if value < 0:
        return False
    return True

def format_output(value):
    return f"Result: {value}"
```

### Step 2: Prompt AI with Complex Task

Open chat and use this prompt:

```
I need to refactor this Python project:
1. Add type hints to all functions
2. Add docstrings
3. Add error handling
4. Create tests for all functions
5. Add input validation

Please create a todo list and work through each item step by step.
Use Agent mode.
```

### What Just Happened

- AI detected multiple steps and called the `todo` built-in tool
- A visual todo list appeared above the chat
- AI marked items as "in-progress" and "completed" as it worked
- You can see exactly what's done and what's remaining

### Step 3: Verify Todo Behavior

Watch the todo list update as the agent works:
- Items turn from white → blue (in-progress) → green (completed)
- You can click on todo items to see related changes
- If AI gets interrupted, the list shows where it stopped

### Success Check

✅ You can locate the built-in tools icon in your IDE  
✅ AI created a visual todo list above the chat  
✅ Todo items updated automatically as AI completed steps  
✅ You can see the final state of all completed tasks

---

## Exercise 2: External Markdown Todo List

### What We'll Do

You'll create a Markdown file with a structured todo list, then ask AI to reference it using @-mentions and maintain it as work progresses.

### Step 1: Create External Todo File

Create `TODO.md` in your project root:

```markdown
# Project Refactoring Tasks

## Phase 1: Code Quality
- [ ] Add type hints to main.py functions
- [ ] Add type hints to utils.py functions
- [ ] Add docstrings to all functions (Google style)
- [ ] Add error handling for divide by zero

## Phase 2: Testing
- [ ] Create test_main.py with unit tests
- [ ] Create test_utils.py with unit tests
- [ ] Add pytest configuration
- [ ] Verify 80%+ code coverage

## Phase 3: Documentation
- [ ] Create README.md with usage examples
- [ ] Add inline comments for complex logic
- [ ] Create requirements.txt

## Progress Notes
_AI will update this section as work progresses_
```

### Step 2: Reference Todo in Prompt

Use @-mentions to reference the file:

```
I have a @TODO.md file with all the tasks for this project.

Please:
1. Read the todo list
2. Work through Phase 1 tasks one by one
3. Update the checklist in TODO.md as you complete each item
4. Add notes to the "Progress Notes" section

Use Agent mode and work autonomously.
```

### What Just Happened

- AI read the TODO.md file as context
- AI worked through items sequentially
- AI updated checkboxes from `- [ ]` to `- [x]` as tasks completed
- AI added notes about what was done in each step
- The external file now serves as a persistent record

### Step 3: Resume Work Later

Close the chat and start a new conversation:

```
Check @TODO.md and continue where you left off.
Complete Phase 2 tasks.
```

The AI will:
- Read the current state of TODO.md
- See what's already completed (checked boxes)
- Continue from the next uncompleted item
- Update the file as it progresses

### Success Check

✅ Created structured TODO.md with phases and tasks  
✅ AI referenced and read the external todo file  
✅ AI updated checkboxes and notes as work progressed  
✅ You can resume work across different chat sessions

---

## Exercise 3: Project Specification + Todo Combination

### What We'll Do

For complex projects, you'll learn to combine a high-level specification document with a detailed todo list. This gives AI both strategic context (the "why") and tactical steps (the "what").

### Step 1: Create Project Spec

Create `PROJECT_SPEC.md`:

```markdown
# Calculator Refactoring Project

## Goal
Transform a simple calculator script into a production-ready Python package with:
- Clean, testable code
- Comprehensive error handling
- Full test coverage
- Professional documentation

## Technical Requirements
- Python 3.9+
- Type hints throughout
- Google-style docstrings
- Pytest for testing
- 80%+ code coverage

## Architecture Decisions
- Keep single-file simplicity (no package structure yet)
- Use standard library only (no external dependencies except pytest)
- Error messages should be user-friendly

## Quality Standards
- All functions must have type hints
- All public functions need docstrings
- All functions need unit tests
- No code duplication
- Input validation on all user-facing functions

## Out of Scope
- GUI interface
- Database integration
- Advanced mathematical operations
```

### Step 2: Create Detailed Todo

Create `IMPLEMENTATION_TODO.md`:

```markdown
# Implementation Checklist

## Setup
- [ ] Create virtual environment
- [ ] Create requirements.txt with pytest
- [ ] Create .gitignore for Python

## Code Quality - main.py
- [ ] Add type hints to calculate()
- [ ] Add docstring to calculate()
- [ ] Add error handling (ZeroDivisionError, invalid operation)
- [ ] Add input validation
- [ ] Refactor: extract operation logic to separate functions

## Code Quality - utils.py
- [ ] Add type hints to all functions
- [ ] Add docstrings
- [ ] Add input validation
- [ ] Handle edge cases

## Testing
- [ ] Create test_main.py structure
- [ ] Write tests for all calculate() operations
- [ ] Write tests for error cases
- [ ] Create test_utils.py structure
- [ ] Write tests for validation functions
- [ ] Run coverage report
- [ ] Fix any gaps to reach 80%+

## Documentation
- [ ] Create README with installation steps
- [ ] Add usage examples to README
- [ ] Add development guide to README
- [ ] Review all docstrings for clarity

## Final Review
- [ ] Run all tests
- [ ] Check type hints with mypy (optional)
- [ ] Verify all checkboxes completed
```

### Step 3: Use Both Documents Together

Prompt the AI:

```
I have two documents:
- @PROJECT_SPEC.md - High-level goals and requirements
- @IMPLEMENTATION_TODO.md - Detailed task checklist

Please:
1. Read both documents to understand context and tasks
2. Work through IMPLEMENTATION_TODO.md systematically
3. Ensure all work aligns with PROJECT_SPEC.md requirements
4. Update IMPLEMENTATION_TODO.md as you complete tasks
5. If anything conflicts or is unclear, ask me before proceeding

Use Agent mode and create a built-in todo list to track your progress.
```

### What Just Happened

- AI reads both strategic context (spec) and tactical steps (todo)
- AI creates built-in todo list for visual tracking
- AI updates external Markdown file as permanent record
- You get both real-time progress and persistent documentation
- AI can verify each change against the quality standards in spec

### Step 4: Checkpoint and Resume

After AI completes a few tasks, stop it and start a new chat:

```
Review @PROJECT_SPEC.md and @IMPLEMENTATION_TODO.md.
Continue where we left off.
```

The AI will:
- Understand the project goals from spec
- See what's done in the todo list
- Continue seamlessly

### Success Check

✅ Created both specification and detailed todo documents  
✅ AI referenced both files for context  
✅ AI aligned work with high-level requirements  
✅ AI updated todo list as work progressed  
✅ You can resume complex projects across sessions

---

## Understanding Check

1. **What is the main limitation that todo lists solve for AI agents?**
   - AI agents don't naturally maintain memory across messages - they process each prompt independently. Todo lists provide persistent context about what needs to be done and what's already completed.

2. **When should you use built-in todo tool vs external Markdown todo list?**
   - Built-in tool: Quick tasks in single session, visual progress tracking, no need for persistence
   - External Markdown: Complex multi-session work, need for documentation, team collaboration, resuming work later

3. **How do you access built-in tools in VS Code?**
   - Click the wrench icon (🔧) or two keys icon (🔑) next to the model name in GitHub Copilot chat panel

4. **How do you reference an external todo list in your prompt?**
   - Use @-mention syntax: `@TODO.md` or `@IMPLEMENTATION_TODO.md`

5. **What's the benefit of combining PROJECT_SPEC.md with TODO.md?**
   - Spec provides "why" and quality standards; todo provides "what" and tactical steps. AI can verify each change against requirements while following detailed implementation steps.

6. **How does an external todo list help when resuming work later?**
   - The file shows exactly what's completed (checked boxes) and what remains. AI reads the current state and continues from the next task without repeating work.

7. **What should you include in a good external todo list?**
   - Phases or sections for organization
   - Checkboxes for each task
   - Clear, actionable task descriptions
   - Progress notes section for AI updates
   - Specific enough to track detailed work

---

## Troubleshooting

**Issue:** AI doesn't create built-in todo list  
**Solution:** Explicitly mention "create a todo list" or "track this with todo list" in your prompt. Ensure Agent mode is enabled.

**Issue:** AI doesn't update external TODO.md file  
**Solution:** Explicitly ask AI to "update the checkboxes in @TODO.md as you complete tasks". Make sure the file is referenced with @-mention.

**Issue:** Todo list items are too vague  
**Solution:** Break down tasks into specific, measurable steps. Instead of "improve code", use "add type hints to calculate() function" and "add error handling for division by zero".

**Issue:** AI completes tasks but doesn't mark them done  
**Solution:** Remind AI: "Update the todo list after completing each task, not all at once at the end".

**Issue:** Can't find built-in tools icon  
**Solution:** Look for wrench, key, or settings icon near the chat input. In some versions it's above the input, in others below. Try clicking near the model name selector.

**Issue:** External todo list gets out of sync  
**Solution:** Periodically ask AI to "verify @TODO.md reflects actual completion status and update if needed". Add explicit instruction in prompt: "Keep TODO.md synchronized".

---

## Advanced Techniques

### Hierarchical Todo Lists

For very complex projects, use nested todo lists:

```markdown
# Epic: Calculator Package Refactoring

## Phase 1: Foundation ✅ COMPLETED
- [x] Setup
- [x] Initial refactoring

## Phase 2: Testing 🔵 IN PROGRESS
- [x] Write test structure
- [ ] Implement unit tests
  - [x] test_calculate_add()
  - [x] test_calculate_subtract()
  - [ ] test_calculate_multiply()
  - [ ] test_calculate_divide()
  - [ ] test_error_cases()
- [ ] Achieve 80% coverage

## Phase 3: Documentation ⏳ NOT STARTED
- [ ] Create README
- [ ] Add docstrings
```

### Todo + Decision Log

Combine todo with decision tracking:

```markdown
# TODO + Decisions

## Tasks
- [x] Add type hints
- [x] Add error handling
- [ ] Add logging

## Decisions Made
- **2026-02-17:** Decided to use Google-style docstrings (more readable than Sphinx)
- **2026-02-17:** Chose pytest over unittest (better fixtures and plugins)

## Questions for User
- Should we add logging? If yes, what level (INFO, DEBUG)?
- Do you want config file support?
```

### Combined Memory Stack

For maximum effectiveness, use all three:
1. **PROJECT_SPEC.md** - Strategic goals and requirements
2. **TODO.md** - Tactical task list
3. **Built-in todo** - Real-time visual progress

Prompt template:
```
I have:
- @PROJECT_SPEC.md with project requirements
- @TODO.md with implementation tasks

Please:
1. Read both documents
2. Create built-in todo list for visual tracking
3. Update @TODO.md as you complete each task
4. Verify all changes align with spec requirements

Use Agent mode.
```

---

## Next Steps

You now know how to give AI agents persistent memory through todo lists. In the next module, [Version Control with Git](../060-version-control-git/about.md), you'll learn how to save your progress and roll back mistakes using Git's baby steps approach.

**Try this:** Before moving on, practice with a real task from your work. Create a todo list for something you need to build, then let AI work through it autonomously.
