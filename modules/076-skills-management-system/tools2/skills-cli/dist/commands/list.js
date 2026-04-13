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
exports.runList = runList;
const config = __importStar(require("../lib/config"));
const gitops = __importStar(require("../lib/gitops"));
function runList(args) {
    if (args.includes('--help') || args.includes('-h')) {
        console.log(`List all available skills in the repository.

Usage:
  skills list

Active skills (checked out in this workspace) are marked with ✅.
Other skills exist in the repo but are not part of your current groups.

`);
        return;
    }
    const cfg = config.load();
    const repoDir = config.REPO_SUB_DIR;
    let allSkills;
    try {
        allSkills = gitops.listAllSkills(repoDir);
    }
    catch (err) {
        console.error(`Error: failed to list skills: ${err}`);
        process.exit(1);
    }
    const activeSet = new Set(cfg.skills);
    console.log(`Skills repository: ${cfg.repo_url}`);
    console.log(`Groups:           ${cfg.groups.join(', ')}\n`);
    let activeCount = 0;
    for (const s of allSkills) {
        if (activeSet.has(s)) {
            console.log(`  ✅ ${s}`);
            activeCount++;
        }
        else {
            console.log(`  ○  ${s}`);
        }
    }
    console.log(`\nActive: ${activeCount}  |  Total: ${allSkills.length}`);
}
