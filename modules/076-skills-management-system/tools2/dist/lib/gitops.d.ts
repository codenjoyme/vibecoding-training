export declare function clone(sourceURL: string, targetDir: string): void;
export declare function setupSparseCheckout(repoDir: string, skills: string[]): void;
export declare function defaultBranch(repoDir: string): string;
export declare function checkoutBranch(repoDir: string, branch: string): void;
export declare function pull(repoDir: string): void;
export declare function listAllSkills(repoDir: string): string[];
export declare function createBranch(repoDir: string, branchName: string): void;
export declare function stageAndCommit(repoDir: string, skillName: string): void;
export declare function push(repoDir: string, branchName: string): void;
export declare function getRemoteURL(repoDir: string): string;
export interface SkillInfo {
    description: string;
    owner: string;
}
export declare function loadSkillInfo(repoDir: string, skillName: string): SkillInfo | null;
