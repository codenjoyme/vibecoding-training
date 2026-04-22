<follow>
    iterative-prompt.agent.md
</follow>

## Context

During a training session on module 040 (Agent Mode Under the Hood), a gap was identified:
the **Anchor technique** is never explicitly named or described anywhere in the course modules.

**What the Anchor technique is:**
When you show the model an example of the desired output directly in the prompt, you anchor the first tokens of generation toward your intent. This works because the model predicts the next token based on all preceding text — a concrete example shifts the probability distribution immediately.

It is different from chain-of-thought (which structures reasoning) and different from "explain then implement" (which delays action). Anchor is specifically about **showing, not describing** the expected result shape.

**Where it's relevant:**
- Module 040: explains token generation and temperature — Anchor fits naturally here as a practical implication
- Module 056: Prompt Engineering Toolkit — already covers chain-of-thought; Anchor belongs in the same toolkit
- Module 064: Debugging — already uses `expect/actually` pattern which is a form of anchoring

## UPD1

Research and decide:
1. Where should Anchor technique be documented — 040, 056, or both?
2. What's the minimal addition (a paragraph, a section, a new Part)?
3. Draft the content — keep it consistent with the existing walkthrough style

Do NOT implement yet. Only produce a proposal with the draft content and placement rationale.
