import * as config from '../lib/config';
import * as gitops from '../lib/gitops';

export function runPush(args: string[]): void {
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`Create a branch, commit local changes to a skill, and push for review.

Usage:
  skills push <skill-name>

The command will:
  1. Create branch: feature/<skill-name>-update
  2. Stage all changes in instructions/<skill-name>/
  3. Commit with a conventional commit message
  4. Push the branch to origin
  5. Print the Pull Request URL (for GitHub/GitLab remotes)

`);
    return;
  }

  const positional = args.filter(a => !a.startsWith('--'));
  if (positional.length === 0) {
    console.error('Error: skill name is required');
    console.error('Usage: skills push <skill-name>');
    process.exit(1);
  }

  const skillName = positional[0];
  const branchName = `feature/${skillName}-update`;

  const cfg = config.load();
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
    process.exit(1);
  }
  console.log('  ✓ Changes committed');

  console.log(`→ Pushing branch ${branchName} ...`);
  try {
    gitops.push(repoDir, branchName);
  } catch (err) {
    console.error(`Error: push failed: ${err}`);
    process.exit(1);
  }
  console.log('  ✓ Branch pushed');

  // Build PR URL hint for GitHub/GitLab
  let prUrl = '';
  try {
    const remoteURL = gitops.getRemoteURL(repoDir);
    const normalized = remoteURL.replace(/\.git$/, '').replace('git@github.com:', 'https://github.com/');
    if (normalized.includes('github.com')) {
      prUrl = `${normalized}/compare/${branchName}?expand=1`;
    } else if (normalized.includes('gitlab.com')) {
      prUrl = `${normalized}/-/merge_requests/new?merge_request%5Bsource_branch%5D=${branchName}`;
    }
  } catch { /* ignore */ }

  console.log(`\n✅ Skill "${skillName}" pushed for review`);
  console.log(`   Branch: ${branchName}`);
  if (prUrl) console.log(`   Open PR: ${prUrl}`);
  void cfg; // suppress unused warning
}
