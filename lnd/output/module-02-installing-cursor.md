Module 2: Installing Cursor (Optional)

Background
What if a code editor was built from the ground up for AI-assisted work? That is exactly what Cursor is — an AI-native IDE based on the VS Code engine but redesigned to put AI interactions at the center of every workflow. While VS Code with GitHub Copilot is the primary tool for this course, some learners prefer Cursor's streamlined AI experience.

This module is optional. If you are satisfied with your VS Code + Copilot setup from Module 1, you may skip ahead. If you are curious about alternatives or want a backup IDE, install Cursor alongside VS Code. Both can coexist on the same machine.

**Learning objectives.** Upon completion of this module, you will be able to:
- Install and configure Cursor IDE on your operating system.
- Import existing VS Code settings into Cursor.
- Use Cursor’s AI features to generate code and answer questions.
- Choose between Cursor and VS Code based on task requirements.

Page 1: Install Cursor
Background
Cursor uses the same core as VS Code, so the interface will feel familiar. The key difference is that AI features are deeply integrated — not bolted on as extensions. Cursor can import your VS Code settings, themes, and extensions so you do not lose any customization.

Steps (Personal Use — Part A)
1. Open your web browser and navigate to https://cursor.sh/.
2. Click the Download button for your operating system.
3. Run the downloaded installer:
   - Windows: Run the .exe file and follow the installation wizard.
   - macOS: Open the .dmg file and drag Cursor to the Applications folder.
   - Linux: Follow the distribution-specific instructions.
4. Launch Cursor after installation completes.
5. You should see the Cursor welcome screen.

Steps (EPAM Employees — Part B)
1. Open your browser and navigate to https://leap.epam.com/news/5039.
2. Follow the installation manual provided on that page.
3. Use the approved download link from the EPAM guide.
4. Complete the installation according to EPAM internal procedures (follow any additional security requirements).
5. Launch Cursor after installation completes.

✅ Result
Cursor is installed and running on your computer.

Page 2: Initial Configuration
Background
When Cursor starts for the first time, it offers to import your VS Code settings. This includes themes, keyboard bindings, and installed extensions. If you completed Module 1, importing gives you a familiar environment right away.

Steps
1. Cursor may ask to import settings from VS Code. Choose Yes if you want to keep your VS Code settings, themes, and extensions. Choose No if you prefer a fresh start.
2. Sign in to Cursor using your GitHub account (the same one you set up in Module 1).
3. Complete the initial setup wizard if one is presented.
4. Verify: You should see the main Cursor editor interface — it looks similar to VS Code.

✅ Result
Cursor is configured and signed in. The interface is ready for use.

Page 3: Test Cursor AI Features
Background
Cursor's AI features are accessible through the built-in chat panel and command palette — similar to Copilot Chat in VS Code but with additional capabilities like codebase-wide context and multi-file editing.

Steps
1. In Cursor, go to File > Open Folder.
2. Navigate to c:/workspace/hello-genai/ (Windows) or ~/workspace/hello-genai/ (macOS/Linux) — the same workspace you created in Module 1.
3. Open the folder. If prompted about trust, click Yes, I trust.
4. Open the AI Chat panel using the menu or sidebar.
5. Type a request:
   Create a simple hello world function in Python
6. Press Enter. Verify: Cursor should generate code based on your request.
7. Ask a conceptual question in the chat:
   What are the key differences between Python and JavaScript?
8. Verify: You receive a detailed response from the AI.

✅ Result
Cursor opens your workspace, generates code, and answers questions through the AI Chat.

Page 4: When to Use Cursor vs VS Code
Background
Having two IDEs is not about choosing one forever — it is about having the right tool available when you need it. Understanding the strengths of each helps you make a quick decision when starting a task.

Use Cursor when:
- Starting a new project from scratch (strong project scaffolding support).
- You need deep codebase-wide AI understanding across many files.
- You prefer a streamlined AI-first experience without managing extensions.

Use VS Code when:
- Working with a team that standardizes on VS Code.
- You need specific VS Code extensions not yet available in Cursor.
- Your organization provides Copilot licenses but not Cursor licenses.

Both tools are capable — the course works fully with either one.

✅ Result
You understand when each IDE is most useful and can make an informed choice for your workflow.

Summary
In this module, you installed Cursor — the AI-native IDE that answers the question "what if the editor was built around AI from day one?" You imported settings, tested AI features on the same workspace, and learned when each tool excels. For the remainder of the course, use whichever IDE you prefer — all instructions work in both.

Key takeaways:
- Cursor is built on the VS Code engine but with deeper AI integration.
- Both IDEs can coexist — install both and use whichever fits the task.
- The course works identically in VS Code + Copilot or Cursor.

Quiz
1. What is the main difference between Cursor and VS Code?
   a) Cursor is built with AI features deeply integrated from the ground up, while VS Code adds AI capabilities through extensions.
   b) Cursor uses a completely different programming language support system than VS Code.
   c) Cursor requires a separate AI subscription for each programming language you work with.
   Correct answer: a. Cursor was designed as an AI-native editor where AI is part of the core experience, while VS Code achieves AI capabilities through extensions like GitHub Copilot. Option (b) is incorrect — Cursor is built on the same VS Code engine and supports the same languages. Option (c) is incorrect — Cursor’s AI works across all languages with a single subscription.

2. When is VS Code with GitHub Copilot a better choice than Cursor?
   a) When your team standardizes on VS Code and you need specific extensions not yet available in Cursor.
   b) When you want AI-first experience without managing individual extensions.
   c) When you are starting a new project from scratch with no existing codebase.
   Correct answer: a. VS Code has the largest extension ecosystem and is the industry standard for team collaboration. If your team or organization standardizes on it, staying consistent reduces friction. Option (b) describes a strength of Cursor, not VS Code. Option (c) also favors Cursor, which excels at project scaffolding.
