# Development Environment Setup - Hands-on Walkthrough

In this module, you'll set up the essential development tools needed for vibecoding: **Node.js** (with npm and nvm) and **Docker** (with Docker Compose). These tools form the foundation for building and running modern applications, containers, and MCP servers.

## Prerequisites

Before starting, ensure you have:
- Completed [Module 060: Version Control with Git](../060-version-control-git/about.md)
- Administrator/sudo access on your computer
- Active internet connection
- At least 5 GB free disk space
- Basic familiarity with terminal/command line

## What We'll Install

**Node.js Ecosystem:**
- **Node.js** (~100 MB) - JavaScript runtime for running scripts and servers
- **npm** (included with Node.js) - Node package manager for installing dependencies
- **npx** (included with Node.js) - Tool for running npm packages without installation
- **nvm** - Node Version Manager for switching between Node.js versions

**Docker Ecosystem:**
- **Docker Engine/Desktop** (~500 MB - 1 GB) - Container platform for running isolated applications
- **Docker Compose** (included in Docker Desktop, separate on Linux) - Tool for defining multi-container applications

**Why these tools?**
- Node.js powers MCP servers, web applications, and automation scripts
- Docker enables consistent environments across different machines
- nvm allows working on projects requiring different Node.js versions
- Docker Compose simplifies running complex multi-service applications

**Time required:** 15-20 minutes

---

## Part 1: Node.js Installation

### What We'll Do

Install Node.js, which includes npm and npx. We'll install the **LTS (Long Term Support)** version for stability.

Choose your operating system and follow the instructions:

---

### Windows

**Step 1: Download Node.js Installer**

1. Open browser and navigate to: https://nodejs.org/
2. Click the **LTS** button (left button, typically shows version like 20.x.x)
3. Download completes: `node-v20.x.x-x64.msi` (~30 MB)

**Step 2: Run Installer**

1. Double-click the downloaded `.msi` file
2. Click **Next** through the installation wizard
3. **Important:** Keep "Add to PATH" checkbox checked (default)
4. Accept license agreement
5. Keep default installation location: `C:\Program Files\nodejs\`
6. Click **Install** (requires administrator privileges)
7. Wait for installation to complete (~1-2 minutes)
8. Click **Finish**

**Step 3: Verify Installation**

Open **PowerShell** or **Command Prompt** and run:
```powershell
node --version
npm --version
npx --version
```

**Expected output:**
```
v20.11.0
10.2.4
10.2.4
```

Your version numbers may be slightly different - that's okay!

---

### macOS

**Step 1: Download Node.js Installer**

1. Open browser and navigate to: https://nodejs.org/
2. Click the **LTS** button (shows version like 20.x.x)
3. Download completes: `node-v20.x.x.pkg` (~30 MB)

**Step 2: Run Installer**

1. Open the downloaded `.pkg` file
2. Click **Continue** through the installation wizard
3. Accept license agreement
4. Keep default installation location
5. Click **Install** (will prompt for your password)
6. Enter your macOS password
7. Wait for installation to complete (~1-2 minutes)
8. Click **Close**

**Step 3: Verify Installation**

Open **Terminal** and run:
```bash
node --version
npm --version
npx --version
```

**Expected output:**
```
v20.11.0
10.2.4
10.2.4
```

---

### Linux

**Step 1: Update Package Index**

Open terminal and update your package list:
```bash
sudo apt update
```

**Step 2: Install Node.js via NodeSource Repository**

NodeSource provides up-to-date Node.js packages for Debian/Ubuntu.

```bash
# Download and run NodeSource setup script for Node.js 20.x LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

