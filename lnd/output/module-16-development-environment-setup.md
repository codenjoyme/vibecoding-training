# Module 16: Development Environment Setup

### Background
You have a backlog of tasks, instruction files, skills, and even MCP integrations. But to build a working web application — something you can actually open in a browser — you need developer tools installed on your machine. This module walks you through installing Node.js, npm, nvm, and Docker, step by step, with the AI doing the heavy lifting. You do not need to understand programming to complete this module. Every tool is explained in plain language before you install it.

**Learning Objectives**

Upon completion of this module, you will be able to:
- Explain the purpose of Node.js, npm, nvm, and Docker in plain language.
- Install and verify Node.js and npm using nvm on your operating system.
- Install and verify Docker Desktop for running containers locally.
- Prepare a project skeleton structure for web application prototyping.

## Page 1: What Are These Tools and Why Do You Need Them
### Background
Before installing anything, you should understand what each tool does and why your project needs it.

**Node.js** is a program that runs JavaScript code outside of a web browser. When you build a web application (which you will do in Module 17), Node.js is the engine that powers the server — the part that handles requests, connects to APIs, and sends data back to the browser. Think of it as the "brain" of your application.

**npm (Node Package Manager)** is a tool that comes with Node.js. It downloads and manages libraries — pre-built blocks of code that other developers have shared. Instead of writing everything from scratch, npm lets you install ready-made components (e.g., a library for connecting to Jira API) with a single command. Think of it as an "app store" for code building blocks.

**nvm (Node Version Manager)** is a tool that lets you install and switch between different versions of Node.js. Different projects may require different Node.js versions. nvm lets you switch instantly without uninstalling anything. It is optional but strongly recommended.

**Docker** is a tool that packages your application and all its dependencies into a self-contained "container." This means your application will run the same way on your machine, on a colleague's machine, and on a server. Think of it as a shipping container for software — everything the application needs is inside. Docker is needed when your project uses a database (like PostgreSQL) or when you want to share your prototype with others.

### Steps
1. Open VS Code with your project.
2. Ask the AI: "Explain to me in simple terms what Node.js, npm, nvm, and Docker are and why I need them for building a web application."
3. Read the response. Notice how the AI connects these tools to practical use cases.
4. Ask any follow-up questions you have. There are no stupid questions — this is a learning environment.

### ✅ Result
You understand the purpose of each tool and can explain why your project needs them.

## Page 2: Installing nvm and Node.js
### Background
nvm (Node Version Manager) is the recommended way to install Node.js. It gives you control over which version is installed and makes it easy to update later.

The installation process differs by operating system. The AI assistant knows your operating system and will generate the correct commands for you.

### Steps
1. Ask the AI: "Check if I have nvm installed. If not, help me install it for my operating system."
2. The AI will detect your OS and provide the appropriate installation method:
   - **Windows:** Downloads nvm-windows from GitHub, runs the installer.
   - **macOS/Linux:** Runs the official install script via curl.
3. After nvm is installed, close and reopen your terminal (important — nvm needs a fresh terminal session).
4. Ask the AI: "Install Node.js LTS version using nvm."
5. The AI will run: `nvm install --lts` and then `nvm use --lts`.
6. Verify by asking: "Check that Node.js and npm are installed correctly and show me the versions."
7. You should see output like:
   - `node --version` → v20.x.x (or newer LTS)
   - `npm --version` → 10.x.x (or newer)

If nvm installation fails, the AI can fall back to installing Node.js directly from the official website. This works but means you will need to manually update Node.js in the future.

### ✅ Result
You have Node.js and npm installed and verified. The `node` and `npm` commands work in your terminal.

## Page 3: Installing Docker
### Background
Docker lets you run databases, message queues, and other infrastructure locally without installing each service separately. In Module 17, your prototype will use PostgreSQL as a database — Docker makes this a one-command setup instead of a complex manual installation.

Docker Desktop is a graphical application that runs Docker on Windows and macOS. On Linux, Docker Engine is installed directly via the package manager.

### Steps
1. Ask the AI: "Check if Docker is installed on my machine. If not, help me install Docker Desktop."
2. The AI will guide you through:
   - **Windows:** Download Docker Desktop from docker.com, run the installer, enable WSL 2 integration if prompted.
   - **macOS:** Download Docker Desktop .dmg, drag to Applications, launch.
   - **Linux:** Install Docker Engine and Docker Compose via apt/yum.
3. After installation, Docker Desktop may ask you to sign in — you can skip this for now.
4. Verify by asking: "Check that Docker is running and show me the version."
5. You should see: `docker --version` → Docker version 24.x.x (or newer).
6. Test Docker with: `docker run hello-world`. This downloads a tiny test image and prints a confirmation message.

If Docker Desktop requires a paid license for your organization, the AI can help you find alternatives (e.g., Podman, Rancher Desktop). Ask: "What are free alternatives to Docker Desktop?"

### ✅ Result
You have Docker installed and verified. The `docker` command works, and `docker run hello-world` completes successfully.

