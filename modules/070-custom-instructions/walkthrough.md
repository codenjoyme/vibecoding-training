# From Prompt to Instruction System

> **Time:** 20-25 minutes  
> **Goal:** Transform one-time prompts into reusable instruction architecture

---

## Introduction: The Problem with Copy-Pasting Prompts

### Scenario: Repetitive Tasks

You successfully worked with AI to solve a problem. It took iterations (like Module 050 taught):
1. Initial prompt
2. AI response
3. Refinement: "actually, do it this way..."
4. Another refinement: "and also consider..."
5. Final version works perfectly!

**Next week:** Same type of task appears. You want that refined prompt again.

**Current solution:** Copy-paste from old chat. But:
- Which chat was it?
- Which message had the final version?
- Did you edit it after copying?

**Better solution:** Save it as reusable instruction.

---

## Part 1: Evolution Stages (5 minutes)

### Stage 1: Everything is a Prompt

**You type every time:**
```
Create Python function that:
- Validates email format
- Checks domain against whitelist
- Returns detailed error messages
- Includes type hints
- Has docstring with examples
```

**Works for one-off tasks.** But repetitive for common patterns.

### Stage 2: Text File

**You save to:** `my-prompts.txt`

```
EMAIL VALIDATOR PROMPT:
Create Python function that validates email format, checks domain against whitelist,
returns detailed error messages, includes type hints, has docstring with examples.
```

**Usage:** Open file, copy, paste into chat with "Do this for user registration form"

**Better!** But still manual copy-paste. And growing unstructured file becomes messy.

### Stage 3: Markdown Format

**You create:** `email-validation.md`

```markdown
# Email Validation Function

Create Python function with:
- Email format validation using regex
- Domain whitelist checking
- Detailed error messages for each validation failure
- Type hints for all parameters and return values
- Docstring with usage examples

Implementation requirements:
- Use `re` module for regex
- Return tuple: (is_valid: bool, error_message: str)
- Whitelist as function parameter with default common domains
```

**Why markdown?**
- AI agents **love** markdown structure
- Headers organize requirements
- Lists make requirements scannable
- Code blocks show examples clearly
- More maintainable than plain text

**Still manual:** You attach file or copy-paste content.

### Stage 4: Instruction System

**The magic:** AI automatically sees relevant instructions when you ask.

**You just type:**
```
Create email validator for signup form
```

**AI sees (automatically):**
- Your `email-validation.agent.md` instruction
- Knows to apply structured requirements
- Consistent output every time

**How?** Continue to next part...

---

## Part 2: Creating Your First Instruction (6 minutes)

### Step 1: Choose a Repetitive Task

Think about your recent AI sessions. What did you ask more than once?

**Examples:**
- "Create Python function with type hints and docstrings"
- "Write unit tests for this code"
- "Refactor this to follow SOLID principles"
- "Generate API documentation from code"
- "Create .gitignore for Python project"

**Pick one** you want to try first.

### Step 2: Create Instruction File

**Folder structure:**
```
your-project/
  instructions/
    main.agent.md         (will create later)
    create-function.agent.md
    write-tests.agent.md
```

**Naming convention:**
- `[action-verb]-[subject].agent.md`
- Examples: `create-function`, `write-tests`, `refactor-code`, `generate-docs`
- Start with **verb** (action you want AI to perform)

**Let's create `create-function.agent.md`:**

**Prompt for AI:**
```
Following instructions in ./instructions/creating-instructions.agent.md,
create instruction for Python function creation with:
- Type hints required
- Docstring with examples
- Input validation
- Error handling
- Unit test friendly structure
```

**AI will create file like:**
```markdown
- All functions must include type hints for parameters and return values
- Add comprehensive docstring with purpose, parameters, returns, and examples
- Validate input parameters at function start
- Raise appropriate exceptions for invalid inputs
- Use descriptive variable names
- Keep functions focused on single responsibility
- Structure code to enable easy unit testing
- Example format:
  + Function signature with types
  + Docstring with usage example
  + Input validation block
  + Main logic
  + Return statement
```

**Notice:**
- Bullet points (not headers) - easier for AI to parse
- Action-oriented statements
- Concrete requirements
- Example structure at end

### Step 3: Test Your Instruction

