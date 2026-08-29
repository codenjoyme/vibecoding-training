- Confirm that the machine is Windows and that the CodeMie CLI is missing before installing it.
- Run installation and verification commands in a native PowerShell or Command Prompt window, not an IDE terminal.
- If Node.js and CodeMie CLI are already installed, skip installation and start with the verification commands.
- Check Node.js and npm with `node --version` and `npm.cmd --version`; CodeMie requires Node.js 20 or newer.
- Prefer the official Windows bootstrap installer when prerequisites are missing:
  + `irm https://raw.githubusercontent.com/codemie-ai/codemie-code/main/install/windows/install.ps1 | iex`
- If Node.js is already installed and PowerShell blocks `npm.ps1`, install the official package through the Windows command shim:
  + `npm.cmd install --global @codemieai/code --fetch-retries=5 --fetch-retry-mintimeout=2000 --fetch-retry-maxtimeout=30000 --fetch-timeout=120000`
  + Never install an unrelated package named `codemie`; the package name is `@codemieai/code`.
- Verify the CLI before configuration with `codemie.cmd --version` and `codemie.cmd --help`.
- If a command is still not found after installation, open a new native terminal before changing PATH.
- Run `codemie.cmd setup` and choose the following defaults:
  + Store configuration globally in `~/.codemie/`.
  + Select `CodeMie SSO` as the LLM provider.
  + Use `https://codemie.lab.epam.com` as the CodeMie organization URL.
  + Complete authentication only in the browser with the user's EPAM SSO account; never request or transmit passwords, tokens, or cookies through chat or terminal input.
  + Let the wizard auto-select the authenticated project, select an available regular model such as `claude-sonnet-5`, and save the profile as `default`.
- Accept the wizard's offer to install Claude Code with the supported version; if the wizard skips or fails that step, run `codemie.cmd install claude --supported`.
- If Claude installation fails with checksum verification, remove `$env:USERPROFILE\.local\share\codemie` and retry from a new native terminal.
- If Claude Code reports that `C:\Users\<user>\.local\bin` is not in PATH, add that exact directory to the current user's PATH and start a new terminal.
- If the PowerShell npm or CodeMie shim is blocked by execution policy, use the `.cmd` command first; when the user permits a user-scoped fix, run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force`.
- Verify the external agent with `claude --version` and the CodeMie wrapper with `codemie-claude --help`.
- Validate the local terminal setup with `codemie.cmd profile status`, `codemie.cmd doctor`, `claude --version`, and `codemie-claude --help`.
- Treat missing Python, AWS CLI, SpecKit, BMAD, or a repository context warning as optional unless the requested agent workflow needs one; require Node.js, npm, an active SSO profile, operational SSO, and installed CodeMie/Claude agents.
- If the SSO session expires, run `codemie.cmd profile refresh` or `codemie.cmd profile login --url https://codemie.lab.epam.com`, then repeat the local verification commands.
- Stop after the terminal checks pass; use the training module for optional IDE integration.