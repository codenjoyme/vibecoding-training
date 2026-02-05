# DIAL Integration with Python and Langchain - Hands-on Walkthrough

In this walkthrough, you'll build a complete Python project that connects to EPAM AI DIAL using the langchain framework. You'll learn proper project structure, virtual environments, dependency management, and secure credential handling.

## Prerequisites

- Python 3.10 or higher installed
- Valid EPAM AI DIAL API key (from Module 170)
- Command line access (PowerShell or Terminal)
- Text editor or IDE (VS Code recommended)

## Quick Start: Automated Setup (RECOMMENDED)

For fastest setup, use the automated installation script for your operating system. The script handles everything: Python environment setup, dependency installation, and file copying.

**Choose based on your OS:**

### Option 1: Windows (Recommended for Windows users)

```powershell
cd docs\modules\180-dial-langchain-python-integration\tools
.\install-python-windows.ps1
```

This downloads portable Python 3.12.8, creates virtual environment, installs all dependencies, and copies example files to `work/python-ai-workspace`.

### Option 2: Linux/macOS

```bash
cd docs/modules/180-dial-langchain-python-integration/tools
./install-python-linux.sh
```

Uses system Python 3.10+, creates virtual environment, installs dependencies, copies files.

### Option 3: Docker (Use only if native installation fails)

**Windows:**
```powershell
cd docs\modules\180-dial-langchain-python-integration\tools
.\install-python-docker.ps1 -Script "query_dial.py"
```

**Linux/macOS:**
```bash
cd docs/modules/180-dial-langchain-python-integration/tools
./install-python-docker.sh query_dial.py
```

Builds Docker container with isolated Python environment.

**After automated setup completes:**
1. Configure your DIAL API key in `work/python-ai-workspace/.env`
2. Skip to **Part 6: Understanding the Demo Script** to learn what was installed
3. Continue to **Part 7: Running Your First AI Query**

---

**Alternative: Manual Setup for Learning**

If you want to understand every step in detail, continue with Part 1-5 below. Manual setup teaches you virtual environments, dependency management, and Python project structure - valuable knowledge for future projects. However, for completing this training module, automated setup above is faster and recommended.

---

## Part 1: Understanding the Stack

Before diving in, let's understand what we're building with and why these choices matter.

### Why Python + Langchain?

**The Goal:** We want to rapidly prototype GenAI applications that are more sophisticated than just running a single prompt on a model. Real-world AI solutions need conversation management, multi-step reasoning, tool integration, and error handling.

**Why Python specifically?**
- Scripting language - quick to write, easy to test, no compilation needed
- Helps solve various local automation tasks beyond just AI
- Massive ecosystem of libraries for data processing, web scraping, file manipulation
- Industry standard for AI/ML development - most frameworks support Python first

**Why Langchain?**
- Accelerates prototyping of complex GenAI workflows
- Handles the tedious parts: API authentication, retries, parsing, streaming
- Pre-built integrations with 100+ AI models, databases, and tools
- Lets you focus on business logic, not plumbing code

### Core Components

**Python:** General-purpose programming language, popular for AI and data science

**Virtual Environment:** Isolated Python environment for your project - like a sandbox where packages don't conflict with other projects. Critical because we don't want libraries installed in this module to "leak" into your system Python. They're needed only here, for this specific project.

**Libraries (Packages):** Collections of code written by other programmers to solve common problems. Langchain is one such library. Libraries depend on other libraries, which depend on third libraries - you'll see this whole dependency chain installing automatically when we set up the environment.

**Langchain:** Framework that simplifies working with AI models - handles API calls, conversation history, and response parsing

**python-dotenv:** Package for loading configuration from .env files securely

**Why not just use cURL?** Langchain provides:
- Automatic conversation history management
- Retry logic and error handling
- Response streaming and parsing
- Integration with other tools (databases, APIs, document loaders)
- Cleaner, more maintainable code

## Part 2: Understanding the Demo Script

The automated setup script already copied `query_dial.py` and `color.py` to your workspace. Let's understand what they do.

Open `query_dial.py` in your editor (location: `work/python-ai-workspace/query_dial.py`):

