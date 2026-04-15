#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const root_1 = require("./commands/root");
(0, root_1.execute)(process.argv.slice(2));
