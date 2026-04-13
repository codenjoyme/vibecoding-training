export declare const CONFIG_FILE = "instructions/.manifest/config.json";
export declare const REPO_SUB_DIR = "instructions";
export interface Config {
    repo_url: string;
    groups: string[];
    skills: string[];
}
export declare function load(): Config;
export declare function save(cfg: Config): void;
export declare function repoPath(): string;
