# AI for Data Analysis & Reporting - Hands-on Walkthrough

In this walkthrough, you'll take a real CSV file, ask AI to analyse it as if it were your data analyst, generate charts, and produce a written report — all through conversation and AI-generated code. No prior data science experience required.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

By the end of this walkthrough you will have:

- **An AI-powered analysis session** — insights, summaries, and anomalies from a real dataset extracted through AI conversation
- **A generated chart** — a matplotlib visualisation of your data saved as an image file
- **A written report** — a Markdown report with executive summary, key findings, and recommendations, written by AI from your data
- **A reusable `analyse.py` script** — runs on any CSV file and outputs analysis + report automatically

---

## Part 1: Start with raw conversation — no code yet

**What we're about to do:** Experience how powerful AI is as an analyst even before writing any code, by pasting data directly into chat.

If you don't have a CSV file on hand, use this sample sprint data:

```
sprint,story_points_planned,story_points_completed,bugs_opened,bugs_closed,team_size
Sprint 1,45,38,5,3,6
Sprint 2,50,49,8,7,6
Sprint 3,55,41,12,5,7
Sprint 4,60,55,9,9,7
Sprint 5,60,60,6,11,7
Sprint 6,65,52,15,8,8
```

Open AI chat with Agent Mode enabled. Paste the data and ask:

```
Here is sprint data from my team for the last 6 sprints.
Without writing any code, answer these questions:
1. Is the team improving or declining in velocity? What's the trend?
2. What concerns you about the bug data?
3. Which sprint was the worst and why?
4. If I'm a VP asking "is the team on track?", what's your one-sentence answer?
```

Read the analysis. This is the baseline — pure AI reasoning on raw data. The answers you get in 30 seconds would have taken 30 minutes to extract manually from a spreadsheet.

---

## Part 2: Ask for structured analysis

**What we're about to do:** Go deeper — ask AI to compute specific metrics and group the data in ways that reveal patterns.

In the same chat, continue:

```
Now give me structured analysis:
1. Calculate the average completion rate (completed/planned) per sprint
2. Calculate the bug injection rate (bugs_opened / story_points_completed) per sprint — is it getting worse?
3. What is the team's average velocity when team size = 6 vs team size = 7?
4. If the current trend continues, what will story points completed be in Sprint 7?

Show your calculations step by step, not just the results.
```

This converts you from "data consumer" to "analyst with a data assistant."

---

## Part 3: Generate a visualisation

**What we're about to do:** Ask AI to write a Python script that creates a chart from your data.

```
Write a Python script that:
1. Reads this data from a CSV file called sprint_data.csv:
   [paste the same data as column headers + rows]
2. Creates a two-panel matplotlib figure:
   - Left panel: bar chart of story_points_planned vs story_points_completed per sprint
   - Right panel: line chart of bugs_opened and bugs_closed per sprint
3. Adds a title, legend, and labels to each panel
4. Saves the figure as sprint_report.png
5. Prints "Chart saved to sprint_report.png" when done

Use only matplotlib and pandas. No seaborn or other libraries.
```

Save the data as `sprint_data.csv`, save the script as `generate_chart.py`, run it:

**Windows:** `python c:/workspace/hello-genai/generate_chart.py`  
**macOS/Linux:** `python ~/workspace/hello-genai/generate_chart.py`

Open `sprint_report.png`. Verify the chart matches the data.

**What just happened:** You described a chart in natural language and got runnable code. This eliminates the "how do I do a grouped bar chart in matplotlib?" search-and-iteration loop.

---

## Part 4: Generate a written report

**What we're about to do:** Ask AI to write an executive-level summary report from the raw data — with conclusions, not just numbers.

```
Based on all the analysis above, write a sprint performance report for my team.

The report should be in Markdown format and include:
1. Executive Summary (3 sentences: what's happening, what's the risk, what's the recommendation)
2. Key Metrics Table (sprint, velocity, completion rate, bug rate)
3. Trends Section (2-3 paragraphs: velocity trend, quality trend, team growth impact)
4. Concerns Section (bullet points: what needs immediate attention)
5. Recommendations (3 specific, actionable items)
6. Next Steps (what data to track next sprint to validate the recommendations)

Write it for a VP who will spend 2 minutes reading it, not an engineer who will spend 20.
```

Save the output as `sprint-report.md`. This is a deliverable-quality document produced in under a minute.

---

## Part 5: Build the reusable analysis script

**What we're about to do:** Combine everything into a single Python script that runs on any CSV file and produces both the chart and the report automatically.

Ask AI:

