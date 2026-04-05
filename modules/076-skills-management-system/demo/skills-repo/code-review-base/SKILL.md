# Code Review Base — SKILL.md

## Purpose
Baseline code review guidelines applicable to all projects.

## Review Checklist
- [ ] Function and variable names are clear and descriptive
- [ ] No hardcoded secrets or credentials
- [ ] Error handling is explicit (no silent swallows)
- [ ] Code follows the team's style guidelines
- [ ] New functionality has corresponding tests or test plan
- [ ] No circular dependencies introduced

## Anti-patterns to Flag
- Magic numbers without named constants
- Deeply nested conditionals (prefer early return)
- Functions exceeding 50 lines (suggest splitting)
- Missing input validation at system boundaries
