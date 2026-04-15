"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.execute = execute;
const init_1 = require("./init");
const pull_1 = require("./pull");
const push_1 = require("./push");
const list_1 = require("./list");
const create_1 = require("./create");
const help_1 = require("./help");
function execute(args) {
    if (args.length === 0 || args[0] === 'help' || args[0] === '--help' || args[0] === '-h') {
        (0, help_1.printHelp)();
        return;
    }
    switch (args[0]) {
        case 'init':
            (0, init_1.runInit)(args.slice(1));
            break;
        case 'pull':
            (0, pull_1.runPull)(args.slice(1));
            break;
        case 'push':
            (0, push_1.runPush)(args.slice(1));
            break;
        case 'list':
            (0, list_1.runList)(args.slice(1));
            break;
        case 'create':
            (0, create_1.runCreate)(args.slice(1));
            break;
        default:
            console.error(`Error: unknown command "${args[0]}"\n`);
            (0, help_1.printHelp)();
            process.exit(1);
    }
}
