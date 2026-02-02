# Installing VSCode + GitHub Copilot - Hands-on Walkthrough

In this walkthrough, you'll install Visual Studio Code, set up GitHub Copilot, and create your first AI-assisted coding workspace.

## Prerequisites

- Computer with Windows, macOS, or Linux
- Internet connection
- Administrator access to install software

---

## Step-by-Step Instructions

### Part 1: Install Visual Studio Code

1. Open your web browser and navigate to [https://code.visualstudio.com/](https://code.visualstudio.com/)

1. Click the **Download** button for your operating system (Windows, macOS, or Linux)

1. Once downloaded, run the installer:
   - **Windows**: Run the `.exe` file and follow the installation wizard
   - **macOS**: Open the `.dmg` file and drag VS Code to Applications folder
   - **Linux**: Follow the distribution-specific instructions

1. Launch Visual Studio Code after installation completes

1. Verify installation: You should see the VS Code welcome screen

### Part 2: Create GitHub Account and Enable Copilot

1. Open your browser and go to [https://github.com/](https://github.com/)

1. If you don't have a GitHub account:
   - Click **Sign up** in the top-right corner
   - Enter your email, create a password, and choose a username
   - Complete the verification process
   - Verify your email address

1. Sign in to your GitHub account

1. Navigate to [https://github.com/features/copilot](https://github.com/features/copilot)

1. Click **Start free trial** or **Subscribe** (GitHub Copilot offers a free trial period)

1. Complete the subscription process

1. Verify that Copilot is enabled in your account settings

### Part 3: Install GitHub Copilot Extension

1. In VS Code, click the **Extensions** icon in the left sidebar (or press `Ctrl+Shift+X` / `Cmd+Shift+X`)

1. In the search box, type: `GitHub Copilot`

1. Find the official **GitHub Copilot** extension (published by GitHub)

1. Click **Install**

1. Wait for the extension to install (should take a few seconds)

1. You'll see a prompt to sign in to GitHub - click **Sign in to GitHub**

1. Your browser will open - click **Authorize GitHub Copilot**

1. Return to VS Code - you should see a confirmation that you're signed in

### Part 4: Select AI Model

1. In VS Code, open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)

1. Type: `Copilot: Chat Model` and select it

1. Choose your preferred model from the list:
   - `gpt-4` - Most capable, best for complex tasks
   - `gpt-3.5-turbo` - Faster, good for simple tasks
   - `claude-3.5-sonnet` - Alternative model (if available)

1. For this training, we recommend starting with **gpt-4**

### Part 5: Create Your First Workspace

1. Open File Explorer (Windows) or Finder (macOS)

1. Navigate to your `C:` drive (Windows) or home directory (macOS/Linux)

1. Create a new folder: `workspace`
   - Full path on Windows: `c:/workspace/`
   - Full path on macOS/Linux: `~/workspace/`

1. Inside the `workspace` folder, create another folder: `hellogenai`
   - Full path: `c:/workspace/hellogenai/`

1. In VS Code, go to **File > Open Folder** (or `Ctrl+K Ctrl+O` / `Cmd+K Cmd+O`)

1. Navigate to `c:/workspace/hellogenai/` and click **Select Folder**

1. VS Code will open this as your workspace

1. If prompted "Do you trust the authors of the files in this folder?", click **Yes, I trust the authors**

### Part 6: Test GitHub Copilot

1. In VS Code, create a new file: **File > New File** (or `Ctrl+N` / `Cmd+N`)

1. Save the file as `hello.py` (**File > Save** or `Ctrl+S` / `Cmd+S`)

1. Type the following comment:
   ```python
   # Function to greet the user
   ```

1. Press `Enter` and wait a moment

1. You should see Copilot suggest code (in gray text)

1. Press `Tab` to accept the suggestion

1. Verify: You should see a function created by Copilot

---

## Success Criteria

Congratulations! You've successfully completed this module if:

✅ VS Code is installed and running on your computer  
✅ You have a GitHub account with Copilot subscription active  
✅ GitHub Copilot extension is installed and authenticated in VS Code  
✅ You've selected an AI model (gpt-4 recommended)  
✅ You've created the workspace folder at `c:/workspace/hellogenai/`  
✅ VS Code opened the workspace folder  
✅ Copilot is making code suggestions when you type

## Troubleshooting

**Copilot not showing suggestions?**
- Check that the Copilot icon in the status bar (bottom-right) is not showing an error
- Try restarting VS Code
- Verify you're signed in: Check the account icon in the bottom-left corner

**Can't authorize Copilot?**
- Make sure you're signed in to GitHub in your browser
- Check that popup blockers aren't interfering
- Try the manual authorization process in VS Code settings

**Model selection not available?**
- This feature might require the latest version of Copilot extension
- Check for extension updates in the Extensions panel

## Next Steps

Now that you have VS Code and GitHub Copilot set up, you're ready to explore alternative AI coding environments like Cursor in the next module!
