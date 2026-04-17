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
  skills-cli/                 — skill: CLI usage, creating skills, IDE integration

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

	// Write skills-cli skill (read SKILL-CLI.md from disk as source of truth)
	skillCliContent := loadSkillCliMd()
	writeFile(filepath.Join(folderName, "skills-cli", "SKILL.md"), skillCliContent)
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

// loadSkillCliMd reads SKILL-CLI.md relative to the executable.
func loadSkillCliMd() string {
	exePath, err := os.Executable()
	if err == nil {
		candidate := filepath.Join(filepath.Dir(exePath), "..", "SKILL-CLI.md")
		if data, readErr := os.ReadFile(candidate); readErr == nil {
			return string(data)
		}
	}
	return "# Skills CLI\n\nSee SKILL-CLI.md in the skills-cli package for full reference.\n"
}

const skillsCLIInfo = `{
  "description": "Skills CLI reference: commands, creating skills, IDE integration (VSCode/Copilot, Cursor, Claude Code).",
  "owner": "your-name@example.com"
}
`
