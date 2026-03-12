# Database Schema Design with AI - Hands-on Walkthrough

In this walkthrough, you'll design a relational database schema for your PoC project entirely through AI conversation — starting from a plain-language description of your data. You'll generate migration files, write real queries, and wire the database into your working application.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

By the end of this walkthrough you will have:

- **A SQL schema file** — `schema.sql` with properly designed tables, relationships, indexes, and constraints
- **Migration files** — `migration_001_up.sql` and `migration_001_down.sql` for safe schema deployment and rollback
- **A query library** — 3–5 queries that your PoC actually needs, generated and explained by AI
- **An integrated data layer** — your PoC reading from and writing to the database using the schema you designed

---

## Step 1: Describe your data in plain language

Open AI chat with Agent Mode enabled. Don't open any code yet — start by describing what your application needs to store.

Use this prompt structure:

```
I'm building [describe your PoC in one sentence].
I need to store the following information:

1. [Entity 1] — [describe what it is and the key fields it needs]
2. [Entity 2] — [describe what it is and the key fields it needs]
3. [Entity 3 if any]

Relationships:
- [Entity 1] can have many [Entity 2]
- [Entity 2] belongs to exactly one [Entity 1]
- [describe any other relationships]

Generate a relational SQL schema (SQLite compatible) with:
- Proper primary keys (integer auto-increment)
- Foreign keys with appropriate constraints
- Created/updated timestamps on every table
- Indexes on foreign keys and columns used in WHERE clauses
```

Read the generated schema. It will look something like:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL DEFAULT 'viewer',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_activity_log_user_id ON activity_log(user_id);
```

---

## Step 2: Review and improve the schema

Before accepting the schema, ask AI to review it:

```
Review this schema for these issues:
1. Are there any missing constraints? (NOT NULL, UNIQUE, CHECK)
2. Are there any unnecessary columns?
3. Are the data types appropriate for a production system?
4. Is anything missing that a typical [your app type] would need?
5. Any indexes I should add or remove?
```

Pay attention to:
- **Indexes** — too few means slow queries; too many means slow writes
- **Constraints** — `NOT NULL` on required fields prevents bad data from entering
- **Cascade rules** — `ON DELETE CASCADE` vs `ON DELETE SET NULL`: what should happen to a child row when the parent is deleted?

Ask follow-up questions if anything is unclear. AI can explain any design decision.

---

## Step 3: Generate migration files

**What we're about to do:** Instead of running the schema SQL directly, we'll create versioned migration files. This is how real projects manage database changes — each change gets its own file with an "undo" option.

Ask AI:

```
Convert this schema into a migration file pattern with:
- migration_001_up.sql — creates all tables (what we run to add the feature)
- migration_001_down.sql — drops all tables in reverse order (what we run to undo)

Add a comment at the top of each file:
-- Migration 001: Initial schema
-- Up: creates users, activity_log tables
-- Down: drops activity_log, users (reverse order to respect foreign keys)
```

Save both files in a `migrations/` folder inside your project:

**Windows:** `c:/workspace/hello-genai/migrations/`  
**macOS/Linux:** `~/workspace/hello-genai/migrations/`

Run the up migration to create your tables:

```
sqlite3 ./app.db < migrations/migration_001_up.sql
```

**What just happened:** SQLite created a database file `app.db` and created your tables inside it. You can verify with:

```
sqlite3 ./app.db ".tables"
```

You should see your table names listed.

---

## Step 4: Generate queries your PoC needs

Now ask AI to write the actual queries your application will use. Be specific:

```
Write SQL queries for these operations in my application:
1. Insert a new user (accepts email, role)
2. Find a user by email
3. Insert an activity log entry (accepts user_id, action)
4. Get the last 10 activity log entries for a user, newest first
5. Count how many actions each user has taken, sorted by most active

Use SQLite syntax. For each query, explain what it does and when to use it.
```

Review each query. Ask AI to explain any JOIN, subquery, or aggregate function you don't understand before moving on.

Save these queries as comments in a `queries.sql` file — your reference library.

---

## Step 5: Integrate the database into your PoC

**What we're about to do:** Add a simple database connection layer to your existing PoC application so it reads from and writes to the SQLite database you just designed.

Ask AI to generate the integration code for your language:

```
My PoC is written in [Python/Node.js/other].
I have a SQLite database at ./app.db with these tables: [list your tables].

Generate a simple database module that:
1. Opens a connection to ./app.db
2. Has functions for each operation I need: [list the 5 operations from Step 4]
3. Handles connection closing properly
4. Returns data as dictionaries (Python) / plain objects (JavaScript)

