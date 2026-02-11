# Visual Context with Screenshots - Hands-on Walkthrough

In this walkthrough, you'll learn how to effectively share visual context with your AI assistant using screenshots. This powerful technique helps AI see exactly what you see, enabling accurate guidance when software interfaces differ from AI's expectations.

## Prerequisites

- Completed Module 030 (Model Selection)
- Active AI assistant (VSCode with GitHub Copilot or Cursor)
- Agent Mode enabled
- Any web browser installed (Chrome, Firefox, Edge, Safari)
- Basic familiarity with taking screenshots on your OS

---

## Step-by-Step Instructions

### Part 1: Why Visual Context Matters

AI models are trained on data up to a certain date, and software interfaces change constantly. When you share screenshots:

1. **AI sees your actual interface** - not what it remembers from training data
2. **Reduces miscommunication** - no need for lengthy text descriptions
3. **Enables precise guidance** - AI can reference specific buttons, menus, icons
4. **Saves time** - one image conveys more than paragraphs of text
5. **Works across language barriers** - visual elements are universal

**Common scenarios where screenshots help:**
- New software version with changed UI
- AI suggests menu items you can't find
- Debugging visual layout issues
- Getting help with unfamiliar tools
- Showing error messages or unexpected behavior

### Part 2: Taking Screenshots on Your Operating System

You can capture either full screen or partial screen. Most operating systems provide built-in tools:

**Windows:**
- Full screen: Press `PrtScn` (Print Screen) - copies to clipboard
- Active window: Press `Alt + PrtScn` - copies active window to clipboard
- Snipping Tool: Search for "Snipping Tool" in Start menu - select area to capture
- Snip & Sketch: Press `Windows + Shift + S` - select area to capture

**macOS:**
- Full screen: Press `Cmd + Shift + 3` - saves to desktop
- Selected area: Press `Cmd + Shift + 4` - drag to select area, saves to desktop
- Window: Press `Cmd + Shift + 4`, then `Space`, click window - saves to desktop
- Screenshot app: Press `Cmd + Shift + 5` - opens screenshot toolbar

**Linux (Ubuntu/Debian):**
- Full screen: Press `PrtScn` - saves to Pictures folder
- Selected area: Press `Shift + PrtScn` - drag to select area
- Active window: Press `Alt + PrtScn` - saves active window
- Screenshot app: Search for "Screenshot" in applications

**Choose your preferred method** - you likely already have a favorite way to capture screens. Any method works as long as you can paste the image into the chat.

### Part 3: Sharing Screenshots with AI Assistant

Now let's learn how to share screenshots in your AI chat:

1. Take a screenshot using your preferred method (see Part 2)

1. Open your AI assistant chat window (GitHub Copilot Chat in VSCode or Cursor Chat)

1. Click in the message input field at the bottom

1. Paste the screenshot:
   - Windows/Linux: Press `Ctrl + V`
   - macOS: Press `Cmd + V`

1. The image should appear in the input field as a thumbnail or preview

1. Add your question or request in text along with the screenshot

1. Send the message (press Enter or click Send button)

1. AI will analyze both the screenshot and your text to provide contextual help

**Pro tip:** You can include multiple screenshots in one message if needed!

### Part 4: Practical Exercise - Browser Console with AI Help

Let's practice using screenshots to get AI help with a real task. We'll open the browser developer console and write "Hello World" - a common task that varies between browsers.

**What we'll do:**
- Open any web browser
- Take a screenshot of the browser window
- Ask AI to guide us to open the Developer Console
- AI will see our exact browser interface
- Follow AI's specific instructions for our browser
- Take another screenshot showing the console
- Write "Hello World" in the console with AI's help

**Why screenshots help here:**
- Different browsers (Chrome, Firefox, Edge, Safari) have different UIs
- Menu locations and icons vary
- AI can see which browser you're using
- AI can point to specific buttons or menu items in YOUR interface

Let's begin:

1. Open any web browser on your computer (Chrome, Firefox, Edge, or Safari)

1. Navigate to any website - for example: `https://www.google.com`

1. Take a screenshot of the entire browser window

1. Open your AI assistant chat (GitHub Copilot Chat in VSCode)

1. Paste the screenshot into the chat

1. Type this message along with the screenshot:
   ```
   I want to open the Developer Console in this browser and write "Hello World" in the console. 
   Can you guide me step by step? Point out exactly where to click in my interface.
   ```

1. Send the message

1. Read AI's response - it should identify your browser and provide specific instructions

1. Follow AI's instructions to open the Developer Console

1. Verify: You should now see the Developer Console panel (usually at bottom or side of browser)

### Part 5: Completing the Task with AI Guidance

1. Once the console is open, take another screenshot showing the console panel

1. Paste this new screenshot into the AI chat

1. Type:
   ```
   The console is now open. How do I write "Hello World" here? 
   Show me exactly where to type.
   ```

1. AI will identify the console input area and guide you

1. Follow AI's instructions to type and execute the command

1. Typically, you'll type: `console.log("Hello World")` and press Enter

1. Verify: You should see "Hello World" printed in the console output

1. Take a final screenshot showing your successful "Hello World" output

1. Share this victory screenshot with AI:
   ```
   Success! Here's the result. Thank you for the guidance!
   ```

**What just happened:**
- You shared your exact visual context with AI
- AI adapted its guidance to YOUR specific interface
- You completed a task without knowing the exact steps beforehand
- Screenshots enabled precise, browser-specific instructions

