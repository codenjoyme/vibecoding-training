# Creating Training Modules from Articles — Hands-on Walkthrough

In this module, you'll learn the "module factory" workflow: take any article or resource about a GenAI topic, feed it to an AI agent along with the course creation instructions, and get back a complete, properly formatted training module. You'll create a real module from a real article, verify it against the quality checklist, and integrate it into the course.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

- **Understanding of module anatomy** — What makes a training module: required files, sections, formatting rules
- **A real training module** — Created from an article you choose, with `about.md` + `walkthrough.md`
- **Quality review** — Verified against the course quality checklist
- **Integration** — Module added to `training-plan.md` and committed to Git
- **Contribution workflow** — Fork & PR for contributing to shared repos

---

## Part 1: Understand the Module Structure

Every module in this course follows the same pattern. Before you create one, you need to know the anatomy.

### Module Folder

```
modules/
  [NUMBER]-[descriptive-name]/
    about.md          ← Module description, prerequisites, learning outcome
    walkthrough.md    ← Step-by-step hands-on guide
    tools/            ← (optional) Practical files used during the module
```

### tools/ Folder (Optional)

Some modules include a `tools/` subfolder with files the student uses during the walkthrough:

- **Scripts** — installation scripts, automation helpers, demo runners
- **Templates** — starter files, config templates, boilerplate code
- **Reference files** — sample data, example configs, pre-built artifacts
- **Instructions** — supplementary `.agent.md` files for specific tasks within the module

The walkthrough references these files directly (e.g., "Run the script at `./tools/install.ps1`"). If your module has hands-on exercises that need supporting files — put them in `tools/`. If the module is purely conversational or uses only inline code snippets — skip this folder.

### about.md Required Sections (in order)

1. **Title** — `# Module Name`
2. **Duration** — `**Duration:** 15 minutes`
3. **Skill** — One actionable sentence describing what the student will learn
4. **Walkthrough link** — `**👉 [Start hands-on walkthrough](walkthrough.md)**`
5. **Topics** — Bullet list of 4-6 concrete topics
6. **Learning Outcome** — One paragraph describing the measurable result
7. **Prerequisites** — Machine-parseable format:
   - `### Required Modules` — links to dependency modules
   - `### Required Skills & Tools` — plain bullet list

### walkthrough.md Required Sections

1. **Title** — `# Module Name — Hands-on Walkthrough`
2. **Introduction** — One paragraph explaining what you'll accomplish
3. **Prerequisites** — Single line: `See [module overview](about.md) for full prerequisites list.`
4. **What We'll Build** — List of components/outcomes before starting
5. **Numbered steps** — Using `1.` format (Markdown auto-numbers)
6. **Success Criteria** — Checklist with ✅
7. **Understanding Check** — 5-7 questions with answers
8. **Troubleshooting** — Common problems and solutions
9. **Next Steps** — Pointer to what comes next

### Key Rules

- Cross-platform paths: always show both Windows (`c:/workspace/hello-genai/`) and macOS/Linux (`~/workspace/hello-genai/`)
- No keyboard shortcuts — use menu names or generic descriptions
- Recommend **Claude Sonnet 4.5** as the model choice
- Prerequisites are ONLY in `about.md` — walkthrough just references it
- Understanding Check must have 5-7 questions **with answers**

---

## Part 2: Choose Your Source Material

You need an article, blog post, or technical resource about a GenAI topic. This should be something:

- **Interesting** — a topic you think others should know about
- **Practical** — has a hands-on component (not just theory)
- **Not already covered** — check the existing module list in `training-plan.md`

Good source examples:
- A blog post about a new AI coding tool or technique
- An article about prompt engineering patterns
- A tutorial about a specific MCP server or integration
- Documentation for a new AI framework or library

### Prepare the Source Text

1. Open the article in your browser
2. Copy the full text (or the relevant sections)
3. Create a file to hold it:
   - `c:/workspace/hello-genai/source-article.md` (Windows) or `~/workspace/hello-genai/source-article.md` (macOS/Linux)
4. Paste the article text into this file
5. At the top, add a brief note:

