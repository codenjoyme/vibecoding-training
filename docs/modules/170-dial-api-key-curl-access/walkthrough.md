# DIAL API Key and cURL Access - Hands-on Walkthrough

In this walkthrough, you'll request your EPAM AI DIAL API key and make your first direct call to an AI model using cURL. This is the foundation for programmatic access to EPAM's AI infrastructure.

## Prerequisites

- Active EPAM employee account with access to internal portals
- PowerShell (Windows) or Terminal (macOS/Linux) access
- **VPN connection to EPAM internal network is required** (DIAL is only accessible from EPAM network)

## Part 1: Understanding DIAL and API Keys

EPAM AI DIAL is EPAM's internal AI platform that provides access to various AI models (GPT-4, GPT-4o, Claude, etc.) through a unified interface. Instead of clicking in a chat UI, you can send requests programmatically using an API key.

**Why would you need programmatic access?** As a manager or technical lead, you might need to:
- Automate document analysis and report generation for your team
- Build custom tools that integrate AI into your project workflows
- Process large batches of data (e.g., analyze 100 customer feedback forms)
- Create prototypes and proof-of-concepts to evaluate AI capabilities for your business case
- Integrate AI into existing applications and internal tools
- Control costs and usage by implementing your own rate limiting and logging

**What is an API key?** Think of it as a password that identifies you when your scripts talk to DIAL servers. It's a long string like `57bde47684bd39aebc382b4ca4638abd` that you include in every request.

**Why do we need it?** To track usage, enforce security policies, and ensure compliance with EPAM's AI Policy.

**⚠️ Security Warning:** Your API key is like a password - keep it secret! Anyone with your key can make requests to DIAL on your behalf, which means:
- They can consume your quota and potentially exceed usage limits
- All their actions will be logged under your name
- You'll be held responsible for any policy violations they commit
- Your account could be suspended for misuse

Never commit API keys to Git repositories, share them in chats, or store them in plain text files. We'll cover secure storage methods in later modules.

## Part 2: Requesting Your API Key

1. Open your browser and navigate to EPAM AI DIAL:
   ```
   https://chat.lab.epam.com/
   ```

2. Scroll to the bottom of the chat interface

3. Look for the footer text that mentions:
   ```
   Usage of EPAM AI DIAL must comply with the Prohibited Uses and Approval Steps in EPAM’s AI Policy. The information you share here is not disclosed to third-party companies. However, we anonymize and log all interactions for research purposes. >>> Request API key <<<. Report an issue. Version 0.40.5 Change log
   ```

4. Click on **"Request API key"** link

5. You'll be redirected to EPAM Support Portal with a pre-filled ticket template

6. In the ticket, provide:
   - **Reason for access:** "Testing AI model integration for [your project/learning]"
   - **Intended use case:** "Development and testing with langchain integration"
   - **Your manager's approval:** (if required by your organization)

7. Submit the ticket

8. Wait for approval - typically takes 1-3 business days.

9. You'll receive an email with your API key that looks like:
   ```
   Your DIAL API Key: 57bde47684bd39aebc382b4ca4638abd
   Endpoint: https://ai-proxy.lab.epam.com
   ```

**Important:** Keep your API key secret! Don't commit it to Git repositories or share it publicly.

## Part 3: Understanding the DIAL REST API

Before making requests, let's understand what we're doing:

**REST API** is a way for programs to talk to servers using HTTP requests (the same protocol your browser uses). 

**Key components:**
- **Endpoint URL:** Where to send requests (`https://ai-proxy.lab.epam.com`)
- **API Key:** Your authentication credential
- **Request body:** The question or prompt you're sending
- **Response:** The AI model's answer

**How it works:**
1. Your script sends an HTTP POST request to DIAL endpoint
2. Request includes your API key in headers (for authentication)
3. Request includes your prompt in JSON format
4. DIAL forwards your request to the AI model
5. Model processes and generates response
6. DIAL sends response back to you

### What is DIAL API?

DIAL is EPAM's platform that provides **unified** access to multiple AI models through a simple REST API. It acts as a gateway to various AI providers including OpenAI, Anthropic, Google and others.

**Key Benefits:**
- Single API interface for multiple AI providers
- Consistent parameter structure across different models
- Easy switching between models without code changes

