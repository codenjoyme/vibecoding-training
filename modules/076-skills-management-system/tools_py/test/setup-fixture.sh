#!/usr/bin/env bash
set -e

rm -rf /workspace/skills-repo /workspace/project-repo /workspace/generated-repo
mkdir -p /workspace/skills-repo/.manifest

printf '%s\n' '{' '  "skills": ["creating-instructions"]' '}' > /workspace/skills-repo/.manifest/_global.json
printf '%s\n' '{' '  "skills": ["code-review-base", "style-guidelines"],' '  "sub-configs": ["security"]' '}' > /workspace/skills-repo/.manifest/project-alpha.json
printf '%s\n' '{' '  "skills": ["test-writing"],' '  "sub-configs": []' '}' > /workspace/skills-repo/.manifest/project-beta.json
printf '%s\n' '{' '  "skills": ["security-guidelines"],' '  "sub-configs": []' '}' > /workspace/skills-repo/.manifest/security.json

for skill in creating-instructions code-review-base style-guidelines security-guidelines test-writing; do
    mkdir -p "/workspace/skills-repo/${skill}"
    printf '# %s\n' "${skill}" > "/workspace/skills-repo/${skill}/SKILL.md"
    printf '%s\n' '{' "  \"description\": \"${skill} description.\"," '  "owner": "owner@example.com"' '}' > "/workspace/skills-repo/${skill}/info.json"
done

git -C /workspace/skills-repo init -q
git -C /workspace/skills-repo config user.email smoke-test@test.local
git -C /workspace/skills-repo config user.name "Smoke Test"
git -C /workspace/skills-repo add .
git -C /workspace/skills-repo commit -qm "init: smoke-test skills repository"
git -C /workspace/skills-repo branch -M master
