# Downloading Course Materials - Hands-on Walkthrough

In this walkthrough, you'll download the complete course repository and set it up in your local workspace. This will give you access to all training modules, examples, and tools directly in your IDE.

## Prerequisites

- Completed Module 010 (Installing VSCode + GitHub Copilot)
- Completed Module 020 (Installing Cursor) - optional but recommended
- IDE (VS Code or Cursor) installed and working
- `c:/workspace/hello-genai/` folder created
- Internet connection for downloading

---

## What We'll Download

Before we begin, let's understand what you'll be getting:

**Course Repository Structure:**
- **docs/modules/** - All training modules (030 onwards) with theory and walkthroughs
- **work/** - Workspace for your practice projects and exercises
- **scripts/** - Automation scripts and validation tools
- **instructions/** - AI agent instructions for advanced workflows
- **project/** - Sample projects and templates
- **evaluation/** - Assessment materials and quizzes

**Size:** Approximately 5-10 MB  
**Format:** ZIP archive from GitHub  
**Destination:** Your existing `c:/workspace/hello-genai/` folder

---

## Step-by-Step Instructions

### Part 1: Download the Repository

1. Open your web browser

1. Navigate to the course repository on GitHub:
   ```
   https://github.com/YOUR-ORG/vibecoding-for-managers
   ```
   *(Replace with actual repository URL)*

1. Click the green **Code** button (top-right area of the file list)

1. In the dropdown menu, click **Download ZIP**

1. Your browser will download a file named `vibecoding-for-managers-main.zip`

1. Note where the file was saved (usually your Downloads folder)

1. Verify: Check that the ZIP file appears in your Downloads folder

### Part 2: Extract to Workspace

**What we'll do:** We'll extract the ZIP archive contents directly into your `hello-genai` workspace folder, making all course materials accessible in your IDE.

#### Option A: Using PowerShell (Cross-platform, One Command)

1. Open your IDE (VS Code or Cursor)

1. Open a terminal in your IDE:
   - Go to menu: **Terminal > New Terminal**
   - Or click the terminal icon in the bottom panel

1. Copy and paste this command (works on Windows, macOS, Linux):

   ```powershell
   # Navigate to workspace and extract
   cd c:/workspace/hello-genai/ ; Expand-Archive -Path "$HOME/Downloads/vibecoding-for-managers-main.zip" -DestinationPath . -Force ; Move-Item -Path ./vibecoding-for-managers-main/* -Destination . -Force ; Remove-Item -Path ./vibecoding-for-managers-main -Recurse -Force
   ```

   **For macOS/Linux users**, use this version:
   ```bash
   cd ~/workspace/hello-genai/ && unzip -o ~/Downloads/vibecoding-for-managers-main.zip && mv vibecoding-for-managers-main/* . && rm -rf vibecoding-for-managers-main
   ```

1. Press `Enter` to execute

1. Wait for the extraction to complete (should take 5-10 seconds)

1. Verify: You should see a success message in the terminal

#### Option B: Manual Extraction (GUI)

1. Open your file manager (File Explorer on Windows, Finder on macOS)

1. Navigate to your Downloads folder

1. Right-click on `vibecoding-for-managers-main.zip`

1. Select **Extract All...** (Windows) or double-click (macOS)

1. When prompted for destination, browse to `c:/workspace/hello-genai/`

1. Check the option **"Extract here"** or ensure destination is correct

1. Click **Extract**

1. After extraction, you'll see a folder `vibecoding-for-managers-main`

1. Open that folder and **move all its contents** to `c:/workspace/hello-genai/`
   - Select all files and folders inside `vibecoding-for-managers-main`
   - Cut (Ctrl+X or Cmd+X)
   - Navigate to `c:/workspace/hello-genai/`
   - Paste (Ctrl+V or Cmd+V)

1. Delete the now-empty `vibecoding-for-managers-main` folder

1. Verify: You should see folders like `docs/`, `work/`, `scripts/` directly in `hello-genai/`

**What just happened:** You extracted the ZIP archive and moved all course materials into your workspace root. The repository structure is now integrated with your `hello-genai` folder, making it easy to access everything in your IDE.

### Part 3: Verify Installation in IDE

1. In your IDE, look at the Explorer/File tree panel (left sidebar)

1. You should see the following folders in `hello-genai`:
   - `docs/`
   - `work/`
   - `scripts/`
   - `instructions/`
   - `project/`
   - `evaluation/`

1. Expand the `docs/modules/` folder

1. You should see numbered module folders: `030-model-selection/`, `040-agent-mode-under-the-hood/`, etc.

1. Navigate to `docs/modules/030-model-selection/`

1. Open the `about.md` file

1. Verify: You can read the module content in your IDE

1. Try opening `walkthrough.md` from the same folder

1. Verify: The walkthrough displays correctly with formatting

### Part 4: Explore the Structure

1. In your IDE, open the file explorer and browse through:

   - **docs/modules/** - Each numbered folder is a training module
   - **work/** - Your personal workspace for exercises
   - **scripts/** - Helper scripts for automation
   - **instructions/** - AI agent configuration files (used in advanced modules)

1. Notice that module folders are numbered: 030, 040, 050, etc.

1. This numbering allows for future module insertions (e.g., 035, 045)

1. Each module contains at least two files:
   - `about.md` - Module overview and learning objectives
   - `walkthrough.md` - Step-by-step hands-on practice

1. Verify: You can navigate freely through all folders and open files

---

## Success Criteria

Congratulations! You've successfully completed this module if:

✅ The repository ZIP file is downloaded to your computer  
✅ All files are extracted to `c:/workspace/hello-genai/`  
✅ Folder structure includes `docs/`, `work/`, `scripts/`, and other directories  
✅ Module folders (030, 040, 050, etc.) are visible in `docs/modules/`  
✅ You can open and read `about.md` and `walkthrough.md` files in your IDE  
✅ The file tree in your IDE shows the complete course structure  
✅ No `vibecoding-for-managers-main` folder remains (all contents moved to root)

## Understanding Check

1. **Why do we download the repository locally instead of always accessing it online?**
   - Enables offline work, IDE integration, hands-on experimentation, and prepares for Git workflows later

1. **What are the main folders in the repository and their purposes?**
   - `docs/modules/` - training content; `work/` - practice space; `scripts/` - automation tools; `instructions/` - AI agent configs

1. **Why are modules numbered 030, 040, 050 instead of 03, 04, 05?**
   - Allows inserting new modules between existing ones (e.g., 035 between 030 and 040) without renumbering

1. **What files will you find in each module folder?**
   - At minimum: `about.md` (overview) and `walkthrough.md` (hands-on practice); optionally `tools/` directory

1. **Where will you do your hands-on practice and create project files?**
   - In the `work/` folder, which is your personal workspace for exercises

1. **Can you make changes to the course files?**
   - Yes! Since it's a local copy (not a Git repository yet), you can edit, experiment, and customize freely

1. **What happens if you need updated course materials later?**
   - Until Module 060 (Git), re-download and extract; after Module 060, you'll use `git pull` to get updates

## Troubleshooting

**Download failed or ZIP file is corrupted?**
- Check your internet connection
- Try downloading again from GitHub
- Clear browser cache and retry
- Try a different browser

**Can't find the downloaded ZIP file?**
- Check your browser's download settings for the save location
- Look in default Downloads folder: `C:\Users\YourName\Downloads` (Windows) or `~/Downloads` (macOS/Linux)
- Check browser's download history (Ctrl+J or Cmd+Shift+J)

**Extraction command fails in PowerShell?**
- Make sure you're in PowerShell, not Command Prompt
- Verify the ZIP file path is correct
- Try the manual extraction method instead
- Check you have write permissions to `c:/workspace/hello-genai/`

**"Access Denied" or permission errors during extraction?**
- Close any files from that folder open in your IDE or other programs
- Run your IDE as administrator (Windows)
- Check folder permissions
- Try manual extraction instead of command line

**Don't see all folders after extraction?**
- Make sure you moved contents from `vibecoding-for-managers-main/` to workspace root
- Check if files are hidden (enable "Show hidden files" in your file manager)
- Verify extraction completed without errors

**Module files won't open in IDE?**
- Make sure you have the workspace folder open in IDE (File > Open Folder)
- Try closing and reopening the workspace
- Check file permissions
- Verify files are not corrupted (try opening in a text editor)

**PowerShell command doesn't work on macOS/Linux?**
- Use the Bash version of the command provided in Option A
- Or use the manual extraction method (Option B)
- Make sure to use `~/workspace/hello-genai/` instead of `c:/workspace/hello-genai/`

## When to Use This vs Git Clone

**Use ZIP download (this module) when:**
- You're just starting and haven't learned Git yet (Module 060)
- You want a simple, one-time setup
- You don't need version control or updates
- You're working through modules 030-055

**Use Git clone (Module 060+) when:**
- You've completed Git training
- You want to track your changes
- You need to pull updates from the repository
- You're ready for professional development workflows

## Next Steps

Now that you have the complete course materials downloaded and accessible in your IDE, you're ready to:

1. Continue with **Module 030: Model Selection** to learn about choosing the right AI model
2. Work through modules 030-055 directly from your local copy
3. Use the `work/` folder for your hands-on exercises
4. When you reach **Module 060: Version Control with Git**, you'll learn to convert this into a proper Git repository

**Pro tip:** Keep your IDE open with this workspace for all future modules. You'll have instant access to all materials, examples, and reference documentation!