# Install Node.js and npm
sudo apt install -y nodejs
```

**For other Linux distributions:**
- **Fedora/RHEL/CentOS**: See https://github.com/nodesource/distributions#rpm
- **Arch Linux**: `sudo pacman -S nodejs npm`
- **openSUSE**: `sudo zypper install nodejs npm`

**Step 3: Verify Installation**

```bash
node --version
npm --version
npx --version
```

**Expected output:**
```
v20.11.0
10.2.4
10.2.4
```

---

## Part 2: nvm (Node Version Manager)

### What We'll Do

Install **nvm** to manage multiple Node.js versions. This is especially useful when working on different projects that require different Node.js versions.

**Note for Windows users:** We'll use **nvm-windows**, which is a separate project from the macOS/Linux nvm.

Choose your operating system:

---

### Windows

**Step 1: Download nvm-windows**

1. Navigate to: https://github.com/coreybutler/nvm-windows/releases
2. Download **nvm-setup.exe** from the latest release (~2 MB)

**Step 2: Run Installer**

1. Double-click `nvm-setup.exe`
2. Click **Next** through the wizard
3. Accept license agreement
4. Keep default installation path: `C:\Users\[YourName]\AppData\Roaming\nvm`
5. Select Node.js symlink directory: `C:\Program Files\nodejs`
6. Click **Install**
7. Click **Finish**

**Step 3: Verify nvm Installation**

**Close and reopen PowerShell** (important!), then run:
```powershell
nvm version
```

**Expected output:**
```
1.1.12
```

**Step 4: List Installed Node.js Versions**

```powershell
nvm list
```

You should see your currently installed Node.js version.

---

### macOS

**Step 1: Install nvm via Homebrew or curl**

**Option A - Using Homebrew (recommended if you have it):**
```bash
brew install nvm
```

**Option B - Using curl:**
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

**Step 2: Configure Shell Profile**

Add nvm to your shell profile. The installer usually does this automatically, but verify:

**For bash (default on older macOS):**
```bash
echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bash_profile
echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bash_profile
source ~/.bash_profile
```

**For zsh (default on newer macOS):**
```bash
echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.zshrc
echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.zshrc
source ~/.zshrc
```

**Step 3: Verify nvm Installation**

```bash
nvm --version
```

**Expected output:**
```
0.39.7
```

**Step 4: List Installed Node.js Versions**

```bash
nvm list
```

---

### Linux

**Step 1: Install nvm**

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

**Step 2: Load nvm**

The installer adds nvm to your shell profile automatically. Reload your profile:

```bash
# For bash
source ~/.bashrc

# For zsh
source ~/.zshrc
```

**Step 3: Verify nvm Installation**

```bash
nvm --version
```

**Expected output:**
```
0.39.7
```

**Step 4: List Installed Node.js Versions**

```bash
nvm list
```

---

## Part 3: Docker Installation

### What We'll Do

Install Docker, the container platform that allows running applications in isolated environments. **Windows and macOS** use **Docker Desktop** (graphical application), while **Linux** uses **Docker Engine** (command-line).

Choose your operating system:

---

### Windows

**Step 1: Check Windows Requirements**

Docker Desktop for Windows requires:
- Windows 10/11 64-bit (Pro, Enterprise, or Education)
- WSL 2 (Windows Subsystem for Linux 2) enabled
- Virtualization enabled in BIOS

**Step 2: Enable WSL 2**

Open PowerShell as Administrator and run:
```powershell
wsl --install
```

**If already enabled, you'll see:**
```
Windows Subsystem for Linux is already installed.
```

**If not enabled:**
- Installation will proceed (~5 minutes)
- **Restart your computer** when prompted
- After restart, continue to Step 3

**Step 3: Download Docker Desktop**

1. Navigate to: https://www.docker.com/products/docker-desktop/
2. Click **Download for Windows**
3. Download completes: `Docker Desktop Installer.exe` (~500 MB)

**Step 4: Install Docker Desktop**

1. Double-click `Docker Desktop Installer.exe`
2. Keep **"Use WSL 2 instead of Hyper-V"** checked (recommended)
3. Keep **"Add shortcut to desktop"** checked
4. Click **OK** to start installation (~5 minutes)
5. Click **Close** when installation completes
6. **Restart your computer**

**Step 5: Start Docker Desktop**

1. Double-click **Docker Desktop** icon on desktop
2. Accept service agreement if prompted
3. Wait for Docker to start (~30 seconds)
4. Look for whale icon in system tray (bottom-right)
5. When whale icon is steady (not animated), Docker is running

**Step 6: Verify Docker Installation**

Open PowerShell and run:
```powershell
docker --version
docker compose version
```

**Expected output:**
```
Docker version 24.0.7, build afdd53b
Docker Compose version v2.23.3
```

**Note:** Docker Desktop includes Docker Compose automatically!

---

### macOS

**Step 1: Check macOS Requirements**

Docker Desktop for macOS requires:
- macOS 11 (Big Sur) or newer
- At least 4 GB RAM

**Step 2: Download Docker Desktop**

1. Navigate to: https://www.docker.com/products/docker-desktop/
2. Choose your chip:
   - **Apple Silicon (M1/M2/M3)**: Click "Download for Mac - Apple Chip"
   - **Intel chip**: Click "Download for Mac - Intel Chip"
3. Download completes: `Docker.dmg` (~500 MB)

**Not sure which chip?** Click Apple menu → About This Mac:
- If you see "Apple M1" or "Apple M2" → Apple Silicon
- If you see "Intel Core" → Intel chip

**Step 3: Install Docker Desktop**

1. Open `Docker.dmg` file
2. Drag **Docker** icon to **Applications** folder
3. Open **Applications** folder
4. Double-click **Docker** app
5. macOS may ask "Are you sure you want to open it?" → Click **Open**
6. Click **OK** when prompted for privileged access
7. Enter your macOS password
8. Accept service agreement if prompted
9. Wait for Docker to start (~30 seconds)
10. Look for whale icon in menu bar (top-right)

**Step 4: Verify Docker Installation**

Open Terminal and run:
```bash
docker --version
docker compose version
```

**Expected output:**
```
Docker version 24.0.7, build afdd53b
Docker Compose version v2.23.3
```

**Note:** Docker Desktop includes Docker Compose automatically!

---

### Linux

**Step 1: Remove Old Docker Versions** (if any)

```bash
sudo apt remove docker docker-engine docker.io containerd runc
```

**Step 2: Install Prerequisites**

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release
```

