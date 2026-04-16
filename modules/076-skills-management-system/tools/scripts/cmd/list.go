package cmd

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"github.com/vibecoding/skills-cli/internal/config"
	"github.com/vibecoding/skills-cli/internal/gitops"
	"github.com/vibecoding/skills-cli/internal/manifest"
)

type skillJSON struct {
	Name        string `json:"name"`
	Active      bool   `json:"active"`
	Description string `json:"description,omitempty"`
	Owner       string `json:"owner,omitempty"`
}

// RunList handles the `skills list` command.
func RunList(args []string) {
	fs := flag.NewFlagSet("list", flag.ExitOnError)
	verbose := fs.Bool("verbose", false, "Show description and owner from info.json")
	jsonOut := fs.Bool("json", false, "Output skills as JSON array")
	fs.Usage = func() {
		fmt.Print(`List all available skills in the repository.

Usage:
  skills list [--verbose] [--json]

Flags:
`)
		fs.PrintDefaults()
		fmt.Print(`
Active skills (checked out in this workspace) are marked with ✅.
Other skills exist in the repo but are not part of your current groups.

`)
	}

	if err := fs.Parse(args); err != nil {
		os.Exit(1)
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

	// Resolve active skills dynamically from manifests
	groups := ResolveEffectiveGroups(cfg)
	resolvedSkills, _ := manifest.ResolveSkills(cfg.RepoPath(), groups)
	resolvedSkills = ApplyExtraAndExcluded(resolvedSkills, cfg)
	activeSet := make(map[string]bool, len(resolvedSkills))
	for _, s := range resolvedSkills {
		activeSet[s] = true
	}

	// JSON output mode
	if *jsonOut {
		var items []skillJSON
		for _, s := range allSkills {
			item := skillJSON{Name: s, Active: activeSet[s]}
			if info := gitops.LoadSkillInfo(cfg.RepoPath(), s); info != nil {
				item.Description = info.Description
				item.Owner = info.Owner
			}
			items = append(items, item)
		}
		data, _ := json.MarshalIndent(items, "", "  ")
		fmt.Println(string(data))
		return
	}

	// Normal / verbose text output
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
		if *verbose {
			if info := gitops.LoadSkillInfo(cfg.RepoPath(), s); info != nil {
				fmt.Printf("     %s\n", info.Description)
				fmt.Printf("     Owner: %s\n", info.Owner)
			}
		}
	}

	fmt.Printf("\nActive: %d  |  Total: %d\n", activeCount, len(allSkills))
}
