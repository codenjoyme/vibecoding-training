# IDE Workspace as Knowledge Base - Hands-on Walkthrough

In this module you will turn a regular IDE workspace into a knowledge base. You'll organize a collection of documents into a folder, use AI chat to extract insights from them, and summarize your findings into reusable knowledge artifacts — all without writing a single line of code or setting up any infrastructure.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Cover

- **The concept** — why a workspace folder + AI chat is a viable alternative to RAG for many tasks
- **Setting up a knowledge workspace** — organizing documents for AI consumption
- **Querying your documents** — practical techniques for getting answers from scattered sources
- **Cross-referencing and contradiction detection** — finding inconsistencies across documents
- **Summarizing outcomes** — turning a chat session into a reusable instruction or knowledge file
- **Security checkpoint** — understanding what data leaves your machine

---

## Step 1: Understand the Idea

### What we'll do

Understand why an IDE workspace works as a lightweight knowledge base and when to choose it over more complex solutions.

### The spectrum of knowledge tools

```
Simplest                                                    Most complex
   │                                                             │
   ▼                                                             ▼
 Notepad          IDE + AI Chat         RAG Pipeline       Enterprise Search
 (manual)         (this module)         (embeddings+DB)    (Elasticsearch etc.)
```

| Approach | Setup time | Best for |
|---|---|---|
| Read documents manually | 0 min | 1-2 short documents |
| **IDE workspace + AI chat** | **5 min** | **5-50 documents, one-off or recurring analysis** |
| RAG pipeline | 2-8 hours | 100+ documents, repeated queries by multiple people |
| Enterprise search | Weeks | Organization-wide knowledge management |

### Why this works

Modern AI assistants in IDEs can read the files in your workspace. When you open a chat and reference files or folders, the AI gets that content as context. This turns your folder into a queryable knowledge base with zero setup.

The world is increasingly text-based: meeting transcriptions, Slack exports, Confluence pages exported as markdown, regulatory PDFs converted to text. All of this is AI-ready — you just need to put it in one place.

### Key insight

You don't need to write code to use an IDE productively. The IDE is a powerful text environment with AI built in. Documents are just files. The AI doesn't care whether the file contains Python or a meeting transcript.

---

## Step 2: Security Checkpoint — Before You Start

### What we'll do

Understand the security implications of putting documents into an AI-accessible workspace.

### What happens when you chat about workspace files

When you reference a file in AI chat, the content of that file is sent to the AI model's servers (GitHub Copilot → GitHub/Microsoft/Anthropic/OpenAI, Cursor → their respective providers). This means:

- **The document content leaves your machine**
- **It is processed by a third-party AI service**
- **Retention policies vary by provider and license type**

### Before you begin — get approval

| Document type | Action required |
|---|---|
| Public information | No approval needed |
| Internal company docs | Check with your manager / team lead |
| Client-specific documents | Get explicit client approval |
| Documents with PII (names, emails, IDs) | Anonymize first or don't use |
| Regulated data (HIPAA, GDPR, financial) | Likely prohibited — check with compliance |

### Practical checklist

Before adding documents to your workspace, answer these questions:

1. ✅ Is this data classified as public or internal?
1. ✅ Does my organization allow sending this data to AI services?
1. ✅ Has the client/stakeholder approved AI processing of their materials?
1. ✅ Have I removed or anonymized any PII?
1. ✅ Am I using a business license (not personal) where enterprise data policies apply?

**Verify:** You have mentally (or actually) classified the documents you plan to use and confirmed you have permission to process them with AI.

---

## Step 3: Set Up Your Knowledge Workspace

### What we'll do

Create a dedicated folder and organize your documents for AI consumption.

### Create the workspace folder

1. Create a new folder anywhere on your machine:
   - `c:/workspace/my-knowledge-base/` (Windows) or `~/workspace/my-knowledge-base/` (macOS/Linux)

1. Open this folder in your IDE (VS Code or Cursor) as a workspace:
   - File → Open Folder → select your new folder

### Organize your documents

Create a simple folder structure inside:

```
my-knowledge-base/
├── sources/              ← Raw input documents
│   ├── meeting-notes/    ← Meeting transcriptions, minutes
│   ├── specs/            ← Project specifications, requirements
│   ├── proposals/        ← Proposals, RFCs, decision docs
│   └── reference/        ← Standards, regulations, guidelines
├── analysis/             ← Your AI-assisted analysis outputs
└── README.md             ← What this workspace is for
```

### What to put in

Copy or move your documents into the appropriate subfolder. Supported formats that work best:

| Format | AI readability | Notes |
|---|---|---|
| `.md` (Markdown) | Excellent | Best format — structured, lightweight |
| `.txt` (Plain text) | Excellent | Simple and reliable |
| `.json` | Good | Structured data, AI handles well |
| `.csv` | Good | Tabular data |
| `.html` | Good | AI can parse, but noisy |
| `.pdf` | Limited | Most IDEs can't read PDFs natively — convert to text first |

