# Installing VSCode + GitHub Copilot - Hands-on Walkthrough

In this walkthrough, you'll install Visual Studio Code, set up GitHub Copilot, and create your first AI-assisted coding workspace.

## ⚠️ Important Note for EPAM Employees

**If you are an EPAM employee**, please use **Part 2.2** below for GitHub Copilot subscription. All other users should follow **Part 2.1**.

---

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

### Part 2.1: Create GitHub Account and Enable Copilot (Personal Use)

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

### Part 2.2: Request GitHub Copilot License (EPAM Employees)

**For EPAM employees only:**

1. Open your browser and navigate to the EPAM Support portal:
   - [https://support.epam.com/ess?id=sc_cat_item_guide&sys_id=ae81891897eb5d98386e3a871153afdf&name=SoftwareLicenses](https://support.epam.com/ess?id=sc_cat_item_guide&sys_id=ae81891897eb5d98386e3a871153afdf&name=SoftwareLicenses)

1. In the Software Licenses request form, select **GitHub Copilot** from the available options

1. Choose the purpose for using GitHub Copilot:
   - **Education and Internal project only** - Select this for learning and internal development
   - **Project needs (for external/client projects)** - Select this if you need Copilot for client work

1. If you selected "Project needs":
   - You will need to specify the project name/code
   - You must obtain approval from your project manager before proceeding
   - Wait for the approval confirmation before continuing

1. Carefully read all license agreements and terms of use

1. Accept the agreements if you agree with the terms

1. Submit your request

1. Wait for the license to be provisioned (you'll receive an email notification)

1. Once approved, you'll receive instructions on how to activate your GitHub Copilot license

1. **Important**: Your GitHub username will be in the format: `Name-Surname_epam`
   - Example: `Ivan-Petrov_epam`
   - Use this exact username format for authentication

1. Open your browser and navigate to GitHub ([https://github.com/](https://github.com/))

1. Sign in using your EPAM GitHub account:
   - Username: `Name-Surname_epam` (the one provided to you)
   - You will be redirected to Microsoft SSO authentication page

1. On the Microsoft SSO page:
   - Enter your EPAM credentials (same as for other EPAM portals)
   - Complete multi-factor authentication if prompted
   - You'll be redirected back to GitHub after successful authentication

1. Verify: Check that Copilot is now enabled in your GitHub account settings

1. Proceed to **Part 3: Authorize GitHub Copilot** below

### Part 3: Authorize GitHub Copilot

1. In VS Code, you'll see a prompt to sign in to GitHub Copilot (or click the Copilot icon in the status bar at the bottom)

1. Click **Sign in to GitHub**

1. Your browser will open - sign in to your GitHub account if prompted

1. Click **Authorize GitHub Copilot**

1. Return to VS Code - you should see a confirmation that you're signed in

1. Verify: The Copilot icon in the status bar (bottom-right) should show as active (no error indicators)

### Part 4: Create Your First Workspace

1. Open File Explorer (Windows) or Finder (macOS)

1. Navigate to your `C:` drive (Windows) or home directory (macOS/Linux)

1. Create a new folder: `workspace`
   - Full path on Windows: `c:/workspace/`
   - Full path on macOS/Linux: `~/workspace/`

1. Inside the `workspace` folder, create another folder: `hello-genai`
   - Full path on Windows: `c:/workspace/hello-genai/`
   - Full path on macOS/Linux: `~/workspace/hello-genai/`

1. In VS Code, go to **File > Open Folder**

1. Navigate to `c:/workspace/hello-genai/` (Windows) or `~/workspace/hello-genai/` (macOS/Linux) and click **Select Folder**

1. VS Code will open this as your workspace

1. If prompted "Do you trust the authors of the files in this folder?", click **Yes, I trust the authors**

### Part 5: Test GitHub Copilot

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

✅ VS Code is installed and running on your computer  
✅ You have a GitHub account with Copilot subscription active  
✅ GitHub Copilot is authorized in VS Code  
✅ You've created the workspace folder at `c:/workspace/hello-genai/` (Windows) or `~/workspace/hello-genai/` (macOS/Linux)  
✅ VS Code opened the workspace folder  
✅ Copilot Chat is responding to your questions

## Troubleshooting

**Copilot not showing suggestions?**
- Check that the Copilot icon in the status bar (bottom-right) is not showing an error
- Try restarting VS Code
- Verify you're signed in: Check the account icon in the bottom-left corner

**Can't authorize Copilot?**
- Make sure you're signed in to GitHub in your browser
- Check that popup blockers aren't interfering
- Try the manual authorization process in VS Code settings

## Next Steps

Now that you have VS Code and GitHub Copilot set up, you have two options:

### Option A: Continue with Cursor (Optional)
If you'd also like to set up an alternative AI-native IDE, proceed to **Module 020: Installing Cursor**.

### Option B: Download Course Materials (Recommended)
To continue the training with AI agent guidance, copy the link below and **paste it into the Copilot Chat panel** in VS Code (the same chat you just tested!):

```
https://github.com/codenjoyme/vibecoding-training/blob/main/modules/025-downloading-course-materials/walkthrough.md
```

The AI agent will read the instructions from that link and guide you through downloading the course repository. From that point on, the agent will conduct all remaining modules for you automatically! 🚀
