package cmd

import (
	"fmt"
	"os"
)

// Execute dispatches CLI arguments to the appropriate command handler.
func Execute(args []string) {
	if len(args) == 0 || args[0] == "help" || args[0] == "--help" || args[0] == "-h" {
		PrintHelp()
		return
	}

	switch args[0] {
	case "init":
		RunInit(args[1:])
	case "pull":
		RunPull(args[1:])
	case "push":
		RunPush(args[1:])
	case "list":
		RunList(args[1:])
	case "create":
		RunCreate(args[1:])
	case "enable":
		RunEnable(args[1:])
	case "disable":
		RunDisable(args[1:])
	default:
		fmt.Fprintf(os.Stderr, "Error: unknown command %q\n\n", args[0])
		PrintHelp()
		os.Exit(1)
	}
}

// PrintHelp outputs general usage information.
func PrintHelp() {
	fmt.Print(`Skills CLI — manage shared AI instruction skills across your team

Usage:
  skills <command> [flags]

Commands:
  init    Initialize workspace from a central skills repository
  pull    Update local skills from the remote repository
  push    Propose changes to a skill via a branch and Pull Request
  list    List available skills in the repository
  create  Create a new skill with SKILL.md and info.json templates
  enable  Enable a group or individual skill
  disable Disable a group or individual skill
  help    Show this help message

Use "skills <command> --help" for more information about a command.

Examples:
  skills init --repo https://github.com/org/skills --groups backend
  skills init --repo ../skills-repo --groups backend,security
  skills init --repo ../skills-repo backend security
  skills pull
  skills push code-review-base
  skills list
`)
}
