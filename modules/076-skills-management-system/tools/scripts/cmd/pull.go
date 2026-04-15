package cmd

import (
	"flag"
	"fmt"
	"os"

	"github.com/vibecoding/skills-cli/internal/config"
	"github.com/vibecoding/skills-cli/internal/gitops"
)

// RunPull handles the `skills pull` command.
func RunPull(args []string) {
	fs := flag.NewFlagSet("pull", flag.ExitOnError)
	fs.Usage = func() {
		fmt.Print(`Update local skills from the remote repository.

Usage:
  skills pull

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

	fmt.Print("→ Pulling latest skills ...\n")
	if err := gitops.Pull(cfg.RepoPath()); err != nil {
		fmt.Fprintf(os.Stderr, "Error: pull failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Println("✅ Skills updated successfully")
}
