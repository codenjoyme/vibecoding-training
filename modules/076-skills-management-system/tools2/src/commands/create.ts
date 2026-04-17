import * as fs from 'fs';
import * as path from 'path';
import * as config from '../lib/config';
import * as gitops from '../lib/gitops';

const SKILL_TEMPLATE = `# Skill: %NAME%

## Purpose

_Describe what this skill teaches or enables._

## Instructions

_Write the detailed instructions for the AI agent here._
`;

const INFO_TEMPLATE = `{
  "description": "This skill provides _____. It can be used for _____. The main features include _____.",
  "owner": "Your_Name@domain.com"
}
`;

export function runCreate(args: string[]): void {
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`Create a new skill in the local instructions/ folder.

Usage:
  skills create <skill-name>

Creates:
  instructions/<skill-name>/SKILL.md   — skill instructions template
  instructions/<skill-name>/info.json  — skill metadata (description, owner)

`);
    return;
  }

  const positional = args.filter(a => !a.startsWith('--'));
  if (positional.length === 0) {
    console.error('Error: skill name is required');
    console.error('Usage: skills create <skill-name>');
    process.exit(1);
  }

  const skillName = positional[0];

  // Verify workspace is initialized
  try {
    config.load();
  } catch (err) {
    console.error(String(err));
    process.exit(1);
  }

  const skillDir = path.join(config.REPO_SUB_DIR, skillName);

  // Check if skill already exists
  if (fs.existsSync(skillDir)) {
    console.error(`Error: skill "${skillName}" already exists at ${skillDir}`);
    process.exit(1);
  }

  // Create skill directory
  fs.mkdirSync(skillDir, { recursive: true });

  // Write SKILL.md
  const skillPath = path.join(skillDir, 'SKILL.md');
  fs.writeFileSync(skillPath, SKILL_TEMPLATE.replace('%NAME%', skillName), 'utf8');

  // Write info.json
  const infoPath = path.join(skillDir, 'info.json');
  fs.writeFileSync(infoPath, INFO_TEMPLATE, 'utf8');

  // Add to sparse-checkout so git can track the new skill
  try {
    gitops.addToSparseCheckout(config.REPO_SUB_DIR, skillName);
  } catch { /* ignore — may not be a sparse repo */ }

  // Register in extra_skills so pull doesn't lose it
  const cfg = config.load();
  if (!cfg.extra_skills.includes(skillName)) {
    cfg.extra_skills.push(skillName);
    config.save(cfg);
  }

  console.log(`✅ Skill "${skillName}" created at ${skillDir}`);
  console.log(`   → ${skillPath}`);
  console.log(`   → ${infoPath}`);
  console.log('\nEdit SKILL.md with your instructions, then use `skills push` to propose it.');
}
