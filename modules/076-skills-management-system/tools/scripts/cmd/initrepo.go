package cmd

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
)

// RunInitRepo handles the `skills init-repo <folder-name>` command.
func RunInitRepo(args []string) {
	fs := flag.NewFlagSet("init-repo", flag.ExitOnError)
	fs.Usage = func() {
		fmt.Print(`Initialize a new skills repository with base structure.

Creates a Git-initialized folder with:
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
`)
	}

	if err := fs.Parse(args); err != nil {
		os.Exit(1)
	}

	positional := fs.Args()
	if len(positional) == 0 {
		fmt.Fprintln(os.Stderr, "Error: folder name is required")
		fs.Usage()
		os.Exit(1)
	}

	folderName := positional[0]

	if _, err := os.Stat(folderName); err == nil {
		fmt.Fprintf(os.Stderr, "Error: folder %q already exists\n", folderName)
		os.Exit(1)
	}

	fmt.Printf("→ Creating skills repository at %s ...\n", folderName)

	// Create directory structure
	dirs := []string{
		filepath.Join(folderName, ".manifest"),
		filepath.Join(folderName, "creating-instructions"),
		filepath.Join(folderName, "iterative-prompting"),
		filepath.Join(folderName, "skills-cli"),
	}
	for _, d := range dirs {
		if err := os.MkdirAll(d, 0755); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}
	}

	// Write manifest files
	writeFile(filepath.Join(folderName, ".manifest", "_global.json"), globalJSON)
	writeFile(filepath.Join(folderName, ".manifest", "group-1.json"), group1JSON)
	writeFile(filepath.Join(folderName, ".manifest", "sub-group.json"), subGroupJSON)

	// Write creating-instructions skill
	writeFile(filepath.Join(folderName, "creating-instructions", "SKILL.md"), creatingInstructionsSkill)
	writeFile(filepath.Join(folderName, "creating-instructions", "info.json"), creatingInstructionsInfo)

	// Write iterative-prompting skill
	writeFile(filepath.Join(folderName, "iterative-prompting", "SKILL.md"), iterativePromptingSkill)
	writeFile(filepath.Join(folderName, "iterative-prompting", "info.json"), iterativePromptingInfo)

	// Write skills-cli skill
	writeFile(filepath.Join(folderName, "skills-cli", "SKILL.md"), skillsCLISkill)
	writeFile(filepath.Join(folderName, "skills-cli", "info.json"), skillsCLIInfo)

	// Write .gitignore
	writeFile(filepath.Join(folderName, ".gitignore"), repoGitignore)

	fmt.Println("  ✓ Files created")
	fmt.Printf("\n✅ Skills repository initialized at %s\n", folderName)
	fmt.Println("\nNext steps:")
	fmt.Printf("  cd %s\n", folderName)
	fmt.Println("  git init && git add . && git commit -m \"init: skills repository\"")
	fmt.Println("  # Then push to your Git hosting")
}

func writeFile(path, content string) {
	if err := os.WriteFile(path, []byte(content), 0644); err != nil {
		fmt.Fprintf(os.Stderr, "Error writing %s: %v\n", path, err)
		os.Exit(1)
	}
}

const globalJSON = `{
  "skills": [
    "creating-instructions",
    "iterative-prompting",
    "skills-cli"
  ]
}
`

const group1JSON = `{
  "skills": [],
  "sub-configs": ["sub-group"]
}
`

const subGroupJSON = `{
  "skills": [],
  "sub-configs": []
}
`

const repoGitignore = `# Skills repo .gitignore
`

const creatingInstructionsSkill = `# Skill: Creating Instructions

## Purpose

Guidelines for creating, organizing, and maintaining AI instruction files using an IDE-agnostic approach.

## Key Principles

- Instructions are pure markdown files describing SDLC workflows — no platform-specific adapters.
- One SDLC workflow per file (Single Responsibility Principle).
- Soft limit: ~700 lines per file. Exceeding → split.
- Complex instructions reference other instructions — composability over monoliths.

## Structure

- ` + "`instructions/`" + ` folder contains all instruction files.
- ` + "`main.agent.md`" + ` serves as catalog of all instructions with brief descriptions.
- Platform-specific entry points reference ` + "`main.agent.md`" + `:
  - ` + "`.github/copilot-instructions.md`" + ` for GitHub Copilot
  - ` + "`.cursor/rules/*.mdc`" + ` for Cursor
  - ` + "`.claude/CLAUDE.md`" + ` for Claude Code

## Naming Convention

- File name: ` + "`<topic>.agent.md`" + `
- Use kebab-case for file names.

## Adapter Pattern

Instructions = **what to do** (platform-agnostic SDLC knowledge).
Wrappers = **how to load** (platform-specific glue, 2-3 lines each).

Team members on different IDEs share identical workflow knowledge without translation.
`

const creatingInstructionsInfo = `{
  "description": "Guidelines for creating and organizing AI instruction files. IDE-agnostic approach with pure markdown files and platform adapter pattern.",
  "owner": "Oleksandr_Baglai@example.com"
}
`

const iterativePromptingSkill = `# Skill: Iterative Prompting

## Purpose

A workflow pattern where you maintain a living file (` + "`main.prompt.md`" + `) instead of chatting in a chat window. Every request is a new ` + "`## UPD[N]`" + ` block; after AI acts, it appends ` + "`### RESULT`" + `.

## How It Works

1. Create ` + "`main.prompt.md`" + ` in a request folder.
2. Add ` + "`## UPD1`" + ` with your task description.
3. AI reads the file, implements changes.
4. AI appends ` + "`### RESULT`" + ` with changelog.
5. Add ` + "`## UPD2`" + ` with next request — repeat.

## Key Insight

A committed prompt file + ` + "`git diff`" + ` gives the AI precise context about what changed — no hallucination, no drift, no lost history.

## Template

` + "```markdown" + `
<follow>
iterative-prompt.agent.md
</follow>

## UPD1

Your task here...
` + "```" + `

## Rules

- Always check ` + "`git diff`" + ` first to see what changed.
- All existing content stays intact — prior corrections are done.
- ` + "`### RESULT`" + ` is concise: file paths + 1-2 sentence description.
`

const iterativePromptingInfo = `{
  "description": "Iterative prompt workflow using UPD markers in .prompt.md files. Maintains living specifications with version-controlled prompt history.",
  "owner": "Oleksandr_Baglai@example.com"
}
`

const skillsCLISkill = `# Skill: Skills CLI Usage

## Purpose

This skill describes how to use the Skills CLI tool to manage shared AI instruction skills across your team.

## Installation

Install globally via npm (Node.js edition):
` + "```bash" + `
npm install -g git+https://github.com/your-org/skills-cli.git
` + "```" + `

Or use the pre-built Go binary from the tools/ folder.

## Commands

` + "```" + `
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
` + "```" + `

## Typical Workflow

1. ` + "`skills init --repo <url> --groups <group>`" + ` — set up workspace
2. ` + "`skills list --verbose`" + ` — see what's available
3. Edit ` + "`instructions/<skill>/SKILL.md`" + `
4. ` + "`skills push <skill>`" + ` — propose changes via PR
5. ` + "`skills pull`" + ` — get latest updates
`

const skillsCLIInfo = `{
  "description": "How to use the Skills CLI tool to manage shared AI instruction skills. Covers installation, commands, and typical workflows.",
  "owner": "Oleksandr_Baglai@example.com"
}
`
