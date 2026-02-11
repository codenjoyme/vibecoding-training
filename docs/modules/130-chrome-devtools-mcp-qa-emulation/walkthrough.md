# AI-Powered QA with Chrome DevTools MCP - Hands-on Walkthrough

In Module 120, you created a web application prototype. Now you'll supercharge your development workflow by giving your AI assistant **eyes and hands** in the browser. With Chrome DevTools MCP, your AI agent can inspect elements, click buttons, fill forms, take screenshots, and verify functionality—just like a human QA engineer.

The real power comes from **hot reload**: when the agent fixes code, changes appear instantly in the browser, and the agent immediately tests them. This creates a rapid development-testing loop that gradually builds automated regression tests.

## Prerequisites

Before starting, ensure you have:
- Completed [Module 120: Rapid POC Prototyping](../120-rapid-poc-prototyping/about.md)
- Working web application in `work/120-task/` directory
- VS Code or Cursor IDE with MCP integration enabled
- Internet connection for installing Chrome DevTools MCP

## What We'll Build

In this walkthrough, you'll:
- Install Chrome browser (if not already installed)
- Configure Chrome DevTools MCP server in your IDE
- Choose a new feature to add to your web application
- Let AI agent develop the feature
- **Agent autonomously tests the feature in browser**
- Agent catches bugs and fixes them with instant feedback
- Agent creates test scenario markdown for future regression
- Experience the full hot-reload development cycle

**Key insight:** The more tools we give the agent (browser automation, element inspection, screenshot capture), the more independent it becomes. Combined with hot reload, the agent enters a self-correcting loop where it can develop, test, fix, and verify—all autonomously.

**Time required:** 20-25 minutes

---

## Part 1: Chrome Browser Installation

### What We'll Do

Verify Chrome is installed, or install it if missing. Chrome DevTools MCP requires Google Chrome browser.

---

### Step 1: Check if Chrome is Installed

**Windows:**
1. Press Start menu
2. Type "Chrome"
3. If "Google Chrome" appears → already installed, skip to Part 2
4. If not found → continue to Step 2

**macOS:**
1. Open Spotlight (Cmd + Space)
2. Type "Chrome"
3. If "Google Chrome" appears → already installed, skip to Part 2
4. If not found → continue to Step 2

**Linux:**
```bash
google-chrome --version
```

If you see version number → already installed, skip to Part 2  
If "command not found" → continue to Step 2

---

### Step 2: Install Chrome (if needed)

**Windows:**

1. Navigate to: https://www.google.com/chrome/
2. Click **Download Chrome**
3. Run `ChromeSetup.exe` (~2 MB installer)
4. Installer downloads full Chrome (~100 MB) during installation
5. Installation completes automatically
6. Chrome opens automatically after installation

**macOS:**

1. Navigate to: https://www.google.com/chrome/
2. Click **Download Chrome**
3. Download completes: `googlechrome.dmg` (~100 MB)
4. Open the `.dmg` file
5. Drag Chrome icon to Applications folder
6. Open Applications folder
7. Double-click Google Chrome
8. Click **Open** when prompted

**Linux (Debian/Ubuntu):**

```bash
# Download Chrome .deb package
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install Chrome
sudo dpkg -i google-chrome-stable_current_amd64.deb

# Fix dependencies if needed
sudo apt-get install -f

# Verify installation
google-chrome --version
```

**Other Linux distributions:**
- **Fedora**: Download .rpm from https://www.google.com/chrome/ and install with `sudo dnf install ./google-chrome-stable_current_x86_64.rpm`
- **Arch**: `yay -S google-chrome` or use Chromium: `sudo pacman -S chromium`

---

### Step 3: Verify Chrome Installation

Open Chrome and navigate to: `chrome://version`

You should see Chrome version information.

**Chrome is ready! ✅** Continue to Part 2.

---

## Part 2: Configure Chrome DevTools MCP Server

### What We'll Do

Add Chrome DevTools MCP server to your IDE configuration. The configuration differs between VS Code and Cursor.

---

### Step 1: Identify Your IDE