Show the complete code for the module and an example of how to call it.
```

Replace any existing hardcoded test data in your PoC with calls to the new database module. Run the application and verify it reads from and writes to the database.

Test by:
1. Creating a record through your application
2. Querying it back
3. Checking `sqlite3 ./app.db "SELECT * FROM [your table];"` to see the raw data

---

## Step 6: Add one schema evolution

**What good schema design looks like in practice:** requirements change. Let's simulate a real evolution — add one new field or table to your schema.

Ask AI:

```
I need to add [describe a new field or small table].
Generate:
1. migration_002_up.sql — adds the new element
2. migration_002_down.sql — removes it (rollback)
3. Updated queries that use the new field
```

Run the migration:
```
sqlite3 ./app.db < migrations/migration_002_up.sql
```

Verify the change with:
```
sqlite3 ./app.db ".schema [tablename]"
```

**What just happened:** You've practised the real migration workflow. Every future schema change follows this same pattern: write up + down, run up, verify, commit.

---

## Success Criteria

- ✅ You described your data model in plain language and AI generated a valid SQL schema
- ✅ The schema has proper constraints (NOT NULL, UNIQUE, foreign keys, indexes)
- ✅ `migrations/migration_001_up.sql` and `migration_001_down.sql` exist and are runnable
- ✅ Running the up migration creates the tables in SQLite without errors
- ✅ You have 3–5 queries in `queries.sql` with explanations
- ✅ Your PoC reads from and writes to the database using the integration module
- ✅ You added and applied a second migration (migration_002)

---

## Understanding Check

1. **Why generate a "down" migration for every "up" migration?**
   > If a deployment fails, or if a feature is reverted, you need to undo the schema change without manually writing SQL in production. The down migration is the pre-built undo button, tested in advance.

2. **What does `ON DELETE CASCADE` mean on a foreign key? When should you use it instead of `ON DELETE SET NULL`?**
   > Cascade deletes all child rows when the parent is deleted. Use it when child rows have no meaning without the parent (activity logs without a user → delete them). Use SET NULL when child rows should survive but lose the reference (e.g., articles where the author account is deleted — keep the articles but set author_id to null).

3. **Why do we add an index on a foreign key column?**
   > Queries that join on a foreign key (e.g., "all activity for user_id = 42") scan the entire table without an index. An index makes this lookup fast regardless of table size. Without it, performance degrades as data grows.

4. **What is the difference between `NOT NULL` and a `DEFAULT` value?**
   > `NOT NULL` means the column must have a value — the insert fails if it's missing. `DEFAULT` provides a fallback value when nothing is specified. You can have both: `role TEXT NOT NULL DEFAULT 'viewer'` — the column is required (not null), but if you don't provide it, it gets 'viewer' automatically.

5. **Why use AUTOINCREMENT integer primary keys instead of UUIDs?**
   > For SQLite-based prototypes, integers are faster, smaller, and simpler to work with in queries and debug. UUIDs become valuable in distributed systems where multiple databases must generate unique IDs independently. At PoC stage, integers are the right choice.

6. **If a new team member asks "what does our database look like?", how do they find out without access to the production server?**
   > They run the up migrations locally in sequence. The migration files are the single source of truth for the database structure — they version-controlled, reviewable, and reproducible. This is why we commit migrations to Git.

7. **What should you do before running a migration that changes an existing table in production?**
   > Back up the database first. Test the migration on a copy of production data. Have the down migration ready. Schedule it during low-traffic time. Announce to the team. Some teams also run a dry-run plan with `EXPLAIN` queries to estimate impact.

---

## Troubleshooting

**"no such table" error after running the migration**
> Check you ran the up migration against the correct database file. Verify: `sqlite3 ./app.db ".tables"`. Make sure you're connecting to `./app.db` (relative path) from the right working directory.

**Foreign key constraints are not being enforced in SQLite**
> SQLite disables foreign key enforcement by default for backwards compatibility. Run `PRAGMA foreign_keys = ON;` at the start of every connection, or add it to your database initialization code.

**AI generated Postgres-specific SQL but I'm using SQLite**
> Common differences: PostgreSQL uses `SERIAL` for auto-increment; SQLite uses `INTEGER PRIMARY KEY AUTOINCREMENT`. PostgreSQL uses `SERIAL`/`BIGSERIAL`; JSON columns; array types — none of these exist in SQLite. Ask: "Rewrite this for SQLite compatibility."

**Down migration fails with "table doesn't exist"**
> SQLite requires you to drop tables in reverse order of creation (because of foreign key dependencies). The down migration must drop child tables before parent tables. Ask AI: "Fix the drop order in this down migration — child tables must be dropped before parent tables."

**Integration code is connecting but data is not persisting between restarts**
> Check that you're connecting to a file path (`./app.db`), not `:memory:`. An in-memory SQLite database is wiped on every restart — it's useful for tests but not for persistent storage.

---

## Next Steps

Your PoC now has a real data layer. The next step is to add automated QA so you know it keeps working:

**→ [Module 130 — QA with Chrome DevTools MCP](../130-chrome-devtools-mcp-qa-emulation/about.md)**

With a database behind your application, browser-level QA testing becomes much more meaningful — you can verify that user actions actually persist.
