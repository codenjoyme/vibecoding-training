# AI-Assisted Code Review - Hands-on Walkthrough

In this walkthrough, you'll review a pull request that an AI coding agent created — using AI to help you understand the changes, catch issues, and produce structured feedback. You'll also build a review instruction that makes every future review consistent.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

By the end of this walkthrough you will have:

- **An AI-powered review of a real PR** — structured feedback on a pull request from your repository, produced with AI assistance
- **A code review instruction** — `instructions/code-review.agent.md` with a repeatable review framework
- **A team review protocol** — a one-page checklist for reviewing AI-generated PRs that you can share

---

## Part 1: Understand why AI code needs review

Ask AI this question before looking at any code:

```
I delegated a coding task to a GitHub AI agent and it created a pull request.
My assumption was: if the tests pass and the CI is green, I should just merge.

What are 5 types of bugs or quality issues that:
- Would not be caught by automated tests
- Would not fail CI
- But would cause real problems in production or over time

Give me examples, not just categories.
```

Read the response. The typical problems AI introduces silently:
- **Logic is correct but fragile** — works for current inputs, breaks with edge cases not tested
- **Oversimplified error handling** — catches all exceptions with a single `except Exception: pass`
- **Hidden coupling** — function modifies a global state, breaking other code paths
- **Poor naming that obscures intent** — code is right but unreadable in 3 months
- **Hardcoded values that should be config** — limits, timeouts, URLs embedded in functions

These are what you'll look for.

---

## Part 2: Get AI to summarise the PR for you

Open a PR from your GitHub repository — ideally one created by the GitHub coding agent in module 150. Copy the full diff (all changed files with their before/after state).

Ask AI:

```
Summarise this pull request for me as if I'm the code reviewer.

1. What is the intent of this PR? (1-2 sentences, inferred from the changes)
2. What files were changed and why?
3. What are the 3 highest-risk changes — the ones most likely to cause bugs?
4. What questions should I ask the author before merging?

[paste the PR diff here]
```

Review the summary. The AI's summary often captures things you'd miss in a quick scan — especially risk areas. Use the "questions to ask the author" list as your review checklist.

---

## Part 3: Use Copilot in VS Code to review the changed file

Pull the PR branch locally:

```
git fetch origin
git checkout [branch-name]
```

Open the primary changed file in VS Code. With Copilot active, ask in the chat panel:

```
Review this file as a senior developer. Look for:
1. Logic errors — cases where the code doesn't do what the developer intended
2. Missing error handling — what happens if the API returns an error? If a file is missing?
3. Hardcoded values — numbers, strings, URLs that should be configuration
4. Performance issues — unnecessary loops, repeated database calls, blocking operations
5. Security concerns — any inputs used without validation, any credentials visible

For each issue: quote the relevant code, describe the problem, and suggest the fix.
```

Work through the findings. For each one, decide: is this a blocker, a suggestion, or a nitpick?

---

## Part 4: Find the "looks good but isn't" patterns

These are the patterns that pass all tests but are silently wrong. Ask AI:

```
Here is a function from the pull request:

[paste the most complex function from the PR]

Without running it, identify:
1. What edge case inputs would make this function behave incorrectly?
2. Does this function have any hidden side effects (modifying external state)?
3. If I call this function 100 times in parallel, would there be any race conditions?
4. What happens if the operation this function calls raises an exception midway?
```

Even if you don't understand every answer, ask AI to explain the most serious risk in plain language. "So if X happens, the result would be Y — is that what we want?"

---

## Part 5: Write structured review feedback

Now write the actual review. Don't write comments like "this is bad" or "change this." Ask AI to help you write professional, actionable feedback:

```
I'm writing a code review for this pull request. Help me phrase these findings
as professional, constructive GitHub review comments.

My findings:
1. [describe finding 1 in plain language]
2. [describe finding 2]
3. [describe finding 3]

For each finding, write a comment that:
- Quotes the relevant code on a single line (backtick format)
- Explains why it's a problem
- Suggests a specific fix or asks a specific question
- Stays respectful and collaborative in tone
```

Post the comments on the PR in GitHub. You can use "Request Changes" if there are blockers, or "Comment" for suggestions.

---

## Part 6: Build a reusable review instruction

Capture this workflow as a reusable instruction. Ask AI:

```
Create an AI agent instruction file for code review.
The instruction should guide the agent to review any pull request diff by:

1. Summarising the PR intent in 2 sentences
2. Listing the top 3 risk areas
3. Checking for: logic errors, missing error handling, hardcoded values, security issues
4. Identifying "looks good but isn't" patterns
5. Drafting 3-5 review comments in GitHub comment style (quote + explain + suggest)

Format it as a .agent.md file that I can attach in any VS Code AI chat session.
```

