## Generate Algorithm Code

## ⚠️ CLARIFICATION STEP (REQUIRED)

Before generating any algorithm code, check whether the user has specified **both**:
1. **Algorithm** — which algorithm to implement
2. **Language** — which programming language (or set of languages) to use

**If either is missing** — use the `vscode_askQuestions` tool to ask the user. Ask both questions at once in a single call:
- Question 1 (`algorithm`): "Which algorithm would you like me to implement?" — provide options: Bubble Sort, Binary Search, Merge Sort, Quick Sort, Insertion Sort, Selection Sort, Dijkstra, DFS, BFS, Other (free text)
- Question 2 (`language`): "Which programming language(s)?" — provide options: Java, Python, TypeScript, Go, C#, Kotlin, Other (free text); allow multi-select

**Skip the clarification step if** the user has already specified both the algorithm and the language(s) in their request, or if user says "copy code" / "give me code" / "output only" — treat missing language as Java in that case.

---

- When user asks for an algorithm implementation, output **only the method** — no class wrapper, no imports, no `main`.
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
- Language default: Java, unless user specifies otherwise.
- If user asks to "copy code" or "give me code" — this means output-only mode: no prose, no options, no questions.

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

- Same pattern applies to: binary search, merge sort, quick sort, insertion sort, selection sort, Dijkstra, DFS, BFS, etc.
- If user requests a different language — switch language, keep all other rules identical.
- If multiple languages requested — output one fenced code block per language, in the order requested.
