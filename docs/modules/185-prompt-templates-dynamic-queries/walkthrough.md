# Prompt Templates for Dynamic Queries - Hands-on Walkthrough

In this walkthrough, you'll learn how to use Langchain's prompt templates to create reusable, parameterized AI queries. Instead of hardcoding prompts with specific values, you'll build templates that accept variables and generate consistent, structured queries.

## Prerequisites

- Completed **Module 180: DIAL Integration with Python and Langchain**
- Python virtual environment set up in `work/python-ai-workspace`
- DIAL API credentials configured in `.env` file
- Virtual environment activated (showing `.venv` prefix in terminal)

## Part 1: Understanding the Problem with Hardcoded Prompts

Let's start by understanding why templates matter.

**The Hardcoded Approach (Module 180):**
```python
query = "Tell me about artificial intelligence in the style of a pirate."
response = llm.invoke(query)
```

**Problems:**
- Want different topic? Copy-paste and change the string
- Want different style? Copy-paste again
- Need 10 variations? 10 hardcoded strings
- Typo in template format? Fix in 10 places
- Hard to test different variations systematically

**The Template Solution:**
```python
template = "Tell me about {topic} in the style of {style}."
# Now just change variables: topic="physics", style="teacher"
```

**Benefits:**
- Write template once, reuse with different inputs
- Consistent format across all queries
- Easy to modify template logic (change once, apply everywhere)
- Testable with different parameter combinations
- Maintainable code that scales

## Part 2: Setting Up Your Workspace

**Good news!** You already have everything installed from Module 180. We're reusing the same Python environment with Langchain - no reinstallation needed.

1. Navigate to the workspace created in Module 180:
   
   **Windows:**
   ```powershell
   cd work\python-ai-workspace
   ```
   
   **macOS/Linux:**
   ```bash
   cd work/python-ai-workspace
   ```

2. Activate virtual environment if not already active:
   
   **Windows:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   
   **macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

3. Verify you see the `.venv` prefix in your prompt

**What's already here:**
- ✅ Python virtual environment
- ✅ Langchain and dependencies installed
- ✅ `.env` file with DIAL credentials
- ✅ `color.py` utility from module 180

**What we'll add:**
- 📝 `prompt_template.py` - The example from this module

## Part 3: Creating Your First Prompt Template

1. Copy the template example from this module's tools directory:
   
   **Windows:**
   ```powershell
   Copy-Item ..\..\docs\modules\185-prompt-templates-dynamic-queries\tools\prompt_template.py .
   ```
   
   **macOS/Linux:**
   ```bash
   cp ../../docs/modules/185-prompt-templates-dynamic-queries/tools/prompt_template.py .
   ```

2. Open `prompt_template.py` in your editor and examine the structure:

**Template Definition:**
```python
template = """
"Tell me about {topic} in the style of {style}."
"""
```
- `{topic}` and `{style}` are placeholders (variables)
- Template is a string with marked positions for dynamic values
- Triple quotes allow multi-line templates

**Creating Template Object:**
```python
prompt_template = PromptTemplate(
    input_variables=["topic", "style"],  
    template=template
)
```
- `input_variables` declares what variables the template expects
- Langchain validates you provide these when formatting
- Prevents typos and missing parameters

**Formatting with Values:**
```python
prompt = prompt_template.format(
    topic="the history of pirates", 
    style="a pirate")
```
- `.format()` replaces `{topic}` and `{style}` with actual values
- Returns completed string ready for AI model
- Same template, different inputs = different prompts

## Part 4: Running Your First Template

1. Run the script:
   ```powershell
   python prompt_template.py
   ```

2. Observe the output structure:
   ```
   ======================================
   Template
   ======================================
   "Tell me about {topic} in the style of {style}."
   
   ======================================
   Prompt variables
   ======================================
   Topic: the history of pirates
   Style: a pirate
   
   ======================================
   Query
   ======================================
   Tell me about the history of pirates in the style of a pirate.
   
   ======================================
   Response
   ======================================
   content='Ahoy, matey! Let me spin ye a yarn...'
   ```

**What happened:**
- Template showed structure with placeholders
- Variables displayed before formatting
- Formatted query showed final prompt sent to AI
- Response generated based on that prompt