**Which IDE are you using?**
- **VS Code** (Microsoft's editor) → Follow "For VS Code" instructions
- **Cursor** (AI-focused fork of VS Code) → Follow "For Cursor" instructions

---

### Step 2: Configure MCP Server

**For VS Code:**

1. Open VS Code
2. Open Command Palette: `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
3. Type: **"MCP: Edit Config"** and select it
4. This opens `cline_mcp_settings.json` file

**Add Chrome DevTools MCP server** to the `mcpServers` section:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

**If you already have other MCP servers**, add chrome-devtools to the existing list:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem@latest", "c:/workspace/hello-genai"]
    },
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

Save the file (`Ctrl+S` or `Cmd+S`).

---

**For Cursor:**

1. Open Cursor
2. Open Command Palette: `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
3. Type: **"Cursor Settings: MCP"** or navigate to Settings → MCP
4. This opens MCP configuration file

**Important:** Cursor uses **`servers`** key instead of `mcpServers`.

**Add Chrome DevTools MCP server:**

```json
{
  "servers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

**If you already have other MCP servers**, add chrome-devtools to the existing list:

```json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem@latest", "c:/workspace/hello-genai"]
    },
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

Save the file.

---

### Step 3: Restart IDE

**Close and reopen your IDE** for MCP configuration to take effect.

---

### Step 4: Verify MCP Server is Available

1. Open AI chat in your IDE
2. Look for available tools/integrations
3. You should see Chrome DevTools MCP tools available

**Ask your AI assistant:**
```
Do you have access to Chrome DevTools MCP tools? List what you can do with them.
```

**Expected response includes capabilities like:**
- Open browser and navigate to URLs
- Inspect elements and DOM structure
- Click buttons and interact with page
- Fill forms and input fields
- Take screenshots
- Read console logs and errors
- Execute JavaScript on the page

**If tools are available → MCP server configured successfully! ✅**

---

## Part 3: Prepare Your Application

### What We'll Do

Ensure your web application from Module 120 is ready for development and testing.

---

### Step 1: Navigate to Your Project

Open terminal in your IDE and navigate to the project:

```bash
# Windows
cd c:/workspace/hello-genai/work/120-task

# macOS/Linux
cd ~/workspace/hello-genai/work/120-task
```

---

### Step 2: Verify Project Structure

Check that you have the basic structure from Module 120:

```
work/120-task/
├── index.html
├── style.css (or styles.css)
├── script.js (or app.js)
└── package.json (if using build tools)
```

**If your project uses a development server** (like Vite, webpack-dev-server, etc.), ensure you know how to start it.

**If your project is plain HTML/CSS/JS**, you can serve it with a simple HTTP server.

---

### Step 3: Start Your Application

**Option A: If you have a dev server configured (e.g., Vite):**

```bash
npm run dev
```

**Option B: If plain HTML, start simple HTTP server:**

```bash
# Using Python (if installed)
python -m http.server 8080

# Or using Node.js http-server
npx http-server -p 8080
```

**Your application should be running at:** http://localhost:8080 (or similar port shown in terminal)

---

### Step 4: Verify Application Loads

1. Open Chrome browser
2. Navigate to: http://localhost:8080 (or your server's address)
3. Verify your application loads correctly

**Application is running! ✅** Keep it running throughout this module.

---

## Part 4: Choose a Feature to Add

### What We'll Do

Select a new feature to add to your web application. This feature will be developed and tested by the AI agent.

---

### Step 1: Review Feature Options

Here are feature ideas suitable for AI agent testing:

**1. Contact Form with Validation**
- Form fields: name, email, message
- Client-side validation (required fields, email format)
- Success message after submission
- Error messages for invalid inputs

**Why good for testing:**
- Multiple interaction points (input fields, submit button)
- Clear success/failure states
- Validation edge cases to verify

---

**2. Dark/Light Theme Toggle**
- Toggle button in header/navbar
- Switches between dark and light color schemes
- Saves preference in localStorage
- Persists across page reloads

**Why good for testing:**
- Simple interaction (click button)
- Visual verification (colors change)
- State persistence to verify

---

**3. Simple TODO List**
- Add new tasks with input field
- Mark tasks as complete (checkbox or click)
- Delete tasks
- Tasks persist in localStorage

**Why good for testing:**
- CRUD operations to verify
- Multiple user flows (add, complete, delete)
- State management to test

---

