# Installing Cursor - Hands-on Walkthrough

In this walkthrough, you'll install Cursor IDE, an AI-native code editor, and set it up for effective vibecoding.

## ⚠️ Important Note for EPAM Employees

**If you are an EPAM employee**, please use **Part 1.2** below for installation instructions. All other users should follow **Part 1.1**.

---

## Prerequisites

- Computer with Windows, macOS, or Linux
- Internet connection
- Completed Module 1 (Installing VSCode + GitHub Copilot)
- Understanding of basic IDE concepts

---

## Step-by-Step Instructions

### Part 1.1: Download and Install Cursor (Personal Use)

1. Open your web browser and navigate to [https://cursor.sh/](https://cursor.sh/)

1. Click the **Download** button for your operating system

1. Once downloaded, run the installer:
   - **Windows**: Run the `.exe` file and follow the installation wizard
   - **macOS**: Open the `.dmg` file and drag Cursor to Applications folder
   - **Linux**: Follow the distribution-specific instructions

1. Launch Cursor after installation completes

1. Verify installation: You should see the Cursor welcome screen

### Part 1.2: Download and Install Cursor (EPAM Employees)

**For EPAM employees only:**

1. Open your web browser and navigate to [https://leap.epam.com/news/5039](https://leap.epam.com/news/5039)

1. Follow the installation manual provided on that page

1. Use the approved download link provided in the EPAM guide

1. Complete the installation according to EPAM's internal procedures:
   - Follow any additional security requirements
   - Use company-approved installation settings
   - Complete any required registration or approval steps

1. Launch Cursor after installation completes

1. Verify installation: You should see the Cursor welcome screen

1. Proceed to **Part 2: Initial Configuration** below

### Part 2: Initial Configuration

1. Cursor may ask to import settings from VS Code - choose based on your preference:
   - **Yes** - If you want to keep your VS Code settings, extensions, and themes
   - **No** - If you want to start fresh

1. Sign in to Cursor (you can use your GitHub account)

1. Complete the initial setup wizard if presented

1. Verify: You should now see the main Cursor editor interface

### Part 3: Create Test Workspace

1. In Cursor, go to **File > Open Folder**

1. Navigate to `c:/workspace/` (or `~/workspace/` on macOS/Linux)

1. Create a new folder: `hello-genai`
   - Full path on Windows: `c:/workspace/hello-genai/`
   - Full path on macOS/Linux: `~/workspace/hello-genai/`

1. Open this folder in Cursor

1. If prompted about trust, click **Yes, I trust**

1. Verify: Cursor opens the workspace successfully

### Part 4: Test Cursor AI Features

1. In Cursor, open the AI command palette using the keyboard shortcut or menu

1. Type a simple request:
   ```
   Create a simple hello world function in Python
   ```

1. Press `Enter`

1. Verify: Cursor should generate code based on your request

1. Open the chat feature using the keyboard shortcut or menu

1. Ask a question in the chat panel:
   ```
   What are the key differences between Python and JavaScript?
   ```

1. Verify: You receive a detailed response from the AI

---

## Success Criteria

Congratulations! You've successfully completed this module if:

✅ Cursor is installed and running on your computer  
✅ You've signed in to Cursor  
✅ You've created and opened the test workspace at `c:/workspace/hello-genai/` (Windows) or `~/workspace/hello-genai/` (macOS/Linux)  
✅ AI Command Palette generates code  
✅ AI Chat responds to your questions  
✅ You understand the key differences between Cursor and VS Code

## Troubleshooting

**Cursor not generating code?**
- Check your internet connection
- Verify you're signed in (check account icon)
- Try restarting Cursor
- Check if AI model is selected in settings

**Can't sign in to Cursor?**
- Make sure you're using a valid email or GitHub account
- Check for popup blockers
- Try the alternative sign-in method

**AI commands not working?**
- Check Settings to ensure AI features are enabled
- Make sure you're not in a modal or dialog
- Try using menu items: Edit menu for AI features

## When to Use Cursor vs VS Code

**Use Cursor when:**
- Starting a new project from scratch
- Need deep codebase understanding
- Want faster AI-native experience
- Prefer integrated AI without extensions

**Use VS Code when:**
- Working with existing team using VS Code
- Need specific VS Code extensions not available in Cursor
- Prefer familiar VS Code workflow
- Organization standardizes on VS Code

## Next Steps

Now that you have both VS Code and Cursor set up, it's time to download the course materials and let the AI agent guide you through the rest of the training!

Copy the link below and **paste it into the AI Chat panel** in your IDE (VS Code Copilot Chat or Cursor Chat):

```
https://github.com/codenjoyme/vibecoding-training/blob/main/docs/modules/025-downloading-course-materials/walkthrough.md
```

The AI agent will read the instructions from that link and guide you through downloading the course repository. From that point on, the agent will conduct all remaining modules for you automatically! 🚀