### Part 6: When to Use Screenshots vs Text

Not every question needs a screenshot. Use this decision guide:

**Use screenshots when:**
- ✅ Describing UI elements or layouts
- ✅ AI's suggestion doesn't match what you see
- ✅ Software version differs from AI's knowledge
- ✅ Showing error messages or unexpected behavior
- ✅ Getting help with visual design or styling
- ✅ You don't know the correct terminology for what you see

**Use text only when:**
- ✅ Asking conceptual questions ("What is REST API?")
- ✅ Requesting code examples or explanations
- ✅ Discussing algorithms or logic
- ✅ Sharing code snippets (use text, not screenshot)
- ✅ Asking about best practices or patterns

**Combine both when:**
- ✅ Debugging: show the code + the error screen
- ✅ UI implementation: show design mockup + ask for code
- ✅ Following tutorials: show the tutorial page + your current state

### Part 7: Best Practices for Screenshot-Based Help

1. **Capture relevant area** - Don't include unnecessary parts of screen that might confuse AI

1. **Include enough context** - Don't crop so tight that AI loses orientation

1. **Use full-color screenshots** - Color helps AI identify elements

1. **Avoid blurry images** - Ensure text in screenshot is readable

1. **Annotate if needed** - You can draw arrows or circles before pasting (using any image editor)

1. **Describe what's wrong** - Screenshot + text explanation = best results

1. **Update screenshots** - If interface changes during conversation, take new screenshot

1. **Privacy consideration** - Avoid sharing screenshots with sensitive data (passwords, personal info, proprietary code)

---

## Success Criteria

Congratulations! You've successfully completed this module if:

✅ You know how to take screenshots on your operating system  
✅ You can paste screenshots into AI chat  
✅ You understand when screenshots are more effective than text  
✅ You successfully opened browser Developer Console with AI guidance using screenshots  
✅ You executed "Hello World" in the console with AI's help  
✅ You understand that AI can see and analyze your screen captures  
✅ You know best practices for sharing visual context  
✅ You can combine screenshots with text questions for optimal results

## Understanding Check

Test your knowledge of visual context techniques:

**Question 1:** Why are screenshots helpful when working with AI assistants?  
**Expected answer:** Screenshots show AI the exact interface you're seeing, which helps when software versions differ, UI has changed, or text descriptions would be lengthy and imprecise.

**Question 2:** Name three scenarios where screenshots are more effective than text descriptions.  
**Expected answer:** Any three of: new software versions with changed UI, finding menu items AI suggests but you can't locate, debugging visual issues, showing error messages, getting help with unfamiliar interfaces.

**Question 3:** How do you paste a screenshot into GitHub Copilot Chat?  
**Expected answer:** Take screenshot using OS tool, click in chat input field, press Ctrl+V (Windows/Linux) or Cmd+V (macOS).

**Question 4:** What's the difference between full screen and partial screen capture, and when would you use each?  
**Expected answer:** Full screen captures entire display, partial captures selected area. Use full screen for overall context, partial for focusing on specific area without irrelevant information.

**Question 5:** Should you share screenshots with sensitive information like passwords or proprietary code?  
**Expected answer:** No, never share screenshots containing passwords, personal information, API keys, or proprietary/confidential code.

**Question 6:** In the practical exercise, what did we accomplish with AI's help?  
**Expected answer:** Opened browser Developer Console and executed console.log("Hello World") with browser-specific guidance based on screenshots.

**Question 7:** When should you use text-only questions instead of screenshots?  
**Expected answer:** For conceptual questions, requesting code examples, discussing algorithms, asking about best practices - situations where visual context isn't relevant.

## Troubleshooting

**Screenshot won't paste into chat?**
- Ensure screenshot is actually in clipboard (try pasting into notepad/textedit first)
- Try different screenshot method on your OS
- Save screenshot as file and drag-drop into chat instead
- Restart your IDE if paste function isn't working
- Check if your AI chat supports image input (most modern versions do)

**AI doesn't seem to see the screenshot?**
- Verify image appears as thumbnail in your message before sending
- Some AI models may not support vision - check your model selection
- Try text description if image support is limited
- Make sure screenshot is clear and not corrupted

**Screenshot is too large to share?**
- Crop to relevant area only
- Use partial screen capture instead of full screen
- Reduce image size using screenshot tool settings
- Most chats auto-resize, but extremely large images may fail

**Browser console won't open following AI's instructions?**
- Take another screenshot showing current state
- Tell AI exactly what happened when you tried
- AI will adjust instructions based on new screenshot
- Different browsers have different access methods - ensure AI knows which browser you use

**"Hello World" not appearing in console?**
- Share screenshot of console with your typed command
- Verify you pressed Enter after typing
- Check if console shows error message
- AI will help debug based on what's visible in screenshot

**Privacy concerns about sharing screenshots?**
- Review screenshot before pasting - look for sensitive info
- Crop out or blur sensitive areas using image editor
- Close tabs/windows with confidential information before capturing
- Remember: chat conversations may be stored - don't share secrets

## Next Steps

Now that you understand visual context, you're ready to dive deeper into how AI agents work under the hood in Module 040. You'll learn about the tools and capabilities that make Agent Mode so powerful!

Continue to: [Agent Mode & AI Mechanics](../040-agent-mode-under-the-hood/about.md)
