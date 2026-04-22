# Module 2b: Installing `Claude Code` via `Codemie` (Optional)

### Background
What if you could bring one of the most capable AI models — `Anthropic`'s `Claude` — directly into your `VS Code` workflow without switching tools? This module covers two tools that make it possible: `Codemie`, a CLI tool that handles corporate authentication for `Claude`, and `Claude Code`, a `VS Code` extension that brings `Claude`-powered AI assistance directly into the editor.

`Claude Code` is `Anthropic`'s answer to AI-assisted development. Compared to `Cursor` (a standalone AI-native IDE) and `GitHub Copilot` (tightly integrated with the `Microsoft`/`OpenAI` stack), `Claude Code` sits inside your existing `VS Code` as an extension — using `Anthropic`'s `Claude` family of models known for nuanced reasoning, long-context understanding, and strong code generation. `Codemie` complements it by managing corporate `SSO` authentication so developers never deal with raw `API` keys.

This module is optional. If you are satisfied with your `VS Code` + `GitHub Copilot` setup from `Module 1`, you may skip ahead. If you work in an organization that provides a managed `Claude` account, or if you want a second AI assistant with a different reasoning style, both tools are worth adding.

**Learning objectives.** Upon completion of this module, you will be able to:
- Install the `Codemie` CLI tool and configure it with your corporate `Claude` account.
- Install the `Claude Code` extension in `VS Code`.
- Use `Claude Code` features — chat, code generation, and inline suggestions — inside `VS Code`.
- Explain the positioning of `Claude Code` / `Codemie` relative to `GitHub Copilot` and `Cursor`.

## Page 1: What Are `Codemie` and `Claude Code`?
### Background
Before installing anything, it is important to understand that `Codemie` and `Claude Code` are **two separate tools** — not two names for the same thing.

**`Codemie`** is a CLI adapter. It is installed as an `npm` package and runs in your terminal. Its job is to authenticate your corporate `Claude` account and route requests from your local machine to `Anthropic`'s `Claude` models. Think of it as the authentication and networking layer — it makes `Claude` available from the command line and manages your corporate `SSO` session so you never handle raw `API` keys.

**`Claude Code`** is `Anthropic`'s official `VS Code` extension. It brings a `Claude`-powered AI chat panel, inline code suggestions, and agent-mode interactions directly into the editor — without opening a terminal or switching tools. You install it from the `VS Code` Marketplace just like any other extension.

In a typical corporate setup, both are used together: `Codemie` handles the authentication layer in the terminal, and the `Claude Code` extension surfaces the AI capabilities inside `VS Code`. For purely terminal-based workflows, `Codemie` alone is sufficient. For editor-integrated AI assistance, the `Claude Code` extension is the right tool.

`Anthropic` built `Claude` with a focus on safety, nuanced instruction-following, and an unusually large context window — meaning it can hold more of your codebase in memory at once compared to earlier-generation models. For developers working on large or unfamiliar codebases, this makes a real practical difference.

### ✅ Result
You understand the difference between `Codemie` (terminal adapter, authentication layer) and `Claude Code` (VS Code extension, editor integration) and why both are useful.

## Page 2: Install `Node.js` and `Codemie` CLI
### Background
The `Claude Code` extension relies on `Codemie` being present and authenticated, so installing the CLI first is the correct starting point.

`Codemie` requires `Node.js` — a JavaScript runtime that includes `npm` (Node Package Manager). You will install `Node.js` directly from the `VS Code` integrated terminal, then use `npm` to install `Codemie`. Keeping everything in one window avoids switching between tools and reinforces the habit of using the terminal inside `VS Code`.

### Steps
1. Open `VS Code` (installed in `Module 1`).
2. Go to `View` > `Terminal` to open the integrated terminal.
3. Install `Node.js` using the package manager for your operating system:
   - **`Windows`** (using `winget`, built into `Windows 10`/`11`):
     ```
     winget install OpenJS.NodeJS.LTS
     ```
   - **`macOS`** (using `Homebrew`):
     ```
     brew install node
     ```
   - **`Linux`** (`Ubuntu`/`Debian`):
     ```
     sudo apt update && sudo apt install nodejs npm
     ```
4. After installation completes, **close and reopen the integrated terminal** so the new `Node.js` path is picked up.
5. Verify `Node.js` is installed:
   ```
   node --version
   ```
   You should see a version number (e.g., `v22.x.x`).
6. Verify `npm` is available:
   ```
   npm --version
   ```
7. Now install `Codemie` globally:
   ```
   npm install -g @codemieai/code
   ```
8. Verify the `Codemie` installation:
   ```
   codemie --version
   ```
   You should see a version number printed in the terminal (e.g., `1.x.x`).

### ✅ Result
`Node.js` and the `Codemie` CLI are installed. The `codemie` command responds in the `VS Code` integrated terminal.

## Page 3: Install the `Claude Code` Extension in `VS Code`
### Background
With the CLI in place, the next step is to bring `Claude Code` into `VS Code` directly. `Anthropic` publishes an official `Claude Code` extension for `VS Code` that provides an inline AI chat panel, code suggestions, and agent-mode interactions — all powered by `Claude` models.

Installing the extension is the same as installing any `VS Code` extension: find it in the Marketplace, click Install.

