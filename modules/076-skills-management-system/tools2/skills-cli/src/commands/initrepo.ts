import * as fs from 'fs';
import * as path from 'path';

export function runInitRepo(args: string[]): void {
  if (args.includes('--help') || args.includes('-h')) {
    printInitRepoHelp();
    return;
  }

  const positional = args.filter(a => !a.startsWith('--'));
  if (positional.length === 0) {
    console.error('Error: folder name is required');
    printInitRepoHelp();
    process.exit(1);
  }

  const folderName = positional[0];

  if (fs.existsSync(folderName)) {
    console.error(`Error: folder "${folderName}" already exists`);
    process.exit(1);
  }

  console.log(`→ Creating skills repository at ${folderName} ...`);

  // Create directory structure
  const dirs = [
    path.join(folderName, '.manifest'),
    path.join(folderName, 'creating-instructions'),
    path.join(folderName, 'iterative-prompting'),
    path.join(folderName, 'skills-cli'),
  ];
  for (const d of dirs) {
    fs.mkdirSync(d, { recursive: true });
  }

  // Write manifest files
  writeFile(path.join(folderName, '.manifest', '_global.json'), GLOBAL_JSON);
  writeFile(path.join(folderName, '.manifest', 'group-1.json'), GROUP1_JSON);
  writeFile(path.join(folderName, '.manifest', 'sub-group.json'), SUBGROUP_JSON);

  // Write creating-instructions skill
  writeFile(path.join(folderName, 'creating-instructions', 'SKILL.md'), CREATING_INSTRUCTIONS_SKILL);
  writeFile(path.join(folderName, 'creating-instructions', 'info.json'), CREATING_INSTRUCTIONS_INFO);

  // Write iterative-prompting skill
  writeFile(path.join(folderName, 'iterative-prompting', 'SKILL.md'), ITERATIVE_PROMPTING_SKILL);
  writeFile(path.join(folderName, 'iterative-prompting', 'info.json'), ITERATIVE_PROMPTING_INFO);

  // Write skills-cli skill
  writeFile(path.join(folderName, 'skills-cli', 'SKILL.md'), SKILLS_CLI_SKILL);
  writeFile(path.join(folderName, 'skills-cli', 'info.json'), SKILLS_CLI_INFO);

  // Write .gitignore
  writeFile(path.join(folderName, '.gitignore'), '# Skills repo .gitignore\n');

  console.log('  ✓ Files created');
  console.log(`\n✅ Skills repository initialized at ${folderName}`);
  console.log('\nNext steps:');
  console.log(`  cd ${folderName}`);
  console.log('  git init && git add . && git commit -m "init: skills repository"');
  console.log('  # Then push to your Git hosting');
}

function writeFile(filePath: string, content: string): void {
  fs.writeFileSync(filePath, content, 'utf8');
}

function printInitRepoHelp(): void {
  console.log(`Initialize a new skills repository with base structure.

Creates a folder with:
  .manifest/_global.json      — global skills config
  .manifest/group-1.json      — example group config
  .manifest/sub-group.json    — example sub-config
  creating-instructions/      — skill: how to create AI instructions
  iterative-prompting/        — skill: iterative prompt workflow
  skills-cli/                 — skill: how to use this CLI tool

Usage:
  skills init-repo <folder-name>

Examples:
  skills init-repo my-skills-repo
  skills init-repo ../shared-skills
`);
}

const GLOBAL_JSON = `{
  "skills": [
    "creating-instructions",
    "iterative-prompting",
    "skills-cli"
  ]
}
`;

const GROUP1_JSON = `{
  "skills": [],
  "sub-configs": ["sub-group"]
}
`;

const SUBGROUP_JSON = `{
  "skills": [],
  "sub-configs": []
}
`;