## Part 5: Experimenting with Different Variables

Now let's modify the script to try different combinations.

1. Open `prompt_template.py` and find these lines:
   ```python
   topic = "the history of pirates"
   style = "a pirate"
   ```

2. Change to different values:
   ```python
   topic = "machine learning"
   style = "a kindergarten teacher"
   ```

3. Run again:
   ```powershell
   python prompt_template.py
   ```

4. Try several combinations:
   - **Technical to simple:** topic="quantum computing", style="a sports commentator"
   - **Serious to humorous:** topic="climate change", style="a stand-up comedian"
   - **Professional:** topic="project management", style="an executive coach"

**Notice:** Template stays the same, only variables change. This is the power of templates!

## Part 6: Creating a Multi-Variable Template

Let's build a more complex template with additional parameters.

1. Create a new file `advanced_template.py`:
   ```python
   from color import header
   header("Advanced Template Example", "cyan")
   
   import os
   from langchain_openai import AzureChatOpenAI
   from langchain.prompts import PromptTemplate
   from dotenv import load_dotenv
   
   load_dotenv()
   
   llm = AzureChatOpenAI(
       azure_deployment = os.getenv("AZURE_OPENAI_API_DEPLOYMENT"),
       api_version      = os.getenv("AZURE_OPENAI_API_VERSION"),
       api_key          = os.getenv("AZURE_OPENAI_API_KEY"),
       azure_endpoint   = os.getenv("AZURE_OPENAI_ENDPOINT"),
       max_tokens       = 500,
       temperature      = 0.7
   )
   
   # Multi-variable template for product descriptions
   template = """
   Write a {tone} product description for a {product_type} called "{product_name}".
   
   Key features:
   {features}
   
   Target audience: {audience}
   
   Length: {length} sentences
   """
   
   prompt_template = PromptTemplate(
       input_variables=["tone", "product_type", "product_name", "features", "audience", "length"],
       template=template
   )
   
   # Fill template with specific values
   prompt = prompt_template.format(
       tone="enthusiastic and professional",
       product_type="smart watch",
       product_name="TimeMaster Pro",
       features="- Heart rate monitoring\n- GPS tracking\n- 7-day battery life",
       audience="fitness enthusiasts",
       length="3-4"
   )
   
   header("Generated Prompt")
   print(prompt)
   
   response = llm.invoke(prompt)
   
   header("AI Response")
   print(response.content)
   ```

2. Run the advanced template:
   ```powershell
   python advanced_template.py
   ```

3. Experiment with different product descriptions:
   - Change `product_type` to "laptop", "coffee maker", "backpack"
   - Modify `tone` to "technical", "playful", "luxury"
   - Adjust `audience` to "students", "professionals", "travelers"

## Part 7: Building a Template Library

For real applications, you'll want reusable templates.

1. Create `template_library.py`:
   ```python
   from color import header
   header("Template Library Demo", "green")
   
   import os
   from langchain_openai import AzureChatOpenAI
   from langchain.prompts import PromptTemplate
   from dotenv import load_dotenv
   
   load_dotenv()
   
   llm = AzureChatOpenAI(
       azure_deployment = os.getenv("AZURE_OPENAI_API_DEPLOYMENT"),
       api_version      = os.getenv("AZURE_OPENAI_API_VERSION"),
       api_key          = os.getenv("AZURE_OPENAI_API_KEY"),
       azure_endpoint   = os.getenv("AZURE_OPENAI_ENDPOINT"),
       max_tokens       = 300,
       temperature      = 0.7
   )
   
   # Library of reusable templates
   TEMPLATES = {
       "email": PromptTemplate(
           input_variables=["recipient", "purpose", "tone"],
           template="Write a {tone} email to {recipient} about {purpose}."
       ),
       
       "summary": PromptTemplate(
           input_variables=["text", "length"],
           template="Summarize the following text in {length} sentences:\n\n{text}"
       ),
       
       "translation": PromptTemplate(
           input_variables=["text", "source_lang", "target_lang"],
           template="Translate from {source_lang} to {target_lang}:\n\n{text}"
       ),
       
       "code_review": PromptTemplate(
           input_variables=["code", "language"],
           template="Review this {language} code and suggest improvements:\n\n{code}"
       )
   }
   
   def use_template(template_name, **variables):
       """Helper function to use a template from library"""
       template = TEMPLATES[template_name]
       prompt = template.format(**variables)
       
       header(f"Template: {template_name}")
       print(prompt)
       
       response = llm.invoke(prompt)
       
       header("Response")
       print(response.content)
       print("\n")
       return response.content
   
   # Example usage
   use_template("email",
       recipient="project team",
       purpose="upcoming deadline for deliverables",
       tone="professional but friendly"
   )
   
   use_template("summary",
       text="Artificial intelligence is transforming industries by automating tasks, providing insights from data, and enabling new capabilities that were previously impossible. Machine learning, a subset of AI, allows systems to learn from data and improve over time without explicit programming.",
       length="2"
   )
   ```

