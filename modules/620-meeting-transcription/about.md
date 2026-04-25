# Microsoft Teams Meeting Transcription

**Duration:** 15-25 minutes
**Skill:** Take a raw Teams meeting transcript (`.docx`), unpack it, parse the underlying XML, produce a clean `.txt` that an LLM can consume — with optional anonymization of speaker names so personal data never leaves your machine.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- A `.docx` file is just a ZIP archive — how to open it without external libraries
- Where the actual content lives: `word/document.xml` and the `<w:p>` / `<w:r>` / `<w:t>` schema
- Bootstrapping a transcription helper from an existing instruction (`transform-meeting-transcript.agent.md`)
- Anonymization on extraction: speakers → `Speaker 1`, `Speaker 2`, …; redacting names inside the body and in the metadata
- The two trust levels: the anonymized `.txt` (safe to send to an LLM) vs the `.mapping.json` sidecar (must never leave the machine)
- Choosing between the inline PowerShell pipeline and a small Python wrapper

## Learning Outcome

You can take any Teams meeting recording transcript, turn it into a clean text file that's easy to feed to an LLM, and decide per-run whether to keep real names or strip them down to neutral pseudonyms.

## Prerequisites

### Required Modules

- [108 — Token & API Key Management](../108-token-api-key-management/about.md)
- [110 — Development Environment Setup](../110-development-environment-setup/about.md)

### Required Skills & Tools

- A Microsoft Teams meeting recording with transcript enabled, exported as a `.docx`
- PowerShell (Windows) — built-in
- Optional: Python 3.10+ if you prefer a Python wrapper

## When to Use

- You want to summarize, search, or analyze meeting content with an LLM
- You need to share meeting takeaways with people outside the meeting and want to strip personal names first
- You're building any automation that needs the spoken content of a meeting as plain text

## Resources

- [`transform-meeting-transcript.agent.md`](../../instructions/coaching/transform-meeting-transcript.agent.md) — the canonical instruction with the full extraction pipeline, anonymization algorithm, summary templates, and quality checklist
- The same file on GitHub (so you can `Setup ...` it from any project): https://github.com/codenjoyme/vibecoding-training/blob/main/instructions/coaching/transform-meeting-transcript.agent.md
- [600 — Microsoft Teams AI Chat Summarizer](../600-teams-ai-chat-summarizer/about.md) — the natural follow-up: post the resulting summary back into Teams