### Tip: Converting documents

If you have PDFs or Word documents, convert them to markdown or text first:
- Use online converters or ask AI: "Convert this PDF content to clean markdown"
- Copy-paste content from web pages into `.md` files
- Export Confluence/Notion pages as markdown
- Export Slack threads as text

### Create a README.md

Create a `README.md` in the root with a brief description:

```markdown
# Project X Knowledge Base

## Purpose
Collecting and analyzing documentation for Project X onboarding.

## What's here
- Meeting notes from kickoff and weekly syncs
- Technical specifications (architecture, API docs)
- Stakeholder requirements and proposals

## Questions I'm trying to answer
- What are the key technical decisions already made?
- What are the open risks and blockers?
- Who are the key stakeholders and their concerns?
```

This README helps AI understand the context of your workspace when you start asking questions.

**Verify:** You have a workspace open in your IDE with at least 3-5 documents organized in folders with a README.md describing the purpose.

---

## Step 4: Query Your Documents

### What we'll do

Use AI chat to extract answers from your document collection.

### Basic querying techniques

Open AI chat in your IDE and start asking questions. Here are effective patterns:

**Pattern 1: Direct question**
```
Look at the files in the sources/ folder.
What are the main requirements for Project X?
```

**Pattern 2: Cross-document summary**
```
Read all files in sources/meeting-notes/.
Create a timeline of key decisions made across all meetings.
```

**Pattern 3: Extract specific information**
```
From the documents in sources/specs/, extract all mentioned:
- API endpoints
- Database tables
- External integrations
List them in a table format.
```

**Pattern 4: Find contradictions**
```
Compare the requirements in sources/specs/requirements.md
with the decisions in sources/meeting-notes/.
Are there any contradictions or unaddressed requirements?
```

**Pattern 5: Generate action items**
```
Read all meeting notes in sources/meeting-notes/.
Extract all action items, who they're assigned to,
and whether they appear to be completed based on later meetings.
```

**Pattern 6: Explain in simple terms**
```
I'm new to this project. Based on all documents in sources/,
explain the project architecture to me as if I'm joining the team today.
What are the 5 most important things I need to know?
```

### Hands-on

Pick any 3 patterns above and try them against your documents. Adjust the prompts to match your actual content.

**Verify:** You received meaningful answers from at least 3 different queries across your documents.

---

## Step 5: Deep Analysis — Compare and Decide

### What we'll do

Use AI to perform deeper analysis that would take hours to do manually.

### Comparison analysis

If you have multiple proposals or options to evaluate:

```
I have two technical proposals in sources/proposals/.
Compare them across these dimensions:
1. Implementation complexity
2. Timeline
3. Risk factors
4. Cost implications
5. Team skill requirements

Present as a comparison table with a recommendation.
```

### Gap analysis

```
Based on the requirements in sources/specs/requirements.md
and the current architecture described in sources/specs/architecture.md,
what gaps exist? What requirements have no corresponding
technical solution described?
```

### Stakeholder summary

```
I need to present a 5-minute update to leadership.
Based on all documents in sources/, create:
1. A 3-sentence executive summary
2. Top 3 risks with mitigation status
3. Key decision needed from leadership
```

### Hands-on

Choose the analysis type most relevant to your situation and run it. If none of the above fit, describe your actual analysis need to the AI — remember, you can ask anything.

**Verify:** You produced at least one analysis output that would have taken you 30+ minutes to create manually.

---

## Step 6: Summarize and Preserve Knowledge

### What we'll do

Turn your chat session outcomes into reusable artifacts — instructions, knowledge files, or decision records.

### Why summarize

A chat session is ephemeral. The insights you extracted are valuable. Capture them before starting a new session.

### Three output formats

**Format 1: Knowledge summary (for yourself or your team)**

Ask AI:
```
Based on our conversation, create a knowledge summary document.
Include:
- Key findings
- Decisions made or recommended  
- Open questions that remain
- Sources referenced

Save it as analysis/knowledge-summary.md
```

**Format 2: Instruction file (for repeating this process)**

If you'll need to do this type of analysis again:
```
Based on what we did in this session, create an instruction file
that I can use next time I need to analyze similar documents.
Include the prompts that worked best and the folder structure.
Save it as analysis/how-to-analyze.md
```

**Format 3: Decision record (for stakeholders)**

```
Create an Architecture Decision Record (ADR) based on our analysis.
Use the standard ADR format:
- Title, Status, Context, Decision, Consequences
Save it as analysis/adr-001-[topic].md
```

### Hands-on