### Steps
1. Open `VS Code`.
2. Click the `Extensions` icon in the Activity Bar.
3. In the search box, type `Claude Code`.
4. Look for the extension published by `Anthropic`.
5. Click the `Install` button.
6. Wait for installation to complete.

### ✅ Result
The `Claude Code` extension is installed in `VS Code` and visible in the Activity Bar or Extensions panel.

## Page 4: Configure `Codemie` with a Corporate `Claude` Account
### Background
`Codemie` acts as an adapter between `VS Code`/the CLI and `Anthropic`'s `Claude` models. In a corporate setup, instead of using a personal `API` key, your organization provides access through a managed `Claude` account. `Codemie` handles the authentication handshake so individual developers do not need to manage keys directly.

This page covers the corporate setup path. If you are using a personal `API` key instead, the steps are similar — you will enter your key in the configuration dialog rather than authenticating through the corporate portal.

### Steps (Corporate Account — Part A)
1. Open a terminal and run:
   ```
   codemie login
   ```
2. `Codemie` will open a browser window asking you to authenticate. Follow the corporate `SSO` flow provided by your organization.
3. After successful login, the terminal will confirm that you are authenticated.
4. Back in `VS Code`, open the `Claude Code` extension panel from the Activity Bar.
5. The extension should detect the authenticated session automatically.

### Steps (Personal API Key — Part B)
1. Log in to your `Anthropic` account at [https://console.anthropic.com/](https://console.anthropic.com/).
2. Navigate to `API Keys` in your account settings.
3. Create a new key and copy it.
4. In `VS Code`, open the `Claude Code` extension panel.
5. Paste the `API` key into the configuration field when prompted.

### ✅ Result
`Codemie` and the `Claude Code` extension are authenticated. The extension panel shows your account status as connected.

## Page 5: Test `Claude Code` in `VS Code`
### Background
With installation and authentication in place, it is time to verify that everything works end-to-end. You will open the same workspace used in `Module 1` and ask `Claude Code` a few questions — both practical coding requests and conceptual ones.

### Steps
1. In `VS Code`, go to `File` > `Open Folder`.
2. Navigate to `c:\workspace\hello-genai\` (`Windows`) or `~/workspace/hello-genai/` (`macOS`/`Linux`) — the workspace from `Module 1`.
3. Open the folder. If prompted about trust, click `Yes, I trust`.
4. Open the `Claude Code` chat panel from the Activity Bar.
5. Type a code generation request:
   ```
   Create a simple hello world function in Python
   ```
6. Press Enter and wait for the response. Verify that `Claude` returns a working `Python` function.
7. Ask a follow-up question to test conversational context:
   ```
   Now add a docstring to that function explaining what it does.
   ```
8. Verify: `Claude` modifies the previous code by adding a docstring — demonstrating that it holds context across turns.

### ✅ Result
`Claude Code` responds to code generation and follow-up requests inside `VS Code`. The setup is confirmed working end-to-end.

## Summary
Key takeaways:
- `Codemie` and `Claude Code` are **two separate tools**: `Codemie` is a terminal-based CLI adapter for authenticating and routing requests to `Claude`; `Claude Code` is a `VS Code` extension that surfaces `Claude` AI capabilities directly in the editor.
- `Claude Code` is `Anthropic`'s AI coding assistant known for large-context reasoning and nuanced instruction-following.
- Installation involves three steps: install `Node.js` via the `VS Code` integrated terminal, then the `npm` CLI package (`@codemieai/code`) for the `Codemie` terminal layer, and finally the `Claude Code` extension from the `VS Code` Marketplace for the editor layer.
- In corporate environments, `Codemie` handles authentication via `SSO` (`codemie login`) so individual developers never manage raw `API` keys.
- `Claude Code` complements `GitHub Copilot` rather than replacing it: different models have different strengths, and having both available broadens your toolkit.

**Useful links:**
- [`Codemie` on GitHub](https://github.com/codemie-ai/codemie-code)
- [`Anthropic` Console (API keys & account)](https://console.anthropic.com/)
- [`Node.js` download](https://nodejs.org/)

## Quiz
**Question 1.** What is the difference between `Codemie` and `Claude Code`?

A) They are two names for the same product — `Anthropic`'s `VS Code` extension.
B) `Codemie` is a terminal-based CLI adapter for authentication; `Claude Code` is the `VS Code` extension for editor-integrated AI assistance.
C) `Codemie` is `Anthropic`'s AI model; `Claude Code` is the CLI that runs it.

*Correct answer: B. `Codemie` is the CLI adapter (terminal layer) responsible for authentication and routing. `Claude Code` is the `VS Code` extension (editor layer) that surfaces AI features in the editor. Both together form the complete setup.*

---

**Question 2.** Which command installs the `Codemie` CLI globally?

A) `npm install codemie`
B) `npm install -g @codemieai/code`
C) `pip install codemie`

*Correct answer: B. The package is scoped under `@codemieai/code` and installed globally with the `-g` flag.*

---

**Question 3.** In a corporate setup, how does a developer authenticate `Codemie`?

A) By generating a personal `API` key from the `Anthropic` console and pasting it into `VS Code`.
B) By running `codemie login` which opens a browser-based corporate `SSO` flow.
C) By sharing a single `API` key stored in the team's shared drive.

*Correct answer: B. Corporate authentication uses `codemie login` + `SSO`, so individual developers never handle raw `API` keys.*