const CREATING_INSTRUCTIONS_SKILL = `# Skill: Creating Instructions

## Purpose

Guidelines for creating, organizing, and maintaining AI instruction files using an IDE-agnostic approach.

## Key Principles

- Instructions are pure markdown files describing SDLC workflows — no platform-specific adapters.
- One SDLC workflow per file (Single Responsibility Principle).
- Soft limit: ~700 lines per file. Exceeding → split.
- Complex instructions reference other instructions — composability over monoliths.

## Structure

- \`instructions/\` folder contains all instruction files.
- \`main.agent.md\` serves as catalog of all instructions with brief descriptions.
- Platform-specific entry points reference \`main.agent.md\`:
  - \`.github/copilot-instructions.md\` for GitHub Copilot
  - \`.cursor/rules/*.mdc\` for Cursor
  - \`.claude/CLAUDE.md\` for Claude Code

## Naming Convention

- File name: \`<topic>.agent.md\`
- Use kebab-case for file names.

## Adapter Pattern

Instructions = **what to do** (platform-agnostic SDLC knowledge).
Wrappers = **how to load** (platform-specific glue, 2-3 lines each).

Team members on different IDEs share identical workflow knowledge without translation.
`;

const CREATING_INSTRUCTIONS_INFO = `{
  "description": "Guidelines for creating and organizing AI instruction files. IDE-agnostic approach with pure markdown files and platform adapter pattern.",
  "owner": "Oleksandr_Baglai@example.com"
}
`;

const ITERATIVE_PROMPTING_SKILL = `# Skill: Iterative Prompting

## Purpose

A workflow pattern where you maintain a living file (\`main.prompt.md\`) instead of chatting in a chat window. Every request is a new \`## UPD[N]\` block; after AI acts, it appends \`### RESULT\`.

## How It Works

1. Create \`main.prompt.md\` in a request folder.
2. Add \`## UPD1\` with your task description.
3. AI reads the file, implements changes.
4. AI appends \`### RESULT\` with changelog.
5. Add \`## UPD2\` with next request — repeat.

## Key Insight

A committed prompt file + \`git diff\` gives the AI precise context about what changed — no hallucination, no drift, no lost history.

## Rules

- Always check \`git diff\` first to see what changed.
- All existing content stays intact — prior corrections are done.
- \`### RESULT\` is concise: file paths + 1-2 sentence description.
`;

const ITERATIVE_PROMPTING_INFO = `{
  "description": "Iterative prompt workflow using UPD markers in .prompt.md files. Maintains living specifications with version-controlled prompt history.",
  "owner": "Oleksandr_Baglai@example.com"
}
`;

const SKILLS_CLI_SKILL = `# Skill: Skills CLI Usage

## Purpose

This skill describes how to use the Skills CLI tool to manage shared AI instruction skills across your team.

## Installation

Install globally via npm (Node.js edition):
\`\`\`bash
npm install -g git+https://github.com/your-org/skills-cli.git
\`\`\`

Or use the pre-built Go binary from the tools/ folder.

## Commands

\`\`\`
skills init --repo <url> --groups <g1>[,<g2>...]   Clone repo, resolve, sparse checkout
skills init                                         Re-init from existing skills.json
skills pull                                         Pull latest skills
skills push <skill-name>                            Branch + commit + push for review
skills list [--verbose] [--json]                    List skills
skills create <name>                                Create new skill
skills enable group <name>                          Enable a group
skills disable group <name>                         Disable a group
skills enable <skill>                               Enable individual skill
skills disable <skill>                              Exclude a skill
skills init-repo <folder>                           Create new skills repository
skills ai-help                                      Show LLM-friendly reference
skills help                                         Show help
\`\`\`

## Typical Workflow

1. \`skills init --repo <url> --groups <group>\` — set up workspace
2. \`skills list --verbose\` — see what's available
3. Edit \`instructions/<skill>/SKILL.md\`
4. \`skills push <skill>\` — propose changes via PR
5. \`skills pull\` — get latest updates
`;

const SKILLS_CLI_INFO = `{
  "description": "How to use the Skills CLI tool to manage shared AI instruction skills. Covers installation, commands, and typical workflows.",
  "owner": "Oleksandr_Baglai@example.com"
}
`;
