# GitHub Copilot CLI Installation Guide

This guide describes how to install and configure GitHub Copilot CLI for Windows.

## Prerequisites

- Windows 10/11
- GitHub account with Copilot subscription
- VS Code with GitHub Copilot extension installed

## Step 1: Install Node Version Manager (nvm-windows)

1. Download nvm-windows installer:
   - Go to https://github.com/coreybutler/nvm-windows/releases
   - Download `nvm-setup.exe` from latest release

2. Run installer with default settings

3. Verify installation in PowerShell:
   ```powershell
   nvm version
   ```
   You should see version number like `1.1.12`

4. Install Node.js:
   ```powershell
   nvm install 20.19.0
   nvm use 20.19.0
   ```

5. Verify Node.js installation:
   ```powershell
   node --version
   ```
   Should output: `v20.19.0`

## Step 2: Add Node.js to PATH (Temporary)

In PowerShell, before using copilot command:

```powershell
$env:PATH = "C:\Java\nvm\v20.19.0;$env:PATH"
```

**Note:** Replace `C:\Java\nvm` with your actual nvm installation path. Default is `C:\Users\<Username>\AppData\Roaming\nvm`

To find your nvm path:
```powershell
where.exe nvm
```

## Step 3: Verify Copilot CLI Installation

GitHub Copilot CLI is automatically installed with VS Code Copilot extension.

Find copilot.bat location:
```powershell
where.exe copilot
```

Expected path:
```
C:\Users\<Username>\AppData\Roaming\Code\User\globalStorage\github.copilot-chat\copilotCli\copilot.bat
```

Or for VS Code Insiders:
```
C:\Users\<Username>\AppData\Roaming\Code - Insiders\User\globalStorage\github.copilot-chat\copilotCli\copilot.bat
```

## Step 4: Using Copilot CLI

### Basic Command Structure

```powershell
# Set PATH first (in each new PowerShell session)
$env:PATH = "C:\Java\nvm\v20.19.0;$env:PATH"

# Run copilot with prompt
copilot -p "Your question here" --allow-all -s
```

### With File References

```powershell
# Reference files with @
copilot -p "@path\to\instruction.md" -p "@path\to\file.md" --allow-all --no-ask-user -s
```

### Working in Specific Directory

```powershell
# Change to target directory
cd path\to\module

# Run copilot with access to current directory
copilot -p "@..\..\..\instructions\instruction.md" --add-dir "." --allow-all --no-ask-user -s
```

## Command Options Explained

- `-p "text"` or `-p "@file"` - Prompt text or file reference
- `--allow-all` - Enable all permissions (tools, paths, URLs)
- `--no-ask-user` - Agent works autonomously without asking questions
- `-s` or `--silent` - Output only agent response (no stats)
- `--add-dir "path"` - Grant access to specific directory

## Common Issues

### Issue: "copilot: command not found"

**Solution:** Copilot CLI is installed with VS Code Copilot extension. Check:
```powershell
where.exe copilot
```

If not found, reinstall GitHub Copilot extension in VS Code.

### Issue: "Cannot find GitHub Copilot CLI"

**Solution:** This message appears in interactive mode. Use `-p` flag for non-interactive:
```powershell
copilot -p "your question" --allow-all -s
```

### Issue: Node.js not found

**Solution:** Add Node.js to PATH:
```powershell
$env:PATH = "C:\Java\nvm\v20.19.0;$env:PATH"
```

Or find your Node.js path:
```powershell
Get-Command node | Select-Object Source
```

### Issue: "The command line is too long"

**Solution:** Use file references with `@` instead of passing large text as argument:
```powershell
# Create temporary file
$prompt | Out-File -FilePath "temp.txt" -Encoding UTF8

# Reference file
copilot -p "@temp.txt" --allow-all -s
```

## Example: Validating Walkthrough Files

Complete example for validation script:

```powershell
# 1. Set PATH
$env:PATH = "C:\Java\nvm\v20.19.0;$env:PATH"

# 2. Navigate to module directory
cd .\docs\modules\010-installing-vscode-github-copilot

# 3. Run validation with instruction file
copilot -p "@..\..\..\instructions\validate-walkthrough.instruction.md" --add-dir "." --allow-all --no-ask-user -s

# 4. Check result
cat todo.md
```

## Permanent PATH Configuration (Optional)

To avoid setting PATH in every session:

1. Open System Environment Variables:
   - Press `Win + R`
   - Type: `sysdm.cpl`
   - Go to "Advanced" tab
   - Click "Environment Variables"

2. Under "User variables", find "Path"

3. Click "Edit" → "New"

4. Add: `C:\Java\nvm\v20.19.0` (or your nvm path)

5. Click OK and restart PowerShell

## Summary

- **nvm-windows**: Node version manager
- **Node.js 20.19.0**: Required for Copilot CLI
- **Copilot CLI**: Installed with VS Code Copilot extension
- **PATH setup**: Required before each use (or set permanently)
- **Command pattern**: `$env:PATH = ".."; copilot -p "@file" --flags`

---

*This guide was created during troubleshooting session on 2026-02-03*
