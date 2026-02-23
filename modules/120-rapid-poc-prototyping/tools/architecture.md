# Meta-Architecture: Full-Stack SPA with MCP Support

A blueprint for building full-stack web applications on this tech stack with spec-driven development and AI agent integration.

---

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + React Router v6 + Vite |
| Backend | Node.js ≥ 20 + Express 4 |
| Database | PostgreSQL 15 |
| Auth | Google OAuth + JWT (HTTP-only cookie) |
| AI Agent Protocol | MCP (`@modelcontextprotocol/sdk`) |
| Infrastructure | Docker + Docker Compose |
| Testing (backend) | Jest + Supertest |
| Testing (frontend) | Vitest + Testing Library |
| Dev Workflow | spec-kit (spec-driven development) |

---

## Project Structure

```
project-root/
├── backend/
│   ├── src/
│   │   ├── index.js          # entry point — starts HTTP server
│   │   ├── app.js            # Express app setup, route mounting
│   │   ├── admin/            # admin API (secret-protected)
│   │   ├── auth/             # Google OAuth + JWT
│   │   ├── mcp/              # MCP server + tools
│   │   ├── cli/              # REST alternative to MCP (optional)
│   │   ├── portal/           # end-user API
│   │   ├── download/         # file/token download
│   │   ├── db/               # pool.js + migrate.js
│   │   ├── middleware/       # shared Express middleware
│   │   └── services/         # business logic (no HTTP concern)
│   ├── migrations/           # ordered SQL files: 001-..., 002-...
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── Dockerfile            # multi-stage: builds React → serves SPA + API
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── pages/
│   │   ├── components/
│   │   ├── context/
│   │   └── services/         # API client functions
│   ├── tests/
│   └── package.json
├── specs/                    # spec-kit artifacts (see below)
├── instructions/             # AI agent instructions
│   └── main.agent.md         # entry point — links to other instruction files
├── docker-compose.yml
└── .github/
    └── copilot-instructions.md  # always points to instructions/main.agent.md
```

---

## Architectural Patterns

### 1. Single Backend, SPA Served as Static Files

The React app is built at Docker image build time (Vite bakes `VITE_*` env vars into the bundle) and placed into `backend/public/`. Express serves the static files and a catch-all `GET *` returns `index.html` for client-side routing.

In development, Vite runs on its own dev server (separate port) with a proxy to the backend.

### 2. Route Segmentation by Auth Concern

Each router module owns a single auth concern:

| Route prefix | Auth mechanism |
|-------------|---------------|
| `/admin` | `ADMIN_SECRET` env var in request header |
| `/auth` | Public (issues the JWT) |
| `/api` | JWT in HTTP-only cookie |
| `/mcp/:token` | Opaque token in URL path |
| `/download` | Short-lived one-time token |

### 3. Services Layer (no HTTP)

Business logic lives in `src/services/` and knows nothing about Express. Routers call service functions, services talk to the DB. This makes unit testing straightforward without spinning up HTTP.

### 4. SQL Migrations as Plain Files

No ORM. Migrations are numbered SQL files (`001-initial-schema.sql`, `002-...`). `db/migrate.js` runs them in order on startup, tracking applied migrations in a `migrations` table.

### 5. MCP Endpoint for AI Agent Integration

The `/mcp/:token` route implements the [Model Context Protocol](https://modelcontextprotocol.io/). Define tools in `mcp/tools/` — each tool is a function that AI agents (GitHub Copilot, Claude, etc.) can call. Auth is a unique per-user token embedded in the URL.

### 6. Two Auth Roles

- **Admin** — identified by a shared secret (`ADMIN_SECRET`). No user account needed.
- **End user** — Google OAuth → backend issues a JWT stored in an HTTP-only cookie. All `/api` routes use this.

---

## Docker Compose Services

```
postgres   → PostgreSQL 15-alpine (named volume for data)
backend    → multi-stage build: 1) build React, 2) run Node
test       → same codebase, profile "test", points to same postgres
```

The test service uses `profiles: ["test"]` so it never starts by default. Run with:
```
docker compose run --rm test
```

---

## Spec-Driven Development Workflow (spec-kit)

Features are developed spec-first. Each feature lives in its own branch and folder:

```
specs/
  001-<feature-name>/
    spec.md        ← WHAT and WHY (no tech choices here)
    plan.md        ← HOW, tech stack decisions
    data-model.md  ← DB schema
    tasks.md       ← ordered task list for implementation
    contracts/     ← API contracts
    checklists/    ← QA checklists
```

### Slash Commands (in order)

```
/speckit.constitution        ← once per project: establish principles
/speckit.specify <desc>      ← create spec.md from plain English
/speckit.clarify             ← Q&A to resolve ambiguities
/speckit.plan <tech stack>   ← generate plan.md, data-model.md
/speckit.tasks               ← generate tasks.md
/speckit.analyze             ← consistency check before coding
/speckit.implement           ← execute tasks
/speckit.checklist           ← QA validation
```

### Installation (one-time)

```powershell
# Install uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install spec-kit CLI
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Init in existing project (Windows + Copilot)
specify init --here --force --ai copilot --script ps --no-git
```

---

## AI Agent Instructions Pattern

```
.github/copilot-instructions.md   ← always just re-reads main.agent.md
instructions/
  main.agent.md                   ← catalog of all instruction files
  spec-kit.agent.md               ← spec-kit workflow
  creating-instructions.agent.md  ← how to manage instruction files
  <feature>.agent.md              ← per-feature instructions (optional)
```

The copilot-instructions file always says: *"reload `instructions/main.agent.md` every prompt"*. This makes the instruction set dynamic and evolvable.

---

## Key Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `ADMIN_SECRET` | ✅ | Protects admin API |
| `JWT_SECRET` | ✅ | Signs user session tokens |
| `GOOGLE_CLIENT_ID` | for OAuth | Google OAuth client ID |
| `BASE_URL` | | Public URL of the backend |
| `FRONTEND_URL` | | Allowed CORS origin |
| `DEV_AUTH_ENABLED` | | `true` to bypass auth locally |