**4. Image Gallery with Modal**
- Grid of thumbnail images
- Click thumbnail opens full-size in modal overlay
- Close modal with X button or outside click
- Navigation arrows (previous/next)

**Why good for testing:**
- Multiple interaction methods
- Modal open/close states
- Keyboard navigation edge cases

---

**5. Your Own Idea**
- Think of a feature your application needs
- Should have clear user interactions
- Should have verifiable outcomes

---

### Step 2: Choose Your Feature

**Decide which feature you want to add.**

For this walkthrough example, we'll use **Contact Form with Validation** in instructions. If you choose a different feature, adapt the testing scenarios accordingly.

**Note your choice** and continue to Part 5.

---

## Part 5: Develop Feature with AI Agent

### What We'll Do

Ask your AI agent to implement the chosen feature. The agent will write the code, but we won't manually test it yet—that's the agent's job in Part 6.

---

### Step 1: Provide Feature Requirements

Open AI chat and provide detailed requirements for your chosen feature.

**Example prompt for Contact Form:**

```
I want to add a Contact Form feature to my web application.

Requirements:
1. Add a contact form to index.html with these fields:
   - Name (text input, required)
   - Email (email input, required, must be valid email format)
   - Message (textarea, required, minimum 10 characters)
   - Submit button

2. Add client-side validation:
   - Show error message below field if validation fails
   - Error messages: "Name is required", "Valid email required", "Message must be at least 10 characters"
   - Disable submit button if form is invalid

3. On successful submission:
   - Show success message: "Thank you! Your message has been received."
   - Clear the form
   - Hide success message after 3 seconds

4. Style the form to match existing design
   - Form should be responsive
   - Error messages in red
   - Success message in green

5. Add form to the main content area of index.html

Current application is running at http://localhost:8080
Files are in: c:/workspace/hello-genai/work/120-task/

Please implement this feature and let me know when done.
```

**Adjust the file path** for your OS (Windows vs macOS/Linux).

---

### Step 2: Wait for Implementation

The AI agent will:
- Read your current files
- Add HTML for the form
- Add CSS for styling
- Add JavaScript for validation and submission handling
- Save the changes

**Important:** If you have hot reload enabled (Vite dev server, live-server, etc.), changes will appear automatically in the browser. Otherwise, refresh the page.

---

### Step 3: Verify Files Were Modified

Agent should report which files were changed:

**Expected changes:**
- `index.html` - added contact form HTML
- `style.css` - added form styles
- `script.js` - added validation and submission logic

**Don't manually test yet!** That's what we'll automate in Part 6.

---

## Part 6: AI Agent Tests the Feature

### What We'll Do

Now comes the powerful part: **the AI agent autonomously tests the feature** it just built using Chrome DevTools MCP.

---

### Step 1: Request Agent Testing

**Ask your AI agent:**

```
Now test the Contact Form feature you just implemented using Chrome DevTools MCP.

Test these scenarios:
1. Navigate to http://localhost:8080
2. Verify the contact form is visible
3. Test empty form submission - should show error messages
4. Test invalid email format - should show email error
5. Test short message (less than 10 chars) - should show message error
6. Test valid submission - should show success message and clear form
7. Take screenshots of error states and success state

Create a markdown file `work/120-task/test-contact-form.md` documenting:
- Each test scenario
- Expected result
- Actual result (pass/fail)
- Screenshots (reference them)
- Any bugs found

If you find bugs, fix them and re-test.
```

**Adjust the URL and file paths** for your environment.

---

### Step 2: Watch Agent Work

The agent will:

1. **Open Chrome with DevTools** connection
2. **Navigate to your app** at http://localhost:8080
3. **Inspect the page** to find form elements
4. **Test Scenario 1:** Click submit with empty form
   - Verify error messages appear
   - Take screenshot
5. **Test Scenario 2:** Enter invalid email
   - Verify email validation error
   - Take screenshot
6. **Test Scenario 3:** Enter short message
   - Verify message length error
   - Take screenshot
7. **Test Scenario 4:** Fill valid data and submit
   - Verify success message appears
   - Verify form clears
   - Take screenshot
8. **Document results** in markdown file
9. **If bugs found:** Fix code and re-test

---

### Step 3: Review Test Documentation

Once agent completes testing, open the test documentation:

**File:** `work/120-task/test-contact-form.md`

