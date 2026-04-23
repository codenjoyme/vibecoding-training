# Course Feedback & Completion - Hands-on Walkthrough

Congratulations on reaching the final module! This walkthrough will guide you through reflecting on your learning journey and providing detailed feedback that helps improve the course for future participants.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Do

- Review all the skills you've acquired during the course
- Fill out a structured feedback template covering key aspects of the training
- Send your feedback to the course author via email
- Celebrate completing the course!

---

## Part 1: Reflect on Your Journey

Before writing feedback, take a moment to review what you've learned.

1. Open the [training plan](../../training-plan.md) and scroll through the module list.

1. For each module you completed, ask yourself:
   - Did I acquire the skill described?
   - Have I used this skill in my real work?
   - Was the walkthrough clear and actionable?

1. Make a mental note (or jot down) which modules were:
   - **Most valuable** — the ones that changed how you work
   - **Most challenging** — the ones where you got stuck
   - **Least relevant** — the ones that didn't apply to your context

---

## Part 2: Prepare Your Feedback

1. Create a new file in your workspace called `work/my-feedback.md`:

   ```
   work/my-feedback.md
   ```

1. Copy the following feedback template into the file:

   ```markdown
   # Course Feedback — Vibecoding for Everyone

   **Date:** [today's date]
   **Name (optional):** [your name or anonymous]
   **Role:** [your role, e.g. Engineering Manager, Tech Lead, Developer]
   **Modules completed:** [approximate number or "all"]

   ## Overall Impression

   Rate the course overall (1-10): [ ]

   What is your one-sentence summary of this course?
   > [your answer]

   ## Most Valuable Modules

   Which 3 modules gave you the most practical value? Why?
   1. [module name] — [why it was valuable]
   2. [module name] — [why it was valuable]
   3. [module name] — [why it was valuable]

   ## Least Valuable / Needs Improvement

   Which modules felt less useful or need rework? Why?
   1. [module name] — [what could be improved]
   2. [module name] — [what could be improved]

   ## Difficulty Level

   Was the course too easy, too hard, or about right?
   > [your answer]

   Which module was the hardest? What made it difficult?
   > [your answer]

   ## Missing Topics

   What topics or skills are NOT covered but should be?
   1. [topic suggestion]
   2. [topic suggestion]

   ## Course Format & Structure

   What do you think about the module-per-skill format?
   > [your answer]

   Was the walkthrough format (step-by-step with verification) effective?
   > [your answer]

   How was the pacing? (too fast / too slow / just right)
   > [your answer]

   ## AI Tools Experience

   Before this course, how would you rate your AI tool proficiency (1-10)? [ ]
   After this course, how would you rate it (1-10)? [ ]

   What was the biggest "aha moment" for you?
   > [your answer]

   ## For Your Team (if applicable)

   Would you recommend this course to your team? Why or why not?
   > [your answer]

   What would you change for a team-wide rollout?
   > [your answer]

   ## Open Comments

   Anything else you'd like to share — suggestions, complaints, praise, ideas?
   > [your answer]
   ```

1. Fill out each section thoughtfully. The more specific your answers, the more useful they are for improving the course.

1. Save the file when you're done.

### What Just Happened

You now have a structured feedback document that covers all aspects of the training — content quality, difficulty, format, missing topics, and your personal growth. This format makes it easy for the course author to identify patterns and prioritize improvements.

---

## Part 3: Send Your Feedback via Email

You have several options to send your feedback. Choose the one that works best for you.

### Option A: Using mailto Link

1. Open this link in your browser (replace the body with your feedback or attach the file):

   **Primary:** [apofig@gmail.com](mailto:apofig@gmail.com?subject=Course%20Feedback%20-%20Vibecoding%20for%20Everyone)

   **Alternative:** [oleksandr_baglai@epam.com](mailto:oleksandr_baglai@epam.com?subject=Course%20Feedback%20-%20Vibecoding%20for%20Everyone)

1. Copy the contents of your `work/my-feedback.md` file and paste it into the email body.

1. Send the email.

### Option B: Using PowerShell (Windows)

