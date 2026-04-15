export function printHelp(): void {
  console.log(`Skills CLI — manage shared AI instruction skills across your team

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
  ai-help   Show concise CLI reference for AI agents
  init-repo Initialize a new skills repository with base structure
  help      Show this help message

Use "skills <command> --help" for more information about a command.

Examples:
  skills init --repo https://github.com/org/skills --groups backend
  skills init --repo ../skills-repo --groups backend,security
  skills init --repo ../skills-repo backend security
  skills pull
  skills push code-review-base
  skills list
`);
}
