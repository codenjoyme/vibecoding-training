#!/usr/bin/env python3
"""
Patch JN class in Copilot extension to add tokenizer as own property.

Root cause: JN uses `get tokenizer() { return "o200k_base" }` (prototype getter,
no setter). When endpoint is spread with `{...endpoint, ...}`, prototype getters
are NOT copied -> spread object has tokenizer: undefined -> "Unknown tokenizer".

Simple assignment `this.tokenizer = "o200k_base"` throws in strict mode:
  "Cannot set property tokenizer of #<JN> which has only a getter"

Fix: use Object.defineProperty to create an own enumerable property that
shadows the prototype getter AND survives the spread operation.
"""
import sys

path = r".\\VSCode\\3b8129f1d0\\resources\\app\\extensions\\copilot\\dist\\extension.js"

with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

DEFINE = "Object.defineProperty(this,'tokenizer',{value:'o200k_base',writable:!0,enumerable:!0,configurable:!0});"

# Handle both: original (never patched) and already patched with broken assignment
CANDIDATES = [
    # Already patched with broken assignment -> replace it
    (
        'this.isExtensionContributed=!0;this.tokenizer="o200k_base";this._maxTokens=e.maxInputTokens',
        'this.isExtensionContributed=!0;' + DEFINE + 'this._maxTokens=e.maxInputTokens'
    ),
    # Original (never patched)
    (
        'this.isExtensionContributed=!0;this._maxTokens=e.maxInputTokens',
        'this.isExtensionContributed=!0;' + DEFINE + 'this._maxTokens=e.maxInputTokens'
    ),
]

patched = None
for OLD, NEW in CANDIDATES:
    count = content.count(OLD)
    if count == 1:
        print(f"Found target: {OLD[:60]}...")
        patched = content.replace(OLD, NEW, 1)
        break
    elif count > 1:
        print(f"ERROR: {count} occurrences of candidate, expected 1, aborting")
        sys.exit(1)

if patched is None:
    print("ERROR: no matching pattern found - extension may have been updated")
    print("Search for 'isExtensionContributed' in extension.js and patch manually")
    sys.exit(1)

# Verify
if DEFINE not in patched:
    print("ERROR: patch verification failed")
    sys.exit(1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(patched)

print("Patched successfully!")
print("JN constructor now uses Object.defineProperty to create own 'tokenizer' property")