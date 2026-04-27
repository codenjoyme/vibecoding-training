# Vibecoding for Everyone Training

A comprehensive, hands-on training program teaching everyone how to effectively use AI coding assistants (vibecoding) in their work. Each module delivers one actionable skill you can apply immediately.

Read more about the project motivation and approach: [Motivation](motivation.md)

## 🚀 Get Started

- **Learners** → open [quickstart.md](quickstart.md) — install the IDE, pick a model, and start your first module.
- **Authors / contributors** → open [for-authors.md](for-authors.md) — everything you need to write modules and improve the course.
- **Recommended path** → see [base-course.md](base-course.md) for a curated sequence of base + advanced modules.

## 💬 Just Talk to Your IDE

Open this project in **VS Code (Copilot)**, **Cursor**, or **Claude Code** in agent mode and ask in plain language:

- `давай пройдем модуль 050` / `let's do module 050`
- `я хочу решить такую-то задачу — какие модуля мне помогут?` / `which modules help me with X?`
- `создай новый модуль про Y` / `create a new module about Y`

The AI will pick the right instructions, walk you through the module, and track your progress.

## 🗂 Module Catalog

The full, up-to-date list of modules (ID, name, description) lives in [modules/module-catalog.md](modules/module-catalog.md). Browse the [training plan](training-plan.md) for the recommended sequence.

## 🧱 How a Module Is Structured

Each module is a single folder under [modules/](modules/) and contains, at minimum:

- **about.md** — duration, skill statement, topics, learning outcome, prerequisites
- **walkthrough.md** — step-by-step hands-on practice
- **tools/** *(optional)* — `skills.md`, scripts, reference materials, sample data — anything the practical part needs

## 🤖 How the Automation Works

All automation is driven by **tool-agnostic instruction files** in [instructions/](instructions/). The architecture is described in [creating-instructions.agent.md](instructions/creating-instructions.agent.md): IDE-specific entry points (Copilot / Claude / Cursor / others) all route into [main.agent.md](instructions/main.agent.md), which dispatches to the right instruction.

Two instructions do most of the heavy lifting:

- [create-training-module.agent.md](instructions/create-training-module.agent.md) — used whenever you ask the agent to create a module
- [training-mode.agent.md](instructions/training-mode.agent.md) — used whenever you ask the agent to run you through a module in coaching mode

Full author workflow is documented in [for-authors.md](for-authors.md).

## 🛠 How Improvements Are Made

Course-wide changes and new module proposals are tracked as **iterative prompts** in [requests/](requests/), following the [iterative-prompt.agent.md](instructions/iterative-prompt.agent.md) approach. Browse that folder to see exactly how previous modules and edits were created — it's the best way to learn the contribution style by example.

## 🤝 Contributing

Contributions of any size are welcome — typo fixes, content improvements, new modules, new topic requests. Start with [for-authors.md](for-authors.md), or open an issue describing what you'd like to see.

The course itself is "vibecoded" — built with AI assistance following its own instructions and patterns. 🙏
