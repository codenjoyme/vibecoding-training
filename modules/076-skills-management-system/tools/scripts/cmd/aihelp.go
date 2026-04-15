package cmd

import (
	"fmt"
	"os"
	"path/filepath"
)

// RunAIHelp handles the `skills ai-help` command — prints the SKILL-CLI.md reference.
func RunAIHelp(_ []string) {
	// Try to find SKILL-CLI.md relative to the executable
	exePath, err := os.Executable()
	if err == nil {
		skillCliPath := filepath.Join(filepath.Dir(exePath), "..", "SKILL-CLI.md")
		data, err := os.ReadFile(skillCliPath)
		if err == nil {
			fmt.Print(string(data))
			return
		}
	}
	// Fallback: print inline summary
	fmt.Print(aiHelpText)
}

const aiHelpText = `# Skills CLI — Quick Reference for AI Agents

## Commands

skills init --repo <url> --groups <g1>[,<g2>...]   Clone repo, resolve skills, sparse checkout
skills init                                         Re-init from existing skills.json
skills pull                                         Pull latest from remote
skills push <skill-name>                            Branch + commit + push for review
skills list                                         List skills (active/inactive)
skills list --verbose                               Include description and owner
skills list --json                                  Output as JSON array
skills create <name>                                Create new skill (SKILL.md + info.json)
skills enable group <name>                          Add group to workspace config
skills disable group <name>                         Remove group from workspace config
skills enable <skill>                               Add individual skill or re-enable excluded
skills disable <skill>                              Exclude skill from resolution
skills ai-help                                      Show this reference
skills help                                         Show general help

## Config: skills.json (project root)

{
  "repo_url": "../skills-repo",
  "groups": ["project-alpha"],
  "skills": ["resolved-skill-1", "resolved-skill-2"],
  "extra_groups": ["security"],
  "extra_skills": ["my-custom-skill"],
  "excluded_skills": ["unwanted-skill"]
}

## Skill Resolution Priority

1. _global.json skills (for everyone)
2. Group manifest skills (<group>.json + sub-configs)
3. extra_groups (same as groups)
4. extra_skills (individual additions)
5. excluded_skills (removals applied last)
`
