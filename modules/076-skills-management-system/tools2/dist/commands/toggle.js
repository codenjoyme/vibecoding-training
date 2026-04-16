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
exports.runEnable = runEnable;
exports.runDisable = runDisable;
exports.resolveEffectiveGroups = resolveEffectiveGroups;
exports.applyExtraAndExcluded = applyExtraAndExcluded;
const config = __importStar(require("../lib/config"));
const gitops = __importStar(require("../lib/gitops"));
const manifest = __importStar(require("../lib/manifest"));
function runEnable(args) {
    if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
        printEnableHelp();
        return;
    }
    if (args[0] === 'group') {
        if (args.length < 2) {
            console.error('Error: group name is required');
            console.error('Usage: skills enable group <group-name>');
            process.exit(1);
        }
        enableGroup(args[1]);
    }
    else {
        enableSkill(args[0]);
    }
}
function runDisable(args) {
    if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
        printDisableHelp();
        return;
    }
    const force = args.includes('--force');
    const filtered = args.filter(a => a !== '--force');
    if (filtered[0] === 'group') {
        if (filtered.length < 2) {
            console.error('Error: group name is required');
            console.error('Usage: skills disable group <group-name>');
            process.exit(1);
        }
        disableGroup(filtered[1], force);
    }
    else {
        disableSkill(filtered[0], force);
    }
}
function enableGroup(name) {
    let cfg;
    try {
        cfg = config.load();
    }
    catch (err) {
        console.error(String(err));
        process.exit(1);
    }
    if (cfg.groups.includes(name)) {
        console.error(`Group "${name}" is already enabled`);
        process.exit(1);
    }
    cfg.groups = [...cfg.groups, name];
    config.save(cfg);
    console.log(`✅ Group "${name}" enabled`);
    reapplySparseCheckout(cfg);
}
function disableGroup(name, force) {
    let cfg;
    try {
        cfg = config.load();
    }
    catch (err) {
        console.error(String(err));
        process.exit(1);
    }
    let found = false;
    cfg.groups = cfg.groups.filter(g => { if (g === name) {
        found = true;
        return false;
    } return true; });
    if (!found) {
        console.error(`Group "${name}" is not currently enabled`);
        process.exit(1);
    }
    // Check for uncommitted changes in skills that will be removed
    if (!force) {
        const before = resolveAllSkills(cfgWithGroups(cfg, [...cfg.groups, name]));
        const after = resolveAllSkills(cfg);
        const removing = before.filter(s => !after.includes(s));
        const dirty = removing.filter(s => gitops.hasUncommittedChanges(config.REPO_SUB_DIR, s));
        if (dirty.length > 0) {
            // Restore groups since we haven't saved yet
            console.error(`Error: cannot disable group "${name}" - uncommitted changes in: ${dirty.join(', ')}`);
            console.error('Commit or discard your changes first, or use --force to override.');
            process.exit(1);
        }
    }
    config.save(cfg);
    console.log(`✅ Group "${name}" disabled`);
    reapplySparseCheckout(cfg);
}
function enableSkill(name) {
    let cfg;
    try {
        cfg = config.load();
    }
    catch (err) {
        console.error(String(err));
        process.exit(1);
    }
    // If it was excluded, remove from exclusion
    const excluded = cfg.excluded_skills ?? [];
    if (excluded.includes(name)) {
        cfg.excluded_skills = excluded.filter(s => s !== name);
        config.save(cfg);
        console.log(`✅ Skill "${name}" re-enabled (removed from exclusion list)`);
        reapplySparseCheckout(cfg);
        return;
    }
    if ((cfg.extra_skills ?? []).includes(name)) {
        console.error(`Skill "${name}" is already enabled`);
        process.exit(1);
    }
    cfg.extra_skills = [...(cfg.extra_skills ?? []), name];
    config.save(cfg);
    console.log(`✅ Skill "${name}" enabled`);
    reapplySparseCheckout(cfg);
}
function disableSkill(name, force) {
    let cfg;
    try {
        cfg = config.load();
    }
    catch (err) {
        console.error(String(err));
        process.exit(1);
    }
    // Check for uncommitted changes before disabling
    if (!force && gitops.hasUncommittedChanges(config.REPO_SUB_DIR, name)) {
        console.error(`Error: cannot disable skill "${name}" - uncommitted local changes detected`);
        console.error('Commit or discard your changes first, or use --force to override.');
        process.exit(1);
    }
    // Remove from extra_skills if present
    cfg.extra_skills = (cfg.extra_skills ?? []).filter(s => s !== name);
    if ((cfg.excluded_skills ?? []).includes(name)) {
        console.error(`Skill "${name}" is already disabled`);
        process.exit(1);
    }
    cfg.excluded_skills = [...(cfg.excluded_skills ?? []), name];
    config.save(cfg);
    console.log(`✅ Skill "${name}" disabled`);
    reapplySparseCheckout(cfg);
}
function printEnableHelp() {
    console.log(`Enable a group or individual skill in this workspace.

Usage:
  skills enable group <group-name>   Add a group to the workspace
  skills enable <skill-name>         Add an individual skill

Sparse checkout is re-applied automatically after enabling.

Examples:
  skills enable group security
  skills enable my-custom-skill
`);
}
function printDisableHelp() {
    console.log(`Disable a group or individual skill in this workspace.

Usage:
  skills disable group <group-name>   Remove a group from the workspace
  skills disable <skill-name>         Exclude an individual skill

Flags:
  --force   Force disable even if there are uncommitted local changes

If the skill has uncommitted local changes, the command will refuse
to disable it. Use --force to override this check.

Sparse checkout is re-applied automatically after disabling.

Examples:
  skills disable group security
  skills disable security-guidelines
  skills disable security-guidelines --force
`);
}
function resolveEffectiveGroups(cfg) {
    const seen = new Set();
    const groups = [];
    for (const g of cfg.groups) {
        if (!seen.has(g)) {
            groups.push(g);
            seen.add(g);
        }
    }
    return groups;
}
function applyExtraAndExcluded(resolved, cfg) {
    const skillSet = new Set(resolved);
    for (const s of cfg.extra_skills ?? [])
        skillSet.add(s);
    for (const s of cfg.excluded_skills ?? [])
        skillSet.delete(s);
    return Array.from(skillSet).sort();
}
function resolveAllSkills(cfg) {
    const groups = resolveEffectiveGroups(cfg);
    let skills;
    try {
        skills = manifest.resolveSkills(config.REPO_SUB_DIR, groups);
    }
    catch {
        skills = [];
    }
    return applyExtraAndExcluded(skills, cfg);
}
function cfgWithGroups(cfg, groups) {
    return { ...cfg, groups };
}
function reapplySparseCheckout(cfg) {
    const skills = resolveAllSkills(cfg);
    console.log(`→ Applying sparse checkout (${skills.length} skill(s)) ...`);
    try {
        gitops.setupSparseCheckout(config.REPO_SUB_DIR, skills);
        console.log('  ✓ Sparse checkout applied');
    }
    catch (err) {
        console.error(`Warning: sparse checkout failed: ${err}`);
        console.error('Run `skills init` to re-apply manually.');
    }
}
