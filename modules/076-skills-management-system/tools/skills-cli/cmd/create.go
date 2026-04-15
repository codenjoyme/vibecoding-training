package cmd

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"

	"github.com/vibecoding/skills-cli/internal/config"
)

const skillTemplate = `# Skill: %s

## Purpose

_Describe what this skill teaches or enables._

## Instructions

_Write the detailed instructions for the AI agent here._
`

const infoTemplate = `{
  "description": "This skill provides _____. It can be used for _____. The main features include _____.",
  "owner": "Your_Name@domain.com"
}
`

// RunCreate handles the `skills create <name>` command.
func RunCreate(args []string) {
	fs := flag.NewFlagSet("create", flag.ExitOnError)
	fs.Usage = func() {
		fmt.Print(`Create a new skill in the local instructions/ folder.

Usage:
  skills create <skill-name>

Creates:
  instructions/<skill-name>/SKILL.md   — skill instructions template
  instructions/<skill-name>/info.json  — skill metadata (description, owner)

`)
		fs.PrintDefaults()
	}

	if err := fs.Parse(args); err != nil {
		os.Exit(1)
	}

	positional := fs.Args()
	if len(positional) == 0 {
		fmt.Fprintln(os.Stderr, "Error: skill name is required")
		fs.Usage()
		os.Exit(1)
	}

	skillName := positional[0]

	// Verify workspace is initialized
	if _, err := config.Load(); err != nil {
		fmt.Fprintln(os.Stderr, "Error:", err)
		os.Exit(1)
	}

	skillDir := filepath.Join(config.RepoSubDir, skillName)

	// Check if skill already exists
	if _, err := os.Stat(skillDir); err == nil {
		fmt.Fprintf(os.Stderr, "Error: skill %q already exists at %s\n", skillName, skillDir)
		os.Exit(1)
	}

	// Create skill directory
	if err := os.MkdirAll(skillDir, 0755); err != nil {
		fmt.Fprintf(os.Stderr, "Error: failed to create directory: %v\n", err)
		os.Exit(1)
	}

	// Write SKILL.md
	skillPath := filepath.Join(skillDir, "SKILL.md")
	if err := os.WriteFile(skillPath, []byte(fmt.Sprintf(skillTemplate, skillName)), 0644); err != nil {
		fmt.Fprintf(os.Stderr, "Error: failed to write SKILL.md: %v\n", err)
		os.Exit(1)
	}

	// Write info.json
	infoPath := filepath.Join(skillDir, "info.json")
	if err := os.WriteFile(infoPath, []byte(infoTemplate), 0644); err != nil {
		fmt.Fprintf(os.Stderr, "Error: failed to write info.json: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("✅ Skill %q created at %s\n", skillName, skillDir)
	fmt.Printf("   → %s\n", skillPath)
	fmt.Printf("   → %s\n", infoPath)
	fmt.Println("\nEdit SKILL.md with your instructions, then use `skills push` to propose it.")
}