**Import section:**
```python
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
```
- `AzureChatOpenAI` - langchain's interface to Azure-compatible APIs (DIAL uses Azure format)
- `load_dotenv` - loads variables from .env file into environment

**Configuration section:**
```python
load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_OPENAI_API_DEPLOYMENT"),
    api_version      = os.getenv("AZURE_OPENAI_API_VERSION"),
    api_key          = os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint   = os.getenv("AZURE_OPENAI_ENDPOINT"),
    max_tokens       = 1000,
    temperature      = 0
)
```
- `load_dotenv()` reads .env file and sets environment variables
- `os.getenv()` retrieves values from environment
- `AzureChatOpenAI()` creates connection object configured for DIAL
- `max_tokens` limits response length (cost control)
- `temperature=0` makes responses deterministic (same question → same answer)

**Query section:**
```python
query = "Tell me about artificial intelligence in the style of a pirate."
response = llm.invoke(query)
print(response)
```
- `invoke()` sends query to AI model and waits for response
- Response is returned as structured object with metadata

**Why this is better than cURL:**
- Cleaner syntax - compare to JSON formatting in cURL
- Automatic retry on network failures
- Easy to add conversation history (just pass message array)
- Response parsing handled automatically
- Can stream responses token-by-token for long generations

## Part 3: Running Your First AI Query

Now let's configure your API key and run the script.

1. Open `.env` file in `work/python-ai-workspace/.env`

2. Replace `YOUR_API_KEY_HERE` with your actual DIAL API key from Module 170:
   ```env
   AZURE_OPENAI_API_KEY=your_actual_key_from_module_170
   ```

3. Save the file

4. Navigate to workspace and activate virtual environment:
   
   **Windows:**
   ```powershell
   cd work\python-ai-workspace
   .\.venv\Scripts\Activate.ps1
   ```
   
   **macOS/Linux:**
   ```bash
   cd work/python-ai-workspace
   source .venv/bin/activate
   ```

5. Run the script:
   ```powershell
   python query_dial.py
   ```

3. You should see output like:
   ```
   ======================================
   Query on Azure example
   ======================================
   Python executable: C:\Java\CopipotTraining\vibecoding-for-managers\work\python-ai-workspace\.venv\Scripts\python.exe
   Python version: 3.12.x
   Current directory: C:\Java\CopipotTraining\vibecoding-for-managers\work\python-ai-workspace
   
   Query
   -----
   Tell me about artificial intelligence in the style of a pirate.
   
   Response
   --------
   content='Ahoy, matey! Gather 'round as I spin ye a yarn about Artificial Intelligence...'
   response_metadata={'token_usage': {...}, 'model_name': 'gpt-4o-mini-2024-07-18'}
   
   ======================================
   Demonstration completed!
   ======================================
   ```

**What just happened:**
- Script loaded your API key from .env
- Created langchain connection to DIAL
- Sent your query to GPT-4o-mini model
- Received and displayed response
- All done in ~10 lines of code vs 30+ lines for raw cURL!

## Part 4: Experimenting with the Script

Now let's modify the script to try different queries.

1. Open `query_dial.py` in editor

2. Find the query line:
   ```python
   query = "Tell me about artificial intelligence in the style of a pirate."
   ```

3. Change it to something else:
   ```python
   query = "Explain machine learning to a 10-year-old"
   ```

4. Save and run again:
   ```powershell
   python query_dial.py
   ```

5. Try a few more variations:
   - `"List 5 use cases for AI in healthcare"`
   - `"Write a Python function to calculate fibonacci numbers"`
   - `"Translate 'Good morning' to Japanese"`

6. Experiment with temperature parameter (line with `temperature = 0`):
   - `temperature = 0` - Deterministic, same answer every time
   - `temperature = 0.7` - Balanced creativity
   - `temperature = 1.5` - Very creative, more random

7. Try different models by changing `.env` file:
   ```env
   AZURE_OPENAI_API_DEPLOYMENT=gpt-4o
   ```
   
   Available models (check DIAL chat interface for current list):
   - `gpt-4o-mini-2024-07-18` - Fast, cheap, good for most tasks
   - `gpt-4o` - More capable, slower, more expensive
   - `gpt-4` - Most capable, slowest, most expensive

## Success Criteria