**Step 3: Add Docker's Official GPG Key**

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

**Step 4: Set Up Docker Repository**

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**Step 5: Install Docker Engine**

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Installation takes ~2-3 minutes.

**Step 6: Start Docker Service**

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

**Step 7: Add Your User to Docker Group** (optional but recommended)

This allows running Docker without `sudo`:
```bash
sudo usermod -aG docker $USER
```

**Log out and log back in** for this change to take effect.

**Step 8: Verify Docker Installation**

```bash
docker --version
docker compose version
```

**Expected output:**
```
Docker version 24.0.7, build afdd53b
Docker Compose version v2.23.3
```

**For other Linux distributions:**
- **Fedora**: https://docs.docker.com/engine/install/fedora/
- **CentOS**: https://docs.docker.com/engine/install/centos/
- **Arch Linux**: `sudo pacman -S docker docker-compose`

---

## Part 4: Docker Compose

### What We Already Have

**Good news!** Docker Compose installation status varies by platform:

---

### Windows

**Docker Compose is already installed!**

Docker Desktop for Windows includes Docker Compose v2 by default. You verified this in Part 3, Step 6 when you ran:
```powershell
docker compose version
```

**No additional steps needed.** Skip to Part 5.

---

### macOS

**Docker Compose is already installed!**

Docker Desktop for macOS includes Docker Compose v2 by default. You verified this in Part 3, Step 4 when you ran:
```bash
docker compose version
```

**No additional steps needed.** Skip to Part 5.

---

### Linux

**Docker Compose is already installed!**

When you installed Docker Engine in Part 3, you included the `docker-compose-plugin` package. You verified this in Part 3, Step 8.

**If you need to verify again:**
```bash
docker compose version
```

**Expected output:**
```
Docker Compose version v2.23.3
```

**Note:** Modern Docker uses `docker compose` (with space), not the older `docker-compose` (with hyphen).

**No additional steps needed.** Continue to Part 5.

---

## Part 5: Quick Verification Tests

### What We'll Do

Run simple tests to verify everything works correctly. These tests are identical regardless of your operating system.

---

### Test 1: Docker Hello World

**Step 1: Run Hello World Container**

Open terminal and run:
```bash
docker run hello-world
```

**What happens:**
1. Docker downloads the `hello-world` image (~2 KB)
2. Creates and runs a container from that image
3. Container prints a message and exits

**Expected output:**
```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
...
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

**If you see "Hello from Docker!" → Docker works! ✅**

**Step 2: Check Docker Images**

```bash
docker images
```

You should see the `hello-world` image listed:
```
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
hello-world   latest    9c7a54a9a43c   3 months ago   13.3kB
```

---

### Test 2: Docker Compose with Simple Service

**Step 1: Create Test Directory**

Navigate to your workspace:
```bash
# Windows
cd c:/workspace/hello-genai/work/

