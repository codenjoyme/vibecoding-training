# Skills CLI — Comprehensive Test Checklist

## Test Environment

- **Go binary**: `tools/scripts/skills.exe`
- **Node.js entry**: `tools2/scripts/dist/index.js`
- **Demo setup**: `demo/setup.ps1` → copies `demo/skills-repo/` to `work/076-task/skills-repo/`
- **Test workspace**: `work/076-task/go/` and `work/076-task/node/`

---

## 1. Help & Unknown Commands

| # | Test | Go | Node.js |
|---|------|:--:|:-------:|
| 1.1 | `skills help` — shows all commands | ✅ | ✅ |
| 1.2 | `skills --help` — same as help | ✅ | ✅ |
| 1.3 | `skills` (no args) — same as help | ✅ | ✅ |
| 1.4 | `skills unknown-cmd` — error + help | ✅ | ✅ |

## 2. Init (fresh)

| # | Test | Go | Node.js |
|---|------|:--:|:-------:|
| 2.1 | `skills init --repo ../skills-repo --groups project-alpha` — clones, resolves, sparse checkout | ✅ | ✅ |
| 2.2 | Verify `skills.json` created at project root | ✅ | ✅ |
| 2.3 | Verify `instructions/` created with correct skills | ✅ | ✅ |
| 2.4 | Verify `test-writing` NOT present (only in project-beta) | ✅ | ✅ |
| 2.5 | `skills init --repo ../skills-repo --groups project-alpha` again — "already initialized" error | ✅ | ✅ |
| 2.6 | `skills init --repo ../skills-repo --groups project-alpha,security` — multiple groups | ✅ | ✅ |
| 2.7 | `skills init --repo nonexistent --groups x` — error for bad repo | ✅ | ✅ |
| 2.8 | `skills init --repo ../skills-repo` — error: no groups | ✅ | ✅ |
| 2.9 | `skills init --help` — shows init help | ✅ | ✅ |

## 3. Init (re-init from existing config)

| # | Test | Go | Node.js |
|---|------|:--:|:-------:|
| 3.1 | After fresh init, `skills init` (no args) — re-resolves from skills.json | ✅ | ✅ |
| 3.2 | `skills init` with no skills.json — error | ✅ | ✅ |

## 4. Pull

| # | Test | Go | Node.js |
|---|------|:--:|:-------:|
| 4.1 | `skills pull` — pulls latest from repo | ✅ | ✅ |
| 4.2 | `skills pull` without init — error (no config) | ✅ | ✅ |
| 4.3 | `skills pull --help` — shows pull help | ✅ | ✅ |

## 5. Push

| # | Test | Go | Node.js |
|---|------|:--:|:-------:|
| 5.1 | Edit a SKILL.md, `skills push code-review-base` — creates branch, commits, pushes | ✅ | ✅ |
| 5.2 | `skills push nonexistent-skill` — error | ✅ | ✅ |
| 5.3 | `skills push` without skill name — error | ✅ | ✅ |
| 5.4 | `skills push --help` — shows push help | ✅ | ✅ |

## 6. List

| # | Test | Go | Node.js |
|---|------|:--:|:-------:|
| 6.1 | `skills list` — shows skill names with ✅/○ | ✅ | ✅ |
| 6.2 | `skills list --verbose` — shows description/owner | ✅ | ✅ |
| 6.3 | `skills list --json` — valid JSON array output | ✅ | ✅ |
| 6.4 | `skills list --verbose --json` — JSON takes priority or both work | ✅ | ✅ |
| 6.5 | `skills list` without init — error | ✅ | ✅ |
| 6.6 | `skills list --help` — shows list help | ✅ | ✅ |

## 7. Create

| # | Test | Go | Node.js |
|---|------|:--:|:-------:|
| 7.1 | `skills create my-new-skill` — creates SKILL.md + info.json | ✅ | ✅ |
| 7.2 | Verify SKILL.md content is a template | ✅ | ✅ |
| 7.3 | Verify info.json is pretty-printed with description + owner | ✅ | ✅ |
| 7.4 | `skills create my-new-skill` again — "already exists" error | ✅ | ✅ |
| 7.5 | `skills create` without name — error | ✅ | ✅ |
| 7.6 | `skills create --help` — shows create help | ✅ | ✅ |
| 7.7 | `skills create test` without init — error | ✅ | ✅ |

## 8. Enable/Disable Group