Save to `instructions/code-review.agent.md`.

---

## Part 7: Create a one-page team review protocol

The review process shouldn't depend on who's doing it. Ask AI to help you create a protocol:

```
Create a one-page code review protocol for a team doing AI-assisted development.
The protocol should specify:

1. What every reviewer must check in an AI-generated PR (the non-negotiable list)
2. What is optional / judgment call
3. When to approve vs. request changes vs. block a PR
4. How to distinguish "it works" from "it's correct and maintainable"
5. Maximum time a PR should sit unreviewed before escalating

Keep it to one page. Use numbered lists, not prose.
```

Review the output, adjust it for your team's context, and save it as `docs/pr-review-protocol.md`.

---

## Success Criteria

- ✅ You used AI to summarise a real PR and identify risk areas
- ✅ You found at least one "looks good but isn't" issue using the Copilot review
- ✅ You wrote at least 3 structured review comments with quote + explanation + suggestion
- ✅ `instructions/code-review.agent.md` created and saved
- ✅ `docs/pr-review-protocol.md` exists with a team-ready checklist
- ✅ You understand the distinction: automated tests catch crashes; code review catches design problems

---

## Understanding Check

1. **Why is "tests pass, CI is green" not enough to merge a PR?**
   > Automated tests only verify behaviour you expected when you wrote the tests. They don't verify code structure, readability, hidden coupling, performance under load, or behaviour in untested edge cases. A PR can be functionally correct and still be a maintenance nightmare.

2. **What is the difference between a blocker and a suggestion in code review?**
   > A blocker is something that must be fixed before the code is safe to merge — bugs, security vulnerabilities, logic errors that will cause failures. A suggestion is an improvement worth making but not urgent enough to delay the merge — naming, structure, minor optimisations. Confusing the two slows teams down without improving safety.

3. **Why does AI-generated code often have weak error handling?**
   > AI is trained to produce code that "works for the happy path." Error handling is harder to demonstrate in short examples and is often omitted in tutorial data. AI also lacks the context of what "failure modes" exist in your specific infrastructure — it doesn't know your API rate limits, your database connection timeouts, or your network reliability.

4. **What makes a good code review comment? What makes a bad one?**
   > Good: quotes the exact line, explains why it's a problem, suggests a concrete fix. Bad: vague ("this is wrong"), emotional ("this is terrible code"), commanding without explaining ("change this"). Good comments improve the author's understanding, not just the specific line.

5. **You're reviewing a PR where the AI agent added a database call inside a loop. Why is this a problem?**
   > Each iteration executes a separate database query. For 10 items this is fine. For 1000 items this is 1000+ database round trips — potentially seconds of delay or a database timeout. This is called the "N+1 query problem." The fix is to load all needed data in one query before the loop.

6. **If your team is shipping AI-generated code, why is having a review protocol more important than in traditional teams?**
   > In traditional teams, all code is written by humans who understand the codebase context. AI agents generate code that may be structurally correct but contextually wrong — it doesn't know your team conventions, your implicit constraints, or your future roadmap. Without a protocol, the same issues get caught by some reviewers but missed by others.

---

## Troubleshooting

**The PR diff is too large to paste into AI chat**
> Focus on the most changed or most critical file. Ask AI to review it first. Then do a second pass on the supporting files. You can also ask: "Given this description of the PR changes, what are the most likely problem areas to focus my review on?"

**AI summary sounds too positive — it's not finding real issues**
> Make the prompt adversarial: "You are a senior developer who is sceptical of AI-generated code. What would make you uncomfortable about this PR? What would you push back on? What would you want the author to explain?"

**I can't tell if AI's suggested fix is correct**
> Ask AI to explain the fix step by step: "Walk me through why this fix solves the problem. What would happen if we kept the original code and the edge case you described actually occurred?" If the explanation doesn't convince you, ask a more experienced developer.

**Team members are not following the review protocol**
> Add it as a PR template: `.github/PULL_REQUEST_TEMPLATE.md`. Every new PR will pre-populate with the checklist. Reviewers see the same list every time and can check items off. Consistency comes from structure, not from enforcing compliance.

---

## Next Steps

Now that you can review AI-generated PRs, the next step is to automate the quality gates:

**→ [Module 155 — CI/CD Pipeline with AI Agents](../155-cicd-pipeline-with-ai-agents/about.md)**

Combine code review (this module) with automated testing (module 132) and the full delegation loop (module 150) into a pipeline that runs on every push.
