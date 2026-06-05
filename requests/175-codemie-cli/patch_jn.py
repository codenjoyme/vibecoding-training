#!/usr/bin/env python3
"""
Patch JN class in Copilot extension to add tokenizer as own property.
Root cause: JN uses `get tokenizer() { return "o200k_base" }` (prototype getter).
When the endpoint is spread with `{...endpoint, modelMaxPromptTokens: X}`,
prototype getters are NOT included, so the spread object has tokenizer: undefined.
Then Wte.acquireTokenizer(spreadObj) throws "Unknown tokenizer: undefined".

Fix: add `this.tokenizer = "o200k_base"` in JN constructor so it becomes
an own enumerable property that survives the spread.
"""
import sys

path = r".\\VSCode\\3b8129f1d0\\resources\\app\\extensions\\copilot\\dist\\extension.js"

with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

OLD = 'this.isExtensionContributed=!0;this._maxTokens=e.maxInputTokens'
NEW = 'this.isExtensionContributed=!0;this.tokenizer="o200k_base";this._maxTokens=e.maxInputTokens'

count = content.count(OLD)
print(f"Occurrences of target string: {count}")

if count != 1:
    print("ERROR: expected exactly 1 occurrence, aborting")
    sys.exit(1)

patched = content.replace(OLD, NEW, 1)

# Verify patch
if 'this.tokenizer="o200k_base"' not in patched:
    print("ERROR: patch verification failed")
    sys.exit(1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(patched)

print("Patched successfully!")
print("JN constructor now has: this.tokenizer = 'o200k_base' as own property")