**Prompt:**
```
Following ./instructions/create-function.agent.md,
create function to parse CSV file and return list of dictionaries
```

**AI should apply all rules from instruction automatically.**

**Review output:**
- Has type hints? ✓
- Has docstring with examples? ✓
- Input validation? ✓
- Error handling? ✓

**If something missing:** Update instruction file to be more explicit.

---

## Part 3: Instruction Architecture (5 minutes)

### The main.agent.md Pattern

**Problem:** You have 10+ instruction files. How does AI know which one to use?

**Solution:** Create catalog file that AI checks every time.

### Step 4: Create main.agent.md

**File:** `./instructions/main.agent.md`

```markdown
# Main Instruction Catalog

This file serves as catalog of all project instructions.

## Available Instructions

- `create-function.agent.md` - Python function creation with type hints, docstrings, validation, and test-friendly structure
- `write-tests.agent.md` - Unit test creation with pytest, fixtures, parametrize, and coverage considerations
- `generate-docs.agent.md` - API documentation generation from code with examples and usage patterns
```

**Pattern:**
- One line per instruction
- Brief description of what it covers
- AI scans this on every prompt to find relevant instruction

### Step 5: Create Entry Point

**This makes AI load main.agent.md automatically.**

#### For VSCode + GitHub Copilot:

**File:** `.github/copilot-instructions.md`
```markdown
- Important! Always follow the instructions in `./instructions/main.agent.md` file.
- It contains links to other files with instructions.
- You should reload it in **every prompt** to get the latest instructions - because of the dynamic nature of the project.
```

**That's it!** Now AI sees your instruction catalog on every prompt.

#### For Cursor:

**File:** `.cursor/rules/main.mdc`
```markdown
---
description: Main instruction orchestrator
globs:
alwaysApply: true
---

- Important! Always follow the instructions in `./instructions/main.agent.md` file.
- It contains links to other files with instructions.
- You should reload it in **every prompt** to get the latest instructions.
```

### Step 6: Test Auto-Discovery

**Just type:**
```
Create function to validate phone numbers
```

**AI should:**
1. Check `main.agent.md`
2. Find `create-function.agent.md` is relevant
3. Apply those rules
4. Create function with type hints, docstring, validation, etc.

**No need to reference instruction explicitly!**

### ⚡ Alternative: Bootstrap with Single Command

**Don't want to set up files manually? Use the bootstrap shortcut.**

In a **brand-new project with no instruction infrastructure**, open a fresh agent session and type:

```
Setup https://github.com/codenjoyme/vibecoding-training/blob/main/instructions/creating-instructions.agent.md
```

**What happens:**
1. AI fetches the `creating-instructions.agent.md` from GitHub
2. Detects your IDE by checking for `.github/` or `.cursor/` folder
3. Creates all required files automatically:
   - Entry point (`.github/copilot-instructions.md` or `.cursor/rules/mcpyrex.mdc`)
   - `instructions/main.agent.md` catalog
   - `instructions/creating-instructions.agent.md` locally
   - IDE settings (`.vscode/settings.json` for VSCode)
4. Confirms installation is complete

**When to use:**
- ✅ Starting a new project from scratch
- ✅ Onboarding a team member to a repo that has no instructions yet
- ✅ Replicating instruction infrastructure to another project

**After bootstrap** — you continue from Step 7 and add your own instructions on top.

---

## Part 4: SPR Principle and When to Split (4 minutes)

### Single Responsibility Principle for Instructions

**One instruction = One workflow**

### Example: Too Broad ❌

**File:** `python-best-practices.agent.md`
```markdown
- Use type hints
- Write docstrings
- Add unit tests
- Follow PEP 8
- Use virtual environments
- Create .gitignore
- Write README
- Add logging
- Handle exceptions
- ... (50 more points)
```

**Problem:**
- Applied to every Python task (even when irrelevant)
- Hard to maintain
- Difficult to reuse parts

### Example: Well Split ✅

**Separate files:**
- `create-function.agent.md` - Function creation specifics
- `write-tests.agent.md` - Testing workflow
- `setup-project.agent.md` - Project initialization
- `code-style.agent.md` - Style guide

**Benefits:**
- Specific prompts trigger specific instructions
- Easy to update one aspect
- Reusable across projects

### When to Split

