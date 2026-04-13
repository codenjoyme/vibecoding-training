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
exports.REPO_SUB_DIR = exports.CONFIG_FILE = void 0;
exports.load = load;
exports.save = save;
exports.repoPath = repoPath;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
exports.CONFIG_FILE = 'instructions/.manifest/config.json';
exports.REPO_SUB_DIR = 'instructions';
function load() {
    if (!fs.existsSync(exports.CONFIG_FILE)) {
        console.error('Error: not a skills workspace — run `skills init` first');
        process.exit(1);
    }
    try {
        const data = fs.readFileSync(exports.CONFIG_FILE, 'utf8');
        return JSON.parse(data);
    }
    catch (err) {
        console.error(`Error: corrupted config (${exports.CONFIG_FILE}):`, err);
        process.exit(1);
    }
}
function save(cfg) {
    const dir = path.dirname(exports.CONFIG_FILE);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(exports.CONFIG_FILE, JSON.stringify(cfg, null, 2), 'utf8');
}
function repoPath() {
    return exports.REPO_SUB_DIR;
}
