Module 1: Installing VS Code + GitHub Copilot

Background
According to GitHub's 2025 developer survey, developers using AI coding assistants report a 55% increase in productivity — and that advantage is no longer exclusive to developers. As a manager, you can leverage the same tools to automate repetitive tasks, generate reports, and build internal utilities — without writing code from scratch.

In this module, you will install Visual Studio Code (VS Code) — a free, lightweight code editor — and set up GitHub Copilot, an AI assistant that lives inside the editor. By the end, you will have a working AI-powered workspace ready for the rest of the course.

Think of VS Code as your workbench, and GitHub Copilot as an always-available colleague who can write code, answer questions, and help you solve problems on the spot.

**Learning objectives.** Upon completion of this module, you will be able to:
- Install and launch Visual Studio Code on your operating system.
- Activate a GitHub Copilot subscription (personal or EPAM license path).
- Authorize GitHub Copilot inside VS Code and verify the connection.
- Create a dedicated workspace folder and interact with Copilot Chat.

Page 1: Install Visual Studio Code
Background
Visual Studio Code is a free editor created by Microsoft. It runs on Windows, macOS, and Linux. Unlike heavyweight development environments, VS Code is lightweight, fast, and supports thousands of extensions — including GitHub Copilot. It is the most popular code editor in the world and the primary tool you will use throughout this course.

Steps
1. Open your web browser and navigate to https://code.visualstudio.com/.
2. Click the Download button for your operating system (Windows, macOS, or Linux).
3. Run the downloaded installer:
   - Windows: Run the .exe file and follow the installation wizard. Accept default settings.
   - macOS: Open the .dmg file and drag VS Code to the Applications folder.
   - Linux: Follow the distribution-specific instructions on the download page.
4. Launch Visual Studio Code after the installation completes.
5. You should see the VS Code Welcome tab — a screen with quick links and recent project shortcuts.

✅ Result
VS Code is installed and running. You can see the Welcome tab.

Page 2: Create a GitHub Account and Enable Copilot
Background
GitHub Copilot is an AI-powered coding assistant built by GitHub (a Microsoft company). It integrates directly into VS Code and can generate code, answer questions, explain concepts, and perform multi-step tasks autonomously. To use it, you need a GitHub account with an active Copilot subscription.

There are two paths depending on whether you are using a personal account or an EPAM corporate account.

Steps (Personal Use — Part A)
1. Open your browser and go to https://github.com/.
2. If you do not have an account, click Sign up in the top-right corner.
3. Enter your email, create a password, choose a username, and complete verification.
4. Verify your email address by clicking the link GitHub sends to your inbox.
5. Sign in to your GitHub account.
6. Navigate to https://github.com/features/copilot.
7. Click Start free trial or Subscribe (GitHub Copilot offers a free trial period).
8. Complete the subscription process.
9. Verify that Copilot is enabled in your account settings under the Copilot section.

Steps (EPAM Employees — Part B)
1. Open the EPAM Support portal: https://support.epam.com/ess?id=sc_cat_item_guide&sys_id=ae81891897eb5d98386e3a871153afdf&name=SoftwareLicenses.
2. In the Software Licenses request form, select GitHub Copilot from the available options.
3. Choose the purpose: Education and Internal project only (for learning) or Project needs (for client work — requires manager approval).
4. Read and accept the license agreements.
5. Submit the request and wait for the license to be provisioned (you will receive an email notification).
6. Your EPAM GitHub username follows the format: Name-Surname_epam (for example, Ivan-Petrov_epam).
7. Go to https://github.com/ and sign in with your EPAM GitHub account. You will be redirected to a Microsoft SSO page — enter your EPAM credentials there.
8. After authentication, verify that Copilot is enabled in your GitHub account settings.

✅ Result
You have a GitHub account with an active Copilot subscription.

Page 3: Authorize GitHub Copilot in VS Code
Background
With your GitHub account and Copilot subscription ready, the next step is to connect VS Code to GitHub so the AI assistant can operate inside the editor.

Steps
1. In VS Code, look for the Copilot icon in the bottom status bar. Click it (or wait for the sign-in prompt to appear automatically).
2. Click Sign in to GitHub.
3. Your browser will open — sign in to your GitHub account if prompted.
4. Click Authorize GitHub Copilot when asked.
5. Return to VS Code. You should see a confirmation that the sign-in was successful.
6. Check the Copilot icon in the bottom-right status bar — it should appear active with no error indicators.

✅ Result
GitHub Copilot is authorized and active inside VS Code.

Page 4: Create Your First Workspace
Background
A workspace is a folder on your computer that VS Code opens as a project. All files, settings, and AI interactions are scoped to this folder. Throughout the course, you will use a dedicated workspace folder for all hands-on exercises.

