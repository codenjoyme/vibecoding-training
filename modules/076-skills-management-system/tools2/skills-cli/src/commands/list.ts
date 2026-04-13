import * as config from '../lib/config';
import * as gitops from '../lib/gitops';

export function runList(args: string[]): void {
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`List all available skills in the repository.

Usage:
  skills list

Active skills (checked out in this workspace) are marked with ✅.
Other skills exist in the repo but are not part of your current groups.

`);
    return;
  }

  const cfg = config.load();
  const repoDir = config.REPO_SUB_DIR;

  let allSkills: string[];
  try {
    allSkills = gitops.listAllSkills(repoDir);
  } catch (err) {
    console.error(`Error: failed to list skills: ${err}`);
    process.exit(1);
  }

  const activeSet = new Set<string>(cfg.skills);

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
  }

  console.log(`\nActive: ${activeCount}  |  Total: ${allSkills.length}`);
}
