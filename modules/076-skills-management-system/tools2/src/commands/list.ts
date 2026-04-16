import * as config from '../lib/config';
import * as gitops from '../lib/gitops';
import * as manifest from '../lib/manifest';
import { resolveEffectiveGroups, applyExtraAndExcluded } from './toggle';

export function runList(args: string[]): void {
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`List all available skills in the repository.

Usage:
  skills list [--verbose] [--json]

Flags:
  --verbose  Show description and owner from info.json
  --json     Output skills as JSON array

Active skills (checked out in this workspace) are marked with ✅.
Other skills exist in the repo but are not part of your current groups.

`);
    return;
  }

  const verbose = args.includes('--verbose');
  const jsonOut = args.includes('--json');

  let cfg: config.Config;
  try {
    cfg = config.load();
  } catch (err) {
    console.error(String(err));
    process.exit(1);
  }
  const repoDir = config.REPO_SUB_DIR;

  let allSkills: string[];
  try {
    allSkills = gitops.listAllSkills(repoDir);
  } catch (err) {
    console.error(`Error: failed to list skills: ${err}`);
    process.exit(1);
  }

  // Resolve active skills dynamically from manifests
  const groups = resolveEffectiveGroups(cfg);
  let resolvedSkills: string[];
  try {
    resolvedSkills = manifest.resolveSkills(repoDir, groups);
  } catch {
    resolvedSkills = [];
  }
  resolvedSkills = applyExtraAndExcluded(resolvedSkills, cfg);
  const activeSet = new Set<string>(resolvedSkills);

  // JSON output mode
  if (jsonOut) {
    const items = allSkills.map(s => {
      const entry: Record<string, unknown> = { name: s, active: activeSet.has(s) };
      const info = gitops.loadSkillInfo(repoDir, s);
      if (info) {
        entry.description = info.description;
        entry.owner = info.owner;
      }
      return entry;
    });
    console.log(JSON.stringify(items, null, 2));
    return;
  }

  // Normal / verbose text output
  console.log(`Skills repository: ${cfg.repo_url}`);
  console.log(`Groups:           ${cfg.groups.join(', ')}\n`);

  let activeCount = 0;
  for (const s of allSkills) {
    if (activeSet.has(s)) {
      console.log(`  ✅ ${s}`);
      activeCount++;
    } else {
      console.log(`  ○  ${s}`);
    }
    if (verbose) {
      const info = gitops.loadSkillInfo(repoDir, s);
      if (info) {
        console.log(`     ${info.description}`);
        console.log(`     Owner: ${info.owner}`);
      }
    }
  }

  console.log(`\nActive: ${activeCount}  |  Total: ${allSkills.length}`);
}
