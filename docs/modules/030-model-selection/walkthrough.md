# Model Selection - Hands-on Walkthrough

In this walkthrough, you'll learn how to choose the right AI model for your vibecoding work, understand pricing tiers, and configure optimal settings for productive development.

## Prerequisites

- Completed Module 1 (Installing VSCode + GitHub Copilot)
- Completed Module 2 (Installing Cursor)
- Active GitHub Copilot or Cursor subscription
- Understanding of basic AI assistant concepts

---

## Step-by-Step Instructions

### Part 1: Understanding Model Types and Pricing

1. Open your AI coding assistant (VSCode with Copilot or Cursor)

1. Navigate to Settings and find the Models or AI section

1. Review the available models - you'll typically see labels like:
   - `0x` - Free tier models (no premium request cost)
   - `1x` - Standard models (1 premium request per use)
   - `3x` - Advanced models (3 premium requests per use)

1. Understand what this means:
   - Each use of a model consumes premium requests from your quota
   - Higher multipliers (3x) consume quota faster but provide better quality
   - When quota runs out, you're limited to free models or need to upgrade

1. Verify: Check your account settings to see your current premium request balance

### Part 2: Premium Requests and Quotas

1. Understanding premium requests:
   - New subscriptions come with a certain number of premium requests
   - This quota depletes as you use advanced models
   - When depleted: either use free models (degraded quality) or pay to expand quota

1. For personal accounts:
   - You can purchase additional premium requests
   - Quota typically resets monthly

1. For corporate accounts:
   - May need to wait for monthly reset
   - Or submit request to IT/admin to expand quota
   - Check your organization's policies

1. Practical tip: Monitor your usage to understand your consumption patterns

### Part 3: Selecting Your AI Model

1. Open the Command Palette in your IDE

1. Search for model selection option:
   - VSCode: Type `Copilot: Chat Model`
   - Cursor: Go to Settings > Models

1. Review the available models and their characteristics:
   - **Claude Sonnet 4.5** (Recommended) - Best for coding, excellent price/quality ratio
   - **GPT-4o** - Alternative, good general purpose
   - **GPT-4 Turbo** - Older but reliable
   - Other models depending on your subscription

1. For this training, select **Claude Sonnet 4.5**

1. Verify: The selected model should be displayed in your settings or status bar

### Part 4: Understanding Agent Mode vs Ask Mode

1. In your AI assistant, look for mode settings (usually in chat panel or settings)

1. Two main modes available:
   - **Ask Mode** - Simple Q&A, lower token consumption, just answers questions
   - **Agent Mode** - Autonomous problem-solving, uses more tokens, can perform actions

1. **Recommendation: Enable Agent Mode and never change it**
   - Agent mode is more powerful and autonomous
   - It can read files, search codebase, make changes
   - The extra token cost is worth the productivity gain

1. Enable Agent Mode in your IDE settings

1. Verify: Agent mode indicator should show as active

### Part 5: Practical Model Selection Strategy

1. Follow this practical approach for choosing models:
   - **Start with the best model** available (Claude Sonnet 4.5)
   - **Use it consistently** while it works well for you
   - **Switch only when needed**: if it glitches, becomes unavailable, or doesn't meet your needs
   - **Try the next best model** on your list
   - **Evaluate** after some time - stay if better, move on if not
   - **Repeat** until you find your optimal model

1. Don't constantly switch models - give each one time to prove itself

1. Your preferred model will emerge naturally through this process

1. Most users settle on one or two models for 90% of their work

### Part 6: Understanding Real Costs

1. Real-world example of intensive usage:
   - One month of daily AI-assisted coding
   - Using Claude Sonnet 4.5 extensively
   - Generating code every working day
   - Cost: approximately **$80 over base subscription**

1. Perspective on value:
   - Month of AI coding produced more code than entire previous year
   - Cost is negligible compared to productivity gain
   - Most users won't even exhaust their free premium requests

1. **Don't worry about costs** when starting - focus on learning and productivity

1. You'll likely stay within free premium request quota as you're learning

### Part 7: Test Your Model Selection

1. With Claude Sonnet 4.5 selected and Agent Mode enabled, open the chat

1. Ask a coding question to verify setup:
   ```
   Explain the difference between async/await and promises in JavaScript
   ```

1. Verify: You receive a detailed, well-structured response

1. Try a code generation request:
   ```
   Create a Python function that reads a CSV file and converts it to JSON
   ```

1. Verify: Model generates working code with explanations

1. Verify: Agent mode indicator shows it's actively processing

---

## Success Criteria

Congratulations! You've successfully completed this module if:

✅ You understand model pricing tiers (0x, 1x, 3x)  
✅ You know what premium requests are and how quotas work  
✅ You've selected Claude Sonnet 4.5 as your primary model  
✅ You've enabled Agent Mode in your IDE  
✅ You understand the practical model selection strategy  
✅ You know real-world cost expectations ($80/month for intensive use)  
✅ Your AI assistant responds correctly with the selected model  
✅ You're not worried about costs and ready to focus on productivity

## Troubleshooting

**Can't find model selection option?**
- Make sure you're signed in to your AI assistant
- Check Settings or Preferences menu
- Try Command Palette search for "model" or "AI"
- Ensure your subscription includes model selection

**Model not available?**
- Some models require specific subscription tiers
- Check your account status and subscription level
- Try alternative models like GPT-4o
- Contact support if expected models are missing

**Agent Mode not working?**
- Verify it's enabled in settings
- Try restarting your IDE
- Check that you have sufficient premium requests
- Some features may require internet connection

**Worried about costs?**
- Start with included premium requests - likely sufficient for learning
- Monitor usage in account settings
- Remember: productivity gain far exceeds cost
- You can always downgrade to free models temporarily

## Understanding Model Performance

Different models excel at different tasks:

- **Claude Sonnet 4.5** - Best for: Code generation, refactoring, complex logic
- **GPT-4o** - Best for: General purpose, documentation, explanations
- **GPT-4 Turbo** - Best for: Quick responses, simple tasks
- **Free models** - Best for: Learning, experimentation, non-critical work

Choose based on task complexity, not just cost.

## Next Steps

Now that you understand model selection and have configured optimal settings, you're ready to learn how AI coding assistants work under the hood in the next module!