# macOS/Linux
cd ~/workspace/hello-genai/work/
```

Create test directory:
```bash
mkdir 110-task
cd 110-task
```

**Step 2: Create docker-compose.yml File**

Create a file named `docker-compose.yml` with this content:

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:latest
    ports:
      - "8080:80"
```

**How to create the file:**
- Open your code editor (VS Code or Cursor)
- Create new file: `docker-compose.yml`
- Paste the content above
- Save in `work/110-task/` directory

**What this does:**
- Defines one service named `nginx`
- Uses official nginx web server image
- Maps port 8080 on your machine to port 80 in container

**Step 3: Start the Service**

In terminal, run:
```bash
docker compose up -d
```

**Expected output:**
```
[+] Running 2/2
 ✔ Network 110-task_default     Created
 ✔ Container 110-task-nginx-1   Started
```

**What happened:**
- Docker Compose created a network
- Downloaded nginx image (~150 MB) if not present
- Started nginx container in background (`-d` = detached mode)

**Step 4: Verify Service is Running**

Check running containers:
```bash
docker compose ps
```

**Expected output:**
```
NAME                 IMAGE          COMMAND                  STATUS         PORTS
110-task-nginx-1     nginx:latest   "/docker-entrypoint.…"   Up 5 seconds   0.0.0.0:8080->80/tcp
```

**Step 5: Test the Web Server**

Open browser and navigate to: http://localhost:8080

**You should see:** "Welcome to nginx!" page

**If you see the nginx welcome page → Docker Compose works! ✅**

**Step 6: Stop the Service**

```bash
docker compose down
```

**Expected output:**
```
[+] Running 2/2
 ✔ Container 110-task-nginx-1   Removed
 ✔ Network 110-task_default     Removed
```

**What happened:**
- Stopped the nginx container
- Removed the container
- Removed the network

---

### Test 3: Node.js Script Execution

**Step 1: Create Simple Node.js Test File**

In the same `work/110-task/` directory, create `test.js`:

```javascript
// Simple Node.js test script
console.log('Node.js is working!');
console.log('Node version:', process.version);
console.log('Platform:', process.platform);

// Simple calculation
const add = (a, b) => a + b;
console.log('2 + 2 =', add(2, 2));
```

**Step 2: Run the Script**

```bash
node test.js
```

**Expected output:**
```
Node.js is working!
Node version: v20.11.0
Platform: win32
2 + 2 = 4
```

**If you see output with your Node version → Node.js works! ✅**

---

### Test 4: npm Package Installation Test

**Step 1: Initialize npm Project**

Still in `work/110-task/` directory:
```bash
npm init -y
```

**Expected output:**
```
Wrote to .../work/110-task/package.json
```

**What happened:**
- Created `package.json` file
- This file tracks project dependencies

**Step 2: Install a Simple Package**

Install `chalk` package (adds colors to terminal output):
```bash
npm install chalk
```

**Expected output:**
```
added 1 package, and audited 2 packages in 2s
found 0 vulnerabilities
```

**What happened:**
- Downloaded `chalk` package from npm registry
- Created `node_modules/` folder with dependencies
- Updated `package.json` with chalk dependency

**Step 3: Test the Installed Package**

Create `test-npm.js`:
```javascript
import chalk from 'chalk';

console.log(chalk.green('✅ npm is working!'));
console.log(chalk.blue('Package installation successful!'));
```

Update `package.json` to add `"type": "module"`:
```json
{
  "name": "110-task",
  "version": "1.0.0",
  "type": "module",
  ...
}
```

Run the script:
```bash
node test-npm.js
```

**Expected output:**
Green text: ✅ npm is working!
Blue text: Package installation successful!

**If you see colored output → npm works! ✅**

---

### Test 5: npx Quick Test

**What is npx?**
npx runs npm packages without installing them globally. Very useful for one-time commands.

**Run a simple npx command:**
```bash
npx cowsay "Development environment ready!"
```

**First run will prompt:**
```
Need to install the following packages:
  cowsay@1.6.0
Ok to proceed? (y)
```

