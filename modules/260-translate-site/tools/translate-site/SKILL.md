---
name: translate-site
description: Translate any website to any language using Chrome DevTools MCP — navigates to the site and applies translation via Google Translate redirect or in-page script injection.
version: 1.1.0
---

## translate-site skill

Opens any website in Chrome via Chrome DevTools MCP and translates it into the requested language.

**Requires:** Chrome DevTools MCP configured and running (see [modules/130-chrome-devtools-mcp-qa-emulation](../../../130-chrome-devtools-mcp-qa-emulation/about.md)).

---

## How to use this skill

Invoke this skill by saying something like:

> "Translate [URL] to [language]"

Examples:
- "Translate https://example.com to French"
- "Open https://docs.github.com and translate it to Japanese"
- "Translate this site to Ukrainian"

The agent will follow the steps below.

---

## Agent steps

### Step 1 — Resolve target language code

Map the requested language to a BCP 47 language code:

| User says | Code |
|---|---|
| English | `en` |
| Russian | `ru` |
| Ukrainian | `uk` |
| French | `fr` |
| German | `de` |
| Spanish | `es` |
| Italian | `it` |
| Japanese | `ja` |
| Chinese | `zh-CN` |
| Portuguese | `pt` |
| Polish | `pl` |
| Korean | `ko` |
| Arabic | `ar` |

If the user specifies a language not in the table, look up its BCP 47 code and proceed.

### Step 2 — Build Google Translate redirect URL

Construct the translation URL using this pattern:

```
https://translate.google.com/translate?sl=auto&tl={lang_code}&u={encoded_url}
```

- `sl=auto` — auto-detect source language
- `tl={lang_code}` — target language code from Step 1
- `u={encoded_url}` — the site URL, percent-encoded if it contains special characters

Example for translating `https://example.com` to French (`fr`):
```
https://translate.google.com/translate?sl=auto&tl=fr&u=https://example.com
```

### Step 3 — Open in Chrome via Chrome DevTools MCP

Navigate to the constructed URL using the Chrome DevTools MCP `navigate_page` tool:

```
mcp_chrome-devtoo_navigate_page:
  type: url
  url: https://translate.google.com/translate?sl=auto&tl=fr&u=https://example.com
```

Or open in a new tab if the user wants to keep the current page:

```
mcp_chrome-devtoo_new_page:
  url: https://translate.google.com/translate?sl=auto&tl=fr&u=https://example.com
```

### Step 4 — Wait for page to load

Wait for visible text that confirms the translation loaded:

```
mcp_chrome-devtoo_wait_for:
  text: ["Translate", "translated", "Google Translate"]
  timeout: 10000
```

### Step 5 — Take a screenshot to confirm

Confirm the translation is visible to the user:

```
mcp_chrome-devtoo_take_screenshot
```

Show the screenshot inline and briefly confirm: "Site translated to [language]. Here's how it looks."

---

## Troubleshooting

- **Google Translate blocks the page:** Some sites disable embedding via `X-Frame-Options`. In that case, fall back to `evaluate_script` to inject a translation library or suggest the user enable Chrome's built-in translation feature manually.
- **Language not recognized:** Ask the user to clarify or specify the target language more precisely.
- **Page takes long to load:** Increase the `wait_for` timeout to 20000 ms.
- **URL contains special characters:** Percent-encode the URL before inserting into the redirect pattern.

---

## Alternative: Google Cloud Translation API (advanced)

For sites that block Google Translate iframes, use `evaluate_script` to fetch page text and translate via API:

```javascript
// Inject fetch call — requires user to have GOOGLE_TRANSLATE_API_KEY available
const response = await fetch(`https://translation.googleapis.com/language/translate/v2?key=API_KEY`, {
  method: 'POST',
  body: JSON.stringify({ q: document.body.innerText, target: 'fr' }),
  headers: { 'Content-Type': 'application/json' }
});
const data = await response.json();
document.body.innerText = data.data.translations[0].translatedText;
```

This approach requires a Google Cloud API key — refer to the user's secrets management workflow before using.