```
Build a Python script called analyse.py that:

1. Accepts a CSV file path as a command-line argument: python analyse.py data.csv
2. Reads the file with pandas and performs:
   a. Basic statistics: row count, column names, missing values per column, numeric column summary (mean, min, max, std)
   b. Detects the date/time column if one exists and shows data range
3. Generates a correlation matrix for all numeric columns and saves it as correlation.png
4. Calls an LLM (via LangChain, API key from .env) with:
   - The first 50 rows as a string
   - Prompt: "You are a data analyst. Analyse this dataset and write a 3-paragraph summary report with: what the data represents, key observations, and 2 actionable recommendations. Be specific about numbers."
5. Saves the LLM's report as report.md
6. Prints: "Analysis complete. See report.md and correlation.png"

Use pandas, matplotlib, and langchain. Handle: file not found, empty CSV, no numeric columns.
```

Test it with your sprint data:

```
python analyse.py sprint_data.csv
```

Verify `report.md` and `correlation.png` are generated. You now have a one-command analysis tool for any CSV.

---

## Part 6: Apply to a real team dataset

Use the `analyse.py` script on a real dataset from your work:
- Jira CSV export (sprint report, backlog, bug tracker)
- GitHub Issues export
- Test results from your CI pipeline
- Any Google Sheets export

Run the script. Read the report. Compare AI's findings to what you already knew. Note: where did AI surface something you hadn't noticed? That's the value.

---

## Success Criteria

- ✅ AI answered 4 analytical questions about raw CSV data in natural language (no code)
- ✅ AI computed sprint metrics including completion rate and bug injection rate
- ✅ `generate_chart.py` produces `sprint_report.png` with two data panels
- ✅ `sprint-report.md` contains an executive summary, metrics table, and recommendations
- ✅ `analyse.py` runs on any CSV file and outputs `report.md` + `correlation.png`
- ✅ You ran the script on a real team dataset and read the AI-generated report
- ✅ You identified at least one insight from the AI report you hadn't noticed before

---

## Understanding Check

1. **Why is pasting data directly into AI chat (Step 1) useful even when you have Python tools?**
   > For quick, one-off questions about a dataset, setting up a script is slower than conversation. If you need "what's the trend in this data?", a 30-second chat answer beats a 5-minute coding session. Use code when you need to repeat the analysis, share it, or apply it to new files. Use conversation for exploration.

2. **What is the risk of asking AI to interpret data it wasn't given? How did Step 1 avoid this?**
   > AI will hallucinate plausible-sounding insights from data it hasn't seen. Step 1 avoids this by pasting the actual data into the prompt. The AI can only reference what's in its context window — no data means no real analysis, just statistics about how teams "typically" perform, which may not apply to yours.

3. **Why ask AI for the "bug injection rate" (bugs/story_points) rather than just bug count?**
   > Raw bug count is misleading — a team completing 60 story points with 6 bugs is outperforming a team completing 20 story points with 3 bugs. Normalising by output (bugs per story point) measures quality relative to throughput. AI can calculate this on request, but you have to know to ask — which is the manager's analytical responsibility.

4. **What is the limitation of the `analyse.py` script when the LLM writes the report?**
   > The LLM only sees the first 50 rows. For large datasets, important patterns in later rows are invisible. Additionally, the LLM doesn't know your business context — it can only reason from the data it sees. A report about "team performance" without knowing sprint goals, external blockers, or headcount changes may miss the real story. Always validate AI reports against your context.

5. **Your VP asks you to run this analysis every Monday and email the report. How would you automate that?**
   > Schedule `analyse.py` as a cron job (Linux/macOS) or Task Scheduler (Windows) to run Monday morning. Add a step that reads the generated `report.md` and sends it via email using Python's `smtplib` or a service like SendGrid. The script already generates the report — automation just needs to trigger it and deliver it.

---

## Troubleshooting

**AI gives generic analysis not specific to my data**
> Check that the data is actually in the prompt — not just described. Paste 20–50 rows of real data directly. If the file is too large, include a representative sample plus summary statistics at the top.

**`generate_chart.py` fails with `ModuleNotFoundError: matplotlib`**
> Install the required libraries: `pip install matplotlib pandas`. If you're in a virtual environment, make sure it's activated before running the script.

**`analyse.py` report is too generic**
> Improve the prompt in the script. Add context: "This data is from a software development sprint tracker. Column X is the team capacity, column Y is actual delivery." Providing domain context as part of the prompt significantly improves analytical quality.

**`correlation.png` shows all correlations near 1.0**
> This usually means your dataset has very few rows (less than 10). Correlation is only meaningful with more data. If your dataset is small, skip the correlation matrix and ask for a different visualisation — a simple bar chart of each metric across time is more useful.

**LLM call in `analyse.py` is slow or times out**
> Add a timeout to the LangChain client. Alternatively, use the cheaper/faster model for analysis (not Claude Sonnet 4.5 — use a faster tier like Claude Haiku) by changing the model name in the script. Fast analysis tasks rarely benefit from the most capable model.

---

## Next Steps

You've completed the Applied track. The next module handles a common need: capturing and exporting your AI work sessions for documentation and sharing.

**→ [Module 250 — Export Chat Session](../250-export-chat-session/about.md)**

Every analysis conversation you've run is valuable institutional knowledge. Learn to capture and preserve it.