✅ Ran automated installation script successfully  
✅ Python environment configured in `work/python-ai-workspace`  
✅ Virtual environment created with langchain and dependencies installed  
✅ Configured DIAL API key in `.env` file  
✅ Ran `query_dial.py` successfully and received AI response  
✅ Modified query and experimented with different prompts  
✅ Tested temperature parameter variations  
✅ Understand virtual environments and dependency isolation  
✅ Know how to secure credentials with .env files

## Troubleshooting

Once your environment is set up, you have multiple options for executing Python scripts. Each method has different advantages depending on your workflow.

### Method 1: Windows Native Execution

**Best for:** Daily development, debugging, quick iterations

**Prerequisites:**
- Completed Part 2-5 (Python installed, venv created, dependencies installed, .env configured)
- Virtual environment exists in `work/python-ai-workspace/.venv`

**Steps:**

1. Navigate to workspace:
   ```powershell
   cd work\python-ai-workspace
   ```

2. Activate virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   
   You should see `(.venv)` prefix in your prompt.

3. Run any script:
   ```powershell
   python query_dial.py
   # Or any other .py script you create
   ```

4. When finished, deactivate (optional):
   ```powershell
   deactivate
   ```

**Advantages:**
- ✅ Fastest execution (no container overhead)
- ✅ Easy debugging with VS Code Python debugger
- ✅ Direct file system access
- ✅ IDE integration works perfectly

**Disadvantages:**
- ❌ Requires Windows setup (not portable to Linux)
- ❌ Depends on host Python version

### Method 2: Linux/macOS Native Execution

**Best for:** Development on Linux/macOS systems with system Python

**Prerequisites:**
- Linux/macOS operating system
- Python 3.10+ installed on system
- Workspace created in `work/python-ai-workspace`

**Steps:**

1. Navigate to workspace:
   ```bash
   cd work/python-ai-workspace
   ```

2. Activate virtual environment:
   ```bash
   source .venv/bin/activate
   ```
   
   You should see `(.venv)` prefix in your prompt.

3. Run any script:
   ```bash
   python3 query_dial.py
   # Or any other .py script you create
   ```

4. When finished, deactivate (optional):
   ```bash
   deactivate
   ```

**Alternative - Automated Setup:**
If you haven't set up the environment yet, use the installation script:

```bash
cd docs/modules/180-dial-langchain-python-integration/tools
./install-python-linux.sh
```

This script performs all setup steps automatically (venv creation, dependencies installation, file copying).

**Advantages:**
- ✅ Fastest execution on Linux/macOS (no container overhead)
- ✅ Easy debugging with native tools
- ✅ Direct file system access
- ✅ Uses system Python 3.10+

**Disadvantages:**
- ❌ Requires Linux/macOS system
- ❌ Depends on system Python version

### Method 3: Docker Deployment (Production-Ready Container)

**Best for:** Reproducible environments, deployment, sharing with team

**Prerequisites:**
- Docker Desktop installed and running
- Workspace exists with scripts to run

**Steps:**

1. Navigate to module tools directory:
   ```powershell
   cd docs\modules\180-dial-langchain-python-integration\tools
   ```

2. Run Docker deployment script:
   
   **Windows:**
   ```powershell
   .\install-python-docker.ps1
   # Or specify different script:
   .\install-python-docker.ps1 -Script "your_script.py"
   ```
   
   **Linux/macOS:**
   ```bash
   ./install-python-docker.sh
   # Or specify different script:
   ./install-python-docker.sh your_script.py
   ```

3. What happens:
   - Builds Docker image (cached after first build - ~1-3 seconds on subsequent runs)
   - Mounts `work/python-ai-workspace` as volume
   - Runs specified script inside container
   - Container removes automatically after execution

4. First build takes ~120 seconds (downloads Ubuntu, installs Python packages):
   ```
   Building Docker image...
   Step 1/7 : FROM ubuntu:22.04
   Step 2/7 : RUN apt-get update && apt-get install -y python3...
   ...
   Successfully built abc123def456
   ```

5. Subsequent runs use cache (~1-3 seconds):
   ```
   Building Docker image...
   Using cache...
   Successfully built abc123def456
   Running script...
   ```

