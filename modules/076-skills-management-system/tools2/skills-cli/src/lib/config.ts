import * as fs from 'fs';

export const CONFIG_FILE = 'skills.json';
export const REPO_SUB_DIR = 'instructions';

export interface Config {
  repo_url: string;
  groups: string[];
  skills: string[];
}

export function load(): Config {
  if (!fs.existsSync(CONFIG_FILE)) {
    throw new Error('not a skills workspace — run `skills init` first');
  }
  try {
    const data = fs.readFileSync(CONFIG_FILE, 'utf8');
    return JSON.parse(data) as Config;
  } catch (err) {
    throw new Error(`corrupted config (${CONFIG_FILE}): ${err}`);
  }
}

export function save(cfg: Config): void {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(cfg, null, 2), 'utf8');
}

export function repoPath(): string {
  return REPO_SUB_DIR;
}
