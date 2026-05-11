# Module 10 Completion Report

## Four Stages of Prompt Maturity
1. Everything is a prompt — type the full request every time, works for one-off tasks
2. Text file — save good prompts to a file, copy-paste when needed
3. Markdown format — structured .md files with organized requirements, delegated to the agent
4. Instruction system — AI automatically sees relevant instructions, no copy-paste needed

## Instruction Files
- instructions/main.agent.md
- instructions/create-jira-report.agent.md
- instructions/update-confluence-page.agent.md

## main.agent.md Contents
```markdown
# Instructions Catalog

- `create-jira-report.agent.md` — Generate a weekly status report from Jira data following the project specification format.
  + Keywords: jira, report, status, weekly
- `update-confluence-page.agent.md` — Update a Confluence page with formatted content using the API.
  + Keywords: confluence, update, page, publish
```

## Sample Instruction
- File: create-jira-report.agent.md
- Contents:
```markdown
# Create Jira Report

- Fetch resolved issues from Jira for the current week (Monday–Friday).
- Group issues by assignee.
- Format output as a Markdown table with columns: Issue Key, Summary, Assignee, Resolution Date.
- Include a summary line with total count of resolved issues.
- Use the Jira API token from the `.env` file — never hardcode credentials.
- If the API returns an error, retry up to 3 times with 30-second intervals.
- Output file: `reports/weekly-status.md`.
```
