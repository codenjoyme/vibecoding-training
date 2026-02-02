# Installing Cursor - Hands-on Walkthrough

In this walkthrough, you'll install Cursor IDE, an AI-native code editor, and set it up for effective vibecoding.

## Prerequisites

- Computer with Windows, macOS, or Linux
- Internet connection
- Completed Module 1 (Installing VSCode + GitHub Copilot)
- Understanding of basic IDE concepts

---

## Step-by-Step Instructions

### Part 1: Download and Install Cursor

1. Open your web browser and navigate to [https://cursor.sh/](https://cursor.sh/)

1. Click the **Download** button for your operating system

1. Once downloaded, run the installer:
   - **Windows**: Run the `.exe` file and follow the installation wizard
   - **macOS**: Open the `.dmg` file and drag Cursor to Applications folder
   - **Linux**: Follow the distribution-specific instructions

1. Launch Cursor after installation completes

1. Verify installation: You should see the Cursor welcome screen

### Part 2: Initial Configuration

1. Cursor may ask to import settings from VS Code - choose based on your preference:
   - **Yes** - If you want to keep your VS Code settings, extensions, and themes
   - **No** - If you want to start fresh

1. Sign in to Cursor (you can use your GitHub account)

1. Complete the initial setup wizard if presented

1. Verify: You should now see the main Cursor editor interface

### Part 3: Select AI Model

1. In Cursor, open Settings (gear icon in the bottom-left or top menu)

1. Navigate to the **Models** or **AI** section

1. Choose your preferred model:
   - `claude-sonnet-4.5` - Best overall model, recommended
   - `gpt-4o` - Alternative model
   - `gpt-4-turbo` - Older reliable model

1. For consistency with VSCode training, we recommend **Claude Sonnet 4.5**

1. Verify: The selected model should be displayed in the settings

### Part 4: Create Test Workspace

1. In Cursor, go to **File > Open Folder**

1. Navigate to `c:/workspace/` (or `~/workspace/` on macOS/Linux)

1. Create a new folder: `hello-cursor`
   - Full path: `c:/workspace/hello-cursor/`

1. Open this folder in Cursor

1. If prompted about trust, click **Yes, I trust**

1. Verify: Cursor opens the workspace successfully

### Part 5: Test Cursor AI Features

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

### Part 6: Understanding Key Differences from VS Code

1. **AI Command Palette** - Direct code generation in the editor

1. **AI Chat** - Side-by-side conversation with AI

1. **Built-in AI** - No need for separate extensions, AI is native

1. **Codebase Context** - Cursor can read your entire codebase for better suggestions

1. Try asking in chat:
   ```
   Explain how Cursor is different from VS Code with Copilot
   ```

1. Verify: AI explains the differences based on its knowledge

---

## Success Criteria

Congratulations! You've successfully completed this module if:

✅ Cursor is installed and running on your computer  
✅ You've signed in to Cursor  
✅ You've selected an AI model (Claude Sonnet 4.5 recommended)  
✅ You've created and opened the test workspace at `c:/workspace/hello-cursor/`  
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

Now that you have both VS Code and Cursor set up, you're ready to learn about choosing the right AI model for different tasks in the next module!
