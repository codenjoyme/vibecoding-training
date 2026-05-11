# Module 08 Completion Report

## Interview Technique
The "ask me clarifying questions" pattern transforms the AI from an implementer into a requirements analyst — instead of guessing, it interviews you to extract the details you did not know you had. This works because the AI has seen thousands of similar projects and knows what information is typically needed.

## Clarifying Questions Count
8

## Technical Specification
```markdown
# Technical Specification: Weekly Status Report Automation

## Overview
Automate the creation of a weekly status report by pulling data from Jira and Confluence, formatting it into a structured document, and sending it via email to stakeholders.

## Data Sources
- Jira: issues resolved this week, issues in progress, blockers
- Confluence: pages updated this week in the team space

## Output Format
- Markdown file with sections: Summary, Completed Items, In Progress, Blockers, Confluence Updates
- Converted to PDF for email attachment

## Recipients
- Direct manager (weekly, every Friday 5 PM)
- Team channel (Slack webhook, same schedule)

## Authentication
- Jira API token (stored in .env file)
- Confluence API token (stored in .env file)

## Constraints
- Report covers Monday–Friday of the current week
- Maximum 2 pages in PDF format
- No sensitive data (customer names redacted)

## Edge Cases
- If no issues were resolved, show "No items completed this week"
- If API is unreachable, retry 3 times with 30-second intervals, then send error notification
```
