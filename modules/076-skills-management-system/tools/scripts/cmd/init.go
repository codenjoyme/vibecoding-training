package cmd

import (
	"flag"
	"fmt"
	"os"
	"strings"

	"github.com/vibecoding/skills-cli/internal/config"
	"github.com/vibecoding/skills-cli/internal/gitops"
	"github.com/vibecoding/skills-cli/internal/manifest"
)

// stringSliceFlag is a custom flag type that accepts comma-separated values
// and can be repeated: --groups a,b or --groups a --groups b
type stringSliceFlag []string

func (s *stringSliceFlag) String() string { return strings.Join(*s, ",") }
func (s *stringSliceFlag) Set(v string) error {
	for _, part := range strings.Split(v, ",") {
		part = strings.TrimSpace(part)
		if part != "" {
			*s = append(*s, part)
		}
	}
	return nil
}

// RunInit handles the `skills init` command.
func RunInit(args []string) {
	fs := flag.NewFlagSet("init", flag.ExitOnError)
	repo := fs.String("repo", "", "URL or local path to the central skills repository (required)")
	var groupsFlag stringSliceFlag
	fs.Var(&groupsFlag, "groups", "Groups to initialize (comma-separated or repeated flag; positional args also accepted)")

	fs.Usage = func() {
		fmt.Print(`Initialize skills workspace from a central repository.

Clones the skills repository, resolves skills for the specified groups, and applies
sparse checkout so only the needed skills are present in the local workspace.

Usage:
  skills init --repo <url-or-path> [--groups <group1>[,<group2>...]] [group...]

Flags:
`)
		fs.PrintDefaults()
		fmt.Print(`
Examples:
  skills init --repo https://github.com/org/skills --groups backend
  skills init --repo ../skills-repo --groups backend,security
  skills init --repo ../skills-repo backend security
`)
	}

	if err := fs.Parse(args); err != nil {
		os.Exit(1)
	}

	// If no --repo specified, try to re-init from existing config
	if *repo == "" {
		existing, err := config.Load()
		if err != nil {
			fmt.Fprintln(os.Stderr, "Error: --repo is required (no existing skills.json found)")
			fs.Usage()
			os.Exit(1)
		}
		fmt.Println("→ Re-initializing from existing skills.json ...")
		repoDir := config.RepoSubDir
		// Remove old clone if present
		if _, err := os.Stat(repoDir); err == nil {
			fmt.Println("→ Removing old instructions/ ...")
			if err := os.RemoveAll(repoDir); err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to remove instructions/: %v\n", err)
				os.Exit(1)
			}
		}
		fmt.Printf("→ Cloning skills repo from %s ...\n", existing.RepoURL)
		if err := gitops.Clone(existing.RepoURL, repoDir); err != nil {
			fmt.Fprintf(os.Stderr, "Error: clone failed: %v\n", err)
			os.Exit(1)
		}
		fmt.Println("  ✓ Cloned")

		groups := ResolveEffectiveGroups(existing)
		fmt.Printf("→ Resolving skills for groups: %s ...\n", strings.Join(groups, ", "))
		skills, err := manifest.ResolveSkills(repoDir, groups)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: manifest resolution failed: %v\n", err)
			os.Exit(1)
		}
		skills = ApplyExtraAndExcluded(skills, existing)
		fmt.Printf("  ✓ Resolved %d skill(s): %s\n", len(skills), strings.Join(skills, ", "))

		fmt.Println("→ Applying sparse checkout ...")
		if err := gitops.SetupSparseCheckout(repoDir, skills); err != nil {
			fmt.Fprintf(os.Stderr, "Error: sparse checkout failed: %v\n", err)
			os.Exit(1)
		}
		fmt.Println("  ✓ Sparse checkout applied")

		existing.Skills = skills
		if err := config.Save(existing); err != nil {
			fmt.Fprintf(os.Stderr, "Error: failed to save config: %v\n", err)
			os.Exit(1)
		}
		fmt.Printf("\n✅ Skills workspace re-initialized!\n")
		fmt.Printf("   Skills:     %s\n", strings.Join(skills, ", "))
		return
	}

	// Combine --groups flag values with remaining positional args
	groups := append([]string(groupsFlag), fs.Args()...)
	if len(groups) == 0 {
		fmt.Fprintln(os.Stderr, "Error: specify at least one group (use --groups flag or positional args)")
		fs.Usage()
		os.Exit(1)
	}

	repoDir := config.RepoSubDir

	// Check if already initialized
	if _, err := os.Stat(config.ConfigFile); err == nil {
		fmt.Fprintln(os.Stderr, "Error: workspace already initialized (skills.json exists)")
		fmt.Fprintln(os.Stderr, "Run `skills pull` to update, or delete skills.json and instructions/ to re-initialize.")
		os.Exit(1)
	}

	fmt.Printf("→ Cloning skills repo from %s ...\n", *repo)
	if err := gitops.Clone(*repo, repoDir); err != nil {
		fmt.Fprintf(os.Stderr, "Error: clone failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("  ✓ Cloned")

	fmt.Printf("→ Resolving skills for groups: %s ...\n", strings.Join(groups, ", "))
	skills, err := manifest.ResolveSkills(repoDir, groups)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: manifest resolution failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("  ✓ Resolved %d skill(s): %s\n", len(skills), strings.Join(skills, ", "))

	fmt.Println("→ Applying sparse checkout ...")
	if err := gitops.SetupSparseCheckout(repoDir, skills); err != nil {
		fmt.Fprintf(os.Stderr, "Error: sparse checkout failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("  ✓ Sparse checkout applied")

	cfg := &config.Config{
		RepoURL: *repo,
		Groups:  groups,
		Skills:  skills,
	}
	if err := config.Save(cfg); err != nil {
		fmt.Fprintf(os.Stderr, "Error: failed to save config: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("\n✅ Skills workspace initialized!\n")
	fmt.Printf("   Repository: %s\n", *repo)
	fmt.Printf("   Groups:     %s\n", strings.Join(groups, ", "))
	fmt.Printf("   Skills:     %s\n", strings.Join(skills, ", "))
	fmt.Printf("   Location:   instructions/\n\n")
	fmt.Println("Your AI agent can now read skills from instructions/<skill-name>/SKILL.md")
}
