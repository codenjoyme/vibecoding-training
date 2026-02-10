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

### Part 1: Download and Extract in One Command

**What we'll do:** We'll use a single command to automatically download the repository and extract it to your workspace.

#### For Windows (PowerShell):

1. Open your IDE (VS Code or Cursor)

1. Open a terminal in your IDE:
   - Go to menu: **Terminal > New Terminal**

1. Copy and paste this one-line command:

   ```powershell
   $url = "https://codeload.github.com/codenjoyme/vibecoding-training/zip/refs/heads/main"; $dest = "c:/workspace/hello-genai"; New-Item -ItemType Directory -Force -Path $dest; (New-Object System.Net.WebClient).DownloadFile($url, "$dest\project.zip"); Expand-Archive -Path "$dest\project.zip" -DestinationPath "$dest\tmp" -Force; Remove-Item "$dest\project.zip"; Move-Item "$dest\tmp\vibecoding-training-main\*" "$dest" -Force; Remove-Item "$dest\tmp" -Recurse -Force
   ```

1. Press `Enter` to execute

1. Wait for the download and extraction to complete (10-30 seconds depending on your internet speed)

1. Verify: You should see folders like `docs/`, `work/`, `scripts/` in your IDE's file explorer

#### For macOS:

1. Open your IDE (VS Code or Cursor)

1. Open a terminal in your IDE:
   - Go to menu: **Terminal > New Terminal**

1. Copy and paste this one-line command:

   ```bash
   url="https://codeload.github.com/codenjoyme/vibecoding-training/zip/refs/heads/main"; dest="$HOME/workspace/hello-genai"; mkdir -p "$dest"; curl -L -o "$dest/project.zip" "$url"; cd "$dest"; unzip -q project.zip; mv vibecoding-training-main/* .; mv vibecoding-training-main/.* . 2>/dev/null || true; rmdir vibecoding-training-main; rm project.zip
   ```

1. Press `Enter` to execute

1. Wait for the download and extraction to complete (10-30 seconds depending on your internet speed)

1. Verify: You should see folders like `docs/`, `work/`, `scripts/` in your IDE's file explorer

#### For Linux:

1. Open your IDE (VS Code or Cursor)

1. Open a terminal in your IDE:
   - Go to menu: **Terminal > New Terminal**

1. Copy and paste this one-line command:

   ```bash
   url="https://codeload.github.com/codenjoyme/vibecoding-training/zip/refs/heads/main"; dest="$HOME/workspace/hello-genai"; mkdir -p "$dest"; wget -O "$dest/project.zip" "$url"; cd "$dest"; unzip -q project.zip; mv vibecoding-training-main/* .; mv vibecoding-training-main/.* . 2>/dev/null || true; rmdir vibecoding-training-main; rm project.zip
   ```

1. Press `Enter` to execute

1. Wait for the download and extraction to complete (10-30 seconds depending on your internet speed)

1. Verify: You should see folders like `docs/`, `work/`, `scripts/` in your IDE's file explorer

**What just happened:** The command automatically:
1. Created the workspace directory if it didn't exist
2. Downloaded the repository as a ZIP file
3. Extracted it to a temporary location
4. Moved all contents from `vibecoding-training-main` folder to your workspace root
5. Cleaned up temporary files

### Part 2: Manual Download (If Automatic Method Fails)

**If the automatic command didn't work**, follow these steps:

1. Open your web browser and navigate to:
   ```
   https://github.com/codenjoyme/vibecoding-training
   ```

1. Click the green **Code** button → **Download ZIP**

1. Download `vibecoding-training-main.zip` to your Downloads folder

1. Extract the ZIP file to `c:/workspace/hello-genai/` (Windows) or `~/workspace/hello-genai/` (macOS/Linux)

1. **Important:** After extraction, move all contents from the `vibecoding-training-main` folder into the root of `hello-genai/` workspace

1. Delete the now-empty `vibecoding-training-main` folder

1. Verify: Folders like `docs/`, `work/`, `scripts/` should be directly in `hello-genai/`, not inside a subfolder

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
✅ No `vibecoding-training-main` folder remains (all contents moved to root)

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
- Try running the command again
- If using PowerShell, make sure you're not in Command Prompt
- Try the manual download method in Part 2

**Command execution fails?**
- Make sure you're in the correct terminal (PowerShell for Windows, Bash for macOS/Linux)
- Check you have write permissions to the workspace folder
- Try running your IDE as administrator (Windows)
- Use the manual download method as fallback

**"Access Denied" or permission errors?**
- Close any files from that folder open in your IDE or other programs
- Run your IDE as administrator (Windows)
- Check folder permissions
- Try manual download method instead

**Don't see all folders after extraction?**
- Refresh your IDE's file explorer (right-click → Refresh)
- Make sure contents were moved from `vibecoding-training-main/` to workspace root
- Check if files are hidden (enable "Show hidden files" in your file manager)
- Try closing and reopening the workspace folder in your IDE

**Module files won't open in IDE?**
- Make sure you have the workspace folder open in IDE (File > Open Folder)
- Try closing and reopening the workspace
- Check file permissions
- Verify files are not corrupted (try opening in a text editor)

**PowerShell command doesn't work on macOS/Linux?**
- Use the Bash version of the command provided for your OS
- Make sure you're using Bash/Zsh terminal, not PowerShell
- Or use the manual download method (Part 2)

**`curl` or `wget` not found?**
- macOS: `curl` should be pre-installed; if not, install Xcode Command Line Tools
- Linux: Install wget with `sudo apt install wget` (Ubuntu/Debian) or `sudo yum install wget` (Red Hat/CentOS)
- Or use the manual download method

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
