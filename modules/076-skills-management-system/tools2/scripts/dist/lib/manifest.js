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
exports.resolveSkills = resolveSkills;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
function loadGlobal(manifestDir) {
    const file = path.join(manifestDir, '_global.json');
    if (!fs.existsSync(file))
        return null;
    const data = fs.readFileSync(file, 'utf8');
    return JSON.parse(data);
}
function loadGroup(manifestDir, name) {
    const file = path.join(manifestDir, `${name}.json`);
    if (!fs.existsSync(file)) {
        throw new Error(`manifest file not found: ${name}.json`);
    }
    const data = fs.readFileSync(file, 'utf8');
    return JSON.parse(data);
}
function resolveSkills(repoPath, groups) {
    const manifestDir = path.join(repoPath, '.manifest');
    const skillSet = new Set();
    // 1. Global skills
    const global = loadGlobal(manifestDir);
    if (global) {
        for (const s of global.skills ?? []) {
            if (s)
                skillSet.add(s);
        }
    }
    // 2. Per-group skills
    for (const group of groups) {
        const grp = loadGroup(manifestDir, group);
        for (const s of grp.skills ?? []) {
            if (s)
                skillSet.add(s);
        }
        // 3. Sub-configs
        for (const sub of grp['sub-configs'] ?? []) {
            try {
                const subGrp = loadGroup(manifestDir, sub);
                for (const s of subGrp.skills ?? []) {
                    if (s)
                        skillSet.add(s);
                }
            }
            catch {
                console.warn(`Warning: sub-config "${sub}" not found, skipping`);
            }
        }
    }
    return Array.from(skillSet).sort();
}
