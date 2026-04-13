import { execSync, ExecSyncOptions } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

function run(dir: string | null, ...args: string[]): string {
  const opts: ExecSyncOptions = { encoding: 'utf8' };
  if (dir) opts.cwd = dir;
  try {
    return (execSync(`git ${args.map(a => `"${a}"`).join(' ')}`, opts) as string).trim();
  } catch (err: unknown) {
    const e = err as { stdout?: Buffer | string; stderr?: Buffer | string; message?: string };
    const msg = (e.stderr?.toString() || e.stdout?.toString() || e.message || String(err)).trim();
    throw new Error(`git ${args.join(' ')}: ${msg}`);
  }
}

export function clone(sourceURL: string, targetDir: string): void {
  fs.mkdirSync(path.dirname(targetDir), { recursive: true });
  run(null, 'clone', sourceURL, targetDir);
}

export function setupSparseCheckout(repoDir: string, skills: string[]): void {
  run(repoDir, 'sparse-checkout', 'init', '--cone');
  run(repoDir, 'sparse-checkout', 'set', '.manifest', ...skills);
}

export function defaultBranch(repoDir: string): string {
  try {
    const out = run(repoDir, 'symbolic-ref', '--short', 'refs/remotes/origin/HEAD');
    const parts = out.split('/');
    if (parts.length >= 2) return parts[parts.length - 1];
  } catch {
    // fall through
  }
  return 'master';
}

export function checkoutBranch(repoDir: string, branch: string): void {
  run(repoDir, 'checkout', branch);
}

export function pull(repoDir: string): void {
  const branch = defaultBranch(repoDir);
  checkoutBranch(repoDir, branch);
  run(repoDir, 'pull', 'origin', branch);
}

export function listAllSkills(repoDir: string): string[] {
  const out = run(repoDir, 'ls-tree', '--name-only', '-d', 'HEAD');
  return out
    .split('\n')
    .map(l => l.trim())
    .filter(l => l.length > 0 && !l.startsWith('.'))
    .sort();
}

export function createBranch(repoDir: string, branchName: string): void {
  run(repoDir, 'checkout', '-b', branchName);
}

export function stageAndCommit(repoDir: string, skillName: string): void {
  const skillPath = skillName.replace(/\\/g, '/') + '/';
  run(repoDir, 'add', skillPath);
  run(repoDir, 'commit', '-m', `feat(${skillName}): update skill instructions`);
}

export function push(repoDir: string, branchName: string): void {
  run(repoDir, 'push', 'origin', branchName);
  const branch = defaultBranch(repoDir);
  try { checkoutBranch(repoDir, branch); } catch { /* ignore */ }
}

export function getRemoteURL(repoDir: string): string {
  return run(repoDir, 'remote', 'get-url', 'origin');
}
