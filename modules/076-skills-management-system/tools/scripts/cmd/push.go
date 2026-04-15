package cmd

import (
	"flag"
	"fmt"
	"os"
	"strings"

	"github.com/vibecoding/skills-cli/internal/config"
	"github.com/vibecoding/skills-cli/internal/gitops"
)

// RunPush handles the `skills push <skill-name>` command.
func RunPush(args []string) {
	fs := flag.NewFlagSet("push", flag.ExitOnError)
	fs.Usage = func() {
		fmt.Print(`Create a branch, commit local changes to a skill, and push for review.

Usage:
  skills push <skill-name>

The command will:
  1. Create branch: feature/<skill-name>-update
  2. Stage all changes in instructions/<skill-name>/
  3. Commit with a conventional commit message
  4. Push the branch to origin
  5. Print the Pull Request URL (for GitHub/GitLab remotes)

`)
		fs.PrintDefaults()
	}

	if err := fs.Parse(args); err != nil {
		os.Exit(1)
	}

	if len(fs.Args()) == 0 {
		fmt.Fprintln(os.Stderr, "Error: skill name is required")
		fs.Usage()
		os.Exit(1)
	}

	skillName := fs.Args()[0]
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
		os.Exit(1)
	}
	fmt.Println("  ✓ Changes committed")

	fmt.Printf("→ Pushing branch %s ...\n", branchName)
	if err := gitops.Push(repoDir, branchName); err != nil {
		fmt.Fprintf(os.Stderr, "Error: push failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("  ✓ Branch pushed")

	fmt.Printf("\n✅ Skill %q pushed for review\n", skillName)
	fmt.Printf("   Branch: %s\n", branchName)

	if remoteURL, err := gitops.GetRemoteURL(repoDir); err == nil {
		if prURL := buildPRURL(remoteURL, branchName); prURL != "" {
			fmt.Printf("   Create PR: %s\n", prURL)
		} else {
			fmt.Println("   (local repository — request a review from the skill owner)")
		}
	}
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