1. Run the following command in your terminal to open your default email client with the feedback:

   ```powershell
   Start-Process "mailto:apofig@gmail.com?subject=Course Feedback - Vibecoding for Everyone"
   ```

1. Paste the contents of `work/my-feedback.md` into the email body and send.

### Option C: Using Python (Cross-platform)

1. If you prefer a command-line approach, you can use Python to construct and open the email:

   ```python
   import webbrowser
   import urllib.parse

   to = "apofig@gmail.com"
   subject = "Course Feedback - Vibecoding for Everyone"

   # Read your feedback file
   with open("work/my-feedback.md", "r", encoding="utf-8") as f:
       body = f.read()

   mailto_url = f"mailto:{to}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
   webbrowser.open(mailto_url)
   ```

1. This will open your default email client with the feedback pre-filled. Review and send.

### Option D: Ask Your AI Agent

1. Simply ask your AI assistant in chat:

   > Read my feedback from `work/my-feedback.md` and help me send it to apofig@gmail.com

1. The agent can help format, refine, and assist with sending the feedback.

### What Just Happened

Your feedback is on its way to the course author. Every piece of feedback — whether it's praise, criticism, or a suggestion — is read and used to improve the course. Thank you for taking the time.

---

## Part 4: Celebrate Your Achievement

You've completed the Vibecoding for Everyone course! Here's what you've accomplished:

- **Setup & Environment:** Installed and configured AI coding tools (VS Code, Cursor, GitHub Copilot)
- **Prompting & Communication:** Learned to communicate effectively with AI assistants
- **Development Practices:** Adopted version control, debugging, and testing workflows with AI
- **Architecture & Integration:** Built prototypes, connected MCP servers, and designed systems with AI
- **Team & Process:** Understood how to scale AI practices across your team
- **Advanced Topics:** Explored RAG, multi-agent orchestration, and career evolution with AI

You are now equipped to lead AI-assisted development in your team and organization.

---

## Success Criteria

- ✅ Reviewed the module list and reflected on your learning journey
- ✅ Created `work/my-feedback.md` with the feedback template
- ✅ Filled out all feedback sections with thoughtful responses
- ✅ Sent feedback email to the course author
- ✅ Celebrated completing the course!

## Understanding Check

1. **Why is structured feedback more useful than "it was great" or "it was bad"?**
   - Structured feedback pinpoints specific modules, topics, and format aspects — making it actionable for the course author to prioritize improvements.

2. **What are the two email addresses for sending course feedback?**
   - `apofig@gmail.com` (primary) and `oleksandr_baglai@epam.com` (alternative).

3. **Why does the feedback template ask about "before and after" AI proficiency?**
   - To measure the learning delta — how much the course actually moved the needle on your skills, which helps evaluate course effectiveness.

4. **How does your feedback about "missing topics" help the course?**
   - It identifies gaps in the curriculum from a real practitioner's perspective. New modules are often created based on participant suggestions.

5. **Why is the "least valuable module" question important?**
   - It helps the author identify modules that need rework, better positioning, or removal — improving the overall course quality for future cohorts.

6. **What value does the "team rollout" question provide?**
   - It surfaces organizational and scaling concerns that individual module walkthroughs don't address, helping adapt the course for team-wide deployment.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Email client doesn't open from mailto link | Copy the email addresses manually and compose the email in your email client |
| Feedback file too long for email body | Attach `work/my-feedback.md` as a file instead of pasting |
| Not sure what to write | Start with the "Most Valuable Modules" section — it's the easiest to answer and gets momentum going |
| Want to give feedback anonymously | Leave the Name field blank — anonymous feedback is equally valued |
| Completed only some modules | That's fine! Note which modules you completed and provide feedback on those |

## Next Steps

This is the final module of the course. From here you can:

- **Apply daily:** Use the skills from this course in your everyday work
- **Share with your team:** Recommend specific modules to colleagues based on their needs
- **Stay updated:** Pull the latest version of the course repository for new modules
- **Contribute:** If you have ideas for new modules, share them in your feedback or open a GitHub issue
- **Revisit modules:** Come back to any module as a reference when you need a refresher

**Thank you for completing the course and for your feedback!**
