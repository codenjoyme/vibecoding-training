package main

import (
	"os"

	"github.com/vibecoding/skills-cli/cmd"
)

func main() {
	cmd.Execute(os.Args[1:])
}
