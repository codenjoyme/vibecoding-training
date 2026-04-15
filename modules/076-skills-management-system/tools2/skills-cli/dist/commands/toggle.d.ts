import * as config from '../lib/config';
export declare function runEnable(args: string[]): void;
export declare function runDisable(args: string[]): void;
export declare function resolveEffectiveGroups(cfg: config.Config): string[];
export declare function applyExtraAndExcluded(resolved: string[], cfg: config.Config): string[];