> **📚 Full API Documentation:**
> See all supported parameters for DIAL `/chat/completions` API:
> [https://dialx.ai/dial_api#operation/sendChatCompletionRequest](https://dialx.ai/dial_api#operation/sendChatCompletionRequest)

### Available Models

DIAL API provides access to three major AI providers:

| Provider | Models |
|----------|--------|
| **OpenAI** | • `gpt-4o`<br>• `gpt-4.1-mini-2025-04-14`<br>• `gpt-4o-mini-2024-07-18` |
| **Anthropic (Claude)** | • `anthropic.claude-v3-haiku`<br>• `claude-3-7-sonnet@20250219`<br>• `claude-sonnet-4@20250514` |
| **Google (Gemini)** | • `gemini-2.5-pro`<br>• `gemini-2.5-flash`<br>• `gemini-2.0-flash-lite` |

**To use a specific model**, replace the model name in your endpoint URL:
```
https://ai-proxy.lab.epam.com/openai/deployments/{MODEL_NAME}/chat/completions
```

Example with Claude:
```
https://ai-proxy.lab.epam.com/openai/deployments/claude-sonnet-4@20250514/chat/completions
```

## Part 4: Testing with cURL

cURL is a command-line tool that makes HTTP requests. It's pre-installed on most systems.

1. Open PowerShell (Windows) or Terminal (macOS/Linux)

2. Verify cURL is available:
   ```powershell
   curl --version
   ```
   
   You should see version information like `curl 8.x.x`

3. Create a test directory:
   ```powershell
   mkdir work\170-task
   cd work\170-task
   ```

4. Create a simple cURL test script. Copy the script from module tools:
   
   **For Windows (PowerShell):**
   Navigate to the module tools directory and examine `test-dial-windows.ps1`:
   ```powershell
   # View the script content
   Get-Content docs\modules\170-dial-api-key-curl-access\tools\test-dial-windows.ps1
   ```

   **For Linux/macOS (Bash):**
   Navigate to the module tools directory and examine `test-dial-linux.sh`:
   ```bash
   # View the script content
   cat docs/modules/170-dial-api-key-curl-access/tools/test-dial-linux.sh
   ```

5. Copy the appropriate script to your test directory:
   
   **Windows:**
   ```powershell
   Copy-Item docs\modules\170-dial-api-key-curl-access\tools\test-dial-windows.ps1 work\dial-test\
   ```
   
   **Linux/macOS:**
   ```bash
   cp docs/modules/170-dial-api-key-curl-access/tools/test-dial-linux.sh work/dial-test/
   chmod +x work/dial-test/test-dial-linux.sh
   ```

6. Open the script in a text editor and replace `YOUR_API_KEY_HERE` with your actual API key

7. Run the script:
   
   **Windows:**
   ```powershell
   .\test-dial.ps1
   ```
   
   **Linux/macOS:**
   ```bash
   ./test-dial.sh
   ```

8. You should see output like:
   ```json
   {
     "id": "chatcmpl-...",
     "object": "chat.completion",
     "created": 1738713600,
     "model": "gpt-4o-mini-2024-07-18",
     "choices": [
       {
         "message": {
           "role": "assistant",
           "content": "Ahoy, matey! Artificial Intelligence, or AI fer short, be the treasure o' the modern age..."
         }
       }
     ]
   }
   ```

**What just happened?**
- Your script sent an HTTP POST request to DIAL
- Included your API key for authentication
- Sent prompt: "Tell me about artificial intelligence in the style of a pirate"
- DIAL forwarded to GPT-4o-mini model
- Model generated pirate-style response
- Response returned to your terminal

## Part 5: Understanding the Request Structure

Let's break down what's in the cURL command:

```bash
curl -X POST https://ai-proxy.lab.epam.com/openai/deployments/gpt-4o-mini-2024-07-18/chat/completions
```
- `-X POST` - Make a POST request (sending data)
- URL points to specific model deployment

```bash
-H "Content-Type: application/json"
```
- Header specifying we're sending JSON data

```bash
-H "api-key: YOUR_KEY"
```
- Header with your authentication key

```bash
-d '{
  "messages": [
    {"role": "user", "content": "Tell me about AI"}
  ]
}'
```
- The actual data being sent (your prompt)
- `messages` array can contain conversation history
- `role: user` means this is a human's message
- `content` is your actual question

## Part 6: Understanding DIAL API Parameters

DIAL API provides various parameters to control model behavior. Understanding these parameters allows you to fine-tune AI responses for your specific needs.

### 🔄 **stream** - Controls response delivery method

- **Default:** `false`
- **When to use streaming:** Real-time applications, chatbots, long responses
- **When to use non-streaming:** Batch processing, simple Q&A

### 🌡️ **temperature** - Controls creativity vs. consistency

- **Range:** 0.0 to 2.0
- **Default:** 1.0
- **Low values (0.0-0.3):** Deterministic, factual responses
- **Medium values (0.4-0.8):** Balanced creativity and consistency
- **High values (0.9-2.0):** Very creative, unpredictable responses

**Example:**
```json
{
  "messages": [{"role": "user", "content": "Explain AI"}],
  "temperature": 0.2
}
```

### 🎯 **top_p** - Nucleus Sampling (alternative to temperature)

- **Range:** 0.0 to 1.0
- **Default:** 1.0
- **How it works:**
  - `top_p: 0.1` = Consider only top 10% most likely tokens
  - `top_p: 0.5` = Consider tokens making up 50% of probability mass
  - `top_p: 1.0` = Consider all possible tokens

**⚠️ Recommendation:** Use either `temperature` OR `top_p`, not both

### 📏 **max_tokens** - Limits response length

- **Default:** No limit (model-dependent maximum)
- **Use cases:**
  - Short summaries: 50-100 tokens
  - Detailed explanations: 500-1000 tokens
  - Long-form content: 2000+ tokens

**Example:**
```json
{
  "messages": [{"role": "user", "content": "Summarize AI"}],
  "max_tokens": 100
}
```

### 🆕 **presence_penalty** - Encourages discussing new topics

- **Range:** -2.0 to 2.0
- **Default:** 0.0
- **Positive values:** Encourage novelty and new topics
- **Negative values:** Allow more repetition of concepts
- **How it works:** Penalizes tokens that have appeared before (yes/no basis)

**⚠️ Note:** This feature works only with OpenAI GPT models. According to the DIAL specification, you can use it with all models, but for those that do not support it, the parameter will be ignored.

### 🔁 **frequency_penalty** - Reduces repetitive word usage

- **Range:** -2.0 to 2.0
- **Default:** 0.0
- **Positive values:** Reduce word repetition
- **Negative values:** Increase word repetition
- **How it works:** Penalizes tokens proportionally to their frequency

**⚠️ Note:** This feature works only with OpenAI GPT models. According to the DIAL specification, you can use it with all models, but for those that do not support it, the parameter will be ignored.

### ⏹️ **stop** - Defines when to stop generation

- **Default:** `null`
- **Use cases:**
  - Structured output (stop at specific markers)
  - Dialogue systems (stop at speaker changes)
  - List generation (stop at natural breaks)

**Examples:**
```json
{
  "stop": ["\n", "END", "###"]
}
```

```json
{
  "stop": "DIAL"
}
```

### 🔢 **n** - Generate multiple response options

- **Default:** 1
- **Use cases:**
  - A/B testing different responses
  - Providing multiple creative options
  - Ensuring response quality through selection

**Example:**
```json
{
  "messages": [{"role": "user", "content": "Write a tagline"}],
  "n": 3
}
```

### 🌱 **seed** - Ensures reproducible results

- **Use cases:**
  - Testing and debugging
  - Consistent results across runs
  - Research and experimentation

**⚠️ Note:** This feature works only with OpenAI GPT and Gemini models. According to the DIAL specification, you can use it with all models, but for those that do not support it, the parameter will be ignored.

**Example:**
```json
{
  "messages": [{"role": "user", "content": "Generate code"}],
  "seed": 42
}
```

### Parameter Combinations Example

Here's a complete example with multiple parameters:

```json
{
  "messages": [
    {"role": "user", "content": "Write a professional email about AI benefits"}
  ],
  "temperature": 0.7,
  "max_tokens": 300,
  "presence_penalty": 0.5,
  "frequency_penalty": 0.3,
  "stop": ["\n\nBest regards"]
}
```

**Understanding DIAL API parameters allows you to:**
- Control AI model behavior precisely
- Optimize for specific use cases
- Create consistent, high-quality outputs
- Experiment with different AI providers seamlessly

**💡 Key Takeaway:** The key to mastering these parameters is experimentation. Try different combinations to see how they affect output for your specific use case.

## Part 7: Experiment with Different Prompts

Now that you have a working connection, try modifying the prompt:

1. Edit your script file

2. Change the content field to something else:
   ```json
   {"role": "user", "content": "Explain quantum computing in simple terms"}
   ```

3. Run the script again

4. Try a few more prompts:
   - "Write a haiku about coding"
   - "List 3 benefits of AI in business"
   - "Translate 'Hello, how are you?' to French"

5. Observe how responses vary based on your input

## Success Criteria

✅ Successfully submitted API key request ticket to EPAM support  
✅ Received API key via email from support team  
✅ Verified cURL is installed and accessible from command line  
✅ Created test script with API key configured  
✅ Successfully executed cURL request to DIAL endpoint  
✅ Received valid JSON response from AI model with generated content  
✅ Tested at least 3 different prompts and received different responses  
✅ Understand basic structure of REST API request (headers, body, endpoint)

## Troubleshooting

### Issue: "Request API key" link not visible on DIAL chat page

**Solution:** 
- Scroll to the very bottom of https://chat.lab.epam.com/
- Look for footer text about AI Policy compliance
- If still not visible, you may need VPN connection to EPAM network
- Alternatively, search EPAM Service Portal for "DIAL API access"

### Issue: API key request ticket rejected or requires manager approval

**Solution:**
- Contact your direct manager to approve AI tool usage
- Reference EPAM AI Policy document for approval process
- Provide clear justification: learning, development, or specific project needs
- Some departments require additional compliance training first

### Issue: cURL command not found

**Solution - Windows:**
```powershell
# cURL should be built into Windows 10+
# If missing, install via chocolatey:
choco install curl
```

**Solution - macOS:**
```bash
# cURL pre-installed, if missing:
brew install curl
```

**Solution - Linux:**
```bash
sudo apt-get install curl  # Ubuntu/Debian
sudo yum install curl      # CentOS/RHEL
```

### Issue: "Unauthorized" or "401" error response

**Solution:**
- Verify you copied the entire API key correctly (no extra spaces)
- Check that API key is placed in the `api-key` header field
- Confirm your API key is active (not expired or revoked)
- Ensure you're on EPAM network or connected to VPN

### Issue: "Connection refused" or "Could not resolve host"

**Solution:**
- Verify you're connected to EPAM VPN if working remotely
- Check endpoint URL is exactly: `https://ai-proxy.lab.epam.com`
- Test network connectivity: `ping ai-proxy.lab.epam.com`
- Check firewall settings aren't blocking outbound HTTPS

### Issue: Response is HTML error page instead of JSON

**Solution:**
- You may be hitting a proxy or firewall page
- Verify endpoint URL has `/openai/deployments/MODEL_NAME/chat/completions` path
- Check that model name is correct: `gpt-4o-mini-2024-07-18`
- Try different model deployment if this one is unavailable

### Issue: Response says "model not found" or "deployment not found"

**Solution:**
- DIAL model deployments may change over time
- Check current available models in DIAL chat interface dropdown
- Update script with correct deployment name
- Common alternatives: `gpt-4`, `gpt-4o`, `gpt-35-turbo`

## When to Use cURL for DIAL Access

**Good use cases:**
- Quick testing of API connectivity
- One-off queries without writing full program
- Debugging authentication issues
- CI/CD pipeline health checks
- Shell script automation for simple tasks

**When to use Python/langchain instead (Module 180):**
- Complex conversational flows with history
- Integration with other data sources
- Application development requiring code structure
- Processing multiple requests programmatically
- Need for error handling and retry logic

## Next Steps

Congratulations! You've successfully accessed DIAL via REST API. You can now send requests to AI models from command line.

Next module: **180-dial-langchain-python-integration** - Learn to build more sophisticated AI applications using Python and langchain framework with the same DIAL infrastructure.

---

**Key Takeaway:** API keys unlock programmatic access to AI models. cURL provides a simple way to test connectivity and make basic requests. For real applications, you'll want proper programming frameworks (covered in Module 180).
