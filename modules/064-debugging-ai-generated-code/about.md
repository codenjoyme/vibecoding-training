# Debugging AI-Generated Code

**Duration:** 15 minutes

**Skill:** Apply a systematic debugging workflow to break out of infinite "paste error → get fix → new error" loops when working with AI-generated code.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Why naive error-pasting fails and how to avoid the debug loop trap
- Reading error messages: type, message, stack trace, location
- Isolation technique: find the minimal reproduction of the problem
- The "debug prompt" template: giving AI the right context
- Escape hatches: when to stop debugging and rewrite or rollback

## Learning Outcome

You can diagnose a broken AI-generated script, isolate the problem systematically, provide AI with the correct context to fix it, and know when to stop and rollback to a clean Git state instead.

## Prerequisites

### Required Modules

- [050 — Effective Prompting](../050-effective-prompting-without-arguing/about.md)
- [060 — Version Control with Git](../060-version-control-git/about.md)

### Required Skills & Tools

- A working project or PoC with some AI-generated code
- Terminal (PowerShell on Windows, bash/zsh on macOS/Linux)
