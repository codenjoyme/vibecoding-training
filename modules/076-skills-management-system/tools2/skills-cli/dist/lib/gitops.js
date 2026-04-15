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
exports.clone = clone;
exports.setupSparseCheckout = setupSparseCheckout;
exports.defaultBranch = defaultBranch;
exports.checkoutBranch = checkoutBranch;
exports.pull = pull;
exports.listAllSkills = listAllSkills;
exports.createBranch = createBranch;
exports.stageAndCommit = stageAndCommit;
exports.push = push;
exports.getRemoteURL = getRemoteURL;
exports.loadSkillInfo = loadSkillInfo;
const child_process_1 = require("child_process");
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
function run(dir, ...args) {
    const opts = { encoding: 'utf8' };
    if (dir)
        opts.cwd = dir;
    try {
        return (0, child_process_1.execFileSync)('git', args, opts).trim();
    }
    catch (err) {
        const e = err;
        const msg = (e.stderr?.toString() || e.stdout?.toString() || e.message || String(err)).trim();
        throw new Error(`git ${args.join(' ')}: ${msg}`);
    }
}
function clone(sourceURL, targetDir) {
    fs.mkdirSync(path.dirname(targetDir), { recursive: true });
    run(null, 'clone', sourceURL, targetDir);
}
function setupSparseCheckout(repoDir, skills) {
    run(repoDir, 'sparse-checkout', 'init', '--cone');
    run(repoDir, 'sparse-checkout', 'set', '.manifest', ...skills);
}
function defaultBranch(repoDir) {
    try {
        const out = run(repoDir, 'symbolic-ref', '--short', 'refs/remotes/origin/HEAD');
        const parts = out.split('/');
        if (parts.length >= 2)
            return parts[parts.length - 1];
    }
    catch {
        // fall through
    }
    return 'master';
}
function checkoutBranch(repoDir, branch) {
    run(repoDir, 'checkout', branch);
}
function pull(repoDir) {
    const branch = defaultBranch(repoDir);
    checkoutBranch(repoDir, branch);
    run(repoDir, 'pull', 'origin', branch);
}
function listAllSkills(repoDir) {
    const out = run(repoDir, 'ls-tree', '--name-only', '-d', 'HEAD');
    return out
        .split('\n')
        .map(l => l.trim())
        .filter(l => l.length > 0 && !l.startsWith('.'))
        .sort();
}
function createBranch(repoDir, branchName) {
    run(repoDir, 'checkout', '-b', branchName);
}
function stageAndCommit(repoDir, skillName) {
    const skillPath = skillName.replace(/\\/g, '/') + '/';
    run(repoDir, 'add', skillPath);
    run(repoDir, 'commit', '-m', `feat(${skillName}): update skill instructions`);
}
function push(repoDir, branchName) {
    run(repoDir, 'push', 'origin', branchName);
    const branch = defaultBranch(repoDir);
    try {
        checkoutBranch(repoDir, branch);
    }
    catch { /* ignore */ }
}
function getRemoteURL(repoDir) {
    return run(repoDir, 'remote', 'get-url', 'origin');
}
function loadSkillInfo(repoDir, skillName) {
    const infoPath = path.join(repoDir, skillName, 'info.json');
    if (!fs.existsSync(infoPath))
        return null;
    try {
        const data = fs.readFileSync(infoPath, 'utf8');
        return JSON.parse(data);
    }
    catch {
        return null;
    }
}
