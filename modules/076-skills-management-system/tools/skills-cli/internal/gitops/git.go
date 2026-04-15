// Package gitops wraps git CLI commands needed by the skills CLI.
// All operations call the system's git binary via os/exec.
package gitops

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"strings"
)

// run executes a git command in the given directory and returns trimmed combined output.
// dir may be empty ("") to run in the current working directory.
func run(dir string, args ...string) (string, error) {
	cmd := exec.Command("git", args...)
	if dir != "" {
		cmd.Dir = dir
	}
	out, err := cmd.CombinedOutput()
	if err != nil {
		return "", fmt.Errorf("git %s: %s", strings.Join(args, " "), strings.TrimSpace(string(out)))
	}
	return strings.TrimSpace(string(out)), nil
}

// Clone clones sourceURL into targetDir. Creates parent directories as needed.
func Clone(sourceURL, targetDir string) error {
	if err := os.MkdirAll(filepath.Dir(targetDir), 0755); err != nil {
		return fmt.Errorf("failed to create parent directory: %w", err)
	}
	_, err := run("", "clone", sourceURL, targetDir)
	return err
}

// SetupSparseCheckout configures cone-mode sparse checkout in repoDir.
// Always includes ".manifest" plus the provided skill directories.
func SetupSparseCheckout(repoDir string, skills []string) error {
	if _, err := run(repoDir, "sparse-checkout", "init", "--cone"); err != nil {
		return err
	}
	// Build the set list: .manifest is always included
	dirs := make([]string, 0, len(skills)+1)
	dirs = append(dirs, ".manifest")
	dirs = append(dirs, skills...)
	args := append([]string{"sparse-checkout", "set"}, dirs...)
	_, err := run(repoDir, args...)
	return err
}

// DefaultBranch returns the remote's default branch (the branch origin/HEAD points to).
// Falls back to "master" if the symbolic ref is not set.
func DefaultBranch(repoDir string) string {
	out, err := run(repoDir, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
	if err == nil {
		// out is like "origin/master" or "origin/main" — strip the prefix
		parts := strings.SplitN(out, "/", 2)
		if len(parts) == 2 {
			return parts[1]
		}
	}
	return "master"
}

// CheckoutBranch switches to the named branch in repoDir.
func CheckoutBranch(repoDir, branch string) error {
	_, err := run(repoDir, "checkout", branch)
	return err
}

// Pull ensures we are on the default branch and then runs git pull.
func Pull(repoDir string) error {
	defBranch := DefaultBranch(repoDir)
	if err := CheckoutBranch(repoDir, defBranch); err != nil {
		return fmt.Errorf("checkout %s: %w", defBranch, err)
	}
	_, err := run(repoDir, "pull", "origin", defBranch)
	return err
}

// ListAllSkills returns all top-level skill directory names in the repo as of HEAD.
// Uses git ls-tree so it works regardless of sparse checkout state.
func ListAllSkills(repoDir string) ([]string, error) {
	out, err := run(repoDir, "ls-tree", "--name-only", "-d", "HEAD")
	if err != nil {
		return nil, err
	}
	var skills []string
	for _, line := range strings.Split(out, "\n") {
		line = strings.TrimSpace(line)
		// Exclude hidden directories (like .manifest)
		if line != "" && !strings.HasPrefix(line, ".") {
			skills = append(skills, line)
		}
	}
	sort.Strings(skills)
	return skills, nil
}

// CreateBranch creates and switches to a new branch in repoDir.
func CreateBranch(repoDir, branchName string) error {
	_, err := run(repoDir, "checkout", "-b", branchName)
	return err
}

// StageAndCommit stages all changes in skillDir/ and commits them with a conventional message.
func StageAndCommit(repoDir, skillName string) error {
	// Use forward slashes for git add argument (works on all platforms)
	skillPath := strings.ReplaceAll(skillName, "\\", "/") + "/"
	if _, err := run(repoDir, "add", skillPath); err != nil {
		return fmt.Errorf("git add failed: %w", err)
	}
	commitMsg := fmt.Sprintf("feat(%s): update skill instructions", skillName)
	_, err := run(repoDir, "commit", "-m", commitMsg)
	return err
}

// Push pushes the named branch to origin, then returns to the default branch.
func Push(repoDir, branchName string) error {
	if _, err := run(repoDir, "push", "origin", branchName); err != nil {
		return err
	}
	// Return to default branch so subsequent pull/list operations work correctly
	defBranch := DefaultBranch(repoDir)
	_ = CheckoutBranch(repoDir, defBranch)
	return nil
}

// GetRemoteURL returns the URL of the 'origin' remote.
func GetRemoteURL(repoDir string) (string, error) {
	return run(repoDir, "remote", "get-url", "origin")
}

// CurrentBranch returns the name of the currently checked-out branch.
func CurrentBranch(repoDir string) (string, error) {
	return run(repoDir, "rev-parse", "--abbrev-ref", "HEAD")
}

// SkillInfo holds metadata from a skill's info.json.
type SkillInfo struct {
	Description string `json:"description"`
	Owner       string `json:"owner"`
}

// LoadSkillInfo reads info.json from a skill directory. Returns nil if not found.
func LoadSkillInfo(repoDir, skillName string) *SkillInfo {
	infoPath := filepath.Join(repoDir, skillName, "info.json")
	data, err := os.ReadFile(infoPath)
	if err != nil {
		return nil
	}
	var info SkillInfo
	if err := json.Unmarshal(data, &info); err != nil {
		return nil
	}
	return &info
}