```markdown
# Source Material for Module Creation

**Article title:** [title]
**Key concept to teach:** [one sentence — what skill should the student get?]
**Proposed module ID:** [3-digit number — check gaps in training-plan.md]

---

[article text below]
```

> **Why save the text to a file?** The AI agent can read files in your workspace. This is more reliable than pasting long text into a chat message, and you keep a record of the source material.

---

## Part 3: The Module Creation Prompt

### What We'll Do

You'll send a structured prompt to the AI agent that combines: your source material + the course creation instructions + a specific module ID. The agent will generate both `about.md` and `walkthrough.md`.

### Open a New Chat Session

In VS Code or Cursor, open a new AI chat. Select **Claude Sonnet 4.5** as your model and enable **Agent Mode**.

### Send This Prompt

```
I want to create a new training module for the "Vibecoding for Everyone" course.

Source material: @source-article.md (read this file)

Instructions: follow the instructions in @create-training-module.agent.md

Key details:
- The article above describes [BRIEF DESCRIPTION OF CONCEPT]
- I want the module to teach: [ONE SKILL SENTENCE]
- Proposed module ID: [YOUR NUMBER]
- Module placement: after module [PREV MODULE ID] and before [NEXT MODULE ID]
- Determine prerequisites by looking at which existing modules 
  the student would need to complete first

Create:
1. about.md — following the exact format from the instructions
2. walkthrough.md — with hands-on steps based on the article content

Put them in a folder with the file path at ./modules/[MODULE-ID]-[descriptive-name]/
```

> **Note:** The `@` syntax references files in your workspace. If your IDE doesn't support this, you can instead say: "Read the file at `./instructions/create-training-module.agent.md` and the file at `./workspace/hello-genai/source-article.md`."

### What Just Happened

The AI agent should:
1. Read both files (source article + creation instructions)
2. Extract the teachable concept from the article
3. Generate `about.md` with proper sections and prerequisites
4. Generate `walkthrough.md` with hands-on steps derived from the article
5. Create the module folder and files

If the agent asks clarifying questions (about prerequisites, placement, etc.), answer them — this is the agent doing its job correctly.

---

## Part 4: Quality Review

The AI generated your module, but AI-generated content needs review. Go through this checklist:

### about.md Checklist

- [ ] Title is clear and describes the skill
- [ ] Duration is set (15 minutes is standard)
- [ ] Skill is one actionable sentence
- [ ] Walkthrough link points to `walkthrough.md`
- [ ] Topics has 4-6 concrete bullet points
- [ ] Learning Outcome is measurable
- [ ] `### Required Modules` uses correct format: `- [NNN — Title](../folder/about.md)`
- [ ] `### Required Skills & Tools` is a plain bullet list
- [ ] No free-form text outside the required format in Prerequisites

### walkthrough.md Checklist

- [ ] Title follows `# Module Name — Hands-on Walkthrough` format
- [ ] Prerequisites section says ONLY: `See [module overview](about.md) for full prerequisites list.`
- [ ] "What We'll Build" section exists before the steps
- [ ] Steps use `1.` numbering (not hardcoded numbers)
- [ ] Cross-platform paths are shown (Windows AND macOS/Linux)
- [ ] No keyboard shortcuts mentioned
- [ ] Success Criteria section has ✅ checkboxes
- [ ] Understanding Check has 5-7 questions WITH answers
- [ ] Troubleshooting section covers common issues
- [ ] Next Steps points to a logical follow-up module
- [ ] Complex actions have "What we'll do" before and "What happened" after

### Fix Issues

If you find problems, ask the AI agent to fix them specifically:

```
Fix these issues in the generated module:
1. Prerequisites format is wrong — use the exact format from the instructions
2. Understanding Check only has 3 questions — add 4 more with answers
3. No cross-platform paths — add Windows and macOS/Linux alternatives
```

---

## Part 5: Integration

### Update training-plan.md

1. Open `./training-plan.md`
2. Find the correct position based on your module ID (modules are listed in ID order)
3. Insert a new line:
   ```
   1. [Your Module Name](modules/[folder-name]/about.md) - Brief one-line description
   ```
