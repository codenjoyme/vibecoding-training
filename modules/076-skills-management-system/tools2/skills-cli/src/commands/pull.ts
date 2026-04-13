import * as config from '../lib/config';
import * as gitops from '../lib/gitops';

export function runPull(args: string[]): void {
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`Update local skills from the remote repository.

Usage:
  skills pull

`);
    return;
  }

  const cfg = config.load();

  console.log('→ Pulling latest skills ...');
  try {
    gitops.pull(cfg.repo_url ? config.REPO_SUB_DIR : config.REPO_SUB_DIR);
  } catch (err) {
    console.error(`Error: pull failed: ${err}`);
    process.exit(1);
  }
  console.log('✅ Skills updated successfully');
}
