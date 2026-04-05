package cmd

import (
	"flag"
	"fmt"
	"os"

	"github.com/vibecoding/skills-cli/internal/config"
	"github.com/vibecoding/skills-cli/internal/gitops"
)

// RunList handles the `skills list` command.
func RunList(args []string) {
	fs := flag.NewFlagSet("list", flag.ExitOnError)
	fs.Usage = func() {
		fmt.Print(`List all available skills in the repository.

Usage:
  skills list

Active skills (checked out in this workspace) are marked with ✅.
Other skills exist in the repo but are not part of your current groups.

`)
		fs.PrintDefaults()
	}

	if err := fs.Parse(args); err != nil {
		os.Exit(1)
	}

	if len(fs.Args()) > 0 && (fs.Args()[0] == "--help" || fs.Args()[0] == "-h") {
		fs.Usage()
		return
	}

	cfg, err := config.Load()
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error:", err)
		os.Exit(1)
	}

	allSkills, err := gitops.ListAllSkills(cfg.RepoPath())
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: failed to list skills: %v\n", err)
		os.Exit(1)
	}

	// Build a fast lookup set for active skills
	activeSet := make(map[string]bool, len(cfg.Skills))
	for _, s := range cfg.Skills {
		activeSet[s] = true
	}

	fmt.Printf("Skills repository: %s\n", cfg.RepoURL)
	fmt.Printf("Groups:           %v\n\n", cfg.Groups)

	activeCount := 0
	for _, s := range allSkills {
		if activeSet[s] {
			fmt.Printf("  ✅ %s\n", s)
			activeCount++
		} else {
			fmt.Printf("  ○  %s\n", s)
		}
	}

	fmt.Printf("\nActive: %d  |  Total: %d\n", activeCount, len(allSkills))
}