Type `y` and press Enter.

**Expected output:**
```
 _________________________________
< Development environment ready! >
 ---------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

**If you see the cow → npx works! ✅**

---

## Success Criteria

You've successfully completed this module when you can check off:

✅ Node.js installed and verified on your operating system  
✅ npm and npx available and working  
✅ nvm installed for Node.js version management  
✅ Docker installed and running  
✅ Docker Compose available and tested  
✅ Successfully ran `docker run hello-world`  
✅ Successfully started and stopped nginx with Docker Compose  
✅ Successfully ran Node.js script from terminal  
✅ Successfully installed and used npm package  
✅ Successfully used npx to run package without installation  

---

## Understanding Check

Answer these questions to verify comprehension:

1. **What is the difference between Node.js, npm, and npx?**
   
   Expected answer: Node.js is the JavaScript runtime that executes JavaScript code outside browsers. npm is the package manager for installing and managing JavaScript packages/dependencies. npx is a tool for running npm packages without installing them globally, useful for one-time commands or testing packages.

2. **Why would you use nvm (Node Version Manager)?**
   
   Expected answer: nvm allows you to install and switch between multiple Node.js versions on the same machine. This is crucial when working on different projects that require different Node.js versions, or when testing your code against multiple Node versions.

3. **What's the difference between Docker Desktop (Windows/macOS) and Docker Engine (Linux)?**
   
   Expected answer: Docker Desktop is a graphical application that includes Docker Engine, GUI for management, and additional tools like Kubernetes. Docker Engine (Linux) is the core Docker daemon and CLI, installed as a system service. Both run containers the same way, but Desktop provides easier management through UI.

4. **What does `docker compose up -d` do?**
   
   Expected answer: It starts services defined in docker-compose.yml file in detached mode. The `-d` flag means containers run in the background, allowing you to continue using the terminal. Without `-d`, container logs would be displayed in the terminal and it would block.

5. **When would you use Docker vs running applications directly on your machine?**
   
   Expected answer: Use Docker when you need consistent environments across machines, isolation between applications, easy deployment, or when application has complex dependencies. Docker ensures "it works on my machine" applies everywhere. Run directly when it's a simple script, you're actively developing and need fast iteration, or overhead isn't worth the isolation.

6. **What's the purpose of package.json in Node.js projects?**
   
   Expected answer: package.json is the manifest file for Node.js projects that tracks project metadata, dependencies (packages your project needs), scripts (commands you can run), and version information. It allows others to install exact same dependencies with `npm install` and ensures reproducible builds.

7. **What command would you use to check if Docker is running?**
   
   Expected answer: `docker --version` checks if Docker is installed. `docker ps` or `docker info` checks if Docker daemon is running and shows running containers or system information. On Windows/macOS, you can also check if Docker Desktop app is running via system tray icon.

---

## Troubleshooting

### Problem: "node is not recognized" after installation (Windows)

**Symptoms:** Running `node --version` shows "command not found" or "not recognized"

**Solutions:**
1. **Close and reopen terminal** - PATH changes require new terminal session
2. **Verify PATH variable:**
   - Open System Properties → Environment Variables
   - Check if `C:\Program Files\nodejs\` is in PATH
   - If missing, add it manually
3. **Restart computer** if PATH changes don't take effect
4. **Reinstall Node.js** and ensure "Add to PATH" is checked during installation

---

### Problem: Docker Desktop won't start (Windows)

**Symptoms:** Docker Desktop shows "Docker Desktop starting..." forever, or fails to start

**Solutions:**
1. **Enable virtualization in BIOS:**
   - Restart computer and enter BIOS (usually F2, F10, or Del during boot)
   - Find "Virtualization Technology" or "Intel VT-x" / "AMD-V"
   - Enable it and save
2. **Enable WSL 2:**
   ```powershell
   wsl --install
   wsl --set-default-version 2
   ```
3. **Update WSL:**
   ```powershell
   wsl --update
   ```
4. **Check Windows version:** Docker Desktop requires Windows 10 build 19041+ or Windows 11
5. **Run as administrator:** Right-click Docker Desktop → Run as administrator

---

### Problem: "permission denied" when running docker commands (Linux)

**Symptoms:** Docker commands fail with "permission denied while trying to connect to Docker daemon"

**Solutions:**
1. **Add user to docker group:**
   ```bash
   sudo usermod -aG docker $USER
   ```
2. **Log out and log back in** - group changes require new session
3. **Verify group membership:**
   ```bash
   groups
   ```
   You should see `docker` in the list
4. **Restart Docker service:**
   ```bash
   sudo systemctl restart docker
   ```
5. **Temporary solution:** Prefix commands with `sudo`:
   ```bash
   sudo docker ps
   ```

---

### Problem: nvm commands not found after installation

**Symptoms:** Running `nvm --version` shows "command not found"

**Solutions:**

**Windows:**
1. Close and reopen PowerShell
2. Run PowerShell as administrator
3. Check if nvm is in PATH
4. Reinstall nvm-windows

**macOS/Linux:**
1. **Reload shell profile:**
   ```bash
   # For bash
   source ~/.bashrc
   
   # For zsh
   source ~/.zshrc
   ```
2. **Verify nvm is in profile:**
   ```bash
   cat ~/.bashrc | grep NVM_DIR
   ```
   Should show nvm configuration lines
3. **Manually add to profile if missing:**
   ```bash
   echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc
   echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc
   source ~/.bashrc
   ```

---

### Problem: Port 8080 already in use during Docker Compose test

**Symptoms:** `docker compose up` fails with "port is already allocated"

**Solutions:**
1. **Find what's using the port:**
   ```bash
   # Windows
   netstat -ano | findstr :8080
   
   # macOS/Linux
   lsof -i :8080
   ```
2. **Stop the process using the port** or choose different port
3. **Edit docker-compose.yml to use different port:**
   ```yaml
   ports:
     - "8081:80"  # Use 8081 instead of 8080
   ```
4. **Stop all Docker containers:**
   ```bash
   docker stop $(docker ps -aq)
   ```

---

### Problem: npm install fails with network errors

**Symptoms:** Package installation fails with "ETIMEDOUT", "ENOTFOUND", or network errors

**Solutions:**
1. **Check internet connection**
2. **Clear npm cache:**
   ```bash
   npm cache clean --force
   ```
3. **Try different registry:**
   ```bash
   npm config set registry https://registry.npmjs.org/
   ```
4. **Use VPN if behind firewall/proxy**
5. **Check if npm registry is accessible:**
   ```bash
   curl https://registry.npmjs.org/
   ```

---

### Problem: Docker Desktop requires Windows update

**Symptoms:** Installation fails with "Windows version not supported"

**Solutions:**
1. **Check Windows version:**
   - Press Win + R
   - Type `winver` and press Enter
   - Note the build number
2. **Update Windows:**
   - Settings → Update & Security → Windows Update
   - Install all available updates
   - Restart computer
3. **Required minimum:** Windows 10 build 19041 or Windows 11
4. **If can't update:** Consider using Docker Toolbox (older solution) or Linux VM

---

## Next Steps

**Congratulations!** You have a complete Node.js and Docker development environment ready. Here's what comes next:

1. **Practice with containers**
   
   Experiment with Docker:
   - Try different images from Docker Hub (postgres, redis, mongodb)
   - Create multi-service applications with Docker Compose
   - Learn Docker basics: images, containers, volumes, networks

2. **Explore Node.js ecosystem**
   
   Build JavaScript skills:
   - Create simple Node.js scripts
   - Install and use popular npm packages
   - Use nvm to switch between Node versions for different projects

3. **Prepare for MCP development**
   
   Your environment is now ready for:
   - Module 100: Understanding Model Context Protocol
   - Building MCP servers with Node.js
   - Running MCP servers in Docker containers
   - Integrating with AI assistants

4. **Continue to Module 120: Rapid POC Prototyping**
   
   Learn how to quickly prototype ideas using your new development environment.

---

## Additional Resources

- [Node.js Official Documentation](https://nodejs.org/docs/latest/api/)
- [npm Documentation](https://docs.npmjs.com/)
- [nvm GitHub Repository](https://github.com/nvm-sh/nvm)
- [Docker Getting Started Guide](https://docs.docker.com/get-started/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Hub - Container Images](https://hub.docker.com/)

---

**Ready to continue your training?** Head to [Module 120: Rapid POC Prototyping](../120-rapid-poc-prototyping/about.md)
