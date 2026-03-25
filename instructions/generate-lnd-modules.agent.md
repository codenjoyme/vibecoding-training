## Motivation

- The course "Vibe Coding for Managers" needs to be published into the EPAM LND LMS platform.
- LND (Learning & Development) department accepts content following strict formatting rules and quality standards.
- This instruction automates the generation of LMS-ready markdown files from existing `walkthrough.md` modules.
- Each generated file is a standalone lesson storyboard for one LND module, ready for LMS upload.
- The practical thread running through the course is a Jira/Confluence automation project built incrementally.

## Context and Source Files

- **Existing modules**: `./modules/[number]-[name]/walkthrough.md` — raw training walkthroughs written for AI-guided sessions.
- **LND rules** (extracted to `.md`): `./lnd/rules/*.md` — formatting standards, lesson development guide, course description guide, test question guide, self-review checklist, content guidelines.
- **LND reference** (extracted to `.md`): `./lnd/reference/*.md` — example modules from another course (n8n automation) showing the expected output format: page-based structure, Background/Steps/Result pattern.
- **LND feedback**: `./lnd/feedback/feedback.md` — reviewer recommendations on which modules to include/exclude.
- **Module plan (ТЗ)**: `./lnd/lnd-module-plan.md` — approved list of modules with sequence, practical assignment notes, and per-module recommendations.
- **PDF/DOCX extraction script**: `./lnd/extract_pdfs.py` — Python script that extracted binary files to markdown.

## Workflow Overview

- Phase 1: Extract content from PDF/DOCX (completed — `.md` files already generated in `lnd/rules/` and `lnd/reference/`).
- Phase 2: Review feedback and agree on module list with course owner (completed — see `lnd/lnd-module-plan.md`).
- Phase 3: Generate LND-ready markdown files, one per module, into `./lnd/output/` folder.
- Phase 4: Course owner reviews, provides corrections, agent iterates.
- Phase 5: Final quality check against SME Self-Review Checklist.

## LND Content Principles (from rules)

- Follow the **Lesson Development Guide**: each lesson has Introduction (hook), Body (chunked content), Conclusion (summary + key takeaways).
- **Introduction hooks**: use intriguing question, statistics, analogy, short story, or problem scenario. Make it relatable and memorable.
- **Body structure**: headings and subheadings in logical order; use "bridge-building" sentences between sections; chunk into small paragraphs and bulleted lists.
- **Conclusion**: recap key points; provide useful links for further learning; list downloadable materials if any.
- Use **second-person pronouns** (you, your) to address the learner. Avoid first-person (we, our, us, my).
- Learning objectives use **observable action verbs** (apply, create, configure, implement, demonstrate). Avoid vague verbs (know, understand, learn, get acquainted).
- Follow **Bloom's taxonomy** levels: Remember → Understand → Apply → Analyze → Evaluate → Create.
- **Plagiarism**: content must be below 8% plagiarism. Rephrase, don't copy-paste from external sources.
- **Quiz questions**: 3 answer options usually enough; 1 correct answer not too obvious among distractors; provide feedback explaining why each answer is correct/incorrect.
- **Practical tasks**: go after theory and quizzes; write detailed instructions on how to complete; connect to real job tasks.
- **Course description**: short description (290 chars max); audience specification; hook (quote/question/stats/case); Why-What-How structure.
- **Visual standards**: images must be relevant and readable; diagrams should have legible text; videos 1920x1080, ~6 min, with subtitles.

## Output File Format (per module)

- One markdown file per module in `./lnd/output/` folder.
- Filename: `module-[sequence-number]-[short-name].md` (e.g., `module-01-installing-vscode.md`).
- Follow the reference module structure from `./lnd/reference/`:

```
# Module [N]: [Title]

### Background
[Introduction hook + context paragraph. Why this matters. What learner will be able to do.]

## Page 1: [Section Title]
### Background
[Context for this section]
### Steps
[Numbered step-by-step instructions]
### ✅ Result
[What learner should see/have after completing this page]

## Page 2: [Section Title]
...

## Page N: [Final Section]
...

## Summary
[Key takeaways, recap of what was accomplished, useful links]

## Quiz
[Quiz questions]
```

- **Heading levels are mandatory** and must be applied consistently:
  - `#` (H1) — Module title only (one per file): `# Module N: Title`
  - `##` (H2) — Page headings, Summary, and Quiz: `## Page 1: Title`, `## Summary`, `## Quiz`
  - `###` (H3) — Section headings within pages: `### Background`, `### Steps`, `### Steps (variant name)`, `### ✅ Result`
- **All URLs must be markdown links.** Never leave bare URLs in the text. Use `[https://example.com](https://example.com)` format. The only exception is URLs inside fenced code blocks (JSON, shell commands, etc.) — those stay as plain text.
- Each "Page" corresponds to a logical section that can be rendered as one LMS page/screen.
- Keep pages focused: one concept or one hands-on task per page.
- Aim for 3-7 pages per module depending on complexity.
- Include `✅ Result` after each page to help learner verify progress.
- Add quiz questions at natural checkpoints (after theory sections, at end of module).

## Generation Process (per module)

- Read the source `walkthrough.md` for the module.
- Read the corresponding `about.md` for learning objectives and topics.
- Read the module-specific notes from `lnd/lnd-module-plan.md`.
- Transform content into the LND page-based format:
  + Rewrite introduction as a proper hook (question, scenario, or statistic).
  + Chunk walkthrough steps into logical pages.
  + Add Background sections explaining "why" before each hands-on section.
  + Convert success criteria into `✅ Result` blocks.
  + Add 2-3 quiz questions per module at appropriate points.
  + Rewrite in second-person voice throughout.
  + Ensure action verbs in all learning objective statements.
- Cross-reference with Self-Review Checklist items:
  + Learning objectives clearly stated?
  + Introduction with hook present?
  + Content accurate and up-to-date?
  + Summary with key points?
  + Quiz/practical task present?
  + Instructions clear and unambiguous?

## Quality Checklist (before delivering each module)

- [ ] Hook in introduction (question/story/stats/analogy)?
- [ ] Learning objectives with action verbs (no "know/understand/learn")?
- [ ] Second-person voice throughout (no "we/our")?
- [ ] Content chunked into readable pages (3-7 pages)?
- [ ] Each page has Background + Steps + ✅ Result?
- [ ] At least 2 quiz questions with feedback?
- [ ] Practical task connected to the Jira/Confluence project thread?
- [ ] Summary with key takeaways?
- [ ] No plagiarized content?
- [ ] Consistent formatting matching reference modules?
