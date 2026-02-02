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

### Part 3: Authorize GitHub Copilot

1. In VS Code, you'll see a prompt to sign in to GitHub Copilot (or click the Copilot icon in the status bar at the bottom)

1. Click **Sign in to GitHub**

1. Your browser will open - sign in to your GitHub account if prompted

1. Click **Authorize GitHub Copilot**

1. Return to VS Code - you should see a confirmation that you're signed in

1. Verify: The Copilot icon in the status bar (bottom-right) should show as active (no error indicators)

### Part 4: Select AI Model and Agent Mode

1. In VS Code, open the Command Palette

1. Type: `Copilot: Chat Model` and select it

1. Choose your preferred model from the list:
   - `claude-sonnet-4.5` - Best overall model, recommended for this training
   - `gpt-4o` - Alternative capable model
   - `gpt-4` - Older but reliable model

1. For this training, we recommend using **Claude Sonnet 4.5**

1. In the Copilot Chat panel, ensure **Agent Mode** is enabled (look for the toggle or setting in the chat interface)

1. Verify: You should see Agent mode indicator active in the chat panel

### Part 5: Create Your First Workspace

1. Open File Explorer (Windows) or Finder (macOS)

1. Navigate to your `C:` drive (Windows) or home directory (macOS/Linux)

1. Create a new folder: `workspace`
   - Full path on Windows: `c:/workspace/`
   - Full path on macOS/Linux: `~/workspace/`

1. Inside the `workspace` folder, create another folder: `hello-genai`
   - Full path: `c:/workspace/hello-genai/`

1. In VS Code, go to **File > Open Folder**

1. Navigate to `c:/workspace/hello-genai/` and click **Select Folder**

1. VS Code will open this as your workspace

1. If prompted "Do you trust the authors of the files in this folder?", click **Yes, I trust the authors**

### Part 6: Test GitHub Copilot

1. In VS Code, open the Copilot Chat panel (click the chat icon in the left sidebar or in the status bar)

1. In the chat input field, type any question or request, for example:
   ```
   Explain what is a variable in programming
   ```

1. Press `Enter` to send the message

1. Wait a moment for the response

1. Verify: You should see a detailed answer from the AI model

1. Try another question to confirm it's working:
   ```
   What is the difference between a list and a dictionary in Python?
   ```

1. Verify: The AI responds to your questions consistently

---

## Success Criteria

Congratulations! You've successfully completed this module if:

✅ VS Code is installed and running on your computer  with Agent Mode enabled  
✅ You've created the workspace folder at `c:/workspace/hello-genai/`  
✅ VS Code opened the workspace folder  
✅ Copilot Chat is responding to your questionsecommended)  
✅ You've created the workspace folder at `c:/workspace/hello-genai/`  
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
- This feature might require signing in to Copilot first
- Make sure you're using the latest version of VS Code
- Some models may require specific subscription tiers

## Next Steps

Now that you have VS Code and GitHub Copilot set up, you're ready to explore alternative AI coding environments like Cursor in the next module!
