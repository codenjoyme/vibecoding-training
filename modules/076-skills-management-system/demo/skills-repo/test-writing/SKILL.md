# Test Writing — SKILL.md

## Purpose
Guidelines for writing effective automated tests.

## Test Structure (AAA Pattern)
```
// Arrange — set up inputs and dependencies
// Act — call the function under test
// Assert — verify the output or side effects
```

## What to Test
- Happy path: expected inputs produce expected outputs
- Edge cases: empty input, max values, null/undefined
- Error cases: invalid input, network failure, timeout
- Integration points: external API calls, database queries

## Naming Convention
Tests should read as sentences:
- `it_returns_empty_list_when_no_users_exist`
- `throws_error_when_token_is_expired`

## Coverage Target
80% line coverage minimum; 100% for security-critical paths.
