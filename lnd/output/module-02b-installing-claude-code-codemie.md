# Module 2b: Installing `Claude Code` via `Codemie` (Optional)

### Background
What if you could bring one of the most capable AI models — `Anthropic`'s `Claude` — directly into your `VS Code` workflow without switching tools? That is exactly what `Codemie` makes possible. It is a `VS Code` extension that integrates `Claude`-powered AI assistance into the editor you already use, adding a second strong AI voice alongside `GitHub Copilot`.

`Claude Code` is `Anthropic`'s answer to AI-assisted development. Compared to `Cursor` (which is a standalone fork of `VS Code`) and `GitHub Copilot` (which is tightly integrated with the `Microsoft`/`OpenAI` stack), `Claude Code` through `Codemie` takes a different path: it installs as an extension inside your existing `VS Code`, using `Anthropic`'s `Claude` family of models known for nuanced reasoning, long-context understanding, and strong code generation.

This module is optional. If you are satisfied with your `VS Code` + `GitHub Copilot` setup from Module 1, you may skip ahead. If you work in an organization that prefers `Anthropic`'s stack, or if you want a backup AI assistant with a different reasoning style, `Codemie` is worth adding.

**Learning objectives.** Upon completion of this module, you will be able to:
- Install the `Codemie` extension in `VS Code`.
- Configure `Codemie` with your `Claude` account or API key.
- Use `Claude Code` features — chat, code generation, and inline suggestions — inside `VS Code`.
- Explain the positioning of `Claude Code` / `Codemie` relative to `GitHub Copilot` and `Cursor`.

## Page 1: What Is `Claude Code` and `Codemie`?
### Background
Before installing anything, it helps to understand what you are actually installing and why these two names appear together. `Claude Code` is `Anthropic`'s brand for its AI coding assistant product — the intelligence layer. `Codemie` is the `VS Code` extension that delivers that intelligence into your editor — the delivery layer.

Think of the relationship the same way as `GitHub Copilot` (intelligence from `OpenAI`) delivered through the `GitHub Copilot` extension (the `VS Code` integration). Here, `Claude` is the intelligence and `Codemie` is the integration.

`Anthropic` built `Claude` with a focus on safety, nuanced instruction-following, and an unusually large context window — meaning it can hold more of your codebase in memory at once compared to earlier-generation models. For developers working on large or unfamiliar codebases, this makes a real practical difference.

### ✅ Result
You understand what `Codemie` is, how it relates to `Claude Code`, and why someone would choose it alongside or instead of `GitHub Copilot`.

## Page 2: Install `Codemie` CLI
### Background
`Codemie` is not only a `VS Code` extension — it also ships a command-line interface (CLI) tool. The CLI is the backbone that manages authentication, routes requests to `Claude` models, and can be used independently from the editor. Installing the CLI first gives you the foundation that the `VS Code` extension relies on.

You will need `Node.js` and `npm` installed on your machine. If you completed Module 1, `Node.js` is already present. If not, download it from [https://nodejs.org/](https://nodejs.org/).

### Steps
1. Open a terminal:
   - `Windows`: Open `PowerShell` or `Command Prompt`.
   - `macOS` / `Linux`: Open `Terminal`.
2. Run the global installation command:
   ```
   npm install -g @codemieai/code
   ```
3. Wait for the installation to finish. `npm` will download and install the `codemie` package globally.
4. Verify the installation succeeded by running:
   ```
   codemie --version
   ```
5. You should see a version number printed in the terminal (e.g., `1.x.x`).

### ✅ Result
The `Codemie` CLI is installed globally and responds to the `codemie` command in your terminal.

## Page 3: Install the `Claude Code` Extension in `VS Code`
### Background
With the CLI in place, the next step is to bring `Claude Code` into `VS Code` directly. `Anthropic` publishes an official `Claude Code` extension for `VS Code` that provides an inline AI chat panel, code suggestions, and agent-mode interactions — all powered by `Claude` models.

Installing the extension is the same as installing any `VS Code` extension: find it in the Marketplace, click Install.

### Steps
1. Open `VS Code`.
2. Click the `Extensions` icon in the Activity Bar (`Ctrl+Shift+X` on `Windows`/`Linux`, `Cmd+Shift+X` on `macOS`).
3. In the search box, type `Claude Code`.
4. Look for the extension published by `Anthropic`.
5. Click the `Install` button.
6. Wait for installation to complete.
7. Optionally, also search for `Codemie` and install that extension if it appears in the Marketplace — it adds additional integration hooks between the CLI and the editor.

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
With installation and authentication in place, it is time to verify that everything works end-to-end. You will open the same workspace used in Module 1 and ask `Claude Code` a few questions — both practical coding requests and conceptual ones.

### Steps
1. In `VS Code`, go to `File` > `Open Folder`.
2. Navigate to `c:\workspace\hello-genai\` (`Windows`) or `~/workspace/hello-genai/` (`macOS`/`Linux`) — the workspace from Module 1.
3. Open the folder. If prompted about trust, click `Yes, I trust`.
4. Open the `Claude Code` chat panel from the Activity Bar or via the Command Palette (`Ctrl+Shift+P` → search `Claude`).
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
- `Claude Code` is `Anthropic`'s AI coding assistant known for large-context reasoning and nuanced instruction-following.
- `Codemie` is the adapter layer — a CLI tool and `VS Code` integration — that connects `Claude` to your editor and supports corporate account authentication.
- Installation involves two steps: the `npm` CLI package (`@codemieai/code`) and the `Claude Code` `VS Code` extension.
- In corporate environments, authentication flows through `SSO` rather than individual `API` keys.
- `Claude Code` complements `GitHub Copilot` rather than replacing it: different models have different strengths, and having both available broadens your toolkit.

**Useful links:**
- [`Codemie` on GitHub](https://github.com/codemie-ai/codemie-code)
- [`Anthropic` Console (API keys & account)](https://console.anthropic.com/)
- [`Node.js` download](https://nodejs.org/)

## Quiz
**Question 1.** What is the role of `Codemie` in the `Claude Code` + `VS Code` setup?

A) It is `Anthropic`'s AI model that generates code.
B) It is an adapter / integration layer that connects `Claude` models to `VS Code` and supports corporate authentication.
C) It is a replacement for `VS Code` built on the `Cursor` engine.

*Correct answer: B. `Codemie` is the integration layer — not the model itself (`Claude` is the model) and not a separate IDE.*

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
