"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.runInitRepo = runInitRepo;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
function runInitRepo(args) {
    if (args.includes('--help') || args.includes('-h')) {
        printInitRepoHelp();
        return;
    }
    const positional = args.filter(a => !a.startsWith('--'));
    if (positional.length === 0) {
        console.error('Error: folder name is required');
        printInitRepoHelp();
        process.exit(1);
    }
    const folderName = positional[0];
    if (fs.existsSync(folderName)) {
        console.error(`Error: folder "${folderName}" already exists`);
        process.exit(1);
    }
    console.log(`→ Creating skills repository at ${folderName} ...`);
    // Create directory structure
    const dirs = [
        path.join(folderName, '.manifest'),
        path.join(folderName, 'skills-cli'),
    ];
    for (const d of dirs) {
        fs.mkdirSync(d, { recursive: true });
    }
    // Write manifest files
    writeFile(path.join(folderName, '.manifest', '_global.json'), GLOBAL_JSON);
    writeFile(path.join(folderName, '.manifest', 'group-1.json'), GROUP1_JSON);
    writeFile(path.join(folderName, '.manifest', 'sub-group.json'), SUBGROUP_JSON);
    // Write skills-cli skill (read SKILL-CLI.md from package root as source of truth)
    const skillCliContent = loadSkillCliMd();
    writeFile(path.join(folderName, 'skills-cli', 'SKILL.md'), skillCliContent);
    writeFile(path.join(folderName, 'skills-cli', 'info.json'), SKILLS_CLI_INFO);
    // Write .gitignore
    writeFile(path.join(folderName, '.gitignore'), '# Skills repo .gitignore\n');
    console.log('  ✓ Files created');
    console.log(`\n✅ Skills repository initialized at ${folderName}`);
    console.log('\nNext steps:');
    console.log(`  cd ${folderName}`);
    console.log('  git init && git add . && git commit -m "init: skills repository"');
    console.log('  # Then push to your Git hosting');
}
function writeFile(filePath, content) {
    fs.writeFileSync(filePath, content, 'utf8');
}
function printInitRepoHelp() {
    console.log(`Initialize a new skills repository with base structure.

Creates a folder with:
  .manifest/_global.json      — global skills config
  .manifest/group-1.json      — example group config
  .manifest/sub-group.json    — example sub-config
  skills-cli/                 — skill: CLI usage, creating skills, IDE integration

Usage:
  skills init-repo <folder-name>

Examples:
  skills init-repo my-skills-repo
  skills init-repo ../shared-skills
`);
}
const GLOBAL_JSON = `{
  "skills": [
    "skills-cli"
  ]
}
`;
const GROUP1_JSON = `{
  "skills": [],
  "sub-configs": ["sub-group"]
}
`;
const SUBGROUP_JSON = `{
  "skills": [],
  "sub-configs": []
}
`;
function loadSkillCliMd() {
    const candidates = [
        path.join(__dirname, '..', '..', 'SKILL-CLI.md'), // from dist/commands/
        path.join(__dirname, '..', 'SKILL-CLI.md'),
    ];
    for (const p of candidates) {
        if (fs.existsSync(p)) {
            return fs.readFileSync(p, 'utf8');
        }
    }
    return '# Skills CLI\n\nSee SKILL-CLI.md in the skills-cli package for full reference.\n';
}
const SKILLS_CLI_INFO = `{
  "description": "Skills CLI reference: commands, creating skills, IDE integration (VSCode/Copilot, Cursor, Claude Code).",
  "owner": "your-name@example.com"
}
`;
