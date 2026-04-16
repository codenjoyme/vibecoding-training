package cmd

import (
	"fmt"
	"os"
	"sort"
	"strings"

	"github.com/vibecoding/skills-cli/internal/config"
	"github.com/vibecoding/skills-cli/internal/gitops"
	"github.com/vibecoding/skills-cli/internal/manifest"
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

	force := false
	var filtered []string
	for _, a := range args {
		if a == "--force" {
			force = true
		} else {
			filtered = append(filtered, a)
		}
	}

	if filtered[0] == "group" {
		if len(filtered) < 2 {
			fmt.Fprintln(os.Stderr, "Error: group name is required")
			fmt.Fprintln(os.Stderr, "Usage: skills disable group <group-name>")
			os.Exit(1)
		}
		disableGroup(filtered[1], force)
	} else {
		disableSkill(filtered[0], force)
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
	reapplySparseCheckout(cfg)
}

func disableGroup(name string, force bool) {
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

	// Check for uncommitted changes in skills that will be removed
	if !force {
		// Build config with group restored to compute "before" skill set
		cfgBefore := *cfg
		cfgBefore.Groups = append(append([]string{}, cfg.Groups...), name)
		before := resolveAllSkills(&cfgBefore)
		after := resolveAllSkills(cfg)
		afterSet := make(map[string]bool)
		for _, s := range after {
			afterSet[s] = true
		}
		var dirty []string
		for _, s := range before {
			if !afterSet[s] && gitops.HasUncommittedChanges(config.RepoSubDir, s) {
				dirty = append(dirty, s)
			}
		}
		if len(dirty) > 0 {
			fmt.Fprintf(os.Stderr, "Error: cannot disable group %q - uncommitted changes in: %s\n", name, strings.Join(dirty, ", "))
			fmt.Fprintln(os.Stderr, "Commit or discard your changes first, or use --force to override.")
			os.Exit(1)
		}
	}

	if err := config.Save(cfg); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("✅ Group %q disabled\n", name)
	reapplySparseCheckout(cfg)
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
		reapplySparseCheckout(cfg)
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
	reapplySparseCheckout(cfg)
}

func disableSkill(name string, force bool) {
	cfg, err := config.Load()
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error:", err)
		os.Exit(1)
	}

	// Check for uncommitted changes before disabling
	if !force && gitops.HasUncommittedChanges(config.RepoSubDir, name) {
		fmt.Fprintf(os.Stderr, "Error: cannot disable skill %q - uncommitted local changes detected\n", name)
		fmt.Fprintln(os.Stderr, "Commit or discard your changes first, or use --force to override.")
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
	reapplySparseCheckout(cfg)
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

Sparse checkout is re-applied automatically after enabling.

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

Flags:
  --force   Force disable even if there are uncommitted local changes

If the skill has uncommitted local changes, the command will refuse
to disable it. Use --force to override this check.

Sparse checkout is re-applied automatically after disabling.

Examples:
  skills disable group security
  skills disable security-guidelines
  skills disable security-guidelines --force
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
	sort.Strings(s)
}

func resolveAllSkills(cfg *config.Config) []string {
	groups := ResolveEffectiveGroups(cfg)
	skills, _ := manifest.ResolveSkills(config.RepoSubDir, groups)
	return ApplyExtraAndExcluded(skills, cfg)
}

func reapplySparseCheckout(cfg *config.Config) {
	skills := resolveAllSkills(cfg)
	fmt.Printf("→ Applying sparse checkout (%d skill(s)) ...\n", len(skills))
	if err := gitops.SetupSparseCheckout(config.RepoSubDir, skills); err != nil {
		fmt.Fprintf(os.Stderr, "Warning: sparse checkout failed: %v\n", err)
		fmt.Fprintln(os.Stderr, "Run `skills init` to re-apply manually.")
		return
	}
	fmt.Println("  ✓ Sparse checkout applied")
}
