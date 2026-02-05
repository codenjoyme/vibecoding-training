## Motivation

- When user asks to create new training module, gather all necessary information before implementation.
- Ensure consistency across all modules in structure and format.
- Maintain proper numbering and linking system.
- Each module is self-contained with clear learning outcomes.

## Module Structure

- All modules located in `./docs/modules/[number]-[name]/` directory.
- Each module contains two required files:
  + `about.md` - Module description, topics, outcomes, prerequisites
  + `walkthrough.md` - Step-by-step hands-on instructions to practice the skill
- Optional `tools/` directory for module-specific resources:
  + Scripts (Python, PowerShell, etc.) referenced in walkthrough
  + AI instruction files for automation tasks
  + Configuration files or templates
  + Any artifacts that learners create or use during practice
- Module folder name format: `[number]-[descriptive-name-with-dashes]`.
- Numbering uses increments of 10: 010, 020, 030, 040, etc.
- This allows inserting modules between existing ones using 015, 025, 035, etc.
- Folder names in alphabetical order match desired learning sequence.

## Creating New Module

- Ask user these key questions:
  + What specific skill will this module teach?
  + Where should it be placed in learning sequence (after which module)?
  + What are the main topics to cover (3-5 bullet points)?
  + What are the prerequisites (which modules should be completed first)?
  + What practical outcome should learner achieve?
  + What are the concrete hands-on steps to practice this skill?
- Determine module number based on placement (use existing number + 5 if between modules).
- Create descriptive folder name that reflects skill being taught.
- Generate both `about.md` and `walkthrough.md` filesbased on placement (use existing number + 5 if between modules).
- Create descriptive folder name that reflects skill being taught.
- Generate `about.md` file with proper structure.

## about.md File Structure

- Title: `# [Module Name]`
- Duration: `**Duration:** 5-7 minutes`
- Skill: `**Skill:** [One-sentence actionable skill description]`
- Link to walkthrough: `**👉 [Start hands-on walkthrough](walkthrough.md)**` (placed after Skill section)
- Topics section with bullet list of main topics covered
- Learning Outcome section with clear result statement
- Prerequisites section listing required prior modules/knowledge
- Optional: When to Use section for practical application guidance
- Optional: Resources section with links to tools/documentation

## walkthrough.md File Structure

- Title: `# [Module Name] - Hands-on Walkthrough`
- Brief introduction paragraph explaining what you'll accomplish
- Prerequisites section listing what needs to be completed first
- **"What We'll Install/Build" section** - Explain components before installation
  + List each component with brief description
  + Explain why it's needed
  + Include size/time estimates where relevant
- Numbered steps using `1.` format for auto-numbering (Markdown will auto-renumber)
- Each step should be clear, actionable, and verifiable
- **Before complex actions** - Section explaining what will happen and why
- **After complex actions** - Section explaining what just happened
- Include specific paths, commands, URLs where applicable
- Add screenshots references where helpful: `![description](./screenshots/step-X.png)`
- Include verification steps: "You should see...", "Verify that..."
- **Success Criteria section** - Checklist with ✅ of what should be accomplished
- **Understanding Check section** - Questions to verify comprehension
  + 5-7 questions covering key concepts
  + Include expected answers or key points to cover
  + Questions should test understanding, not just memory
- **Troubleshooting section** - Common problems and solutions
- Optional: When to Use section for practical guidance
- **Next Steps section** - Brief pointer to what comes next in the training
- Keep language simple and direct
- Use cross-platform paths: `c:/workspace/` (Windows) or `~/workspace/` (macOS/Linux)
- **Do not include keyboard shortcuts or hotkeys** - refer to menu items or generic descriptions instead
- Use `./workspace/hello-genai/` as the default test workspace path for consistency across modules
- Always mention alternative paths for different OS when giving directory examples
- When mentioning AI models, recommend **Claude Sonnet 4.5** as the best choice
- When setting up AI assistants, mention enabling **Agent Mode** where applicable

## Integration Steps

- After creating module folder and about.md file:
  + Update `./docs/training-plan.md` Module Sequence list
  + Insert new module link in correct position (all items use `1.` for auto-numbering)
  + Format: `1. [Module Name](modules/[number]-[name]/about.md) - Brief description`
  + No need to renumber other items - Markdown auto-numbers from `1.` markers
- Verify alphabetical folder order matches training-plan.md sequence.
- Check that module number fits numbering scheme (has space for future insertions).

## Naming Conventions

- Module folder names should be clear and descriptive.
- Use dashes to separate words in folder names.
- Start with verb or key concept that describes the skill.
- Examples: `050-effective-prompting-without-arguing`, `105-mcp-github-integration-issues`
- Keep names concise but meaningful - they appear in file paths.

## Quality Checks

- Ensure Duration is realistic (5-7 minutes).
- Skill statement should be actionable and specific.
- Topics should be concrete, not abstract.
- Learning Outcome should be measurable/verifiable.
- Prerequisites should reference actual prior modules when applicable.
- Check that module fits logically in learning sequence.
- Verify Success Criteria section includes all key accomplishments with ✅ checkboxes.
- **Verify Understanding Check section has 5-7 questions with answers.**
- **Ensure complex actions have "What we'll do" sections before and "What happened" sections after.**
- Ensure Troubleshooting covers common issues from real usage.
- Confirm Next Steps section guides learner to the following module.
- Double-check paths use `./workspace/hello-genai/` for consistency.
- Verify no keyboard shortcuts are mentioned (use menu names instead).
