package cmd

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"strings"

	"github.com/vibecoding/skills-cli/internal/config"
	"github.com/vibecoding/skills-cli/internal/gitops"
)

// RunPush handles the `skills push <skill-name> [--groups <g1> <g2> ...]` command.
func RunPush(args []string) {
	// Parse args manually to support: skills push <name> --groups g1 g2
	var skillName string
	var groups []string
	help := false
	collectingGroups := false

	for _, arg := range args {
		if arg == "--help" || arg == "-h" {
			help = true
			break
		}
		if arg == "--groups" {
			collectingGroups = true
			continue
		}
		if collectingGroups {
			if strings.HasPrefix(arg, "--") {
				collectingGroups = false
			} else {
				for _, g := range strings.Split(arg, ",") {
					g = strings.TrimSpace(g)
					if g != "" {
						groups = append(groups, g)
					}
				}
				continue
			}
		}
		if !strings.HasPrefix(arg, "--") && skillName == "" {
			skillName = arg
		}
	}

	if help {
		printPushHelp()
		return
	}

	if skillName == "" {
		fmt.Fprintln(os.Stderr, "Error: skill name is required")
		fmt.Fprintln(os.Stderr, "Usage: skills push <skill-name> [--groups <group1> <group2> ...]")
		os.Exit(1)
	}

	branchName := fmt.Sprintf("feature/%s-update", skillName)

	cfg, err := config.Load()
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error:", err)
		os.Exit(1)
	}

	repoDir := cfg.RepoPath()

	fmt.Printf("→ Creating branch %s ...\n", branchName)
	if err := gitops.CreateBranch(repoDir, branchName); err != nil {
		fmt.Fprintf(os.Stderr, "Error: failed to create branch: %v\n", err)
		fmt.Fprintf(os.Stderr, "Tip: if the branch already exists, delete it with:\n")
		fmt.Fprintf(os.Stderr, "     git -C instructions branch -D %s\n", branchName)
		os.Exit(1)
	}
	fmt.Println("  ✓ Branch created")

	fmt.Printf("→ Staging and committing changes in %s/ ...\n", skillName)
	if err := gitops.StageAndCommit(repoDir, skillName); err != nil {
		fmt.Fprintf(os.Stderr, "Error: commit failed: %v\n", err)
		fmt.Fprintln(os.Stderr, "Tip: make sure you have changes to commit in instructions/"+skillName+"/")
		_ = gitops.CheckoutBranch(repoDir, gitops.DefaultBranch(repoDir))
		os.Exit(1)
	}
	fmt.Println("  ✓ Changes committed")

	// Optional: add skill to group manifests
	if len(groups) > 0 {
		fmt.Printf("→ Adding skill to group manifest(s): %s ...\n", strings.Join(groups, ", "))
		manifestChanged := false
		for _, group := range groups {
			if addSkillToGroupManifest(repoDir, skillName, group) {
				manifestChanged = true
				fmt.Printf("  ✓ Added to %q\n", group)
			}
		}
		if manifestChanged {
			_ = gitops.AddToSparseCheckout(repoDir, ".manifest")
			if _, err := runGit(repoDir, "add", ".manifest/"); err == nil {
				commitMsg := fmt.Sprintf("feat(%s): add to groups %s", skillName, strings.Join(groups, ", "))
				if _, err := runGit(repoDir, "commit", "-m", commitMsg); err == nil {
					fmt.Println("  ✓ Manifest changes committed")
				} else {
					fmt.Fprintf(os.Stderr, "Warning: failed to commit manifest changes: %v\n", err)
				}
			}
		}
	}

	fmt.Printf("→ Pushing branch %s ...\n", branchName)
	if err := gitops.Push(repoDir, branchName); err != nil {
		fmt.Fprintf(os.Stderr, "Error: push failed: %v\n", err)
		_ = gitops.CheckoutBranch(repoDir, gitops.DefaultBranch(repoDir))
		os.Exit(1)
	}
	fmt.Println("  ✓ Branch pushed")

	fmt.Printf("\n✅ Skill %q pushed for review\n", skillName)
	fmt.Printf("   Branch: %s\n", branchName)
	if len(groups) > 0 {
		fmt.Printf("   Groups: %s\n", strings.Join(groups, ", "))
	}

	if remoteURL, err := gitops.GetRemoteURL(repoDir); err == nil {
		if prURL := buildPRURL(remoteURL, branchName); prURL != "" {
			fmt.Printf("   Create PR: %s\n", prURL)
		} else {
			fmt.Println("   (local repository - request a review from the skill owner)")
		}
	}
	fmt.Printf("\n⚠  Note: switched back to the main branch - skill %q may not be visible locally.\n", skillName)
	fmt.Println("   After the PR is merged, run `skills pull` to get it back.")
}

