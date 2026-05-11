# Module 07 Completion Report

## Artist Metaphor
The more specific your prompt, the less variation in the AI's output — like asking 10 artists to paint "a still life with lilacs and a pear on the left" versus just "a still life." Fewer constraints give more creative freedom; more constraints produce more predictable results.

## Statements Approach
Statement 1: Create a Python function.
Statement 2: It should validate an email address.
Statement 3: Use regex for the validation pattern.
Statement 4: Return True for valid emails, False otherwise.
Statement 5: Handle edge cases like empty strings and strings without @ symbol.

## Why Not Argue
Arguing with the AI pollutes the context window with conflicting instructions, making the model's output progressively worse. Restarting with a refined prompt gives the model a clean context with only correct requirements.

## Edit-and-Regenerate Workflow
When the AI produces unsatisfactory output, do not send a correction in a follow-up message. Instead, edit your original prompt to add missing constraints or clarify requirements, then regenerate the response. This keeps the context clean and produces better results than iterative corrections.

## Practical Test
- Prompt used (5+ statements): Create a Python function. It should validate an email address. Use regex for the validation pattern. Return True for valid emails, False otherwise. Handle edge cases like empty strings and strings without @ symbol.
- AI-generated result:
```python
import re

def validate_email(email):
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```