4. All items use `1.` — Markdown auto-numbers them, so no renumbering needed

### Update module-catalog.md

1. Open `./modules/module-catalog.md`
2. Add a row to the table in the correct ID position:
   ```
   | [ID] | [Name] | [Description] |
   ```

### Verify Folder Naming

- Folder: `modules/[NUMBER]-[descriptive-name-with-dashes]/`
- Contains: `about.md` and `walkthrough.md`
- Folder name is lowercase with dashes, no spaces

### Commit to Git

```
git add modules/[your-folder]/ training-plan.md modules/module-catalog.md
git commit -m "Add module [ID]: [Module Name]"
```

---

## Part 6: Test-Walk the Module in a Fresh Session

### What We'll Do

Before considering the module "done", you need to walk through it yourself — as if you were a student seeing it for the first time. This is the most effective way to catch issues that the quality checklist misses.

### How to Test

1. **Open a new, empty chat session** in your IDE (no prior context)
2. **Ask the AI agent to walk you through the module** — just like a real student would:
   ```
   Let's go through module [ID] — [Module Name]
   ```
3. **Follow the walkthrough step by step** — execute commands, read explanations, answer questions
4. **Note anything that feels off** — unclear instructions, missing context, broken paths, wrong assumptions

### Fixing Issues During the Walk-Through

- When you spot a problem — **pause the walkthrough and fix it right there**
  + Say something like: "Wait, this step is unclear. Let's fix the walkthrough — change X to Y."
  + The AI agent will update the file, and you continue where you left off
- This interleaving of "walk + fix" is the normal workflow — you don't need to finish the whole walkthrough before making corrections
- **If you accumulate many fixes** (5+ edits across different sections), it's better to **start a fresh session** and walk through the module again from scratch
  + Why: the AI's context gets cluttered with edit instructions and may lose track of where you are in the walkthrough
  + A clean session ensures the fixed version reads well end-to-end

### What Just Happened

You've validated the module from the student's perspective. This step often catches 3-5 issues that looked fine during generation but break down during actual practice — wrong file paths, missing prerequisites, unclear transitions between steps.

---

## Part 7: Fork & PR Workflow (for Shared Repos)

If the course lives in a shared GitHub repository, you contribute modules through Pull Requests.

### What We'll Do

Walk through the standard fork → branch → commit → PR workflow for contributing a new module to a shared course repository.

### The Workflow

