import * as config from '../lib/config';
import * as gitops from '../lib/gitops';
import * as manifest from '../lib/manifest';

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

  const force = args.includes('--force');
  const filtered = args.filter(a => a !== '--force');

  if (filtered[0] === 'group') {
    if (filtered.length < 2) {
      console.error('Error: group name is required');
      console.error('Usage: skills disable group <group-name>');
      process.exit(1);
    }
    disableGroup(filtered[1], force);
  } else {
    disableSkill(filtered[0], force);
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
  reapplySparseCheckout(cfg);
}

function disableGroup(name: string, force: boolean): void {
  let cfg: config.Config;
  try { cfg = config.load(); } catch (err) { console.error(String(err)); process.exit(1); }

  let found = false;
  cfg.groups = cfg.groups.filter(g => { if (g === name) { found = true; return false; } return true; });

  if (!found) {
    console.error(`Group "${name}" is not currently enabled`);
    process.exit(1);
  }

  // Determine which skills will be removed
  const before = resolveAllSkills(cfgWithGroups(cfg, [...cfg.groups, name]));
  const after = resolveAllSkills(cfg);
  const removing = before.filter(s => !after.includes(s));
  const dirty = removing.filter(s => gitops.hasUncommittedChanges(config.REPO_SUB_DIR, s));

  if (dirty.length > 0) {
    if (!force) {
      console.error(`Error: cannot disable group "${name}" - uncommitted changes in: ${dirty.join(', ')}`);
      console.error('Commit or discard your changes first, or use --force to override.');
      process.exit(1);
    }
    // Stash dirty skills before sparse checkout
    for (const s of dirty) {
      gitops.stashSkillChanges(config.REPO_SUB_DIR, s);
      console.log(`  ⚠ Stashed uncommitted changes for "${s}" (use \`git stash list\` to review)`);
    }
  }

  config.save(cfg);
  console.log(`✅ Group "${name}" disabled`);
  reapplySparseCheckout(cfg);
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
    reapplySparseCheckout(cfg);
    return;
  }

  if ((cfg.extra_skills ?? []).includes(name)) {
    console.error(`Skill "${name}" is already enabled`);
    process.exit(1);
  }

  cfg.extra_skills = [...(cfg.extra_skills ?? []), name];
  config.save(cfg);
  console.log(`✅ Skill "${name}" enabled`);
  reapplySparseCheckout(cfg);
}

function disableSkill(name: string, force: boolean): void {
  let cfg: config.Config;
  try { cfg = config.load(); } catch (err) { console.error(String(err)); process.exit(1); }

  // Check for uncommitted changes before disabling
  if (gitops.hasUncommittedChanges(config.REPO_SUB_DIR, name)) {
    if (!force) {
      console.error(`Error: cannot disable skill "${name}" - uncommitted local changes detected`);
      console.error('Commit or discard your changes first, or use --force to override.');
      process.exit(1);
    }
    // Stash dirty skill before sparse checkout
    gitops.stashSkillChanges(config.REPO_SUB_DIR, name);
    console.log(`  ⚠ Stashed uncommitted changes for "${name}" (use \`git stash list\` to review)`);
  }

  // Remove from extra_skills if present
  cfg.extra_skills = (cfg.extra_skills ?? []).filter(s => s !== name);

  if ((cfg.excluded_skills ?? []).includes(name)) {
    console.error(`Skill "${name}" is already disabled`);
    process.exit(1);
  }

  cfg.excluded_skills = [...(cfg.excluded_skills ?? []), name];
  config.save(cfg);
  console.log(`✅ Skill "${name}" disabled`);
  reapplySparseCheckout(cfg);
}

function printEnableHelp(): void {
  console.log(`Enable a group or individual skill in this workspace.

Usage:
  skills enable group <group-name>   Add a group to the workspace
  skills enable <skill-name>         Add an individual skill

Sparse checkout is re-applied automatically after enabling.

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

Flags:
  --force   Force disable even if there are uncommitted local changes

If the skill has uncommitted local changes, the command will refuse
to disable it. Use --force to override - changes will be stashed
automatically (use \`git stash list\` inside instructions/ to review).

Sparse checkout is re-applied automatically after disabling.

Examples:
  skills disable group security
  skills disable security-guidelines
  skills disable security-guidelines --force
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

function resolveAllSkills(cfg: config.Config): string[] {
  const groups = resolveEffectiveGroups(cfg);
  let skills: string[];
  try {
    skills = manifest.resolveSkills(config.REPO_SUB_DIR, groups);
  } catch {
    skills = [];
  }
  return applyExtraAndExcluded(skills, cfg);
}

function cfgWithGroups(cfg: config.Config, groups: string[]): config.Config {
  return { ...cfg, groups };
}

function reapplySparseCheckout(cfg: config.Config): void {
  const skills = resolveAllSkills(cfg);
  console.log(`→ Applying sparse checkout (${skills.length} skill(s)) ...`);
  try {
    gitops.setupSparseCheckout(config.REPO_SUB_DIR, skills);
    console.log('  ✓ Sparse checkout applied');
  } catch (err) {
    console.error(`Warning: sparse checkout failed: ${err}`);
    console.error('Run `skills init` to re-apply manually.');
  }
}
