# Test Plan: Skills CLI — Module 076

**Module:** `076-skills-management-system`
**Tool:** `skills` CLI (Go binary)
**Test workspace:** `work/076-task/`
**Date:** 2026-04-05

---

## Test Workspace Layout

```
work/076-task/
├── skills-repo/          ← central skills Git repository (local, bare-compatible)
│   ├── .manifest/
│   │   ├── _global.json
│   │   ├── _agents.json
│   │   ├── project-alpha.json
│   │   ├── project-beta.json
│   │   └── security.json
│   ├── code-review-base/
│   ├── security-guidelines/
│   ├── style-guidelines/
│   ├── test-writing/
│   ├── creating-instructions/  ← global skill
│   └── iterative-prompting/    ← global skill
├── project-alpha/        ← workspace for Project Alpha
└── project-beta/         ← workspace for Project Beta
```

**Group assignments:**
- `_global.json`: `creating-instructions`, `iterative-prompting`
- `project-alpha.json`: `code-review-base`, `style-guidelines`, `security-guidelines` + sub-config `security`
- `project-beta.json`: `code-review-base`, `test-writing`
- `security.json` (sub-config): `security-guidelines`

**Overlap:** both projects include `code-review-base` + both global skills.

---

## TC-001: Happy Path — Init single group

**Command:**
```bash
cd work/076-task/project-alpha
skills init --repo ../skills-repo --groups project-alpha
```

**Expected:**
- `.skills/repo/` cloned from `../skills-repo`
- Sparse checkout applied: `.manifest`, `code-review-base`, `style-guidelines`, `security-guidelines`, `creating-instructions`, `iterative-prompting` present locally
- `test-writing` directory NOT present locally (not in project-alpha groups)
- `.skills/config.json` created with correct `repo_url`, `groups`, `skills`
- Exit code 0, success message printed

---

## TC-002: Happy Path — Init multiple groups

**Command:**
```bash
cd work/076-task/project-alpha
# (first delete .skills/ from TC-001)
skills init --repo ../skills-repo --groups project-alpha,security
```

**Expected:**
- Skills from both `project-alpha.json` and `security.json` resolved (union)
- No duplicates in the resolved skill list
- `.skills/config.json` lists both groups

---

## TC-003: Happy Path — Pull updates

**Setup:** Modify a skill file in `skills-repo` and commit.

**Command:**
```bash
cd work/076-task/project-alpha
skills pull
```

**Expected:**
- `git pull` runs successfully in `.skills/repo/`
- Updated file visible in `.skills/repo/<skill-name>/SKILL.md`
- Exit code 0

---

## TC-004: Happy Path — List skills

**Command:**
```bash
cd work/076-task/project-alpha
skills list
```

**Expected:**
- All skill directories from the repo listed (using `git ls-tree`)
- Active skills (in project-alpha groups) marked with ✅
- Inactive skills (e.g., `test-writing`) marked with ○
- Counts shown: `Active: N | Total: M`

---

## TC-005: Happy Path — Push skill change

**Setup:** Edit `.skills/repo/code-review-base/SKILL.md` in project-alpha workspace.

**Command:**
```bash
cd work/076-task/project-alpha
skills push code-review-base
```

**Expected:**
- Branch `feature/code-review-base-update` created in `.skills/repo`
- Changes staged and committed
- Branch pushed to origin (`../skills-repo`)
- Success message printed
- For local repo: "local repository — request a review" message (no PR URL generated)

**Verify:**
```bash
cd work/076-task/skills-repo
git branch
# should show: feature/code-review-base-update
```

---

## TC-006: Help command

**Commands:**
```bash
skills help
skills --help
skills -h
skills         # no args
```

**Expected:**
- Help text shown with all commands listed
- `skills eval` shown as `(coming soon)`
- Exit code 0

---

## TC-007: Eval command (coming soon)

**Command:**
```bash
skills eval code-review-base
```

**Expected:**
- "coming soon" message printed
- Exit code 0 (not an error state)

---

## TC-008: Sparse checkout verification

**After TC-001:**

**Expected directory state:**
```
.skills/repo/
├── .manifest/       ✅ present (always included)
├── code-review-base/ ✅ present
├── style-guidelines/ ✅ present
├── security-guidelines/ ✅ present
├── creating-instructions/ ✅ present
├── iterative-prompting/ ✅ present
└── test-writing/    ❌ NOT present (not in project-alpha)
```

**Verify:**
```bash
ls work/076-task/project-alpha/.skills/repo/
# test-writing should NOT appear
```

---

## TC-009: Global skills always included

**Setup:** Init project-beta which doesn't explicitly list global skills.

**Command:**
```bash
cd work/076-task/project-beta
skills init --repo ../skills-repo --groups project-beta
```

