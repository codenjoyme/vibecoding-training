## Generate Algorithm Code

### Clarification Step (REQUIRED before generating code)

- **If the user has NOT specified the algorithm or the language(s), you MUST use the `vscode_askQuestions` tool to ask before generating anything.**
- Ask both questions at once in a single `vscode_askQuestions` call:
  1. **Algorithm** — which algorithm to implement (e.g. bubble sort, binary search, Dijkstra, merge sort, quick sort, etc.)
  2. **Language(s)** — which programming language(s) to use; offer a multi-select with common options: Java, Python, TypeScript, Kotlin, Go, C++
- Only skip this step if the user has already provided both pieces of information in their request.
- If user asks to "copy code" or "give me code" — this means output-only mode: no prose, no options, no questions (but still ask if algorithm/language are missing).

### Code Generation Rules

- Output **only the method** — no class wrapper, no imports, no `main`.
- Apply Clean Code principles by default:
  + Meaningful names (`arr`, `temp`, `i`, `j` are acceptable for classic algorithms)
  + No dead code, no commented-out lines
  + Single responsibility — one method does one thing
- Do **not** add:
  + Javadoc or inline comments
  + Unit tests or test stubs
  + `System.out.println` or any debug output
  + Reflection or generics unless explicitly requested
  + Text explanations before or after the code block
- Output format: fenced code block only — nothing outside it.
- If multiple languages are requested — output one fenced code block per language, back to back, no prose between them.

## Examples

User: "Give me bubble sort in Java, Clean Code, only the method"

Expected output:
```java
public static void sort(int[] arr) {
    for (int i = 0; i < arr.length - 1; i++) {
        for (int j = 0; j < arr.length - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}
```

- Same pattern applies to: binary search, merge sort, quick sort, insertion sort, selection sort, etc.
- If user requests a different language — switch language, keep all other rules identical.
