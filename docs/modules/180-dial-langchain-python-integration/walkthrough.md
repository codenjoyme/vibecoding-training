# DIAL Integration with Python and Langchain - Hands-on Walkthrough

In this walkthrough, you'll build a complete Python project that connects to EPAM AI DIAL using the langchain framework. You'll learn proper project structure, virtual environments, dependency management, and secure credential handling.

## Prerequisites

- Python 3.10 or higher installed
- Valid EPAM AI DIAL API key (from Module 170)
- Command line access (PowerShell or Terminal)
- Text editor or IDE (VS Code recommended)

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

## Part 2: Setting Up Python Environment

1. Verify Python installation:
   
   **Windows (PowerShell):**
   ```powershell
   python --version
   ```
   
   **macOS/Linux:**
   ```bash
   python3 --version
   ```
   
   You should see `Python 3.10.x` or higher

2. If Python is not installed or version is below 3.10:
   
   **Windows:**
   - Download from https://www.python.org/downloads/
   - Run installer, **check "Add Python to PATH"**
   - Restart PowerShell after installation
   
   **macOS:**
   ```bash
   brew install python@3.12
   ```
   
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt update
   sudo apt install python3.12 python3.12-venv python3-pip
   ```

3. Create a project directory:
   
   **Windows:**
   ```powershell
   mkdir c:\temp\dial-python-demo
   cd c:\temp\dial-python-demo
   ```
   
   **macOS/Linux:**
   ```bash
   mkdir ~/temp/dial-python-demo
   cd ~/temp/dial-python-demo
   ```

## Part 3: Creating Virtual Environment

Virtual environments keep project dependencies isolated. Without them, installing packages for one project might break another.

1. Create virtual environment:
   
   **Windows:**
   ```powershell
   python -m venv .venv
   ```
   
   **macOS/Linux:**
   ```bash
   python3 -m venv .venv
   ```
   
   This creates a `.venv` folder with isolated Python installation

2. Activate the virtual environment:
   
   **Windows (PowerShell):**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   
   If you get an error about execution policies:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\.venv\Scripts\Activate.ps1
   ```
   
   **macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

3. Verify activation - your prompt should now show `(.venv)` prefix:
   ```
   (.venv) PS C:\temp\dial-python-demo>
   ```

4. Upgrade pip (Python package manager):
   ```powershell
   python -m pip install --upgrade pip
   ```

**Important:** Always activate virtual environment before installing packages or running scripts!

## Part 4: Installing Dependencies

Now we'll install the packages our project needs.

**Understanding Dependencies:** When you install a library like `langchain`, it automatically installs all other libraries it depends on. Those libraries may depend on others, creating a dependency tree. You'll see dozens of packages installing - this is normal! Each solves a specific problem, and together they enable langchain's functionality.

1. Install langchain and Azure OpenAI integration:
   ```powershell
   pip install python-dotenv
   pip install langchain
   pip install langchain-openai
   pip install langchain-community
   ```
   
   Each command will download and install packages plus all their dependencies. This takes 30-60 seconds. You'll see output listing all installed packages - that's the dependency tree resolving automatically.

2. Verify installations:
   ```powershell
   pip list
   ```
   
   You should see packages like:
   ```
   langchain            0.x.x
   langchain-openai     0.x.x
   python-dotenv        1.x.x
   ```

3. (Optional) Save dependencies to file for later reproduction:
   ```powershell
   pip freeze > requirements.txt
   ```
   
   This creates `requirements.txt` with exact versions - anyone can recreate your environment with `pip install -r requirements.txt`

## Part 5: Configuring Environment Variables

Never hardcode API keys in scripts! Use environment variables instead.

1. Copy the example .env file from module tools:
   
   **Windows:**
   ```powershell
   Copy-Item c:\Java\CopipotTraining\vibecoding-for-managers\docs\modules\180-dial-langchain-python-integration\tools\.env.example .\.env
   ```
   
   **macOS/Linux:**
   ```bash
   cp c:/Java/CopipotTraining/vibecoding-for-managers/docs/modules/180-dial-langchain-python-integration/tools/.env.example ./.env
   ```

2. Open `.env` file in text editor

3. Replace the API key with your actual key from Module 170:
   ```env
   AZURE_OPENAI_API_KEY=your_actual_key_here
   AZURE_OPENAI_API_VERSION=2023-03-15-preview
   AZURE_OPENAI_ENDPOINT=https://ai-proxy.lab.epam.com
   AZURE_OPENAI_API_DEPLOYMENT=gpt-4o-mini-2024-07-18
   ```

4. Save and close the file

**Security note:** 
- `.env` files should NEVER be committed to Git
- Add `.env` to your `.gitignore` file
- Share `.env.example` template instead (with placeholder values)

