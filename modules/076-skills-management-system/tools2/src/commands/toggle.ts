import * as config from '../lib/config';

export function runEnable(args: string[]): void {
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    printEnableHelp();
    return;
  }

  if (args[0] === 'group') {
    if (args.length < 2) {
      console.error('Error: group name is required');
      console.error('Usage: skills enable group <group-name>');
      process.exit(1);
    }
    enableGroup(args[1]);
  } else {
    enableSkill(args[0]);
  }
}

export function runDisable(args: string[]): void {
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    printDisableHelp();
    return;
  }

  if (args[0] === 'group') {
    if (args.length < 2) {
      console.error('Error: group name is required');
      console.error('Usage: skills disable group <group-name>');
      process.exit(1);
    }
    disableGroup(args[1]);
  } else {
    disableSkill(args[0]);
  }
}

function enableGroup(name: string): void {
  let cfg: config.Config;
  try { cfg = config.load(); } catch (err) { console.error(String(err)); process.exit(1); }

  if (cfg.groups.includes(name)) {
    console.error(`Group "${name}" is already enabled`);
    process.exit(1);
  }

  cfg.groups = [...cfg.groups, name];
  config.save(cfg);
  console.log(`✅ Group "${name}" enabled`);
  console.log('Run `skills init` to re-apply skill resolution.');
}

function disableGroup(name: string): void {
  let cfg: config.Config;
  try { cfg = config.load(); } catch (err) { console.error(String(err)); process.exit(1); }

  let found = false;
  cfg.groups = cfg.groups.filter(g => { if (g === name) { found = true; return false; } return true; });

  if (!found) {
    console.error(`Group "${name}" is not currently enabled`);
    process.exit(1);
  }

  config.save(cfg);
  console.log(`✅ Group "${name}" disabled`);
  console.log('Run `skills init` to re-apply skill resolution.');
}

function enableSkill(name: string): void {
  let cfg: config.Config;
  try { cfg = config.load(); } catch (err) { console.error(String(err)); process.exit(1); }

  // If it was excluded, remove from exclusion
  const excluded = cfg.excluded_skills ?? [];
  if (excluded.includes(name)) {
    cfg.excluded_skills = excluded.filter(s => s !== name);
    config.save(cfg);
    console.log(`✅ Skill "${name}" re-enabled (removed from exclusion list)`);
    console.log('Run `skills init` to re-apply skill resolution.');
    return;
  }

  if ((cfg.extra_skills ?? []).includes(name)) {
    console.error(`Skill "${name}" is already enabled`);
    process.exit(1);
  }

  cfg.extra_skills = [...(cfg.extra_skills ?? []), name];
  config.save(cfg);
  console.log(`✅ Skill "${name}" enabled`);
  console.log('Run `skills init` to re-apply skill resolution.');
}

function disableSkill(name: string): void {
  let cfg: config.Config;
  try { cfg = config.load(); } catch (err) { console.error(String(err)); process.exit(1); }

  // Remove from extra_skills if present
  cfg.extra_skills = (cfg.extra_skills ?? []).filter(s => s !== name);

  if ((cfg.excluded_skills ?? []).includes(name)) {
    console.error(`Skill "${name}" is already disabled`);
    process.exit(1);
  }

  cfg.excluded_skills = [...(cfg.excluded_skills ?? []), name];
  config.save(cfg);
  console.log(`✅ Skill "${name}" disabled`);
  console.log('Run `skills init` to re-apply skill resolution.');
}

function printEnableHelp(): void {
  console.log(`Enable a group or individual skill in this workspace.

Usage:
  skills enable group <group-name>   Add a group to the workspace
  skills enable <skill-name>         Add an individual skill

After enabling, run \`skills init\` to re-apply skill resolution.

Examples:
  skills enable group security
  skills enable my-custom-skill
`);
}

function printDisableHelp(): void {
  console.log(`Disable a group or individual skill in this workspace.

Usage:
  skills disable group <group-name>   Remove a group from the workspace
  skills disable <skill-name>         Exclude an individual skill

After disabling, run \`skills init\` to re-apply skill resolution.

Examples:
  skills disable group security
  skills disable security-guidelines
`);
}

export function resolveEffectiveGroups(cfg: config.Config): string[] {
  const seen = new Set<string>();
  const groups: string[] = [];
  for (const g of cfg.groups) {
    if (!seen.has(g)) { groups.push(g); seen.add(g); }
  }
  return groups;
}

export function applyExtraAndExcluded(resolved: string[], cfg: config.Config): string[] {
  const skillSet = new Set<string>(resolved);
  for (const s of cfg.extra_skills ?? []) skillSet.add(s);
  for (const s of cfg.excluded_skills ?? []) skillSet.delete(s);
  return Array.from(skillSet).sort();
}
