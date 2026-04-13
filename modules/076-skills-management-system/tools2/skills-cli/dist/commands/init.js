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
exports.runInit = runInit;
const fs = __importStar(require("fs"));
const config = __importStar(require("../lib/config"));
const gitops = __importStar(require("../lib/gitops"));
const manifest = __importStar(require("../lib/manifest"));
function parseArgs(args) {
    if (args.includes('--help') || args.includes('-h')) {
        printInitHelp();
        process.exit(0);
    }
    let repo = '';
    const groups = [];
    let i = 0;
    while (i < args.length) {
        if (args[i] === '--repo' && i + 1 < args.length) {
            repo = args[++i];
        }
        else if (args[i] === '--groups' && i + 1 < args.length) {
            for (const g of args[++i].split(',')) {
                const t = g.trim();
                if (t)
                    groups.push(t);
            }
        }
        else if (!args[i].startsWith('--')) {
            // positional arg treated as group name
            groups.push(args[i]);
        }
        i++;
    }
    return { repo, groups };
}
function printInitHelp() {
    console.log(`Initialize skills workspace from a central repository.

Clones the skills repository, resolves skills for the specified groups,
and applies sparse checkout so only the needed skills are present.

Usage:
  skills init --repo <url-or-path> [--groups <group1>[,<group2>...]] [group...]

Flags:
  --repo    URL or local path to the central skills repository (required)
  --groups  Groups to initialize (comma-separated or repeated flag; positional args also accepted)

Examples:
  skills init --repo https://github.com/org/skills --groups backend
  skills init --repo ../skills-repo --groups backend,security
  skills init --repo ../skills-repo backend security
`);
}
function runInit(args) {
    const { repo, groups } = parseArgs(args);
    if (!repo) {
        console.error('Error: --repo is required');
        printInitHelp();
        process.exit(1);
    }
    if (groups.length === 0) {
        console.error('Error: specify at least one group (use --groups flag or positional args)');
        printInitHelp();
        process.exit(1);
    }
    // Check already initialized
    if (fs.existsSync(config.CONFIG_FILE)) {
        console.error('Error: workspace already initialized (instructions/.manifest/config.json exists)');
        console.error('Run `skills pull` to update, or delete instructions/ to re-initialize.');
        process.exit(1);
    }
    console.log(`→ Cloning skills repo from ${repo} ...`);
    try {
        gitops.clone(repo, config.REPO_SUB_DIR);
    }
    catch (err) {
        console.error(`Error: clone failed: ${err}`);
        process.exit(1);
    }
    console.log('  ✓ Cloned');
    console.log(`→ Resolving skills for groups: ${groups.join(', ')} ...`);
    let skills;
    try {
        skills = manifest.resolveSkills(config.REPO_SUB_DIR, groups);
    }
    catch (err) {
        console.error(`Error: manifest resolution failed: ${err}`);
        process.exit(1);
    }
    console.log(`  ✓ Resolved ${skills.length} skill(s): ${skills.join(', ')}`);
    console.log('→ Applying sparse checkout ...');
    try {
        gitops.setupSparseCheckout(config.REPO_SUB_DIR, skills);
    }
    catch (err) {
        console.error(`Error: sparse checkout failed: ${err}`);
        process.exit(1);
    }
    console.log('  ✓ Sparse checkout applied');
    const cfg = { repo_url: repo, groups, skills };
    config.save(cfg);
    console.log('\n✅ Skills workspace initialized!');
    console.log(`   Repository: ${repo}`);
    console.log(`   Groups:     ${groups.join(', ')}`);
    console.log(`   Skills:     ${skills.join(', ')}`);
    console.log('   Location:   instructions/\n');
    console.log('Your AI agent can now read skills from instructions/<skill-name>/SKILL.md');
}
