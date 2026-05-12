---
name: translate-site
description: Translate any website to any language using Chrome DevTools MCP — the AI model extracts text from the page, translates it, and injects the translation back into the DOM.
version: 2.0.0
---

## translate-site skill

Translates any website in Chrome by extracting visible text via Chrome DevTools MCP, translating it with the AI model itself, and injecting the translated text back into the page DOM. No external translation API required.

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

### Step 1 — Navigate to the target site

Open the target URL in Chrome:

```
mcp_chrome-devtoo_navigate_page:
  type: url
  url: https://example.com
```

Or open in a new tab to keep the current page:

```
mcp_chrome-devtoo_new_page:
  url: https://example.com
```

Wait for the page to fully load before proceeding.

### Step 2 — Extract visible text from the page

Use `evaluate_script` to collect all visible text nodes from the DOM. Return them as a JSON array of `{idx, text}` pairs:

```javascript
mcp_chrome-devtoo_evaluate_script:
  function: |
    () => {
      const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        {
          acceptNode: (node) => {
            const parent = node.parentElement;
            if (!parent) return NodeFilter.FILTER_REJECT;
            const tag = parent.tagName;
            if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'IFRAME'].includes(tag)) return NodeFilter.FILTER_REJECT;
            if (parent.offsetParent === null && tag !== 'BODY') return NodeFilter.FILTER_REJECT;
            const text = node.textContent.trim();
            if (text.length < 2) return NodeFilter.FILTER_REJECT;
            return NodeFilter.FILTER_ACCEPT;
          }
        }
      );
      const nodes = [];
      let idx = 0;
      while (walker.nextNode() && idx < 200) {
        const text = walker.currentNode.textContent.trim();
        nodes.push({ idx: idx++, text });
      }
      return nodes;
    }
```

This returns up to 200 visible text fragments. For very large pages, process in batches.

### Step 3 — Translate the extracted text

The AI model translates each text fragment to the target language. Process the JSON array from Step 2 and produce a new array with translated text:

```json
[
  { "idx": 0, "translated": "Translated text here" },
  { "idx": 1, "translated": "Another translated fragment" }
]
```

**Important:** Preserve formatting, numbers, proper nouns, and code snippets. Only translate natural language text.

### Step 4 — Inject translated text back into the DOM

Use `evaluate_script` to replace original text nodes with translated versions. Embed the translations array directly in the function body (the `args` parameter in Chrome DevTools MCP expects element UIDs, not arbitrary strings):

```javascript
mcp_chrome-devtoo_evaluate_script:
  function: |
    () => {
      const translations = [
        { "idx": 0, "translated": "Translated text here" },
        { "idx": 1, "translated": "Another fragment" }
        // ... all translated items from Step 3
      ];
      const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        {
          acceptNode: (node) => {
            const parent = node.parentElement;
            if (!parent) return NodeFilter.FILTER_REJECT;
            const tag = parent.tagName;
            if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'IFRAME'].includes(tag)) return NodeFilter.FILTER_REJECT;
            if (parent.offsetParent === null && tag !== 'BODY') return NodeFilter.FILTER_REJECT;
            const text = node.textContent.trim();
            if (text.length < 2) return NodeFilter.FILTER_REJECT;
            return NodeFilter.FILTER_ACCEPT;
          }
        }
      );
      const map = new Map(translations.map(t => [t.idx, t.translated]));
      let idx = 0;
      while (walker.nextNode() && idx < 200) {
        if (map.has(idx)) {
          walker.currentNode.textContent = map.get(idx);
        }
        idx++;
      }
      return 'Replaced ' + map.size + ' text nodes';
    }
```

### Step 5 — Take a screenshot to confirm

```
mcp_chrome-devtoo_take_screenshot
```

Show the screenshot inline and confirm: "Site translated to [language] by the AI model. Here's how it looks."

---

## Troubleshooting

- **Too many text nodes:** The script caps at 200 nodes. For longer pages, increase the limit or process sections separately.
- **Dynamic content not captured:** Some SPAs load content lazily. Scroll down first or wait for dynamic elements to render.
- **Translation changes layout:** Text length changes can break CSS layouts. This is cosmetic — the translation itself is correct.
- **Code snippets get translated:** The script filters out SCRIPT and STYLE tags but code inside PRE or CODE may still be picked up. The AI model should recognize code and skip it during translation.
- **Language not recognized:** Ask the user to clarify the target language.
