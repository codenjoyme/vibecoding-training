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
exports.runCreate = runCreate;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const config = __importStar(require("../lib/config"));
const gitops = __importStar(require("../lib/gitops"));
const SKILL_TEMPLATE = `# Skill: %NAME%

## Purpose

_Describe what this skill teaches or enables._

## Instructions

_Write the detailed instructions for the AI agent here._
`;
const INFO_TEMPLATE = `{
  "description": "This skill provides _____. It can be used for _____. The main features include _____.",
  "owner": "Your_Name@domain.com"
}
`;
function runCreate(args) {
    if (args.includes('--help') || args.includes('-h')) {
        console.log(`Create a new skill in the local instructions/ folder.

Usage:
  skills create <skill-name>

Creates:
  instructions/<skill-name>/SKILL.md   — skill instructions template
  instructions/<skill-name>/info.json  — skill metadata (description, owner)

`);
        return;
    }
    const positional = args.filter(a => !a.startsWith('--'));
    if (positional.length === 0) {
        console.error('Error: skill name is required');
        console.error('Usage: skills create <skill-name>');
        process.exit(1);
    }
    const skillName = positional[0];
    // Verify workspace is initialized
    try {
        config.load();
    }
    catch (err) {
        console.error(String(err));
        process.exit(1);
    }
    const skillDir = path.join(config.REPO_SUB_DIR, skillName);
    // Check if skill already exists
    if (fs.existsSync(skillDir)) {
        console.error(`Error: skill "${skillName}" already exists at ${skillDir}`);
        process.exit(1);
    }
    // Create skill directory
    fs.mkdirSync(skillDir, { recursive: true });
    // Write SKILL.md
    const skillPath = path.join(skillDir, 'SKILL.md');
    fs.writeFileSync(skillPath, SKILL_TEMPLATE.replace('%NAME%', skillName), 'utf8');
    // Write info.json
    const infoPath = path.join(skillDir, 'info.json');
    fs.writeFileSync(infoPath, INFO_TEMPLATE, 'utf8');
    // Add to sparse-checkout so git can track the new skill
    try {
        gitops.addToSparseCheckout(config.REPO_SUB_DIR, skillName);
    }
    catch { /* ignore — may not be a sparse repo */ }
    // Register in extra_skills so pull doesn't lose it
    const cfg = config.load();
    if (!cfg.extra_skills.includes(skillName)) {
        cfg.extra_skills.push(skillName);
        config.save(cfg);
    }
    console.log(`✅ Skill "${skillName}" created at ${skillDir}`);
    console.log(`   → ${skillPath}`);
    console.log(`   → ${infoPath}`);
    console.log('\nEdit SKILL.md with your instructions, then use `skills push` to propose it.');
}