## Part 6: Understanding the Demo Script

Before running the script, let's understand what it does.

1. Copy the demo script from module tools:
   
   **Windows:**
   ```powershell
   Copy-Item c:\Java\CopipotTraining\vibecoding-for-managers\docs\modules\180-dial-langchain-python-integration\tools\query_dial.py .
   Copy-Item c:\Java\CopipotTraining\vibecoding-for-managers\docs\modules\180-dial-langchain-python-integration\tools\color.py .
   ```
   
   **macOS/Linux:**
   ```bash
   cp c:/Java/CopipotTraining/vibecoding-for-managers/docs/modules/180-dial-langchain-python-integration/tools/query_dial.py .
   cp c:/Java/CopipotTraining/vibecoding-for-managers/docs/modules/180-dial-langchain-python-integration/tools/color.py .
   ```

2. Open `query_dial.py` in your editor and examine the code:

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

## Part 7: Running Your First AI Query

1. Make sure virtual environment is activated (see `(.venv)` in prompt)

2. Run the script:
   ```powershell
   python query_dial.py
   ```

3. You should see output like:
   ```
   ======================================
   Query on Azure example
   ======================================
   Python executable: C:\temp\dial-python-demo\.venv\Scripts\python.exe
   Python version: 3.12.x
   Current directory: C:\temp\dial-python-demo
   
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

## Part 8: Experimenting with the Script

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

## Part 9: Building a Conversational Script

Let's enhance the script to maintain conversation history.

1. Create a new file `conversation.py`:
   ```python
   from color import header
   header("Conversational AI Demo", "cyan")
   
   import os
   from langchain_openai import AzureChatOpenAI
   from dotenv import load_dotenv
   
   load_dotenv()
   
   llm = AzureChatOpenAI(
       azure_deployment = os.getenv("AZURE_OPENAI_API_DEPLOYMENT"),
       api_version      = os.getenv("AZURE_OPENAI_API_VERSION"),
       api_key          = os.getenv("AZURE_OPENAI_API_KEY"),
       azure_endpoint   = os.getenv("AZURE_OPENAI_ENDPOINT"),
       max_tokens       = 1000,
       temperature      = 0.7
   )
   
   # Conversation history
   messages = []
   
   header("Multi-turn Conversation")
   print("Type 'exit' to quit\n")
   
   while True:
       user_input = input("You: ")
       
       if user_input.lower() == 'exit':
           break
       
       # Add user message to history
       messages.append({"role": "user", "content": user_input})
       
       # Get AI response
       response = llm.invoke(messages)
       
       # Add AI response to history
       messages.append({"role": "assistant", "content": response.content})
       
       print(f"\nAI: {response.content}\n")
   
   header("Conversation ended")
   ```

2. Run the conversational script:
   ```powershell
   python conversation.py
   ```

3. Have a multi-turn conversation:
   ```
   You: What's the capital of France?
   AI: The capital of France is Paris.
   
   You: What's the population?
   AI: Paris has approximately 2.1 million residents...
   
   You: exit
   ```

Notice how the AI remembers context ("What's the population?" - it knows you mean Paris)!

## Part 10: Three Ways to Set Up Your Environment

For reproducibility, you can automate the entire setup. We provide three installation options:

### Option 1: Windows Native (PowerShell)

Best for Windows development with native Python installation. Navigate to tools directory and run the script.

```powershell
cd tools
.\install-python-windows.ps1
```

This script:
- Downloads portable Python 3.12.8
- Creates virtual environment in `.venv`
- Installs all langchain dependencies
- Sets up `.env` template if missing

### Option 2: Linux/macOS (Bash)

Best for Linux/macOS development with system Python. Navigate to tools directory and run the script.

```bash
cd tools && ./install-python-linux.sh
```

This script:
- Detects and validates system Python installation
- Creates virtual environment in `.venv`
- Installs all langchain dependencies
- Guides through manual Python installation if needed

### Option 3: Docker (Cross-platform)

Best for consistent environment across all platforms, testing, or deployment. Navigate to tools directory and run Docker build.

**Windows:**
```powershell
cd tools
.\install-python-docker.ps1
```

**Linux/macOS:**
```bash
cd tools && ./install-python-docker.sh
```

Docker approach:
- Creates clean Ubuntu 22.04 image
- Installs Python and all dependencies in container
- No host system pollution
- Perfect reproducibility across machines
- Ideal for CI/CD pipelines

**Which option to choose?**
- **Windows native**: Fastest for development, integrates with Windows tools
- **Linux/macOS native**: Fastest for development, uses system Python
- **Docker**: Slowest to build, but perfectly isolated and reproducible

All three methods produce the same working environment with identical dependencies!

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
