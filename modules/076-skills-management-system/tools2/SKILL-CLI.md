# Skills CLI - Quick Reference for AI Agents

## Commands

```
skills init --repo <url> --groups <g1>[,<g2>...]   Clone repo, resolve skills, sparse checkout
skills init                                         Re-init from existing skills.json
skills pull                                         Pull latest from remote
skills push <skill-name>                            Branch + commit + push for review
skills list                                         List skills (✅ active, ○ inactive)
skills list --verbose                               Include description and owner
skills list --json                                  Output as JSON array
skills create <name>                                Create new skill (SKILL.md + info.json)
skills enable group <name>                          Add group to workspace config
skills disable group <name>                         Remove group from workspace config
skills enable <skill>                               Add individual skill or re-enable excluded
skills disable <skill>                              Exclude skill from resolution
skills ai-help                                      Show this reference
skills help                                         Show general help
```

## Config: skills.json (project root)

```json
{
  "repo_url": "../skills-repo",
  "groups": ["project-alpha"],
  "skills": ["resolved-skill-1", "resolved-skill-2"],
  "extra_skills": ["my-custom-skill"],
  "excluded_skills": ["unwanted-skill"]
}
```

## Skill Resolution Priority

1. `_global.json` skills (for everyone)
2. Group manifest skills (`<group>.json` + sub-configs)
3. `extra_skills` (individual additions)
4. `excluded_skills` (removals applied last)

## Workspace Layout

```
my-project/
├── skills.json              ← workspace config
├── instructions/             ← cloned skills repo (sparse checkout)
│   ├── .manifest/           ← manifest files
│   ├── skill-name/
│   │   ├── SKILL.md         ← instructions for AI agent
│   │   └── info.json        ← metadata (description, owner)
│   └── ...
└── src/                     ← project source code
```

## Manifest Files (.manifest/)

| File | Purpose |
|------|---------|
| `_global.json` | Skills for all groups: `{"skills": [...]}` |
| `<group>.json` | Group-specific: `{"skills": [...], "sub-configs": [...]}` |
| `<sub>.json` | Sub-config referenced by groups: `{"skills": [...]}` |
| `_agents.json` | IDE bindings (informational) |

## Typical Workflow

```bash
skills init --repo git@github.com:org/skills.git --groups backend
skills list --verbose
# edit instructions/code-review/SKILL.md
skills push code-review
skills pull
skills enable my-new-skill
skills init   # re-apply
```
