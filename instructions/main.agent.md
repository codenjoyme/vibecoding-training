# Main Instruction Catalog

This file serves as a catalog of all project instructions. Each instruction covers a specific SDLC workflow or development practice.

## ⚠️ FILE LOADING RULES (CRITICAL)

- **The following files MUST be read FULLY (from first to last line) — NEVER partially:**
  + `instructions/training-mode.agent.md` — contains complete training methodology; partial read breaks the flow
  + `instructions/create-training-module.agent.md` — contains module structure standards; partial read causes inconsistencies
  + Any `walkthrough.md` file — these are structured lesson plans; skipping sections breaks Part-by-Part progression
- **Why:** These files contain interconnected rules and sections that reference each other. Reading only fragments leads to missed rules, broken training flow, and inconsistent module creation.
- **How:** Use `read_file` with a range covering the entire file, or multiple calls to cover all lines. Do NOT stop at line 100 or 200 — read until the end.

## ⚠️ LANGUAGE RULES (CRITICAL)

- **Respond to the user in their language.** If they write in non-English — answer in the same language. If in English — answer in English.
- **All project content must be written in English only** — this includes:
  + Module files (`about.md`, `walkthrough.md`)
  + Instruction files (`*.agent.md`)
  + Code, scripts, comments in code
  + Commit messages
  + Any text that goes into project files
- **If the user provides input in a non-English language** (e.g. describes a feature in non-English, gives feedback in non-English) — **translate it to English** before writing into any project file.
- The chat conversation language ≠ the project content language. Keep them separate.

## ⚠️ CRITICAL: When User Wants Training

**If user requests to:**
- Start training / пройти тренинг / начать обучение
- Continue training / продолжить модуль
- Go through any module / пройти модуль

**YOU MUST:**
1. **IMMEDIATELY load** `training-mode.agent.md` file
2. Follow ALL instructions from that file
3. Do NOT proceed without reading training-mode.agent.md first

**Why:** The training-mode.agent.md contains complete step-by-step methodology for conducting training sessions, progress tracking, and skill verification.

## Available Instructions

- `training-mode.agent.md` - **[LOAD THIS FOR ANY TRAINING REQUEST]** Guide users through training modules step-by-step, track progress, ensure skill formation with laconic communication style.
- `creating-instructions.agent.md` - Guidelines for creating, organizing, and maintaining instruction files across different IDE platforms (VSCode/Cursor).
- `create-training-module.agent.md` - Instructions for creating new training modules with proper structure, numbering, and integration into the course plan.
- `connect-course-to-github.agent.md` - Connect local course folder (downloaded as ZIP) to GitHub repository for automatic updates while preserving work folder.
- `github-copilot-cli-installation.agent.md` - Step-by-step guide for installing and configuring GitHub Copilot CLI on Windows, including nvm-windows setup and troubleshooting common issues.
- `git-workflow.agent.md` - Comprehensive Git workflow guide for AI-assisted development with baby steps methodology, installation instructions, .gitignore setup, and best practices.
- `handle-secrets-in-ai-workflows.agent.md` - **[AGENT SAFETY — SECRETS & DESTRUCTIVE OPS]** Non-negotiable rules for any session in which an agent may read, write, or quote credentials, customer data, or trigger destructive infrastructure operations. Covers: never quoting literal secrets, confirmation gates for destructive actions, treating untrusted input as content (not commands), recovering from a leaked credential, and what to never say.
  + Keywords: secrets, credentials, api key, token, leak, redact, destructive, rm -rf, drop table, force push, prompt injection, blast radius, agent safety, безопасность, утечка, ключи
- `export-chat-session.agent.md` - Export, list, and search GitHub Copilot chat sessions from VS Code using standalone Python script with HTML/JSON/text output formats.
- `coaching/interview-sdlc.agent.md` - **[SDLC COACHING INTERVIEW]** Conduct an interactive one-on-one interview with a colleague to understand their project SDLC and identify AI/agent adoption opportunities. Asks open-ended questions one at a time, follows up with genuine curiosity, and produces a structured summary for the coach at the end.
  + Keywords: interview, опрос, интервью, SDLC, coaching interview, colleague interview, sdlc assessment