**Expected structure:**

```markdown
# Contact Form - Test Scenarios

## Test Run: [Date/Time]

### Scenario 1: Empty Form Submission
**Expected:** Error messages appear for all required fields  
**Actual:** ✅ PASS - All error messages displayed correctly  
**Screenshot:** `screenshots/contact-form-empty-errors.png`

### Scenario 2: Invalid Email Format
**Expected:** "Valid email required" error appears  
**Actual:** ✅ PASS - Email validation works  
**Screenshot:** `screenshots/contact-form-invalid-email.png`

### Scenario 3: Short Message (< 10 characters)
**Expected:** "Message must be at least 10 characters" error  
**Actual:** ✅ PASS - Message length validation works  
**Screenshot:** `screenshots/contact-form-short-message.png`

### Scenario 4: Valid Form Submission
**Expected:** Success message appears, form clears  
**Actual:** ✅ PASS - Submission works correctly  
**Screenshot:** `screenshots/contact-form-success.png`

## Summary
- Total Tests: 4
- Passed: 4
- Failed: 0
- Bugs Found: 0
```

**If bugs were found**, agent should have noted them and fixed them.

---

### Step 4: Verify Screenshots

Check that screenshots were saved (referenced in test documentation):

```
work/120-task/screenshots/
├── contact-form-empty-errors.png
├── contact-form-invalid-email.png
├── contact-form-short-message.png
└── contact-form-success.png
```

Open screenshots to verify agent captured the correct states.

---

## Part 7: Experience Hot Reload Testing Loop

### What We'll Do

Experience the power of hot reload: make a change, watch it appear instantly in the browser, and have the agent immediately verify it.

---

### Step 1: Introduce a Bug Intentionally

Let's simulate a real development scenario where a bug is introduced.

**Ask your AI agent:**

```
Modify the contact form validation to have a bug:
- Change the email validation regex to allow invalid emails
- For example, make it accept "test@" as a valid email

This simulates a bug being accidentally introduced.
Save the change.
```

---

### Step 2: Agent Detects the Bug

**Ask agent to re-run tests:**

```
Re-run the contact form tests. 
Document if the email validation test now fails.
```

**Expected:**
- Agent navigates to page (changes are already visible due to hot reload)
- Tests email validation
- **Scenario 2 FAILS:** Invalid email "test@" is accepted
- Agent documents the failure

---

### Step 3: Agent Fixes the Bug

**Ask agent:**

```
Fix the email validation bug you found.
Restore proper email validation regex.
Re-run tests to verify the fix.
```

**What happens:**
1. Agent fixes the code
2. Hot reload updates the browser automatically
3. Agent re-tests immediately
4. Scenario 2 now passes
5. Agent updates test documentation

**This is the power of hot reload + AI testing:** Near-instant feedback loop from code → browser → test → fix → verify.

---

## Part 8: Build Regression Test Suite

### What We'll Do

Turn the test documentation into a reusable regression test suite that the agent can run anytime.

---

### Step 1: Create Master Test Suite

**Ask your AI agent:**

```
Create a comprehensive test suite document: `work/120-task/regression-tests.md`

This file should:
1. List all features in the application
2. For each feature, document test scenarios
3. Include commands for running tests
4. Format as checklist so I can manually verify if needed

For now, it should include the Contact Form test scenarios.
```

**Expected file structure:**

```markdown
# Regression Test Suite - Web Application

Last updated: [Date]

## How to Run Tests

1. Start application: `npm run dev` or `npx http-server -p 8080`
2. Open Chrome
3. Ask AI agent to run test scenarios below using Chrome DevTools MCP

## Feature 1: Contact Form

### Test Scenarios

- [ ] Empty form submission shows all error messages
- [ ] Invalid email format shows email validation error  
- [ ] Short message (< 10 chars) shows length error
- [ ] Valid submission shows success message
- [ ] Success message disappears after 3 seconds
- [ ] Form clears after successful submission

### Test Commands for AI Agent

```
Test the Contact Form feature at http://localhost:8080:
1. Click submit with empty form - verify errors
2. Enter "test@" email - verify email error
3. Enter "short" message - verify length error
4. Fill valid data - verify success and form clear
Document results.
```

## Feature 2: [Next Feature]

[To be added when implemented]

---

## Test History

### Run 1: [Date/Time]
- Contact Form: ✅ All tests passed
- See: `test-contact-form.md`

### Run 2: [Date/Time]
- Contact Form: ❌ Email validation bug found
- Bug fixed and verified
- See: `test-contact-form.md` (updated)
```