**Advantages:**
- ✅ Perfect reproducibility (same environment everywhere)
- ✅ No host system pollution (Python stays in container)
- ✅ Layer caching makes rebuilds fast
- ✅ Easy to share (Dockerfile + scripts)
- ✅ Ideal for CI/CD pipelines

**Disadvantages:**
- ❌ First build takes time (~2 minutes)
- ❌ Requires Docker Desktop
- ❌ Slight performance overhead vs native

**Optimization Note:** Docker image is built with base Python environment cached. Scripts are mounted from host, not copied into image, so changing scripts doesn't require rebuild!

### Choosing the Right Method

| Scenario | Recommended Method |
|----------|-------------------|
| Daily development and debugging | Method 1: Windows Native |
| Development on Linux/macOS | Method 2: Linux/macOS Native |
| CI/CD pipeline | Method 3: Docker Deployment |
| Sharing with team | Method 3: Docker Deployment |
| Production deployment | Method 3: Docker Deployment |
| Quick experiments | Method 1: Windows Native |
| Cross-platform validation | Method 2 or 3 |

**Pro Tip:** Use Method 1 for development, then validate with Method 3 before committing to ensure your code works in Docker!

## Part 10: Automated Environment Setup Scripts (Optional)

**Note:** If you already completed Parts 2-5 manually, you can skip this section. These automation scripts are provided for convenience and reproducibility.

For automated setup, we provide installation scripts that perform all the manual steps (Python installation, venv creation, dependency installation, file copying) in one command. These are useful for:
- Setting up fresh environments quickly
- CI/CD pipelines
- Team onboarding
- Reproducible configurations

### Option 1: Windows Automated Setup

Automates Python portable download, venv creation, and dependency installation.

```powershell
cd docs\modules\180-dial-langchain-python-integration\tools
.\install-python-windows.ps1
```

This script performs:
- Downloads portable Python 3.12.8 to workspace `.tools/python`
- Creates virtual environment in `work/python-ai-workspace/.venv`
- Installs langchain, langchain-openai, python-dotenv
- Copies example scripts (query_dial.py, color.py) to workspace
- Sets up `.env` template from `.env.example`
- Creates `.gitignore` for workspace

### Option 2: Linux/macOS Automated Setup

Automates venv creation and dependency installation using system Python.

```bash
cd docs/modules/180-dial-langchain-python-integration/tools
./install-python-linux.sh
```

This script performs:
- Detects and validates system Python 3.10+ installation
- Creates virtual environment in `work/python-ai-workspace/.venv`
- Installs langchain, langchain-openai, python-dotenv
- Copies example scripts (query_dial.py, color.py) to workspace
- Sets up `.env` template from `.env.example`
- Creates `.gitignore` for workspace
- Provides guidance if Python not found

### Option 3: Docker Build-and-Run Automation

Automates Docker image building and script execution in one command.

**Windows:**
```powershell
cd docs\modules\180-dial-langchain-python-integration\tools
.\install-python-docker.ps1 -Script "query_dial.py"
```

**Linux/macOS:**
```bash
cd docs/modules/180-dial-langchain-python-integration/tools
./install-python-docker.sh query_dial.py
```

This script performs:
- Builds Docker image with Python 3.10 + langchain (Ubuntu 22.04 base)
- Mounts `work/python-ai-workspace` as volume
- Runs specified script inside container
- Container auto-removes after execution
- First build ~120 seconds, subsequent builds ~1-3 seconds (cached)

**These automation scripts are equivalent to performing Parts 2-8 manually.** Choose automation for speed, choose manual for learning!

## Success Criteria

✅ Python 3.10+ installed and verified on system  
✅ Created project directory with virtual environment  
✅ Successfully activated virtual environment (showing .venv prefix)  
✅ Installed langchain, langchain-openai, and python-dotenv packages  
✅ Created .env file with DIAL API credentials  
✅ Ran query_dial.py successfully and received AI response  
✅ Modified query and experimented with different prompts  
✅ Tested temperature parameter variations  
✅ Built and tested conversational script with history  
✅ Understand virtual environments and dependency isolation  
✅ Know how to secure credentials with .env files

## Troubleshooting

### Issue: "python: command not found" or "python3: command not found"

