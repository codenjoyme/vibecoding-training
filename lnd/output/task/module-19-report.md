# Module 19 Completion Report

## GitHub Issue
- URL: https://github.com/jane-dev/book-library/issues/8
- Title: Add input validation to POST /books endpoint
- Description: The POST /books endpoint currently accepts any payload without validation. Add checks for required fields (title, author), year range (1000–current year), and ISBN format. Return 400 with descriptive error messages for invalid input.

## Pull Request
- URL: https://github.com/jane-dev/book-library/pull/9
- PR Number: #9
- Status: Merged

## Delegated Task
I delegated the input validation task because it had a clear, well-scoped specification in the issue body — exact fields to validate, expected error format, and edge cases. This made it ideal for the coding agent since there was minimal ambiguity. The agent could read the issue, implement the validation logic, add tests, and open a PR without back-and-forth.

## Outcome Assessment
- Agent completed correctly: Partially
- What you reviewed or adjusted: The agent correctly added validation for title, author, and year range, but the ISBN format check used a simple length check instead of a proper ISBN-10/ISBN-13 regex. I added a comment on the PR requesting the fix, and the agent updated the validation in a follow-up commit. After the fix, I approved and merged.