func printPushHelp() {
	fmt.Print(`Create a branch, commit local changes to a skill, and push for review.

Usage:
  skills push <skill-name> [--groups <group1> <group2> ...]

The command will:
  1. Create branch: feature/<skill-name>-update
  2. Stage all changes in instructions/<skill-name>/
  3. Commit with a conventional commit message
  4. (optional) Add skill to specified group manifests and commit manifest changes
  5. Push the branch to origin
  6. Print the Pull Request URL (for GitHub/GitLab remotes)

Flags:
  --groups  Add skill to specified group manifests (creates group file if not found)

Examples:
  skills push my-skill
  skills push my-skill --groups backend security
  skills push my-skill --groups backend,frontend

Note: when --groups is used, manifest changes are included in the same PR branch.
If a group manifest does not exist, it will be created with the skill as its first entry.
`)
}

type groupManifestFile struct {
	Skills     []string `json:"skills"`
	SubConfigs []string `json:"sub-configs"`
}

func addSkillToGroupManifest(repoDir, skillName, groupName string) bool {
	manifestDir := filepath.Join(repoDir, ".manifest")
	manifestFile := filepath.Join(manifestDir, groupName+".json")

	var m groupManifestFile

	if data, err := os.ReadFile(manifestFile); err == nil {
		if err := json.Unmarshal(data, &m); err != nil {
			m = groupManifestFile{Skills: []string{}, SubConfigs: []string{}}
		}
		for _, s := range m.Skills {
			if s == skillName {
				fmt.Printf("  ℹ Skill %q already in group %q\n", skillName, groupName)
				return false
			}
		}
	} else {
		// Create new group manifest
		if err := os.MkdirAll(manifestDir, 0755); err != nil {
			fmt.Fprintf(os.Stderr, "Error: failed to create .manifest/: %v\n", err)
			return false
		}
		m = groupManifestFile{Skills: []string{}, SubConfigs: []string{}}
		fmt.Printf("  → Creating new group manifest: %s.json\n", groupName)
	}

	m.Skills = append(m.Skills, skillName)
	sort.Strings(m.Skills)
	data, _ := json.MarshalIndent(m, "", "  ")
	if err := os.WriteFile(manifestFile, append(data, '\n'), 0644); err != nil {
		fmt.Fprintf(os.Stderr, "Error: failed to write %s.json: %v\n", groupName, err)
		return false
	}
	return true
}

// runGit is a local helper that runs a raw git command (used for manifest staging).
func runGit(dir string, args ...string) (string, error) {
	cmd := exec.Command("git", args...)
	cmd.Dir = dir
	out, err := cmd.CombinedOutput()
	return strings.TrimSpace(string(out)), err
}

// buildPRURL converts a git remote URL into a PR creation URL for supported hosts.
func buildPRURL(remoteURL, branchName string) string {
	remoteURL = strings.TrimSuffix(strings.TrimSpace(remoteURL), ".git")
	switch {
	case strings.HasPrefix(remoteURL, "https://github.com/"):
		return remoteURL + "/compare/" + branchName
	case strings.HasPrefix(remoteURL, "git@github.com:"):
		return "https://github.com/" + strings.TrimPrefix(remoteURL, "git@github.com:") + "/compare/" + branchName
	case strings.HasPrefix(remoteURL, "https://gitlab.com/"):
		return remoteURL + "/-/merge_requests/new?merge_request[source_branch]=" + branchName
	default:
		return ""
	}
}
