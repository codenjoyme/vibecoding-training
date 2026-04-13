#!/usr/bin/env node

import { execute } from './commands/root';

execute(process.argv.slice(2));