**Create new instruction when:**
- ✅ Task repeats 3+ times
- ✅ Has distinct workflow
- ✅ Takes >2 paragraphs to describe
- ✅ Other projects might need same pattern

**Keep in same instruction when:**
- ❌ Steps always happen together
- ❌ Makes no sense separately
- ❌ Very short (2-3 bullets)

### Referencing Other Instructions

**From one instruction, reference another:**

```markdown
- For function creation specifics, follow `./instructions/create-function.agent.md`
- For test creation, follow `./instructions/write-tests.agent.md`
```

**AI will load referenced instructions automatically.**

---

## Part 5: Capturing Session Knowledge (5 minutes)

### The Critical Habit

**After every successful AI session, ask:**

> "Should I create an instruction from this?"

**Why?** That session had failed attempts, iterations, refinements. You found what works. **Capture it!**

### Step 7: Extract Instruction from Session

**You just spent 20 minutes with AI:**
- Tried 3 different approaches to parse JSON
- Hit encoding issues
- Found working solution with proper error handling

**Don't let that knowledge disappear!**

**Prompt:**
```
Following ./instructions/creating-instructions.agent.md,
create instruction based on this chat session for JSON parsing with robust error handling
```

**AI will:**
1. Review conversation
2. Extract working patterns
3. Note what failed (to avoid in future)
4. Create instruction file

**Result:** Next time JSON parsing needed, you won't repeat same trial-and-error.

### Step 8: Update Existing Instruction

**Scenario:** You have `create-api-client.agent.md` but this session revealed:
- Need retry logic for network failures
- Better timeout handling
- Request rate limiting

**Instead of creating new instruction:**

**Prompt:**
```
Following ./instructions/creating-instructions.agent.md,
update ./instructions/create-api-client.agent.md with new knowledge from this session:
- Add retry logic with exponential backoff
- Include configurable timeouts
- Implement rate limiting to respect API quotas
```

**AI will:**
- Read existing instruction
- Add new points (not rewrite everything)
- Preserve useful existing content
- Build upon it incrementally

**Always specify "update" not "rewrite"** - preserves your good existing content.

---

## Part 6: Making Agents Follow Instructions (3 minutes)

### What If AI Doesn't See Instruction?

**Sometimes AI doesn't auto-detect relevant instruction.**

#### Method 1: Explicit Reference

**Direct approach:**
```
Following ./instructions/create-function.agent.md,
create validator for email addresses
```

**AI will load and apply that instruction.**

#### Method 2: Tell Which Topic

**If you forgot exact filename:**
```
Following instruction for creating functions,
create validator for email addresses
```

**AI will:**
1. Check `main.agent.md` catalog
2. Find `create-function.agent.md` matches "creating functions"
3. Load and apply it

#### Method 3: Shortcut Prompts

**Create shortcuts for common combos:**

**File:** `.cursor/rules/shortcuts.mdc` or `.github/prompts/shortcuts.prompt.md`

```markdown
When user says "new function":
- Follow ./instructions/create-function.agent.md
- Follow ./instructions/write-tests.agent.md

When user says "new API endpoint":
- Follow ./instructions/create-api-endpoint.agent.md
- Follow ./instructions/write-tests.agent.md
- Follow ./instructions/update-docs.agent.md
```

**Now you just type:**
```
new function for email validation
```

**AI applies all related instructions.**

#### Method 4: Smart Model Auto-Detection

**If you selected smart model (GPT-4, Claude Sonnet, etc.):**

**Just describe what you want:**
```
Create email validation function
```

**Smart model will:**
- Scan `main.agent.md`
- Find relevant instructions
- Apply them automatically

**No explicit reference needed** if model is good and instructions are well-organized.

---

## Part 7: Practical Exercise (2 minutes)

### Your Turn: Create Instruction System

1. **Create folder:** `./instructions/`

2. **Think of 2-3 repetitive tasks** you've asked AI to do multiple times

3. **For each task, create instruction file:**
   - Use naming: `[verb]-[subject].agent.md`
   - Write bullet points
   - Keep it actionable
   - Include examples if helpful

4. **Create main.agent.md** with catalog of your instructions

5. **Create entry point** for your IDE (see Part 3, Step 5)

6. **Test it:**
   - Open new chat
   - Ask for task without referencing instruction
   - Check if AI applies your rules

