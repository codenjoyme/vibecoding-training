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
exports.runPush = runPush;
const config = __importStar(require("../lib/config"));
const gitops = __importStar(require("../lib/gitops"));
function runPush(args) {
    if (args.includes('--help') || args.includes('-h')) {
        console.log(`Create a branch, commit local changes to a skill, and push for review.

Usage:
  skills push <skill-name>

The command will:
  1. Create branch: feature/<skill-name>-update
  2. Stage all changes in instructions/<skill-name>/
  3. Commit with a conventional commit message
  4. Push the branch to origin
  5. Print the Pull Request URL (for GitHub/GitLab remotes)

`);
        return;
    }
    const positional = args.filter(a => !a.startsWith('--'));
    if (positional.length === 0) {
        console.error('Error: skill name is required');
        console.error('Usage: skills push <skill-name>');
        process.exit(1);
    }
    const skillName = positional[0];
    const branchName = `feature/${skillName}-update`;
    const cfg = config.load();
    const repoDir = config.REPO_SUB_DIR;
    console.log(`→ Creating branch ${branchName} ...`);
    try {
        gitops.createBranch(repoDir, branchName);
    }
    catch (err) {
        console.error(`Error: failed to create branch: ${err}`);
        console.error(`Tip: if the branch already exists, delete it with:`);
        console.error(`     git -C instructions branch -D ${branchName}`);
        process.exit(1);
    }
    console.log('  ✓ Branch created');
    console.log(`→ Staging and committing changes in ${skillName}/ ...`);
    try {
        gitops.stageAndCommit(repoDir, skillName);
    }
    catch (err) {
        console.error(`Error: commit failed: ${err}`);
        console.error(`Tip: make sure you have changes to commit in instructions/${skillName}/`);
        // Return to default branch before exiting so workspace is not left on a feature branch
        try {
            gitops.checkoutBranch(repoDir, gitops.defaultBranch(repoDir));
        }
        catch { /* ignore */ }
        process.exit(1);
    }
    console.log('  ✓ Changes committed');
    console.log(`→ Pushing branch ${branchName} ...`);
    try {
        gitops.push(repoDir, branchName);
    }
    catch (err) {
        console.error(`Error: push failed: ${err}`);
        process.exit(1);
    }
    console.log('  ✓ Branch pushed');
    // Build PR URL hint for GitHub/GitLab
    let prUrl = '';
    try {
        const remoteURL = gitops.getRemoteURL(repoDir);
        const normalized = remoteURL.replace(/\.git$/, '').replace('git@github.com:', 'https://github.com/');
        if (normalized.includes('github.com')) {
            prUrl = `${normalized}/compare/${branchName}?expand=1`;
        }
        else if (normalized.includes('gitlab.com')) {
            prUrl = `${normalized}/-/merge_requests/new?merge_request%5Bsource_branch%5D=${branchName}`;
        }
    }
    catch { /* ignore */ }
    console.log(`\n✅ Skill "${skillName}" pushed for review`);
    console.log(`   Branch: ${branchName}`);
    if (prUrl)
        console.log(`   Open PR: ${prUrl}`);
    void cfg; // suppress unused warning
}
