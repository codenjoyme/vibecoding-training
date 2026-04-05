# Security Guidelines — SKILL.md

## Purpose
Security-first development practices to prevent common vulnerabilities (OWASP Top 10).

## Always Check
- No hardcoded credentials, API keys, or secrets in source code
- User input validated and sanitized at all system boundaries
- SQL queries use parameterized statements (no string concatenation)
- Authentication tokens have appropriate expiry
- Sensitive data not logged

## Dependency Management
- Scan dependencies for CVEs before adding new packages
- Pin dependency versions in lock files
- Keep dependencies updated (monthly review)

## Code Review Security Gate
Block merge if any of the above are violated.