1. **Fork** the course repository on GitHub (if you haven't already):
   - Go to the repository on GitHub
   - Click "Fork" to create your personal copy

1. **Clone your fork** locally (or add as a remote if you already have the original):
   ```
   git remote add myfork https://github.com/YOUR-USERNAME/REPO-NAME.git
   ```

1. **Create a branch** for your new module:
   ```
   git checkout -b add-module-[ID]-[short-name]
   ```

1. **Add your module files** (already done in Step 5):
   ```
   git add modules/[your-folder]/ training-plan.md modules/module-catalog.md
   git commit -m "Add module [ID]: [Module Name]"
   ```

1. **Push to your fork**:
   ```
   git push myfork add-module-[ID]-[short-name]
   ```

1. **Create a Pull Request** on GitHub:
   - Go to your fork on GitHub
   - Click "Compare & pull request"
   - Describe what the module teaches and what source material you used
   - Submit the PR

### What Just Happened

Your module is now proposed as a contribution. The course maintainer will review the PR, check the module quality, and merge it if it meets standards. This is the "contribute a module" workflow — the same process used for any open-source contribution.

---

## Part 8: The Repeatable Pattern

You now have a repeatable workflow:

```
Find interesting article
    ↓
Save text to source-article.md
    ↓
Send "create module" prompt with @source-article.md + @create-training-module.agent.md
    ↓
AI generates about.md + walkthrough.md (+ tools/ if needed)
    ↓
Quality review against checklist
    ↓
Test-walk the module in a fresh session (fix as you go)
    ↓
Integration (training-plan.md, module-catalog.md)
    ↓
Git commit (or Fork + PR for shared repos)
```

Each iteration takes about 15-20 minutes for generation and review, plus another 10-15 minutes to test-walk and fix. You can produce a polished training module from any good article in under an hour.

---

## Success Criteria

- ✅ Understand the anatomy of a course module (`about.md` + `walkthrough.md` sections)
- ✅ Prepared source material with key concept and proposed module ID
- ✅ Created a complete module from an article using the AI agent
- ✅ Reviewed the generated module against the quality checklist
- ✅ Fixed any quality issues found during review
- ✅ Test-walked the module in a fresh chat session and fixed issues found
- ✅ Integrated the module into `training-plan.md`
- ✅ Understand the fork & PR contribution workflow

## Understanding Check

1. **What are the two required files in every module folder?**
   `about.md` (module description, topics, prerequisites, learning outcome) and `walkthrough.md` (step-by-step hands-on guide with exercises, success criteria, and understanding questions).

2. **Where should prerequisites be listed and why only there?**
   Only in `about.md`, in the `## Prerequisites` section with `### Required Modules` and `### Required Skills & Tools`. The walkthrough.md only references it with a link. This prevents duplication and ensures machine-parseability for dependency graph extraction.

3. **What format must Required Modules links follow?**
   `- [NNN — Title](../folder-name/about.md)` — where NNN is the 3-digit module ID. Optional dependencies get ` *(optional, recommended)*` suffix. This format enables regex parsing: `^\- \[(\d{3}) — (.+?)\]\((.+?)\)`.

4. **Why do we save the source article to a file instead of pasting it into chat?**
   Three reasons: (1) The AI agent can read workspace files reliably via `@` references, (2) long text in chat can hit token limits or get truncated, (3) you keep a record of the source material for future reference or attribution.

5. **What are three common quality issues to check after AI generates a module?**
   (1) Prerequisites not following the standardized format (free-form text instead of structured links), (2) Understanding Check missing answers or having too few questions, (3) Missing cross-platform paths (only showing Windows or only macOS/Linux).

6. **Why do walkthrough steps use `1.` numbering instead of `1.`, `2.`, `3.`?**
   Markdown auto-numbers items when all use `1.`. This means you can insert, remove, or reorder steps without manually renumbering — Markdown handles it automatically.

7. **Why test-walk the module in a fresh chat session, and when should you restart the session?**
   A fresh session has no prior context, so it tests the module the way a real student would experience it. You can fix issues during the walk-through (pause → fix → continue), but if you've made 5+ fixes across different sections, start a new session — the AI's context gets cluttered with edit instructions and may lose its place in the walkthrough.

8. **When would you use the fork & PR workflow vs direct commit?**
   Fork & PR for shared/team repositories where you don't have direct write access, or when you want the module reviewed before it's added. Direct commit when it's your own repository or you have maintainer permissions and the module is already reviewed.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| AI doesn't read the source article file | Check that you're using the correct `@` reference syntax for your IDE. Alternatively, paste the article text directly into the chat with a note: "Here is the source article:" |
| AI ignores the creation instructions format | Re-send with emphasis: "Follow EXACTLY the format in create-training-module.agent.md. Especially the Prerequisites section format and walkthrough.md structure." |
| Generated module is too short/thin | The source article may lack hands-on content. Ask AI: "The walkthrough needs more hands-on steps. Add practical exercises, verification steps, and a troubleshooting section." |
| Prerequisites link to non-existent modules | Verify module folder names in `./modules/`. The AI may guess incorrect folder names. Check and fix the relative paths manually. |
| Module ID conflicts with existing module | Check `training-plan.md` for all existing IDs. Use one of the available gaps documented in `proposed-modules.md`. |
| Fork & PR workflow fails on push | Verify your remote is set correctly: `git remote -v`. Ensure you're pushing to your fork, not the original repo. |
| AI generates keyboard shortcuts in walkthrough | Replace with menu paths or generic descriptions: "Open the command palette" instead of specific key combinations. |

## Next Steps

You can now create training modules from any source material. Consider using this skill to:
- Turn conference talks or webinar notes into team training
- Convert internal documentation into structured learning modules
- Build modules for technologies your team is adopting

Next in the course:
- [250 — Export Chat Session](../250-export-chat-session/about.md) to save your module creation sessions for reference
