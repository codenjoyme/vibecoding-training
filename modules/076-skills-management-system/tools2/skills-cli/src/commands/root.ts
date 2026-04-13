import { runInit } from './init';
import { runPull } from './pull';
import { runPush } from './push';
import { runList } from './list';
import { printHelp } from './help';

export function execute(args: string[]): void {
  if (args.length === 0 || args[0] === 'help' || args[0] === '--help' || args[0] === '-h') {
    printHelp();
    return;
  }

  switch (args[0]) {
    case 'init':
      runInit(args.slice(1));
      break;
    case 'pull':
      runPull(args.slice(1));
      break;
    case 'push':
      runPush(args.slice(1));
      break;
    case 'list':
      runList(args.slice(1));
      break;
    default:
      console.error(`Error: unknown command "${args[0]}"\n`);
      printHelp();
      process.exit(1);
  }
}