---

### Step 2: Commit Tests to Git

Preserve your test documentation in version control.

**Ask your AI agent:**

```
Commit the test documentation to Git:
- test-contact-form.md
- regression-tests.md
- screenshots/ folder

Use commit message: "Add automated QA test scenarios for Contact Form"
```

**Why this matters:**
- Test scenarios are preserved alongside code
- Future developers can re-run tests
- Test history tracks what was verified when
- Gradual build-up of comprehensive test coverage

---

## Part 9: Advanced QA Patterns

### What We Learned

You've now seen the complete AI-powered QA workflow:
1. Agent develops feature
2. Agent tests feature in browser
3. Agent documents test scenarios
4. Agent catches and fixes bugs
5. Tests become regression suite
6. Hot reload enables rapid iteration

### Scaling This Workflow

**Pattern 1: Test-Driven Development**

Reverse the order:
1. Write test scenarios first
2. Ask agent to implement feature that passes tests
3. Agent develops until all tests pass

**Pattern 2: Continuous Regression Testing**

Before deploying:
```
Run all regression tests from regression-tests.md
Document any failures
Fix failures before deployment
```

**Pattern 3: Visual Regression Testing**

```
Take baseline screenshots of all pages
After changes, take new screenshots
Compare screenshots for unexpected visual changes
```

**Pattern 4: Performance Testing**

```
Use Chrome DevTools to measure:
- Page load time
- JavaScript execution time
- Network requests
- Memory usage
Document performance baselines
```

**Pattern 5: Accessibility Testing**

```
Use Chrome DevTools to verify:
- ARIA labels present
- Keyboard navigation works
- Color contrast meets standards
- Screen reader compatibility
```

---

## Part 10: Real-World QA Workflow

### What We'll Do

See how this fits into a complete development workflow.

---

### Typical Development Session

**1. Morning: Start with regression tests**
```
Ask agent: "Run all regression tests and report status"
```

**2. Develop new feature**
```
Define requirements
Agent implements feature
Agent creates test scenarios
Agent runs tests and fixes bugs
Commit feature + tests together
```

**3. Before lunch: Run regression tests again**
```
Ensure new feature didn't break existing features
```

**4. Afternoon: Bug fix**
```
User reports bug
Write test scenario that reproduces bug
Agent fixes bug
Verify test now passes
Add test to regression suite
```

**5. End of day: Final regression test**
```
Run full test suite
Commit any fixes
Deploy if all tests pass
```

---

### Team Workflow

**Developer A:**
- Implements Feature X
- Creates test scenarios
- Commits code + tests

**Developer B:**
- Pulls latest code
- Runs regression tests
- All tests pass → safe to start work
- Implements Feature Y
- Runs regression tests (includes Feature X tests)
- Ensures Feature Y doesn't break Feature X

**QA Engineer:**
- Reviews test scenarios for completeness
- Adds edge cases developers missed
- Runs comprehensive regression before release
- Documents bugs with test scenarios
- Developers fix bugs using test scenarios as specification

---

## Success Criteria

You've successfully completed this module when you can check off:

✅ Chrome browser installed and verified  
✅ Chrome DevTools MCP configured in VS Code or Cursor  
✅ MCP server connection verified  
✅ New feature added to web application from Module 120  
✅ AI agent autonomously tested the feature using browser automation  
✅ Test scenarios documented in markdown file  
✅ Screenshots captured for test evidence  
✅ Bug intentionally introduced and agent detected it  
✅ Agent fixed bug and re-verified with tests  
✅ Regression test suite created  
✅ Test documentation committed to Git  
✅ Understanding of hot reload + AI testing workflow  

---

## Understanding Check

Answer these questions to verify comprehension:

1. **What is Chrome DevTools MCP and why is it powerful for AI agents?**
   
   Expected answer: Chrome DevTools MCP is a Model Context Protocol server that gives AI agents control over Chrome browser through DevTools API. It's powerful because it gives agents "eyes and hands"—agents can see the page, interact with elements, take screenshots, read console logs, and verify functionality just like a human tester. Combined with AI's ability to understand requirements and write test scenarios, it enables autonomous QA.

