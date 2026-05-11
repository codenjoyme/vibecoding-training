# Module 04 Completion Report

## Selected Model
- Model name: Claude Sonnet 4.6
- Pricing tier: 1x

## Agent Mode
- Enabled: Yes

## Technical Question Test
- Question: What is the difference between a compiled and an interpreted programming language?
- Response (first 2–3 sentences): A compiled language is translated entirely into machine code before execution by a compiler, producing a standalone executable. An interpreted language is executed line-by-line at runtime by an interpreter without a separate compilation step. Compiled languages (like C, Go) tend to run faster, while interpreted languages (like Python, JavaScript) offer more flexibility and faster development cycles.

## Code Generation Test
- Request: Generate a Python function that takes a list of numbers and returns the average
- Generated code:
```python
def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
```

## File System Access Test
- Files found: notes.md