1. Choose the format most useful for your situation
1. Ask AI to generate the summary
1. Review the output — does it capture the key insights?
1. Save it in your `analysis/` folder

**Verify:** You have at least one summary file in your `analysis/` folder that captures the key findings from your session.

---

## Step 7: Iterate — New Session, New Question

### What we'll do

Understand the workflow for ongoing use.

### The workflow

```
Question arises → Open workspace → Chat with AI → Get insights → Summarize → Close
        ↑                                                              │
        └──────────── New question? Start fresh session ───────────────┘
```

### Best practices for ongoing use

1. **One question per session** — start a fresh chat for each new investigation. This keeps context clean.
1. **Add new documents as they arrive** — drop new meeting notes, updated specs into the appropriate folder.
1. **Keep analysis/ growing** — each session should produce a summary. Over time, this becomes your real knowledge base.
1. **Use any language** — AI handles documents in any language. You can have Russian meeting notes and English specs in the same workspace.
1. **Any format works** — chat exports, copy-pasted emails, Jira ticket dumps, even code comments. If it's text, it's queryable.
1. **Think outside the box** — this isn't just for project docs. Use it for:
   - Researching a technology you're evaluating
   - Preparing for a certification exam
   - Analyzing competitor products from public sources
   - Planning an event from scattered email threads
   - Understanding a legal contract

### When to graduate to RAG

Consider building a proper RAG pipeline (see [Module 190](../190-rag-document-question-answering/about.md)) when:
- You have 100+ documents
- Multiple team members need to query the same corpus
- You need to query the same documents repeatedly over weeks/months
- You need citation tracking (exact source paragraphs)

For everything else, a workspace folder is faster, simpler, and good enough.

---

## Success Criteria

- ✅ You created a dedicated workspace folder with organized subfolders
- ✅ You added at least 3-5 real documents to the workspace
- ✅ You verified security/confidentiality approval for your documents
- ✅ You successfully queried AI about your documents and got useful answers
- ✅ You performed at least one cross-document analysis (comparison, timeline, gap analysis)
- ✅ You summarized your session findings into a reusable file in the `analysis/` folder
- ✅ You understand when this approach is sufficient vs. when to use RAG

---

## Understanding Check

1. **Why does a workspace folder work as a knowledge base without any special setup?**
   - Because modern AI assistants in IDEs can read workspace files as context. When you reference files in chat, their content is sent to the model. No embeddings, no vector database needed.

2. **What security step must you take before adding documents to an AI-accessible workspace?**
   - Verify that you have approval to send the document content to AI services. Check data classification, client permissions, and ensure PII is anonymized or removed.

3. **What document format works best for AI analysis in a workspace, and why?**
   - Markdown (.md) — it's structured, lightweight, and AI can parse it perfectly. Plain text is also excellent. PDFs need conversion first.

4. **When should you graduate from a workspace approach to a proper RAG pipeline?**
   - When you have 100+ documents, need multi-user access, require repeated queries over long periods, or need exact citation tracking.

5. **Why should you summarize your findings at the end of each session?**
   - Chat sessions are ephemeral. Without summarization, the insights are lost when you start a new session. The summary files in `analysis/` become the persistent knowledge base.

6. **Can you use this approach for non-English documents? For non-code content?**
   - Yes to both. AI handles any language and doesn't care whether files contain code or prose. Meeting notes, legal documents, proposals — all work the same way.

7. **What is the README.md in the workspace root for?**
   - It gives AI context about what the workspace contains and what questions you're trying to answer. This improves the relevance of AI responses from the first query.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| AI says it can't access files | Make sure you have the folder open as a workspace (File → Open Folder). Reference files explicitly by path in your prompt. |
| Responses don't reference my documents | Use explicit references: "Read the file sources/specs/requirements.md and..." rather than vague questions. |
| AI context window too small for all docs | Break your query into smaller chunks — ask about one subfolder at a time, then ask for a combined summary. |
| PDF files aren't readable | Convert PDFs to markdown or plain text first. Copy-paste content or use a converter tool. |
| AI hallucinates facts not in my documents | Ask AI to quote the source: "Answer based only on the documents in sources/. Quote the relevant sections." |
| Sensitive data concerns | Review the security checklist in Step 2. When in doubt, don't add the document. Use anonymization. |

---

## Next Steps

You now have a powerful technique for working with documents that doesn't require any coding or infrastructure. Next, explore:

- [090 — AI Skills & Tools Creation](../090-ai-skills-tools-creation/about.md) — learn to package repeatable tasks as AI skills
- [190 — RAG: Document Question Answering](../190-rag-document-question-answering/about.md) — when you're ready to scale up to a proper retrieval pipeline
- [250 — Export Chat Session](../250-export-chat-session/about.md) — save your analysis chat sessions for future reference