Steps
1. Open File Explorer (Windows) or Finder (macOS).
2. Navigate to your C: drive (Windows) or home directory (macOS/Linux).
3. Create a folder named workspace:
   - Windows: c:/workspace/
   - macOS/Linux: ~/workspace/
4. Inside workspace, create another folder named hello-genai:
   - Windows: c:/workspace/hello-genai/
   - macOS/Linux: ~/workspace/hello-genai/
5. In VS Code, go to File > Open Folder.
6. Navigate to hello-genai and click Select Folder.
7. If prompted "Do you trust the authors of the files in this folder?", click Yes, I trust the authors.

✅ Result
VS Code opens the hello-genai folder as your workspace. You can see the folder name in the Explorer panel on the left.

Page 5: Test GitHub Copilot Chat
Background
The quickest way to verify that everything works is to have a short conversation with Copilot. The Chat panel is where you will interact with the AI assistant throughout the entire course — asking questions, requesting code, and delegating tasks.

Steps
1. In VS Code, open the Copilot Chat panel by clicking the chat icon in the left sidebar (or in the status bar at the bottom).
2. In the chat input field, type:
   Explain what is a variable in programming
3. Press Enter to send the message.
4. Wait a moment — you should see a detailed, well-structured explanation from the AI.
5. Try another question to confirm consistent responses:
   What is the difference between a list and a dictionary in Python?
6. Verify that the AI responds clearly to both questions.

✅ Result
Copilot Chat is responding to your questions. Your AI-powered workspace is fully operational.

Summary
In this module, you installed Visual Studio Code, activated a GitHub Copilot subscription, authorized the AI assistant inside the editor, created a dedicated workspace folder, and verified that Copilot Chat responds to your requests. This workspace and AI assistant will be your primary tools for every remaining module in the course.

Remember the 55% productivity boost from the introduction? That advantage starts right here — with a working editor and an AI assistant ready to help. Every module that follows builds on this foundation.

Key takeaways:
- VS Code is the editor; GitHub Copilot is the AI assistant that lives inside it.
- The hello-genai workspace folder is where all course exercises will take place.
- Copilot Chat is your main interface for interacting with the AI — you can ask questions, request code, and delegate tasks.

[MG]: Квизы хорошо в первых модулях, с тех пор как мы начинаем что-то практическое делать - нужно будет включить практические задачи.
Quiz
1. What is the primary role of GitHub Copilot in VS Code?
   a) It provides an AI assistant that can generate code, answer questions, and perform tasks inside the editor.
   b) It automatically syncs your local files with a cloud backup on GitHub.
   c) It monitors your code for security vulnerabilities and blocks unsafe commits.
   Correct answer: a.
   - (a) is correct because GitHub Copilot is an AI assistant that helps with code generation, Q&A, and task automation directly inside the editor.
   - (b) is incorrect because syncing to GitHub requires separate Git commands — Copilot does not provide backup or file syncing features.
   - (c) is incorrect because security scanning is a different category of tool. Copilot assists with code and tasks, not vulnerability detection.

2. You have installed VS Code and subscribed to GitHub Copilot, but the Copilot Chat panel does not respond. Which action is most likely to resolve the issue?
   a) Reinstall VS Code from scratch.
   b) Check that the Copilot icon in the status bar shows as active and re-authorize your GitHub account if it shows an error.
   c) Install a third-party AI extension from the marketplace.
   Correct answer: b.
   - (a) is incorrect because a full reinstall is excessive — the problem is likely an authorization issue, not a corrupted installation.
   - (b) is correct because the Copilot icon in the status bar is the primary indicator of connection status. If it shows an error, re-authorizing your GitHub account resolves most issues.
   - (c) is incorrect because Copilot is a first-party GitHub extension, not a third-party one. Installing another extension would not fix an authorization problem.

3. Why do you create a dedicated workspace folder for the course instead of opening files individually?
   a) A workspace folder scopes all AI interactions, settings, and instruction files to one project, keeping context relevant and organized.
   b) VS Code cannot open individual files — it only works with folders.
   c) A workspace folder enables Copilot to access the internet during chat sessions.
   Correct answer: a.
   - (a) is correct because a dedicated workspace scopes AI context and project settings, ensuring Copilot's suggestions remain relevant to your course work.
   - (b) is incorrect because VS Code can open individual files — it is not limited to folders. However, opening files individually loses the project-level context that AI assistants rely on.
   - (c) is incorrect because internet access is unrelated to folder structure. Copilot connects to cloud services regardless of how your workspace is organized.
