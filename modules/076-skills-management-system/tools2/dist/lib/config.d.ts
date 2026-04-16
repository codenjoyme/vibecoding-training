export declare const CONFIG_FILE = "skills.json";
export declare const REPO_SUB_DIR = "instructions";
export interface Config {
    repo_url: string;
    groups: string[];
    extra_skills: string[];
    excluded_skills: string[];
}
export declare function load(): Config;
export declare function save(cfg: Config): void;
export declare function repoPath(): string;
