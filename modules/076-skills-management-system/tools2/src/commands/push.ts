import * as fs from 'fs';
import * as path from 'path';
import * as config from '../lib/config';
import * as gitops from '../lib/gitops';

function parseArgs(args: string[]): { skillName: string; groups: string[]; help: boolean } {
  if (args.includes('--help') || args.includes('-h')) {
    return { skillName: '', groups: [], help: true };
  }

  let skillName = '';
  const groups: string[] = [];
  let i = 0;
  let groupsFlag = false;

  while (i < args.length) {
    if (args[i] === '--groups' && i + 1 < args.length) {
      groupsFlag = true;
      i++;
      // Collect all following non-flag args as group names
      while (i < args.length && !args[i].startsWith('--')) {
        for (const g of args[i].split(/[,\s]+/)) {
          const t = g.trim();
          if (t) groups.push(t);
        }
        i++;
      }
      continue;
    } else if (!args[i].startsWith('--') && !skillName) {
      skillName = args[i];
    }
    i++;
  }

  return { skillName, groups, help: false };
}

function printPushHelp(): void {
  console.log(`Create a branch, commit local changes to a skill, and push for review.

Usage:
  skills push <skill-name> [--groups <group1> <group2> ...]

The command will:
  1. Create branch: feature/<skill-name>-update
  2. Stage all changes in instructions/<skill-name>/
  3. Commit with a conventional commit message
  4. (optional) Add skill to specified group manifests and commit manifest changes
  5. Push the branch to origin
  6. Print the Pull Request URL (for GitHub/GitLab remotes)

Flags:
  --groups  Add skill to specified group manifests (creates group file if not found)

Examples:
  skills push my-skill
  skills push my-skill --groups backend security
  skills push my-skill --groups backend,frontend

Note: when --groups is used, manifest changes are included in the same PR branch.
If a group manifest does not exist, it will be created with the skill as its first entry.
`);
}

function addSkillToGroupManifest(repoDir: string, skillName: string, groupName: string): boolean {
  const manifestDir = path.join(repoDir, '.manifest');
  const manifestFile = path.join(manifestDir, `${groupName}.json`);

  let manifest: { skills: string[]; 'sub-configs'?: string[] };

  if (fs.existsSync(manifestFile)) {
    try {
      manifest = JSON.parse(fs.readFileSync(manifestFile, 'utf8'));
    } catch {
      manifest = { skills: [], 'sub-configs': [] };
    }
    if (!manifest.skills) manifest.skills = [];
    if (manifest.skills.includes(skillName)) {
      console.log(`  ℹ Skill "${skillName}" already in group "${groupName}"`);
      return false;
    }
  } else {
    // Create new group manifest
    if (!fs.existsSync(manifestDir)) {
      fs.mkdirSync(manifestDir, { recursive: true });
    }
    manifest = { skills: [], 'sub-configs': [] };
    console.log(`  → Creating new group manifest: ${groupName}.json`);
  }

  manifest.skills.push(skillName);
  manifest.skills.sort();
  fs.writeFileSync(manifestFile, JSON.stringify(manifest, null, 2) + '\n', 'utf8');
  return true;
}

export function runPush(args: string[]): void {
  const { skillName, groups, help } = parseArgs(args);

  if (help) {
    printPushHelp();
    return;
  }

  if (!skillName) {
    console.error('Error: skill name is required');
    console.error('Usage: skills push <skill-name> [--groups <group1> <group2> ...]');
    process.exit(1);
  }

  const branchName = `feature/${skillName}-update`;

  try {
    config.load();
  } catch (err) {
    console.error(String(err));
    process.exit(1);
  }
  const repoDir = config.REPO_SUB_DIR;

  console.log(`→ Creating branch ${branchName} ...`);
  try {
    gitops.createBranch(repoDir, branchName);
  } catch (err) {
    console.error(`Error: failed to create branch: ${err}`);
    console.error(`Tip: if the branch already exists, delete it with:`);
    console.error(`     git -C instructions branch -D ${branchName}`);
    process.exit(1);
  }
  console.log('  ✓ Branch created');

  console.log(`→ Staging and committing changes in ${skillName}/ ...`);
  try {
    gitops.stageAndCommit(repoDir, skillName);
  } catch (err) {
    console.error(`Error: commit failed: ${err}`);
    console.error(`Tip: make sure you have changes to commit in instructions/${skillName}/`);
    // Return to default branch before exiting so workspace is not left on a feature branch
    try { gitops.checkoutBranch(repoDir, gitops.defaultBranch(repoDir)); } catch { /* ignore */ }
    process.exit(1);
  }
  console.log('  ✓ Changes committed');

  // Optional: add skill to group manifests
  if (groups.length > 0) {
    console.log(`→ Adding skill to group manifest(s): ${groups.join(', ')} ...`);
    let manifestChanged = false;
    for (const group of groups) {
      if (addSkillToGroupManifest(repoDir, skillName, group)) {
        manifestChanged = true;
        console.log(`  ✓ Added to "${group}"`);
      }
    }
    if (manifestChanged) {
      try {
        gitops.addToSparseCheckout(repoDir, '.manifest');
        // Stage and commit manifest changes using execFileSync directly
        const { execFileSync } = require('child_process');
        execFileSync('git', ['add', '.manifest/'], { cwd: repoDir, encoding: 'utf8' });
        execFileSync('git', ['commit', '-m', `feat(${skillName}): add to groups ${groups.join(', ')}`], { cwd: repoDir, encoding: 'utf8' });
        console.log('  ✓ Manifest changes committed');
      } catch (err) {
        console.error(`Warning: failed to commit manifest changes: ${err}`);
      }
    }
  }

  console.log(`→ Pushing branch ${branchName} ...`);
  try {
    gitops.push(repoDir, branchName);
  } catch (err) {
    console.error(`Error: push failed: ${err}`);
    try { gitops.checkoutBranch(repoDir, gitops.defaultBranch(repoDir)); } catch { /* ignore */ }
    process.exit(1);
  }
  console.log('  ✓ Branch pushed');

  // Build PR URL hint for GitHub/GitLab
  let prUrl = '';
  try {
    const remoteURL = gitops.getRemoteURL(repoDir);
    const normalized = remoteURL
      .replace(/\.git$/, '')
      .replace(/^git@github\.com:/, 'https://github.com/')
      .replace(/^ssh:\/\/git@github\.com\//, 'https://github.com/')
      .replace(/^git@gitlab\.com:/, 'https://gitlab.com/')
      .replace(/^ssh:\/\/git@gitlab\.com\//, 'https://gitlab.com/');
    if (normalized.includes('github.com')) {
      prUrl = `${normalized}/compare/${branchName}?expand=1`;
    } else if (normalized.includes('gitlab.com')) {
      prUrl = `${normalized}/-/merge_requests/new?merge_request%5Bsource_branch%5D=${branchName}`;
    }
  } catch { /* ignore */ }

  console.log(`\n✅ Skill "${skillName}" pushed for review`);
  console.log(`   Branch: ${branchName}`);
  if (groups.length > 0) {
    console.log(`   Groups: ${groups.join(', ')}`);
  }
  if (prUrl) {
    console.log(`   Create PR: ${prUrl}`);
  } else {
    console.log('   (local repository - request a review from the skill owner)');
  }
  console.log(`\n⚠  Note: switched back to the main branch - skill "${skillName}" may not be visible locally.`);
  console.log('   After the PR is merged, run `skills pull` to get it back.');
}