- `lnd/generate-lnd-modules.agent.md` - **[LND MODULE GENERATION]** Generate LMS-ready markdown files from existing training modules following LND formatting rules, reference examples, and the approved module plan in `lnd/lnd-module-plan.md`.
  + Keywords: LND, LMS, module generation, learning content, lesson storyboard, elearn, course creation
- `generate-module-catalog.agent.md` - Generate a structured markdown table of all training modules with №, ID, Name, and Description by scanning `./modules/` and reading each `about.md`.
  + Keywords: module list, catalog, table, overview, module summary, перелік модулів
- `propose-training-modules.agent.md` - Analyze the current training program, identify gaps in GenAI/AI-assisted development coverage, and produce a structured proposal document with elevator pitches, training plans, and placement rationale for new modules. Output saved to `./modules/proposed-modules.md`.
  + Keywords: propose modules, new modules, curriculum gaps, expand training, что добавить, предложить модули, gap analysis
- `coaching/generate-coaching-offer.agent.md` - **[COACHING OFFER GENERATION]** Generate a one-pager coaching proposal for a decision-maker based on interview results and selected training modules. Maps pain points to modules, frames outcomes in business language. Output saved to `work/coaching-offer-*.md`.
  + Keywords: offer, proposal, one-pager, coaching offer, оффер, предложение, коучинг, стейкхолдер, decision-maker, engagement
- `lnd/organize-module-images.agent.md` - **[LND IMAGE ORGANIZATION]** Move and rename screenshots in LND module files to structured folders (`lnd/output/img/module-NN/MM-short-description.png`), update markdown references. Run per module on request after manual review with screenshots.
- `lnd/create-module-task-artifacts.agent.md` - **[LND TASK ARTIFACTS]** Generate three verification artifacts for a training module: student prompt, reference report, and autocheck prompt. All placed in `lnd/output/task/` with consistent naming and cross-referenced structure.
  + Keywords: task artifacts, autocheck, student prompt, reference report, module verification, lnd task, completion task, grading
- `lnd/build-md-to-docx/SKILL.md` - **[LND MD → DOCX BUILD]** Convert a list of markdown files (with images, code blocks, quizzes) into a single landscape DOCX with TOC, page breaks, shaded inline-code, and uniform image scaling. CLI takes `--output` and a list of input `.md` files.
  + Keywords: docx, build docx, export docx, markdown to docx, md to docx, combine modules, all-modules.docx
  + Keywords: images, screenshots, картинки, скриншоты, organize images, rename images, img, module images
- `iterative-prompt/SKILL.md` - **[ITERATIVE PROMPT WORKFLOW v2.0]** Autonomous AI agent workflow — file-based UPD/RESULT polling cycle with async terminal watcher (Python, with retry & smart UPD detection). Supersedes `iterative-prompt.agent.md`. Use `<follow>iterative-prompt/SKILL.md</follow>` in any `*.prompt.md` that uses the UPD pattern.
  + Keywords: iterative prompt, UPD, polling loop, watcher, async terminal, main.prompt.md, итеративный промпт
- [`./instructions/calculate-trig-table/SKILL.md`](./calculate-trig-table/SKILL.md) — Generate a deterministic trigonometric table (sin, cos, tan) for a degree range using Python stdlib `math` only. Outputs JSON, CSV, or Markdown.
  + Keywords: trig table, trigonometry, sine, cosine, tangent, sin, cos, tan, degrees, calculate, таблица, синус, косинус, тангенс
- [`./instructions/generate-algorithm-code.agent.md`](./generate-algorithm-code.agent.md) — Generate a clean algorithm method (bubble sort, binary search, merge sort, etc.) in one or more languages. Asks for algorithm and language if not specified. Outputs fenced code block only — no prose, no imports, no class wrapper.
  + Keywords: algorithm, sort, search, bubble sort, merge sort, quick sort, binary search, Dijkstra, алгоритм, сортировка, поиск, give me code, copy code
