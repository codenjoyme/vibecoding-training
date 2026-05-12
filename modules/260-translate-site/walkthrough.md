# Translate Any Website with AI Agent — Walkthrough

> **Prerequisites:** see [about.md](about.md) for required modules and tools.

## What You'll Learn

| Part | What | Outcome |
|------|------|---------|
| 1 | Understand the translate-site skill | Know how Google Translate redirect works |
| 2 | Translate your first site | Successfully translate a real website |
| 3 | Handle edge cases | Deal with blocked sites, special characters |
| 4 | Build your own translation workflow | Customize and extend the skill |

---

## Part 1 — How the Translate-Site Skill Works

The [translate-site skill](tools/translate-site/SKILL.md) uses a simple but powerful pattern: it builds a Google Translate redirect URL and opens it in Chrome via the DevTools MCP server.

The URL pattern:
```
https://translate.google.com/translate?sl=auto&tl={lang_code}&u={site_url}
```

- `sl=auto` — auto-detect source language
- `tl={lang_code}` — target language (e.g. `fr`, `uk`, `ja`)
- `u={site_url}` — the website to translate

### Try it

1. Make sure Chrome DevTools MCP is running (see [module 130](../130-chrome-devtools-mcp-qa-emulation/about.md))
2. Ask the agent: **"Translate https://example.com to French"**
3. The agent will build the URL, navigate Chrome, and take a screenshot

### What just happened?

The agent followed the skill's 5 steps: resolve language code → build URL → navigate → wait for load → screenshot. All automated, no manual work.

---

## Part 2 — Translate a Real Website

Now try with a real site you use:

1. Pick any website (documentation, news, blog)
2. Ask: **"Translate [your URL] to [language]"**
3. Verify the result in the screenshot

### Experiment

- Try different languages: Japanese, Ukrainian, Arabic, Korean
- Try sites with different content types: documentation, e-commerce, social media
- Try translating the same site to multiple languages in sequence

---

## Part 3 — Edge Cases and Troubleshooting

Some sites resist translation. Here's what to do:

| Problem | Cause | Solution |
|---------|-------|----------|
| Page shows "refused to connect" | `X-Frame-Options` header blocks embedding | Use Chrome's built-in translate or the script injection fallback |
| Translation is partial | Dynamic content loaded after translate | Wait longer, or scroll to trigger lazy-load |
| Special characters in URL | URL not properly encoded | Agent handles percent-encoding automatically |
| Wrong source language detected | Short text or mixed languages | Specify source language manually: `sl=en` instead of `sl=auto` |

### Try the fallback

If Google Translate redirect doesn't work for a site, the skill includes a fallback approach using `evaluate_script` to inject translation directly into the page. This requires a Google Cloud Translation API key.

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
- [ ] Understood the Google Translate redirect URL pattern
- [ ] Know how to handle sites that block translation

## Understanding Check

1. What URL pattern does the skill use for translation?
2. What does `sl=auto` mean in the redirect URL?
3. What happens when a site has `X-Frame-Options` that blocks Google Translate?
4. How would you translate a site to a language not in the default table?
