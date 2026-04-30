# Jira CLI — Snapshot Tests

> **Note:** Output blocks below use placeholder names, ticket keys, and URLs.
> Real values come from `.env` at runtime — nothing sensitive is hardcoded here.
> The `run-tests.ps1` script loads credentials from the root `.env` via `--env-file`.

---

## Phase 1: Installation & Help

Verify the CLI script is present.

> `ls /workspace/jira_cli.py`
```
/workspace/jira_cli.py
```

Check Python version.

> `python --version`
```
Python 3.12.13
```

Show full help menu.

> `python jira_cli.py --help`
```
usage: jira_cli.py [-h]
                   {search,get,attachments,download,comments,transitions,create,comment,upload,transition,update}
                   ...

Jira CLI — read and write issues, comments, attachments

positional arguments:
  {search,get,attachments,download,comments,transitions,create,comment,upload,transition,update}
    search              Search issues with JQL
    get                 Get issue details
    attachments         List attachments on an issue
    download            Download an attachment
    comments            List comments on an issue
    transitions         List available status transitions
    create              Create a new issue
    comment             Add a comment to an issue
    upload              Upload a file as attachment
    transition          Move issue to a new status
    update              Update issue fields

options:
  -h, --help            show this help message and exit

READ commands:
  search       Search issues with JQL
  get          Get full issue details
  attachments  List attachments on an issue
  download     Download an attachment to disk
  comments     List comments on an issue
  transitions  List available status transitions

WRITE commands (require write-scoped token):
  create       Create a new issue
  comment      Add a comment to an issue
  upload       Upload a file as an attachment
  transition   Move issue to a new status (use transitions to find IDs)
  update       Update summary, priority, or labels
```

---

## Phase 2: Search

Basic JQL search — project issues assigned to current user.
Uses `JIRA_SEARCH_JQL` from `.env` (e.g. `assignee = currentUser() AND sprint in openSprints()`).

> `python jira_cli.py search --jql "$JIRA_SEARCH_JQL" --format plain --max 5`
```
PROJECT-1001: Fix login page styling
PROJECT-1002: Update API documentation
PROJECT-1003: Refactor auth module
PROJECT-1004: Add unit tests for utils
PROJECT-1005: Deploy to staging
```

---

## Phase 3: Get Issue Details

Get full details of the test issue.
Uses `JIRA_TEST_KEY` from `.env`.

> `python jira_cli.py get --key "$JIRA_TEST_KEY"`
```
Key         : PROJECT-1000
Summary     : Implement PDF attachment workflow
Status      : To do
Assignee    : Stiven Pupkin
Reporter    : Jane Smith
Priority    : Low
Created     : 2025-01-15
Updated     : 2025-03-20
Labels      : -
Comments    : 3

Description:
Implement a workflow for processing PDF attachments. See the attached sample-document.pdf for details.
```

---

## Phase 4: List Comments

> `python jira_cli.py comments --key "$JIRA_TEST_KEY"`
```
[2025-03-20] Jane Smith:
  Reviewed the PDF — looks good, proceeding with implementation.

[2025-03-21] Stiven Pupkin:
  Started work, see branch feature/PROJECT-1000.

[2025-03-22] Jane Smith:
  Approved the approach in the design doc.
```

---

## Phase 5: List Attachments

> `python jira_cli.py attachments --key "$JIRA_TEST_KEY"`
```
FILENAME              TYPE             SIZE         
--------------------  ---------------  -------------
sample-document.pdf   application/pdf  81,926 bytes 
diagram-01.png        image/png        172,924 bytes
diagram-02.png        image/png        200,010 bytes
diagram-03.png        image/png        207,144 bytes
```

---

## Phase 6: List Transitions

> `python jira_cli.py transitions --key "$JIRA_TEST_KEY"`
```
ID  NAME          
--  --------------
11  Start Progress
21  Done          
```

---

## Phase 7: Write Operations

> ⚠️ These commands mutate Jira data. Only run with a write-scoped token.
> Set `JIRA_WRITE_PROJECT` in `.env` to control which project to create in.

Add a comment to the test issue.

> `python jira_cli.py comment --key "$JIRA_TEST_KEY" --text "Automated snapshot test — $(date)"`
```
Comment added (id=XXXXXXXX) to PROJECT-1000
```

Create a test issue.

> `python jira_cli.py create --project "$JIRA_WRITE_PROJECT" --summary "CLI snapshot test $(date +%F)" --type Task --description "Created by automated snapshot test"`
```
Created: PROJECT-1010
Link: https://your-jira.example.com/browse/PROJECT-1010
```

---

## Phase 8: Error Handling

Invalid issue key should return a clear error.

> `python jira_cli.py get --key "INVALID-00000" 2>&1 || true`
```
ERROR: 404 — Issue Does Not Exist
```

Invalid JQL should return a helpful error.

> `python jira_cli.py search --jql "project = DOESNOTEXIST12345" --max 1 2>&1 || true`
```
ERROR: 400 — The value 'DOESNOTEXIST12345' does not exist for the field 'project'.
```
