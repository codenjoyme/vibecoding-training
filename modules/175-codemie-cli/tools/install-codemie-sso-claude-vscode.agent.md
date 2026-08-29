- Confirm that the machine is Windows and that the CodeMie CLI is missing before installing it.
- Check Node.js and npm with `node --version` and `npm.cmd --version`; CodeMie requires Node.js 20 or newer.
- Prefer the official Windows bootstrap installer when prerequisites are missing:
  + `irm https://raw.githubusercontent.com/codemie-ai/codemie-code/main/install/windows/install.ps1 | iex`
- If Node.js is already installed and PowerShell blocks `npm.ps1`, install the official package through the Windows command shim:
  + `npm.cmd install --global @codemieai/code --fetch-retries=5 --fetch-retry-mintimeout=2000 --fetch-retry-maxtimeout=30000 --fetch-timeout=120000`
  + Never install an unrelated package named `codemie`; the package name is `@codemieai/code`.
- Verify the CLI before configuration with `codemie.cmd --version` and `codemie.cmd --help`.
- Run `codemie.cmd setup` and choose the following defaults:
  + Store configuration globally in `~/.codemie/`.
  + Select `CodeMie SSO` as the LLM provider.
  + Use `https://codemie.lab.epam.com` as the CodeMie organization URL.
  + Complete authentication only in the browser with the user's EPAM SSO account; never request or transmit passwords, tokens, or cookies through chat or terminal input.
  + Let the wizard auto-select the authenticated project, select an available regular model such as `claude-sonnet-5`, and save the profile as `default`.
- Accept the wizard's offer to install Claude Code with the supported version; if that step fails, run `codemie.cmd install claude --supported`.
- If Claude Code reports that `C:\Users\<user>\.local\bin` is not in PATH, add that exact directory to the current user's PATH and start a new terminal.
- If the PowerShell npm or CodeMie shim is blocked by execution policy, use the `.cmd` command first; when the user permits a user-scoped fix, run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force`.
- Verify the external agent with `claude --version` and the CodeMie wrapper with `codemie-claude --help`.
- Configure the installed VS Code Claude Code extension to use the active CodeMie SSO profile through the local proxy:
  + `codemie proxy connect --vscode-claude-code --verbose`
  + Add `--profile <name>` only when a profile other than the active one is required.
  + Use `--insiders` only when configuring VS Code Insiders.
- Confirm that the command starts a healthy proxy at `http://127.0.0.1:4001` and writes the user's VS Code settings without deleting unrelated settings.
- Confirm that VS Code `settings.json` contains the CodeMie-managed values `claudeCode.disableLoginPrompt: true`, `ANTHROPIC_BASE_URL: http://127.0.0.1:4001`, and `ANTHROPIC_AUTH_TOKEN: codemie-proxy`.
- Do not replace `codemie-proxy` with an EPAM password, SSO cookie, or personal API key; the local proxy uses the encrypted CodeMie SSO credential store.
- Reload VS Code with `Developer: Reload Window` after the connector reports success.
- Validate the final setup with `codemie profile status`, `codemie proxy status --deep`, `codemie doctor`, and `codemie-claude --help`.
- Treat missing Python, AWS CLI, SpecKit, BMAD, or a repository context warning as optional unless the requested agent workflow needs one; require Node.js, npm, an active SSO profile, operational SSO, and installed CodeMie/Claude agents.
- If the SSO session expires, run `codemie profile refresh` or `codemie profile login --url https://codemie.lab.epam.com`, then reconnect the proxy.
- Keep the CodeMie proxy running while the VS Code Claude Code extension is in use; stop it with `codemie proxy stop` when it is no longer needed.