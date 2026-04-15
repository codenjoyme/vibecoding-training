package cmd

import (
	"fmt"
	"os"
	"strings"

	"github.com/vibecoding/skills-cli/internal/config"
)

// RunEnable handles `skills enable group <name>` and `skills enable <skill-name>`.
func RunEnable(args []string) {
	if len(args) == 0 || args[0] == "--help" || args[0] == "-h" {
		printEnableHelp()
		return
	}

	if args[0] == "group" {
		if len(args) < 2 {
			fmt.Fprintln(os.Stderr, "Error: group name is required")
			fmt.Fprintln(os.Stderr, "Usage: skills enable group <group-name>")
			os.Exit(1)
		}
		enableGroup(args[1])
	} else {
		enableSkill(args[0])
	}
}

// RunDisable handles `skills disable group <name>` and `skills disable <skill-name>`.
func RunDisable(args []string) {
	if len(args) == 0 || args[0] == "--help" || args[0] == "-h" {
		printDisableHelp()
		return
	}

	if args[0] == "group" {
		if len(args) < 2 {
			fmt.Fprintln(os.Stderr, "Error: group name is required")
			fmt.Fprintln(os.Stderr, "Usage: skills disable group <group-name>")
			os.Exit(1)
		}
		disableGroup(args[1])
	} else {
		disableSkill(args[0])
	}
}

func enableGroup(name string) {
	cfg, err := config.Load()
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error:", err)
		os.Exit(1)
	}

	// Check not already in groups
	for _, g := range cfg.Groups {
		if g == name {
			fmt.Fprintf(os.Stderr, "Group %q is already enabled\n", name)
			os.Exit(1)
		}
	}

	cfg.Groups = append(cfg.Groups, name)
	if err := config.Save(cfg); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("✅ Group %q enabled\n", name)
	fmt.Println("Run `skills init` to re-apply skill resolution.")
}

func disableGroup(name string) {
	cfg, err := config.Load()
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error:", err)
		os.Exit(1)
	}

	// Remove from groups list
	found := false
	cfg.Groups = removeFromSlice(cfg.Groups, name, &found)

	if !found {
		fmt.Fprintf(os.Stderr, "Group %q is not currently enabled\n", name)
		os.Exit(1)
	}

	if err := config.Save(cfg); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("✅ Group %q disabled\n", name)
	fmt.Println("Run `skills init` to re-apply skill resolution.")
}

func enableSkill(name string) {
	cfg, err := config.Load()
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error:", err)
		os.Exit(1)
	}

	// If it was excluded, remove from excluded list
	wasExcluded := false
	cfg.ExcludedSkills = removeFromSlice(cfg.ExcludedSkills, name, &wasExcluded)
	if wasExcluded {
		if err := config.Save(cfg); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}
		fmt.Printf("✅ Skill %q re-enabled (removed from exclusion list)\n", name)
		fmt.Println("Run `skills init` to re-apply skill resolution.")
		return
	}

	// Check if already in extra_skills
	for _, s := range cfg.ExtraSkills {
		if s == name {
			fmt.Fprintf(os.Stderr, "Skill %q is already enabled\n", name)
			os.Exit(1)
		}
	}

	cfg.ExtraSkills = append(cfg.ExtraSkills, name)
	if err := config.Save(cfg); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("✅ Skill %q enabled\n", name)
	fmt.Println("Run `skills init` to re-apply skill resolution.")
}

func disableSkill(name string) {
	cfg, err := config.Load()
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error:", err)
		os.Exit(1)
	}

	// Remove from extra_skills if present
	wasExtra := false
	cfg.ExtraSkills = removeFromSlice(cfg.ExtraSkills, name, &wasExtra)

	// Check if already excluded
	for _, s := range cfg.ExcludedSkills {
		if s == name {
			fmt.Fprintf(os.Stderr, "Skill %q is already disabled\n", name)
			os.Exit(1)
		}
	}

	// Add to exclusion list
	cfg.ExcludedSkills = append(cfg.ExcludedSkills, name)

	if err := config.Save(cfg); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("✅ Skill %q disabled\n", name)
	fmt.Println("Run `skills init` to re-apply skill resolution.")
}

func removeFromSlice(slice []string, item string, found *bool) []string {
	result := make([]string, 0, len(slice))
	for _, s := range slice {
		if s == item {
			*found = true
		} else {
			result = append(result, s)
		}
	}
	return result
}

func printEnableHelp() {
	fmt.Print(`Enable a group or individual skill in this workspace.

Usage:
  skills enable group <group-name>   Add a group to the workspace
  skills enable <skill-name>         Add an individual skill

After enabling, run ` + "`skills init`" + ` to re-apply skill resolution.

Examples:
  skills enable group security
  skills enable my-custom-skill
`)
}

func printDisableHelp() {
	fmt.Print(`Disable a group or individual skill in this workspace.

Usage:
  skills disable group <group-name>   Remove a group from the workspace
  skills disable <skill-name>         Exclude an individual skill

After disabling, run ` + "`skills init`" + ` to re-apply skill resolution.

Examples:
  skills disable group security
  skills disable security-guidelines
`)
}

// ResolveEffectiveGroups returns the groups list with deduplication.
func ResolveEffectiveGroups(cfg *config.Config) []string {
	groups := make([]string, 0, len(cfg.Groups))
	seen := make(map[string]bool)
	for _, g := range cfg.Groups {
		if !seen[g] {
			groups = append(groups, g)
			seen[g] = true
		}
	}
	return groups
}

// ApplyExtraAndExcluded takes resolved skills and applies extra_skills and excluded_skills.
func ApplyExtraAndExcluded(resolved []string, cfg *config.Config) []string {
	skillSet := make(map[string]bool)
	for _, s := range resolved {
		skillSet[s] = true
	}
	for _, s := range cfg.ExtraSkills {
		skillSet[s] = true
	}
	for _, s := range cfg.ExcludedSkills {
		delete(skillSet, s)
	}

	result := make([]string, 0, len(skillSet))
	for s := range skillSet {
		result = append(result, s)
	}
	// Sort for deterministic output
	sortSlice(result)
	return result
}

func sortSlice(s []string) {
	for i := 0; i < len(s); i++ {
		for j := i + 1; j < len(s); j++ {
			if strings.Compare(s[i], s[j]) > 0 {
				s[i], s[j] = s[j], s[i]
			}
		}
	}
}
