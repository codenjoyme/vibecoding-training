# Structured Output & JSON Mode - Hands-on Walkthrough

In this walkthrough, you'll solve one of the most common integration problems with AI: inconsistent output format. You'll enable structured output mode, define schemas, and build a pipeline where AI responses arrive as typed Python objects — not unpredictable prose.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

By the end of this walkthrough you will have:

- **A structured API call** — code that requests and receives JSON from an LLM with 100% format consistency
- **A Pydantic schema** — a Python class defining exactly what fields the AI must return
- **A working output parser** — Langchain's `PydanticOutputParser` turning raw LLM text into typed Python objects
- **A reusable pipeline** — `structured_pipeline.py` that accepts a prompt, returns validated JSON, and saves it to a file

---

## Step 1: Experience the problem first

**What we're about to do:** See exactly why unstructured AI output breaks integrations — before fixing it.

Create a file called `unstructured_demo.py` in your project:

**Windows:** `c:/workspace/hello-genai/unstructured_demo.py`  
**macOS/Linux:** `~/workspace/hello-genai/unstructured_demo.py`

Ask AI to generate it:

```
Write a Python script that calls an LLM three times with the same prompt:
"List 3 programming languages with their main use case."

Print all three responses. Use the LangChain ChatOpenAI client and load the API key from .env.

I want to see how the format varies between calls.
```

Run it three times. Observe: the structure changes. Sometimes it's a numbered list. Sometimes bullet points. Sometimes prose. Sometimes JSON-like, sometimes not.

This is the problem. If you write code to parse response #1, it breaks on response #2. You cannot build reliable integrations on inconsistent output.

---

## Step 2: Enable JSON mode in the API call

**What we're about to do:** Switch the model to respond only in valid JSON. No prose, no explanations — pure structured data.

Ask AI to generate a new script:

```
Write a Python script that calls an LLM with JSON output mode enabled.

Requirements:
- Use LangChain with ChatOpenAI (or equivalent for DIAL API)
- Enable structured output: the model must return only valid JSON
- Prompt: "List 3 programming languages. For each one return: name, main_use_case, year_created"
- Parse the JSON response and print each field separately
- Load API key from .env using python-dotenv
- Handle the case where the response is not valid JSON (print an error, don't crash)
```

Save as `json_mode_demo.py`. Run it several times. The output should now be consistent JSON every time.

**What just happened:** By telling the model to respond in JSON format and providing an example structure in the prompt, you've constrained its output. The model's instruction-following capability ensures the format is consistent even without a schema enforced at the API level.

---

## Step 3: Define a Pydantic schema

**What we're about to do:** Instead of parsing raw JSON dictionaries, define a Python class that describes exactly what the response must look like. This gives you type safety, validation, and IDE autocomplete.

Ask AI:

```
Create a Pydantic v2 model for this data structure:
- A product review with: title (string), rating (integer 1-5), pros (list of strings), cons (list of strings), recommended (boolean)

Then show me:
1. How to create an instance manually
2. How to parse it from a JSON string using model_validate_json()
3. What error Pydantic raises if rating is 6 (out of range)
4. How to add a validator that enforces rating must be between 1 and 5
```

Study the output. Pydantic gives you:
- **Validation** — wrong types or values raise clear errors before bad data enters your system
- **Serialisation** — `.model_dump()` converts back to dict; `.model_dump_json()` to JSON string
- **Documentation** — the class itself documents the expected structure

---

## Step 4: Connect Pydantic to LangChain with PydanticOutputParser

**What we're about to do:** Use LangChain's output parser to combine the Pydantic schema with the LLM call — so the model's response arrives as a typed Python object automatically.

Ask AI to generate the complete integration:

```
Write a Python script using LangChain that:

1. Defines a Pydantic model called ProductReview with: title (str), rating (int), pros (List[str]), cons (List[str]), recommended (bool)

2. Creates a PydanticOutputParser for this model

3. Builds a PromptTemplate that:
   - Takes a product_name variable
   - Includes the parser's format_instructions in the prompt
   - Asks: "Write a product review for {product_name}"

4. Chains: prompt | llm | parser

5. Invokes the chain with product_name="GitHub Copilot"

6. Prints: review.title, review.rating, review.pros, review.cons, review.recommended (accessing typed fields, not dict keys)

Load API key from .env. Show the complete runnable script.
```

Run the script. Notice: the result is a `ProductReview` object, not a string. You access `review.rating` not `review["rating"]`. You get IDE autocompletion. You get a validation error if the model returns something malformed.

**What just happened:** `PydanticOutputParser` does three things:
1. Generates format instructions that tell the model what JSON to produce
2. Receives the model's text response
3. Parses and validates it into your Pydantic object

---

## Step 5: Build the reusable pipeline

**What we're about to do:** Package everything into a reusable script that accepts any prompt and schema, returns validated JSON, and saves it to a file.

Ask AI:

```
Create a reusable Python module called structured_pipeline.py that:

1. Accepts: a Pydantic model class, a prompt template string, and template variables (dict)
2. Creates a PydanticOutputParser for the given model
3. Builds the chain: PromptTemplate | ChatOpenAI | parser
4. Invokes the chain with the provided variables
5. Saves the result as JSON to output/{model_name}_{timestamp}.json
6. Returns the parsed Pydantic object

Also write a usage example at the bottom (under if __name__ == "__main__":) that:
- Defines a simple JobPosting model (title, company, required_skills: list, remote: bool)
- Calls structured_pipeline with prompt "Generate a job posting for a {role} at a {company_type} company"
- Prints the result and shows the saved file path
```