2. Run the library demo:
   ```powershell
   python template_library.py
   ```

3. Add your own template to the library:
   ```python
   "meeting_notes": PromptTemplate(
       input_variables=["meeting_topic", "attendees", "duration"],
       template="Generate meeting notes for a {duration} minute meeting about {meeting_topic} with {attendees}."
   )
   ```

## Part 8: Three Ways to Run Your Template Scripts

Once you've created template scripts, you have multiple execution options depending on your workflow and environment preferences.

### Method 1: Windows Native Execution

**Best for:** Daily development, debugging, quick iterations

**Prerequisites:**
- Completed Module 180 setup (venv exists in `work/python-ai-workspace`)
- Virtual environment has langchain dependencies installed
- `.env` file configured

**Steps:**

1. Navigate to workspace:
   ```powershell
   cd work\python-ai-workspace
   ```

2. Activate virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Run any template script:
   ```powershell
   python prompt_template.py
   python advanced_template.py
   python template_library.py
   ```

**Advantages:**
- ✅ Fastest execution (no overhead)
- ✅ Easy debugging with IDE
- ✅ Immediate feedback for development

### Method 2: Linux/macOS Native Execution

**Best for:** Development on Linux/macOS systems

**Prerequisites:**
- Linux/macOS operating system
- Completed Module 180 setup (venv exists with dependencies)
- Scripts exist in `work/python-ai-workspace`

**Steps:**

1. Navigate to workspace:
   ```bash
   cd work/python-ai-workspace
   ```

2. Activate virtual environment:
   ```bash
   source .venv/bin/activate
   ```

3. Run template scripts:
   ```bash
   python3 prompt_template.py
   python3 advanced_template.py
   python3 template_library.py
   ```

**Advantages:**
- ✅ Fastest execution on Linux/macOS
- ✅ Easy debugging with native tools
- ✅ Same environment as Module 180

**Note:** If environment not set up yet, run Module 180's installation script first:
```bash
cd docs/modules/180-dial-langchain-python-integration/tools
./install-python-linux.sh
```

### Method 3: Docker Deployment (Production-Ready)

**Best for:** Reproducible execution, team sharing, deployment testing

**Prerequisites:**
- Docker Desktop installed and running
- Scripts exist in `work/python-ai-workspace`

**Steps:**

1. Navigate to Module 180 tools directory (reuse Docker scripts):
   ```powershell
   cd docs\modules\180-dial-langchain-python-integration\tools
   ```

2. Run any template script in Docker:
   
   **Windows:**
   ```powershell
   .\install-python-docker.ps1 -Script "prompt_template.py"
   .\install-python-docker.ps1 -Script "advanced_template.py"
   .\install-python-docker.ps1 -Script "template_library.py"
   ```
   
   **Linux/macOS:**
   ```bash
   ./install-python-docker.sh prompt_template.py
   ./install-python-docker.sh advanced_template.py
   ./install-python-docker.sh template_library.py
   ```

3. First run builds Docker image (~120 seconds), subsequent runs use cache (~1-3 seconds)

**Advantages:**
- ✅ Perfect reproducibility
- ✅ No dependency conflicts
- ✅ Layer caching makes it fast after first build
- ✅ Ideal for CI/CD and deployment testing

**Important:** Module 185 scripts don't require extra Python packages beyond what Module 180 installs (langchain, langchain-openai). Docker scripts work out-of-the-box!

### Choosing the Right Method for Templates

