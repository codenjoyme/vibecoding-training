import * as fs from 'fs';
import * as path from 'path';

export function runAIHelp(): void {
  // Try to find SKILL-CLI.md relative to the script
  const candidates = [
    path.join(__dirname, '..', '..', 'SKILL-CLI.md'),  // from dist/commands/
    path.join(__dirname, '..', 'SKILL-CLI.md'),
  ];

  for (const p of candidates) {
    if (fs.existsSync(p)) {
      console.log(fs.readFileSync(p, 'utf8'));
      return;
    }
  }

  // Fallback inline
  console.log(FALLBACK);
}

const FALLBACK = `# Skills CLI — Quick Reference for AI Agents

## Commands

skills init --repo <url> --groups <g1>[,<g2>...]   Clone repo, resolve skills, sparse checkout
skills init                                         Re-init from existing skills.json
skills pull                                         Pull latest from remote
skills push <skill-name>                            Branch + commit + push for review
skills list                                         List skills (active/inactive)
skills list --verbose                               Include description and owner
skills list --json                                  Output as JSON array
skills create <name>                                Create new skill (SKILL.md + info.json)
skills enable group <name>                          Add group to workspace config
skills disable group <name>                         Remove group from workspace config
skills enable <skill>                               Add individual skill or re-enable excluded
skills disable <skill>                              Exclude skill from resolution
skills ai-help                                      Show this reference
skills help                                         Show general help

## Skill Resolution Priority

1. _global.json skills (for everyone)
2. Group manifest skills (<group>.json + sub-configs)
3. extra_groups (same as groups)
4. extra_skills (individual additions)
5. excluded_skills (removals applied last)
`;