## Page 4: Verifying the Full Environment
### Background
Before moving to prototyping, you need to confirm that all tools work together. A single broken dependency can derail the entire next module, so invest two minutes in verification now.

### Steps
1. Ask the AI: "Verify my complete development environment: check nvm, node, npm, and docker versions. Tell me if anything is missing or outdated."
2. The AI will run all version checks and provide a status report.
3. If anything is missing, the AI will help you fix it.
4. Create a simple test: ask the AI to "Create a folder work/env-test, initialize an npm project there, install the express package, and verify it works."
5. The AI will run:
   - `mkdir work/env-test && cd work/env-test`
   - `npm init -y`
   - `npm install express`
   - Create a minimal test file and run it.
6. If the test passes, you know Node.js + npm work correctly.
7. Clean up: "Delete the work/env-test folder."
8. Commit any configuration files that were created (e.g., .nvmrc if the AI created one for version pinning).

### ✅ Result
Your full development environment is verified and ready for prototyping.

## Page 5: Practical Application — Prepare for Prototyping
### Background
With all tools installed, set up the project structure for the prototype you will build in Module 17. This ensures a smooth start in the next module.

### Steps
[MG]: Наверное ТЗ надо чтобы не писал он в англоязычном курсе :)
1. Ask the AI: "Based on my ТЗ (technical specification) from Module 08, what project structure will we need for a web application with React frontend and Node.js backend?"
2. Review the AI's proposed structure. It should include folders like `frontend/`, `backend/`, and a `docker-compose.yml` file.
3. Ask: "Create the basic project structure with empty placeholder files. Do not implement anything yet — just the folder skeleton."
4. Review the created structure. You should see:
   - `frontend/` — will hold the React UI.
   - `backend/` — will hold the Node.js server.
   - `docker-compose.yml` — will define Docker services (database, etc.).
5. Commit the skeleton: "Commit this project skeleton with message 'chore: project skeleton for prototype'."

### ✅ Result
Your project has a clean structure ready for implementation in Module 17.

## Summary
At the start of this module, you had a backlog full of tasks and ideas — but no way to turn them into a working application you could open in a browser. Now you have the tools to make that happen.

You installed Node.js (the engine that runs JavaScript), npm (the library manager), nvm (the version switcher), and Docker (the container platform). Each tool was explained in plain language before installation, and the AI handled the technical commands. Your verified environment is ready for prototyping in Module 17.

Key takeaways:
- Node.js runs JavaScript code on your machine — it is the engine behind web applications.
- npm downloads and manages code libraries — your "app store" for building blocks.
- nvm manages Node.js versions — install once, switch freely.
- Docker packages applications into portable containers — run databases and services with one command.
- Verifying the full environment before starting a new project phase prevents wasted time on broken dependencies.


[MG]: можно попросить запустить какую-то команду агента, типа а проверь какие версии зависимостей установлены, и попросить результат сбросить в модуль автокодер проверки, вместо квиза.
## Quiz
1. What is the purpose of Node.js in a web application project?
   a) It is a text editor for writing JavaScript files
   b) It runs JavaScript code outside the browser, powering the server side of web applications
   c) It is a database management system for storing user data
   Correct answer: b.
   - (a) Incorrect. Node.js is a runtime, not an editor. You write code in VS Code or another editor; Node.js executes that code on your machine.
   - (b) Correct. Node.js is a runtime that executes JavaScript on your machine, enabling you to build server-side applications, connect to APIs, and handle requests — all without a browser.
   - (c) Incorrect. Node.js does not store data. Databases like PostgreSQL handle data storage. Node.js connects to databases but does not replace them.

2. Why is nvm recommended over installing Node.js directly?
   a) nvm includes additional security patches that the standard Node.js installer does not provide
   b) nvm lets you install and switch between multiple Node.js versions without uninstalling anything — useful when different projects require different versions
   c) nvm is required by Docker to function correctly
   Correct answer: b.
   - (a) Incorrect. nvm does not add security patches. It installs the same official Node.js binaries — the advantage is managing multiple versions side by side.
   - (b) Correct. nvm keeps multiple Node.js versions on your machine and lets you switch instantly. This avoids compatibility issues when working on projects with different version requirements.
   - (c) Incorrect. Docker operates independently of nvm. Docker has its own runtime and does not depend on how Node.js is installed.

3. What does Docker do for your development workflow?
   a) It replaces Node.js and npm with a single unified tool
   b) It packages applications and their dependencies into portable containers that run consistently on any machine — allowing you to start databases and services with one command
   c) It monitors your code for errors and suggests fixes in real time
   Correct answer: b.
   - (a) Incorrect. Docker does not replace Node.js or npm. Your application still uses Node.js inside the container. Docker wraps the application and its environment together.
   - (b) Correct. Docker creates isolated containers that bundle your application with everything it needs. This ensures your prototype runs the same way on your machine, a colleague's machine, and a server.
   - (c) Incorrect. Docker does not analyze or monitor code. It handles packaging and running applications. Code analysis is done by linters, the IDE, or the AI assistant.
