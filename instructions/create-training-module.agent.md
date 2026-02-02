## Motivation

- When user asks to create new training module, gather all necessary information before implementation.
- Ensure consistency across all modules in structure and format.
- Maintain proper numbering and linking system.
- Each module is self-contained with clear learning outcomes.

## Module Structure

- All modules located in `./docs/modules/[number]-[name]/` directory.
- Each module contains single `about.md` file with module description.
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
  + When should this technique/skill be used?
  + Any specific tools or resources needed?
- Determine module number based on placement (use existing number + 5 if between modules).
- Create descriptive folder name that reflects skill being taught.
- Generate `about.md` file with proper structure.

## about.md File Structure

- Title: `# [Module Name]`
- Duration: `**Duration:** 5-7 minutes`
- Skill: `**Skill:** [One-sentence actionable skill description]`
- Topics section with bullet list of main topics covered
- Learning Outcome section with clear result statement
- Prerequisites section listing required prior modules/knowledge
- Optional: When to Use section for practical application guidance
- Optional: Resources section with links to tools/documentation

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
