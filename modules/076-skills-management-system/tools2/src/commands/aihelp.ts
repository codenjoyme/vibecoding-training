import * as fs from 'fs';
import * as path from 'path';

export function runAIHelp(): void {
  // Try to find SKILL-CLI.md relative to the script
  const candidates = [
    path.join(__dirname, '..', '..', 'SKILL-CLI.md'),  // from dist/commands/
    path.join(__dirname, '..', 'SKILL-CLI.md'),
  ];

  for (const p of candidates) {
    if (fs.existsSync(p)) {
      console.log(fs.readFileSync(p, 'utf8'));
      return;
    }
  }

  console.error('Error: SKILL-CLI.md not found.');
  console.error('See https://github.com/codenjoyme/apm-lite/blob/master/SKILL-CLI.md');
  console.error('Or use `skills help` for basic usage.');
  process.exit(1);
}