7. **Refine:**
   - If AI misses something, update instruction
   - Add more specific bullets
   - Include examples of expected output

---

## Key Takeaways

### Evolution Path

```
One-time prompt
    ↓
Copy-paste from old chats
    ↓
Text file with prompts
    ↓
Markdown instruction files
    ↓
Instruction system with auto-detection
```

### Critical Habits

**✅ After every productive session:**
```
Ask: "Should I create/update instruction from this?"
```

**✅ When task repeats 3rd time:**
```
Stop. Create instruction. Never repeat manually again.
```

**✅ Keep instructions focused:**
```
One workflow per file (SPR principle)
```

**✅ Use action verbs in filenames:**
```
create-*, write-*, generate-*, update-*, refactor-*
```

### Architecture Benefits

**Before instructions:**
- Repeat same prompts
- Inconsistent results
- Knowledge lost between sessions

**After instructions:**
- Type simple request
- Consistent high-quality output
- Knowledge compounds over time

### Platform Independence

**Your instructions work:**
- ✓ VSCode + GitHub Copilot
- ✓ Cursor
- ✓ Other AI IDEs (with appropriate entry point)
- ✓ Even copy-paste to ChatGPT/Claude web

**Markdown is universal.** Platform-specific parts are just tiny entry point files.

---

## Next Steps

### Start Small

**Don't create 50 instructions at once.**

**This week:**
1. Create `main.agent.md` catalog (even if empty)
2. Create entry point for your IDE
3. Add ONE instruction for most repetitive task
4. Test it, refine it

**Next week:**
- Add 2nd instruction when pattern repeats
- Update existing instruction if you learn something new

**Over time:**
- You'll accumulate 10-20 solid instructions
- Your AI interactions become more consistent
- Less explanation needed in prompts

### Advanced: Team Sharing

**Instructions are just markdown files** → commit to git!

**Team benefits:**
- Everyone gets same AI output quality
- New members inherit team knowledge
- Instructions evolve with team learnings

**Create:**
```
your-project/
  instructions/
    main.agent.md
    create-function.agent.md
    write-tests.agent.md
  .gitignore  (don't ignore instructions!)
```

**Commit it.** Team members pull, get instructions automatically.

---

## Common Questions

**Q: How long should instruction be?**
**A:** 10-20 bullets usually enough. If >30, consider splitting.

**Q: Should I write instructions for everything?**
**A:** No! Only for repetitive patterns. One-offs don't need instructions.

**Q: What if AI ignores my instruction?**
**A:** 
- Check entry point file exists (`.github/copilot-instructions.md` or `.cursor/rules/main.mdc`)
- Try explicit reference: "Following ./instructions/X.agent.md, do Y"
- Make instruction bullets more specific/concrete

**Q: Can I have multiple main.agent.md files?**
**A:** No, only one catalog. But you can organize instructions in subfolders if project is huge.

**Q: Should instructions include code examples?**
**A:** Yes, but minimal. Show pattern, not full implementation.

**Q: What if my team uses different IDEs?**
**A:** Instructions are IDE-agnostic! Only entry point differs:
- VSCode users create `.github/copilot-instructions.md`
- Cursor users create `.cursor/rules/main.mdc`
- Both reference same `./instructions/main.agent.md`

---

## Reference: Complete File Structure

```
your-project/
  instructions/
    main.agent.md                    # Catalog of all instructions
    create-function.agent.md         # Function creation workflow
    write-tests.agent.md             # Testing workflow
    setup-project.agent.md           # Project initialization
    
  # VSCode + GitHub Copilot:
  .github/
    copilot-instructions.md          # Entry point
    prompts/                         # Optional shortcuts
      to-create-function.prompt.md
      
  # OR Cursor:
  .cursor/
    rules/
      main.mdc                       # Entry point
      shortcuts.mdc                  # Optional shortcuts
```

---

## Further Reading

**Full reference:** [creating-instructions.agent.md](../../instructions/creating-instructions.agent.md)

**Topics covered in detail:**
- IDE-specific syntax and entry points
- Advanced instruction organization
- Referencing shared instructions
- Updating existing instructions without rewriting
- Platform-specific adapters (modes, globs, alwaysApply)
- Team collaboration patterns
- Debugging instruction loading issues