2. **What is the difference between `mcpServers` (VS Code) and `servers` (Cursor)?**
   
   Expected answer: VS Code uses the key `mcpServers` in its MCP configuration file (cline_mcp_settings.json), while Cursor uses `servers` in its MCP config. Both serve the same purpose—listing available MCP servers—but you must use the correct key for your IDE or the configuration won't work. Everything else about the configuration is identical.

3. **Why is hot reload crucial for the AI testing workflow?**
   
   Expected answer: Hot reload automatically reflects code changes in the browser without manual refresh. This creates a rapid feedback loop: agent writes code → changes appear instantly → agent tests immediately → agent sees results and can fix bugs right away. Without hot reload, there would be delays for manual refreshes, breaking the autonomous testing flow and slowing iteration.

4. **Why should test scenarios be documented in markdown files?**
   
   Expected answer: Markdown test documentation serves multiple purposes: (1) Creates regression test suite for future runs, (2) Provides clear specification of expected behavior, (3) Documents what was tested and when, (4) Can be version-controlled alongside code, (5) Human-readable for manual review, (6) AI can parse and execute tests automatically, (7) Gradual accumulation builds comprehensive QA coverage over time.

5. **How does this AI testing workflow differ from traditional manual QA?**
   
   Expected answer: Traditional QA: developer writes code → hands off to QA → QA manually tests → reports bugs → developer fixes → cycle repeats (days/weeks). AI QA: developer/agent writes code → agent immediately tests → agent documents results → agent fixes bugs → agent re-verifies (minutes). AI QA is faster, happens continuously during development, catches bugs immediately, and documentation is automatic. Both have value—AI for rapid iteration, humans for subjective judgment.

6. **What are the limitations of AI-powered browser testing?**
   
   Expected answer: AI testing limitations: (1) Can't evaluate subjective aspects (design aesthetics, UX feel), (2) May miss edge cases humans would intuit, (3) Depends on clear requirements—garbage in, garbage out, (4) Can't test on real devices (mobile, different browsers without setup), (5) May not understand business context, (6) Requires well-structured code for effective testing. Best used in combination with human QA, not as complete replacement.

7. **How would you use this workflow for a bug reported by a user?**
   
   Expected answer: (1) Write test scenario that reproduces the user-reported bug, (2) Run test with agent—should fail, confirming bug exists, (3) Ask agent to fix the code, (4) Agent re-runs test—should now pass, (5) Add test scenario to regression suite to prevent bug from reoccurring, (6) Commit fix + test together, (7) Deploy knowing bug is fixed and won't regress. The test scenario becomes permanent documentation of the bug and its fix.

---

## Troubleshooting

### Problem: Chrome DevTools MCP tools not appearing in IDE

**Symptoms:** Agent says it doesn't have access to Chrome DevTools capabilities

**Solutions:**
1. **Verify MCP configuration:**
   - VS Code: Check `mcpServers` key exists in config
   - Cursor: Check `servers` key exists (not `mcpServers`)
2. **Restart IDE completely** (not just reload window)
3. **Check npx can run:**
   ```bash
   npx chrome-devtools-mcp@latest --help
   ```
   Should download and show help message
4. **Check IDE MCP logs** for connection errors
5. **Try manual MCP server start:**
   ```bash
   npx -y chrome-devtools-mcp@latest
   ```
   Should start without errors

---

### Problem: Agent can't connect to Chrome browser

**Symptoms:** "Failed to connect to Chrome" or "No debugging targets found"

**Solutions:**
1. **Ensure Chrome is closed completely** before agent tries to connect
2. **Try launching Chrome manually with remote debugging:**
   ```bash
   # Windows
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
   
   # macOS
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
   
   # Linux
   google-chrome --remote-debugging-port=9222
   ```
3. **Check if port 9222 is already in use:**
   ```bash
   # Windows
   netstat -ano | findstr :9222
   
   # macOS/Linux
   lsof -i :9222
   ```
4. **Disable Chrome extensions** that might interfere with DevTools Protocol
5. **Update Chrome to latest version**

---

### Problem: Hot reload not working

