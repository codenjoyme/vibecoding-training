# Translate Any Website with AI Agent — Walkthrough

> **Prerequisites:** see [about.md](about.md) for required modules and tools.

## What You'll Learn

| Part | What | Outcome |
|------|------|---------|
| 1 | Understand the translate-site skill | Know how the AI model extracts, translates, and injects text |
| 2 | Translate your first site | Successfully translate a real website using the AI model |
| 3 | Handle edge cases | Deal with dynamic content, long pages, code snippets |
| 4 | Build your own translation workflow | Customize and extend the skill |

---

## Part 1 — How the Translate-Site Skill Works

The [translate-site skill](tools/translate-site/SKILL.md) uses a three-step pipeline — entirely powered by the AI model, no external translation service required:

1. **Extract** — a JavaScript TreeWalker collects all visible text nodes from the page DOM (up to 200 fragments)
2. **Translate** — the AI model translates each text fragment to the target language
3. **Inject** — another script replaces the original text nodes with translated versions in-place

The translations are embedded directly in the injection script (Chrome DevTools MCP `args` expect element UIDs, not arbitrary strings).

### Try it

1. Make sure Chrome DevTools MCP is running (see [module 130](../130-chrome-devtools-mcp-qa-emulation/about.md))
2. Ask the agent: **"Translate https://example.com to French"**
3. The agent will navigate to the site, extract text, translate it, inject back, and take a screenshot

### What just happened?

The agent followed the skill's 5 steps: navigate → extract text nodes → translate with AI → inject back into DOM → screenshot. The AI model itself did the translation — no API keys, no third-party services.

---

## Part 2 — Translate a Real Website

Now try with a real site you use:

1. Pick any website (documentation, news, blog)
2. Ask: **"Translate [your URL] to [language]"**
3. Verify the result in the screenshot — the page should look the same but with translated text

### Experiment

- Try different languages: Japanese, Ukrainian, Arabic, Korean
- Try sites with different content types: documentation, e-commerce, social media
- Try translating the same site to multiple languages in sequence

---

## Part 3 — Edge Cases and Troubleshooting

Some sites present challenges for DOM-based translation:

| Problem | Cause | Solution |
|---------|-------|----------|
| Translation is partial | Dynamic content loaded after extraction | Scroll down first to trigger lazy-load, then re-extract |
| Code snippets get translated | Code inside `<pre>`/`<code>` tags picked up by TreeWalker | The AI model should recognize code and skip it — if not, add tag filters |
| Layout breaks | Translated text is longer/shorter than original | Cosmetic only — the translation itself is correct |
| Too many text nodes | Page has >200 visible text fragments | Increase the cap in the extraction script or process in batches |
| Cookie/popup overlay covers text | Overlay is in a separate DOM layer | Dismiss the overlay first, then extract |

---

## Part 4 — Extend the Workflow

Ideas for building on this skill:

- **Batch translation:** Write a prompt that translates a list of URLs to a specific language and takes screenshots of each
- **Localization QA:** Compare your site in 5 languages side by side
- **Translation diff:** Translate a page, then translate the translation back and compare with original
- **Accessibility audit:** Translate your site to verify it works correctly in RTL languages (Arabic, Hebrew)

### Challenge

Create a `work/260-task/` folder and write a prompt that:
1. Takes a list of 3 URLs
2. Translates each to 2 different languages
3. Takes screenshots of all 6 results
4. Summarizes the translation quality

---

## Success Criteria

- [ ] Translated at least one website using the agent command
- [ ] Tried at least 2 different target languages
- [ ] Understood the extract → translate → inject pipeline
- [ ] Know how to handle edge cases (dynamic content, code snippets, long pages)

## Understanding Check

1. What are the three steps the skill uses to translate a page?
2. Why are translations embedded directly in the injection script instead of passed as arguments?
3. What happens with code snippets inside `<pre>` or `<code>` tags?
4. How would you translate a site to a language the AI model hasn't seen before?
