"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.printHelp = printHelp;
function printHelp() {
    console.log(`Skills CLI - manage shared AI instruction skills across your team

Usage:
  skills <command> [flags]

Commands:
  init      Initialize workspace from a central skills repository
              --repo <url|path>   URL or local path to the skills repo (required)
              --groups <g1,g2>    Groups to activate (comma-separated or positional)

  pull      Update local skills from the remote repository

  push      Propose changes to a skill via a branch and Pull Request
              <skill-name>        Name of the skill to push (required)

  list      List available skills in the repository
              --verbose           Show description and owner from info.json
              --json              Output as JSON array

  create    Create a new skill with SKILL.md and info.json templates
              <skill-name>        Name of the new skill (required)

  enable    Enable a group or individual skill
              group <name>        Add a group to the workspace
              <skill-name>        Add an individual skill (extra_skills)

  disable   Disable a group or individual skill
              group <name>        Remove a group from the workspace
              <skill-name>        Exclude an individual skill (excluded_skills)

  ai-help   Show concise CLI reference for AI agents
  init-repo Initialize a new skills repository with base structure
              <folder-name>       Target folder name (required)

  help      Show this help message

Use "skills <command> --help" for more information about a command.

Examples:
  skills init --repo https://github.com/org/skills --groups backend
  skills init --repo ../skills-repo --groups backend,security
  skills pull
  skills push code-review-base
  skills list --verbose
  skills create my-skill
  skills enable group security
  skills enable my-custom-skill
  skills disable group security
  skills disable obsolete-skill
`);
}
