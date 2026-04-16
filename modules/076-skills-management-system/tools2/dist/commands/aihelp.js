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
exports.runAIHelp = runAIHelp;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
function runAIHelp() {
    // Try to find SKILL-CLI.md relative to the script
    const candidates = [
        path.join(__dirname, '..', '..', 'SKILL-CLI.md'), // from dist/commands/
        path.join(__dirname, '..', 'SKILL-CLI.md'),
    ];
    for (const p of candidates) {
        if (fs.existsSync(p)) {
            console.log(fs.readFileSync(p, 'utf8'));
            return;
        }
    }
    // Fallback inline
    console.log(FALLBACK);
}
const FALLBACK = `# Skills CLI - Quick Reference for AI Agents

Skills CLI manages shared AI instruction files ("skills") across teams.
Each skill is a folder with SKILL.md (instructions for the AI agent) and info.json (metadata).
Skills live in a central Git repository and are distributed to project workspaces via sparse checkout.

## Commands

skills init --repo <url|path> --groups <g1>[,<g2>...]
  Initialize workspace: clone repo, resolve skills for groups, apply sparse checkout.
  --repo (required): Git URL or local path to the central skills repository.
  --groups (optional): comma-separated group names. Also accepts positional args.
  If skills.json exists and no flags given, re-runs resolution from existing config.

skills pull
  Pull latest changes from the remote skills repository.

skills push <skill-name>
  Create branch feature/<skill-name>-update, commit changes, push, print PR URL.

skills list [--verbose] [--json]
  List all skills. Active marked with checkmark. --verbose adds description/owner. --json outputs JSON.

skills create <skill-name>
  Create new skill folder with template SKILL.md and info.json.

skills enable group <name>     Add group to groups array in skills.json.
skills enable <skill-name>     Add skill to extra_skills (or remove from excluded_skills).
skills disable [--force] group <name>    Remove group from groups array.
skills disable [--force] <skill-name>    Add skill to excluded_skills.

skills init-repo <folder>      Scaffold a new skills repository with example structure.
skills ai-help                 Show this reference.
skills help                    Show general help.

Enable/disable re-apply sparse checkout automatically.
Disable refuses if uncommitted changes exist; use --force to override (changes are stashed).

## Config: skills.json

{
  "repo_url": "../skills-repo",
  "groups": ["project-alpha"],
  "extra_skills": [],
  "excluded_skills": []
}

Fields:
  repo_url         - path or URL to central skills repository
  groups           - active groups for this workspace
  extra_skills     - individual skills added outside of groups
  excluded_skills  - skills to exclude even if in groups or global

Active skills are resolved dynamically from manifests. Use "skills list" to see them.

## Skill Resolution Priority

1. _global.json skills (included for everyone)
2. Group manifest skills (<group>.json + sub-configs, resolved recursively)
3. extra_skills (individual additions)
4. excluded_skills (removals applied last, overrides everything above)

## Workspace Layout

my-project/
  skills.json           <- workspace config
  instructions/         <- cloned skills repo (sparse checkout)
    .manifest/          <- group/global manifest JSON files
    skill-name/
      SKILL.md          <- instructions for AI agent
      info.json         <- metadata (description, owner)

## Typical Workflow

skills init --repo git@github.com:org/skills.git --groups backend
skills list --verbose
# edit instructions/code-review-base/SKILL.md
skills push code-review-base
skills pull
skills enable group security
skills init
`;
