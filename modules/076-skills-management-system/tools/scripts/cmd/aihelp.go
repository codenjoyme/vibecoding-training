package cmd

import (
	"fmt"
	"os"
	"path/filepath"
)

// RunAIHelp handles the `skills ai-help` command — prints the SKILL-CLI.md reference.
func RunAIHelp(_ []string) {
	// Try to find SKILL-CLI.md relative to the executable
	exePath, err := os.Executable()
	if err == nil {
		skillCliPath := filepath.Join(filepath.Dir(exePath), "..", "SKILL-CLI.md")
		data, err := os.ReadFile(skillCliPath)
		if err == nil {
			fmt.Print(string(data))
			return
		}
	}
	fmt.Fprintln(os.Stderr, "Error: SKILL-CLI.md not found.")
	fmt.Fprintln(os.Stderr, "See https://github.com/codenjoyme/apm-lite/blob/master/SKILL-CLI.md")
	fmt.Fprintln(os.Stderr, "Or use `skills help` for basic usage.")
	os.Exit(1)
}