| # | Test | Go | Node.js |
|---|------|:--:|:-------:|
| 8.1 | `skills enable group security` — adds to extra_groups, re-resolves | ✅ | ✅ |
| 8.2 | Verify skills.json updated with extra_groups | ✅ | ✅ |
| 8.3 | `skills enable group security` again — "already enabled" message | ✅ | ✅ |
| 8.4 | `skills disable group security` — removes from extra_groups | ✅ | ✅ |
| 8.5 | `skills disable group security` again — "not enabled" message | ✅ | ✅ |
| 8.6 | `skills enable group` without name — error | ✅ | ✅ |
| 8.7 | `skills disable group` without name — error | ✅ | ✅ |

## 9. Enable/Disable Skill

| # | Test | Go | Node.js |
|---|------|:--:|:-------:|
| 9.1 | `skills enable test-writing` — adds to extra_skills | ✅ | ✅ |
| 9.2 | Verify skills.json updated with extra_skills | ✅ | ✅ |
| 9.3 | `skills enable test-writing` again — "already" message | ✅ | ✅ |
| 9.4 | `skills disable style-guidelines` — adds to excluded_skills | ✅ | ✅ |
| 9.5 | Verify skills.json updated with excluded_skills | ✅ | ✅ |
| 9.6 | `skills disable style-guidelines` again — "already excluded" message | ✅ | ✅ |
| 9.7 | `skills enable` without name — error | ✅ | ✅ |
| 9.8 | `skills disable` without name — error | ✅ | ✅ |
| 9.9 | Enable a skill that was previously excluded — removes from excluded | ✅ | ✅ |

## 10. AI-Help

| # | Test | Go | Node.js |
|---|------|:--:|:-------:|
| 10.1 | `skills ai-help` — outputs CLI reference | ✅ | ✅ |
| 10.2 | Output contains all commands | ✅ | ✅ |

## 11. Init-Repo

| # | Test | Go | Node.js |
|---|------|:--:|:-------:|
| 11.1 | `skills init-repo test-repo` — creates folder with full structure | ✅ | ✅ |
| 11.2 | Verify `.manifest/_global.json` with 3 skills | ✅ | ✅ |
| 11.3 | Verify `.manifest/group-1.json` and `sub-group.json` exist | ✅ | ✅ |
| 11.4 | Verify `creating-instructions/SKILL.md` + `info.json` | ✅ | ✅ |
| 11.5 | Verify `iterative-prompting/SKILL.md` + `info.json` | ✅ | ✅ |
| 11.6 | Verify `skills-cli/SKILL.md` + `info.json` | ✅ | ✅ |
| 11.7 | Verify `.gitignore` exists | ✅ | ✅ |
| 11.8 | All JSON files are pretty-printed (2-space indent) | ✅ | ✅ |
| 11.9 | `skills init-repo test-repo` again — "already exists" error | ✅ | ✅ |
| 11.10 | `skills init-repo` without name — error | ✅ | ✅ |
| 11.11 | `skills init-repo --help` — shows help | ✅ | ✅ |

## 12. End-to-End Workflow

| # | Test | Go | Node.js |
|---|------|:--:|:-------:|
| 12.1 | Full flow: init → list → create → push → pull → enable → disable | ✅ | ✅ |
| 12.2 | Init project-beta → verify different skill set than alpha | ✅ | ✅ |

---

## Summary

| Section | Total | Go Pass | Go Fail | Node Pass | Node Fail |
|---------|-------|---------|---------|-----------|-----------|
| 1. Help | 4 | 4 | 0 | 4 | 0 |
| 2. Init fresh | 9 | 9 | 0 | 9 | 0 |
| 3. Init re-init | 2 | 2 | 0 | 2 | 0 |
| 4. Pull | 3 | 3 | 0 | 3 | 0 |
| 5. Push | 4 | 4 | 0 | 4 | 0 |
| 6. List | 6 | 6 | 0 | 6 | 0 |
| 7. Create | 7 | 7 | 0 | 7 | 0 |
| 8. Enable/Disable Group | 7 | 7 | 0 | 7 | 0 |
| 9. Enable/Disable Skill | 9 | 9 | 0 | 9 | 0 |
| 10. AI-Help | 2 | 2 | 0 | 2 | 0 |
| 11. Init-Repo | 11 | 11 | 0 | 11 | 0 |
| 12. E2E Workflow | 2 | 2 | 0 | 2 | 0 |
| **TOTAL** | **66** | **66** | **0** | **66** | **0** |
