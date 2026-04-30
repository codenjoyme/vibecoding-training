# Jira CLI — Snapshot Tests

> ⚠️ **Security note:** This scenario file is committed to git.
> Output blocks below contain real Jira data — **review before committing**.
> The `run-tests.ps1` script loads credentials from the root `.env` via `--env-file`.
> Issue keys and Jira URL come from `JIRA_TEST_KEY` in `.env` — not hardcoded here.

---

## Phase 1: Installation & Help

Verify the CLI script is present.

> `ls /workspace/jira_cli.py`

Check Python version.

> `python --version`

Show full help menu.

> `python jira_cli.py --help`

---

## Phase 2: Search

Basic JQL search — project issues assigned to current user.
Uses `JIRA_SEARCH_JQL` from `.env` (e.g. `assignee = currentUser() AND sprint in openSprints()`).

> `python jira_cli.py search --jql "$JIRA_SEARCH_JQL" --format plain --max 5`

---

## Phase 3: Get Issue Details

Get full details of the test issue.
Uses `JIRA_TEST_KEY` from `.env`.

> `python jira_cli.py get --key "$JIRA_TEST_KEY"`

---

## Phase 4: List Comments

> `python jira_cli.py comments --key "$JIRA_TEST_KEY"`

---

## Phase 5: List Attachments

> `python jira_cli.py attachments --key "$JIRA_TEST_KEY"`

---

## Phase 6: List Transitions

> `python jira_cli.py transitions --key "$JIRA_TEST_KEY"`

---

## Phase 7: Write Operations

> ⚠️ These commands mutate Jira data. Only run with a write-scoped token.
> Set `JIRA_WRITE_PROJECT` in `.env` to control which project to create in.

Add a comment to the test issue.

> `python jira_cli.py comment --key "$JIRA_TEST_KEY" --text "Automated snapshot test — $(date)"`

Create a test issue.

> `python jira_cli.py create --project "$JIRA_WRITE_PROJECT" --summary "CLI snapshot test $(date +%F)" --type Task --description "Created by automated snapshot test"`

---

## Phase 8: Error Handling

Invalid issue key should return a clear error.

> `python jira_cli.py get --key "INVALID-00000" 2>&1 || true`

Invalid JQL should return a helpful error.

> `python jira_cli.py search --jql "project = DOESNOTEXIST12345" --max 1 2>&1 || true`
