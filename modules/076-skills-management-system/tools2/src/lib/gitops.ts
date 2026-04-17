import { execFileSync, ExecSyncOptions } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

function run(dir: string | null, ...args: string[]): string {
  const opts: ExecSyncOptions = { encoding: 'utf8' };
  if (dir) opts.cwd = dir;
  try {
    return (execFileSync('git', args, opts) as string).trim();
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
  try {
    run(repoDir, 'checkout', '-b', branchName);
  } catch {
    // Branch already exists — delete it and recreate
    run(repoDir, 'branch', '-D', branchName);
    run(repoDir, 'checkout', '-b', branchName);
  }
}

export function stageAndCommit(repoDir: string, skillName: string): void {
  const skillPath = skillName.replace(/\\/g, '/') + '/';
  addToSparseCheckout(repoDir, skillName);
  run(repoDir, 'add', skillPath);
  run(repoDir, 'commit', '-m', `feat(${skillName}): update skill instructions`);
}

export function addToSparseCheckout(repoDir: string, skillName: string): void {
  const current = run(repoDir, 'sparse-checkout', 'list')
    .split('\n')
    .map(l => l.trim())
    .filter(l => l.length > 0);
  if (!current.includes(skillName)) {
    run(repoDir, 'sparse-checkout', 'add', skillName);
  }
}

export function push(repoDir: string, branchName: string): void {
  run(repoDir, 'push', 'origin', branchName);
  const branch = defaultBranch(repoDir);
  try { checkoutBranch(repoDir, branch); } catch { /* ignore */ }
}

export function getRemoteURL(repoDir: string): string {
  return run(repoDir, 'remote', 'get-url', 'origin');
}

export interface SkillInfo {
  description: string;
  owner: string;
}

export function loadSkillInfo(repoDir: string, skillName: string): SkillInfo | null {
  // Try local filesystem first (works for active/checked-out skills)
  const infoPath = path.join(repoDir, skillName, 'info.json');
  if (fs.existsSync(infoPath)) {
    try {
      const data = fs.readFileSync(infoPath, 'utf8');
      return JSON.parse(data) as SkillInfo;
    } catch {
      // fall through to git
    }
  }
  // Fall back to reading from git object database (works for non-checked-out skills)
  try {
    const data = run(repoDir, 'show', `HEAD:${skillName}/info.json`);
    return JSON.parse(data) as SkillInfo;
  } catch {
    return null;
  }
}

export function hasUncommittedChanges(repoDir: string, skillName: string): boolean {
  try {
    const out = run(repoDir, 'status', '--porcelain', skillName + '/');
    return out.length > 0;
  } catch {
    return false;
  }
}

export function stashSkillChanges(repoDir: string, skillName: string): void {
  run(repoDir, 'stash', 'push', '-u', '-m', `skills-cli: auto-stash for ${skillName}`, '--', skillName + '/');
}
