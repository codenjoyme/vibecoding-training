# Module 11 Completion Report

## Hallucination Reframing
A hallucination is the AI filling in gaps left in your instructions — it reveals a missing or ambiguous constraint that needs to be made explicit. Each hallucination is feedback that helps you improve your instructions so the same deviation never happens again.

## Improvement Cycle
1. Run the agent using your instruction
2. Observe the output and spot deviations from expectations
3. Delegate the fix — ask the agent to update the instruction with the missing constraint
4. Verify — re-run the instruction and confirm the hallucination is gone

## Instruction Improvement
- File: create-jira-report.agent.md
- What hallucination occurred: The AI included issue descriptions in the report table, making it too long. The instruction only specified columns but did not say "no description column."
- What was fixed: Added explicit constraint: "Table columns are limited to: Issue Key, Summary, Assignee, Resolution Date. Do not include Description or any other columns."

## Updated Instruction Contents
```markdown
# Create Jira Report

- Fetch resolved issues from Jira for the current week (Monday–Friday).
- Group issues by assignee.
- Format output as a Markdown table with columns: Issue Key, Summary, Assignee, Resolution Date.
- Table columns are limited to: Issue Key, Summary, Assignee, Resolution Date. Do not include Description or any other columns.
- Include a summary line with total count of resolved issues.
- Use the Jira API token from the `.env` file — never hardcode credentials.
- If the API returns an error, retry up to 3 times with 30-second intervals.
- Output file: `reports/weekly-status.md`.
```
