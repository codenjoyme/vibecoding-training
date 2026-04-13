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
exports.runPull = runPull;
const config = __importStar(require("../lib/config"));
const gitops = __importStar(require("../lib/gitops"));
function runPull(args) {
    if (args.includes('--help') || args.includes('-h')) {
        console.log(`Update local skills from the remote repository.

Usage:
  skills pull

`);
        return;
    }
    try {
        config.load();
    }
    catch (err) {
        console.error(String(err));
        process.exit(1);
    }
    console.log('→ Pulling latest skills ...');
    try {
        gitops.pull(config.REPO_SUB_DIR);
    }
    catch (err) {
        console.error(`Error: pull failed: ${err}`);
        process.exit(1);
    }
    console.log('✅ Skills updated successfully');
}