**Expected:**
- `creating-instructions` and `iterative-prompting` present locally (from `_global.json`)
- `code-review-base` and `test-writing` present (from `project-beta.json`)
- `style-guidelines` and `security-guidelines` NOT present (not in project-beta groups)

---

## TC-010: Error — Init when already initialized

**Command (after TC-001):**
```bash
cd work/076-task/project-alpha
skills init --repo ../skills-repo --groups project-alpha
```

**Expected:**
- Error message: "workspace already initialized (.skills/repo exists)"
- Hint: "Run `skills pull` to update, or delete .skills/ to re-initialize"
- Exit code 1
- No changes to existing workspace

---

## TC-011: Error — Init with non-existent group

**Command:**
```bash
skills init --repo ../skills-repo --groups non-existent-group
```

**Expected:**
- Clone succeeds
- Error on manifest resolution: `group "non-existent-group": manifest not found`
- Exit code 1
- `.skills/` directory cleaned up (or left in partial state — document behavior)

---

## TC-012: Init without `_global.json`

**Setup:** Temporarily remove `_global.json` from skills-repo.

**Command:**
```bash
skills init --repo ../skills-repo --groups project-alpha
```

**Expected:**
- No crash — global skill loading failure is silently skipped
- Only project-alpha specific skills resolved
- Warning or silent fallback (document behavior)

---

## TC-013: Error — Pull/push/list without init

**Commands (in clean directory):**
```bash
mkdir /tmp/new-project && cd /tmp/new-project
skills pull
skills push code-review-base
skills list
```

**Expected:**
- Error: "not a skills workspace — run `skills init` first"
- Exit code 1 for all three commands

---

## TC-014: Error — Push with no changes

**Setup:** No modifications to skill files since last commit.

**Command:**
```bash
skills push code-review-base
```

**Expected:**
- Branch created
- `git commit` returns "nothing to commit"
- Graceful error (not panic), clear message
- Exit code 1

---

## TC-015: Error — Init with invalid repo path

**Command:**
```bash
skills init --repo /nonexistent/path --groups project-alpha
```

**Expected:**
- Clone fails with clear error: "clone failed: ..."
- Exit code 1
- No `.skills/` directory created

---

## TC-016: Two independent project workspaces

**Setup:** project-alpha and project-beta both initialized from same skills-repo.

**Verify:**
- `project-alpha/.skills/repo/` has alpha skills + globals, NOT `test-writing`
- `project-beta/.skills/repo/` has beta skills + globals, NOT `style-guidelines`
- Changes in one workspace don't affect the other

---

## TC-017: Sub-config resolution

**Context:** `project-alpha.json` references `security` sub-config.

**Verify after TC-001:**
- `security.json` sub-config skills (`security-guidelines`) included in resolved skills
- Same as if listed directly in `project-alpha.json`

---

## TC-018: Missing sub-config (graceful warning)

**Setup:** Add reference to non-existent sub-config in `project-alpha.json`:
```json
{ "skills": ["code-review-base"], "sub-configs": ["nonexistent"] }
```

**Command:**
```bash
skills init --repo ../skills-repo --groups project-alpha
```

**Expected:**
- Warning printed: "Warning: sub-config "nonexistent" not found, skipping"
- Initialization continues with available skills
- Exit code 0

---

## TC-019: Init with `--repo` pointing to remote URL (optional, requires network)

**Command:**
```bash
skills init --repo https://github.com/example/skills-repo --groups backend
```

**Expected:**
- Clones from GitHub (network required)
- Same behavior as local repo after clone

---

## Expected Test Results Summary

| TC | Scenario | Expected Result |
|---|---|---|
| TC-001 | Init single group | ✅ Pass |
| TC-002 | Init multiple groups | ✅ Pass |
| TC-003 | Pull updates | ✅ Pass |
| TC-004 | List skills | ✅ Pass |
| TC-005 | Push skill change | ✅ Pass |
| TC-006 | Help command | ✅ Pass |
| TC-007 | Eval (coming soon) | ✅ Pass |
| TC-008 | Sparse checkout verification | ✅ Pass |
| TC-009 | Global skills included | ✅ Pass |
| TC-010 | Double init error | ✅ Pass |
| TC-011 | Non-existent group | ✅ Pass |
| TC-012 | Missing _global.json | ✅ Pass |
| TC-013 | Pull/push/list without init | ✅ Pass |
| TC-014 | Push with no changes | ✅ Pass |
| TC-015 | Invalid repo path | ✅ Pass |
| TC-016 | Two independent workspaces | ✅ Pass |
| TC-017 | Sub-config resolution | ✅ Pass |
| TC-018 | Missing sub-config warning | ✅ Pass |
| TC-019 | Remote URL (optional) | 🔲 Optional |