Save the file. Run it. Check the `output/` folder — you should see a JSON file with the structured response.

---

## Step 6: Handle validation failures gracefully

Real integrations need to handle cases where the model doesn't follow the schema. Ask AI:

```
Add error handling to structured_pipeline.py for these cases:
1. The model returns text that's not valid JSON at all (output_parsing_error)
2. The JSON is valid but missing required fields (ValidationError)
3. The API call times out or fails (exception from the LLM client)

For each case: catch the error, log what happened, and return None instead of crashing.
Also add a retry: if parsing fails, retry once with an explicit "You must respond with valid JSON" reminder added to the prompt.
```

This retry-on-parse-failure pattern is what production AI integrations use. The model occasionally deviates — a single retry resolves most cases.

---

## Success Criteria

- ✅ You observed inconsistent output from an unstructured LLM call across multiple runs
- ✅ JSON mode produces consistent format every time
- ✅ A Pydantic model validates and rejects data that doesn't match the schema
- ✅ `PydanticOutputParser` chain returns a typed Python object (not a dict or string)
- ✅ `structured_pipeline.py` saves JSON output to a file with a timestamp
- ✅ Error handling catches parse failures and retries once
- ✅ You can access response fields with dot notation (e.g., `review.rating`) and get IDE autocompletion

---

## Understanding Check

1. **What is the fundamental problem that structured output solves?**
   > LLMs are trained to generate natural language — which is inherently variable and inconsistent. When your code needs to parse the output (extract specific fields, feed them to a database, call another API), that variability breaks the integration. Structured output constrains the model to a specific format on every call, making the output as reliable as any other API.

2. **What does a Pydantic model give you that a plain Python dictionary does not?**
   > Type validation (wrong types raise errors at parse time, not when the value is used), field-level documentation, automatic JSON serialisation/deserialisation, and IDE autocompletion. A dict accepts any value for any key silently; a Pydantic model rejects invalid data immediately.

3. **What does `PydanticOutputParser.get_format_instructions()` return, and why does it matter?**
   > It returns a text block describing the JSON structure the model must produce — including field names, types, and constraints derived from your Pydantic model. This text is embedded in the prompt. Without it, the model doesn't know what schema to follow; with it, the model's instruction-following capability produces the right format.

4. **Why retry with an explicit reminder rather than just crashing on a parse error?**
   > Parse failures are usually caused by the model adding extra prose around the JSON, or by a slightly malformed response — not a fundamental misunderstanding of the task. A single retry with a clearer instruction ("respond with valid JSON only, no other text") resolves the majority of transient failures. Crashing would require a human to re-run the pipeline unnecessarily.

5. **When would you use structured output with a simple `response_format={"type": "json_object"}` parameter vs. using PydanticOutputParser?**
   > `json_object` mode guarantees valid JSON but doesn't enforce which fields are present or what their types are — you still have to validate manually. `PydanticOutputParser` enforces the exact schema you defined and gives you a typed object. Use `json_object` for quick experiments; use Pydantic for production code where you need validation and type safety.

6. **Your structured pipeline works for 95% of calls but fails for 5%. After adding the retry, it drops to 0.5%. What would further reduce failures to near-zero?**
   > Add few-shot examples to the prompt — show the model 2-3 examples of correct input/output pairs. Few-shot prompting dramatically improves consistency because the model learns the pattern from examples rather than relying only on instructions. Also consider using a more capable model (Claude Sonnet 4.5) for tasks requiring strict format adherence.

---

## Troubleshooting

**`OutputParserException: Failed to parse` on every call**
> The model is adding text before or after the JSON. Update the prompt to end with: "Respond with ONLY the JSON object. No introduction, no explanation, no markdown code blocks." Also check that `get_format_instructions()` output is actually included in your prompt.

**Pydantic `ValidationError` even though the JSON looks correct**
> Check field types carefully. Common mismatches: model returns `"true"` (string) but Pydantic expects `bool`; model returns `"5"` (string) but Pydantic expects `int`. Add a Pydantic validator with `@field_validator` that coerces the type, or update the prompt to be more explicit: "rating must be an integer, not a string".

**`ImportError: cannot import PydanticOutputParser`**
> The import path changed between LangChain versions. Try: `from langchain_core.output_parsers import PydanticOutputParser` (LangChain 0.2+). Or ask AI: "Fix this import for my LangChain version — show the correct import for `PydanticOutputParser`."

**Output file not saved to the `output/` folder**
> The folder must exist before writing. Add `os.makedirs("output", exist_ok=True)` before the file write. The `exist_ok=True` parameter means it won't crash if the folder already exists.

**The pipeline works locally but breaks in CI**
> The most common cause: the `output/` directory is created at runtime and not in the repository. Either add it to `.gitignore` and create it in CI as a setup step, or change the output path to a temp directory: `import tempfile; output_dir = tempfile.gettempdir()`.

---

## Next Steps

You can now control both input format (prompt templates, module 185) and output format (structured JSON, this module). The next step combines these to build retrieval-augmented generation:

**→ [Module 190 — RAG: Document Question Answering](../190-rag-document-question-answering/about.md)**

Structured output makes RAG pipelines reliable — the retrieved context is processed and returned in a consistent schema your application can depend on.
