import * as fs from 'fs';
import * as path from 'path';

interface GlobalManifest {
  skills: string[];
}

interface GroupManifest {
  skills: string[];
  'sub-configs'?: string[];
}

function loadGlobal(manifestDir: string): GlobalManifest | null {
  const file = path.join(manifestDir, '_global.json');
  if (!fs.existsSync(file)) return null;
  const data = fs.readFileSync(file, 'utf8');
  return JSON.parse(data) as GlobalManifest;
}

function loadGroup(manifestDir: string, name: string): GroupManifest {
  const file = path.join(manifestDir, `${name}.json`);
  if (!fs.existsSync(file)) {
    throw new Error(`manifest file not found: ${name}.json`);
  }
  const data = fs.readFileSync(file, 'utf8');
  return JSON.parse(data) as GroupManifest;
}

export function resolveSkills(repoPath: string, groups: string[]): string[] {
  const manifestDir = path.join(repoPath, '.manifest');
  const skillSet = new Set<string>();

  // 1. Global skills
  const global = loadGlobal(manifestDir);
  if (global) {
    for (const s of global.skills ?? []) {
      if (s) skillSet.add(s);
    }
  }

  // 2. Per-group skills
  for (const group of groups) {
    const grp = loadGroup(manifestDir, group);
    for (const s of grp.skills ?? []) {
      if (s) skillSet.add(s);
    }

    // 3. Sub-configs
    for (const sub of grp['sub-configs'] ?? []) {
      try {
        const subGrp = loadGroup(manifestDir, sub);
        for (const s of subGrp.skills ?? []) {
          if (s) skillSet.add(s);
        }
      } catch {
        console.warn(`Warning: sub-config "${sub}" not found, skipping`);
      }
    }
  }

  return Array.from(skillSet).sort();
}