**Symptoms:** Code changes don't appear in browser automatically

**Solutions:**
1. **Check if dev server supports hot reload:**
   - Vite: Has hot reload built-in
   - webpack-dev-server: Check config has `hot: true`
   - Plain HTML: Use live-server: `npx live-server --port=8080`
2. **Clear browser cache:**
   - Chrome DevTools → Network tab → Check "Disable cache"
   - Or hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (macOS)
3. **Check server console for errors** during file changes
4. **Verify file watching is working:**
   - Make a visible change (add text to HTML)
   - Check if server logs show file change detection

---

### Problem: Agent can't find form elements on page

**Symptoms:** "Element not found" errors during testing

**Solutions:**
1. **Verify page fully loaded:**
   - Add delay: "Wait 2 seconds after page load"
   - Wait for specific element: "Wait until contact form is visible"
2. **Check element selectors:**
   - Use specific IDs: `<form id="contact-form">`
   - Avoid dynamic selectors that change
3. **View page source to verify HTML:**
   ```
   Ask agent: "Show me the HTML source of http://localhost:8080"
   ```
4. **Take screenshot to debug:**
   ```
   Ask agent: "Navigate to http://localhost:8080 and take screenshot"
   ```
5. **Check JavaScript errors in console:**
   ```
   Ask agent: "Check browser console for errors on the page"
   ```

---

### Problem: Screenshots not saving

**Symptoms:** Test documentation references screenshots but files don't exist

**Solutions:**
1. **Create screenshots directory manually:**
   ```bash
   mkdir -p work/120-task/screenshots
   ```
2. **Ask agent explicitly to save screenshots:**
   ```
   "Take screenshot and save it to work/120-task/screenshots/test-name.png"
   ```
3. **Check file permissions** on screenshots directory
4. **Verify path is correct** for your OS:
   - Windows: `c:/workspace/hello-genai/work/120-task/screenshots/`
   - macOS/Linux: `~/workspace/hello-genai/work/120-task/screenshots/`

---

### Problem: Agent tests pass but manual testing shows bugs

**Symptoms:** Agent reports tests pass, but you find bugs when testing manually

**Root cause:** Test scenarios not comprehensive enough or agent misunderstood requirements

**Solutions:**
1. **Review test scenarios for completeness:**
   - Are all user interactions tested?
   - Are edge cases covered?
   - Are error states verified?
2. **Add specific test for the bug you found:**
   ```
   "Add test scenario: [describe specific bug]"
   ```
3. **Make requirements more explicit:**
   - Instead of: "Form should validate"
   - Use: "Email field must reject 'test@' and show error: 'Valid email required'"
4. **Ask agent to show evidence:**
   ```
   "Show me screenshots proving test X passed"
   ```
5. **Consider human review** of critical test paths

---

## Next Steps

**Congratulations!** You've mastered AI-powered QA with browser automation. Here's what comes next:

1. **Expand test coverage**
   
   Add tests for all features:
   - Create test scenarios for existing features
   - Build comprehensive regression suite
   - Automate testing before every commit

2. **Integrate with CI/CD**
   
   Run tests automatically:
   - Configure tests to run on git push
   - Block merges if tests fail
   - Generate test reports for team visibility

3. **Explore advanced DevTools features**
   
   Leverage more Chrome capabilities:
   - Performance profiling
   - Network request inspection
   - Memory leak detection
   - Mobile device emulation

4. **Combine with other MCP servers**
   
   Create powerful workflows:
   - Filesystem MCP for reading test data
   - GitHub MCP for creating issues from test failures
   - Multiple browser instances for parallel testing

5. **Continue to Module 140: Advanced MCP Integration in POC**
   
   Learn how to combine multiple MCP servers for even more powerful automation workflows.

---

## Additional Resources

- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Chrome DevTools MCP GitHub](https://github.com/modelcontextprotocol/servers/tree/main/src/chrome-devtools)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Hot Module Replacement (Vite)](https://vitejs.dev/guide/features.html#hot-module-replacement)
- [Testing Best Practices](https://kentcdodds.com/blog/common-testing-mistakes)

---

**Ready to continue your training?** Head to [Module 140: Advanced MCP Integration in POC](../140-advanced-mcp-integration-in-poc/about.md)