**Solution - Windows:**
```powershell
# Verify installation
where.exe python

# If not found, reinstall Python from python.org
# During installation, CHECK "Add Python to PATH"
```

**Solution - macOS/Linux:**
```bash
# Use python3 explicitly
python3 --version

# Install if missing (macOS)
brew install python@3.12

# Install if missing (Ubuntu/Linux)
sudo apt install python3.12 python3-pip
```

### Issue: "cannot be loaded because running scripts is disabled"

**Solution (Windows PowerShell):**
```powershell
# Allow script execution for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
.\.venv\Scripts\Activate.ps1
```

### Issue: Virtual environment not activating (no .venv prefix)

**Solution:**
- Close and reopen terminal
- Navigate back to project directory
- Try activation command again
- On Windows, try: `.venv\Scripts\activate.bat` (CMD) instead of `.ps1` (PowerShell)

### Issue: "No module named 'langchain'" after installation

**Solution:**
```powershell
# Verify you're in virtual environment (see .venv prefix)
# If not, activate it first:
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # macOS/Linux

# Then install again
pip install langchain langchain-openai
```

### Issue: "Unauthorized" or authentication error when running script

**Solution:**
- Open `.env` file and verify API key is correct (no quotes, no spaces)
- Ensure you copied the actual key, not the placeholder text
- Verify you're connected to EPAM VPN if working remotely
- Check API key hasn't expired (request new one if needed)

### Issue: Script runs but shows "None" or empty response

**Solution:**
- Check `.env` has correct `AZURE_OPENAI_ENDPOINT` (should be https://ai-proxy.lab.epam.com)
- Verify `AZURE_OPENAI_API_DEPLOYMENT` matches available model name
- Check model deployment name in DIAL chat interface for current options
- Try changing to `gpt-4o-mini-2024-07-18` which is stable

### Issue: "rate limit exceeded" or "429 error"

**Solution:**
- DIAL has usage quotas per user
- Wait a few minutes before retrying
- Reduce `max_tokens` in script to use less quota per request
- Contact EPAM DIAL support if you need higher limits for project work

### Issue: Slow response times (30+ seconds)

**Solution:**
- Normal for GPT-4 model - try `gpt-4o-mini` for faster responses
- Check network connection (EPAM VPN can be slow)
- Reduce `max_tokens` parameter to limit response length
- Consider using streaming for better UX (advanced topic)

### Issue: Import error "cannot import name 'AzureChatOpenAI'"

**Solution:**
```powershell
# Uninstall and reinstall with correct packages
pip uninstall langchain langchain-openai
pip install langchain-openai langchain-community
```

### Issue: ".env file not found" error

**Solution:**
- Ensure `.env` file is in same directory as script
- Check filename exactly (not `.env.txt` or `env` - Windows hides extensions!)
- Use `dir -Force` (PowerShell) or `ls -la` (Linux/macOS) to see hidden files
- File should be named `.env` with dot prefix, no extension

## When to Use Python + Langchain vs cURL

**Use cURL (Module 170) when:**
- Quick one-off testing
- CI/CD health checks
- Simple shell script automation
- Learning/debugging API issues

**Use Python + Langchain (this module) when:**
- Building applications or prototypes
- Need conversation history management
- Integrating with databases, files, or other APIs
- Complex prompting logic or chains
- Production-grade error handling required
- Team collaboration on shared codebase

## Next Steps

Excellent work! You've built a complete Python AI application with proper project structure, dependency management, and secure credential handling.

**Practical applications to explore:**
- Build a document Q&A system (load PDFs, query with AI)
- Create a Slack bot powered by DIAL
- Automate report generation with AI insights
- Develop a code review assistant

**Advanced langchain features to learn:**
- Chains: Combine multiple LLM calls in sequence
- Agents: Let AI decide which tools to use
- Memory: Persist conversations across sessions
- Document loaders: Process PDFs, websites, databases
- Vector stores: Semantic search over your documents

Next module: **190-advanced-langchain-patterns** - Build sophisticated AI workflows with chains, agents, and memory.

---

**Key Takeaway:** Python + langchain provides professional-grade structure for AI applications. Virtual environments ensure reproducible deployments. Environment variables keep credentials secure. This foundation supports any AI-powered project you'll build.