| Scenario | Recommended Method |
|----------|-------------------|
| Developing new templates | Method 1: Windows Native |
| Testing template modifications | Method 1: Windows Native |
| Validating Linux compatibility | Method 3: Docker Deployment |
| Sharing templates with team | Method 3: Docker Deployment |
| Production deployment | Method 3: Docker Deployment |

**Pro Tip:** Develop templates with Method 1 for speed, then validate with Method 3 before committing to ensure Docker compatibility!

## Part 9: Template Validation and Error Handling

Templates provide built-in validation:

1. Create `template_validation.py`:
   ```python
   from langchain.prompts import PromptTemplate
   
   template = PromptTemplate(
       input_variables=["name", "age"],
       template="Hello {name}, you are {age} years old."
   )
   
   # This works
   print(template.format(name="Alice", age=30))
   
   # This will fail - missing required variable
   try:
       print(template.format(name="Bob"))
   except KeyError as e:
       print(f"Error: Missing variable {e}")
   
   # This will fail - extra variable not in template
   try:
       print(template.format(name="Charlie", age=25, city="NYC"))
   except Exception as e:
       print(f"Warning: Extra variable provided")
   ```

2. Run to see validation in action:
   ```powershell
   python template_validation.py
   ```

**Key takeaway:** Templates prevent runtime errors by validating inputs upfront.

## Success Criteria

✅ Created and ran prompt_template.py successfully  
✅ Modified template variables and observed different outputs  
✅ Built multi-variable advanced_template.py with 5+ parameters  
✅ Created template_library.py with reusable template collection  
✅ Tested different template types (email, summary, translation)  
✅ Understand difference between template structure and variable values  
✅ Can add new templates to library independently  
✅ Recognize when to use templates vs hardcoded prompts  

## Troubleshooting

### Issue: KeyError when formatting template

**Solution:**
- Ensure all `input_variables` are provided in `.format()` call
- Check variable names match exactly (case-sensitive)
- Example fix:
  ```python
  # Wrong
  template.format(Topic="AI")  # Capital T
  
  # Correct
  template.format(topic="AI")  # Lowercase matches input_variables
  ```

### Issue: Template output doesn't look right

**Solution:**
- Check template string formatting (spaces, newlines, punctuation)
- Remember `{variable}` placeholders are replaced exactly
- Use triple quotes `"""` for multi-line templates
- Test template format with `print(template)` before using

### Issue: Can't modify existing template after creation

**Solution:**
- Templates are immutable by design
- Create new template instance instead:
  ```python
  # Don't try to modify
  old_template.input_variables.append("new_var")  # Won't work
  
  # Create new template
  new_template = PromptTemplate(
      input_variables=["old_var", "new_var"],
      template="..."
  )
  ```

### Issue: Template with complex formatting breaks

**Solution:**
- Escape curly braces that aren't variables: `{{` and `}}`
- Example:
  ```python
  template = "JSON format: {{'key': '{value}'}}"
  # {{ and }} become literal { and }
  # {value} is variable
  ```

## When to Use

**Use Templates:**
- Building applications with repeated query patterns
- Need to maintain consistency across many similar prompts
- Want to test different variations systematically
- Sharing prompts across team (templates are code, not strings)
- Creating prompt libraries for different use cases

**Use Hardcoded Strings:**
- One-off queries or experiments
- Unique prompts that won't be reused
- Very simple queries with no variables
- Quick testing or prototyping

## Next Steps

Excellent work! You've mastered prompt templates - a fundamental building block for scalable AI applications.

**What you've learned:**
- Templates separate structure from content
- Variables make prompts reusable and testable
- Template libraries enable sharing and consistency
- Validation prevents runtime errors

**Next module: 190-rag-document-question-answering** - Build a Retrieval-Augmented Generation (RAG) system that answers questions using your own documents, combining vector search with AI generation.

**Practical applications to try:**
- Build email template system for customer communications
- Create content generation templates for blog posts
- Develop code documentation generator with templates
- Design Q&A bot with template-based responses

---

**Key Takeaway:** Prompt templates transform AI interactions from one-off queries into maintainable, scalable code. By parameterizing prompts, you build reusable patterns that adapt to any input - the foundation for production AI applications.
