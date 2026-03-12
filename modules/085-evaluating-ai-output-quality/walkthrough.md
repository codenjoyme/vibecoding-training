# Evaluating AI Output Quality - Hands-on Walkthrough

In this module you will build a practical quality evaluation framework for AI output. You will learn to spot hallucinations, score responses systematically, and validate uncertain answers by cross-checking between models.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Cover

- **The trust spectrum** — a framework for deciding your response to any AI output
- **Hallucination patterns** — the five most common ways AI is confidently wrong
- **Scoring rubric** — rate responses on four dimensions
- **Cross-validation** — use two models to surface what's uncertain
- **Quality checklist** — a reusable document for your team

---

## Step 1: The Trust Spectrum

### What we'll do

Build a decision framework for how much to trust a given AI output.

### The spectrum

```
TRUST ←——————————————————————————————→ VERIFY ←——→ REJECT
```

| Zone | When | What to do |
|---|---|---|
| **Trust** | Factual, well-scoped, low stakes, verifiable by running it | Accept and proceed |
| **Verify** | Subjective, complex reasoning, high stakes, involves external data | Check one claim independently |
| **Reject** | Model expressed uncertainty, output contradicts known facts, answer is vague | Rephrase or use different model |

### Task type mapping

| Task type | Default trust level |
|---|---|
| Generate a for-loop | Trust — run it, see if it works |
| Explain a business regulation | Verify — regulations change |
| Write a SQL migration | Verify — check schema against your DB |
| Predict future market trends | Reject — not a factual task |
| Debug a specific error | Trust but test |

### Hands-on

Take 5 recent AI outputs you received (from any chat session). Assign each to Trust / Verify / Reject. Were any in Verify that you accepted without checking?

**Verify:** You have 5 responses categorised with a brief justification for each placement.

---

## Step 2: Hallucination Detection Patterns

### What we'll do

Learn the five most common hallucination patterns and how to recognise them in real outputs.

### The 5 patterns

**Pattern 1: Confident citation of fake sources**

> "According to the 2023 McKinsey report on AI adoption, 73% of enterprises..."

Check: Does this report exist? Is that statistic in it? AI invents specific-sounding numbers and titles.

**Pattern 2: Plausible-but-wrong API**

> "Use `os.path.listrecursive(path)` to list files recursively."

`listrecursive` doesn't exist. AI generates plausible-sounding function names that match the naming pattern of real functions.

**Pattern 3: Outdated information stated as current**

> "The latest version of React is 17.0.2."

AI's training has a cutoff. Anything about "current", "latest", "new" is suspect.

**Pattern 4: Mixing correct and incorrect details**

> "Kubernetes was created by Google and open-sourced in 2013, written in Java."

The first part is correct (Google, 2013). The last part is wrong (Go, not Java). Hallucinations often attach to correct facts.

**Pattern 5: Overfitting to the question form**

> Q: "What are the three main causes of the 2008 financial crisis?"  
> A: Three causes are listed, even if the model isn't sure there are exactly three.

AI will produce N items when asked for N, even if there are only 2 real ones or 7 real ones.

### Hands-on

Ask AI: "What is the current stable version of Python and what are its top 3 new features?"

Examine the response. Identify: is the version number correct (check python.org)? Are the features real?

**Verify:** You found at least one thing to verify in the response, and you checked it against an authoritative source.

---

## Step 3: Practical Scoring Rubric

### What we'll do

Score an AI response on four dimensions to produce an objective quality rating.

### The rubric

For each response, score 1–5 on:

| Dimension | 1 | 5 |
|---|---|---|
| **Correctness** | Factually wrong | Fully accurate |
| **Completeness** | Misses the point | Covers everything asked |
| **Relevance** | Off-topic | Directly addresses the question |
| **Safety** | Introduces risk (security flaw, bad advice) | No risks introduced |

**Composite score** = average of four dimensions. Below 3.5 → reject and retry.

### Hands-on

Ask AI the same question three times with slight prompt variations:
1. "Explain Docker containers in simple terms."
2. "Explain Docker containers to a non-technical manager."
3. "What is Docker and how does it differ from a virtual machine?"

Score each response on the rubric. Which variation produced the highest composite score?

Save scores as a table in `c:/workspace/hello-genai/quality-scores.md` (Windows) or `~/workspace/hello-genai/quality-scores.md` (macOS).

**Verify:** You have three scored responses and can explain which prompt produced better quality and why.

---

## Step 4: Cross-Validation Technique

### What we'll do

Use two different AI models on the same question to surface uncertainty.

### Why two models?

When both models agree → high confidence the answer is correct.  
When models disagree → the topic is either complex, contested, or prone to hallucination.  
Disagreement is a signal to verify independently.

### Hands-on

Pick a topic you're genuinely unsure about (e.g. "What is the maximum context window of Claude Sonnet 4.5?").

1. Ask in Copilot (or any Model A). Note the answer.
2. Ask in a second model (Claude, Gemini, or any other). Note the answer.
3. If they agree → accept with reasonable confidence.  
4. If they disagree → check official documentation.

**Verify:** You performed cross-validation on at least one fact and documented whether the models agreed or disagreed.

---

## Step 5: Build a Quality Checklist

### What we'll do

Create a reusable one-page checklist your team can apply to any critical AI output.

### The checklist

Create `c:/workspace/hello-genai/ai-quality-checklist.md` (Windows) or `~/workspace/hello-genai/ai-quality-checklist.md` (macOS):

```markdown
# AI Output Quality Checklist

Use this before accepting any AI-generated content that affects production, customers, or critical decisions.

## 1. Trust Level
- [ ] Is this a Trust / Verify / Reject task? (mark one)
- [ ] If Verify → did I check at least one claim independently?

## 2. Hallucination Check
- [ ] Does the response cite specific statistics or sources? → Verify them.
- [ ] Does it mention specific API methods or library functions? → Test them.
- [ ] Does it use "latest", "current", "new"? → Check official docs.
- [ ] Were exactly N items requested? → Are all N real?

## 3. Scoring (optional, for important outputs)
- [ ] Correctness: /5
- [ ] Completeness: /5
- [ ] Relevance: /5
- [ ] Safety: /5
- [ ] Composite ≥ 3.5?

## 4. Cross-Validation (for high-stakes decisions)
- [ ] Did I check with a second model?
- [ ] Do both models agree?
```

**Verify:** The checklist file exists and has all four sections.

---

## Success Criteria

- ✅ You can place any AI task on the Trust / Verify / Reject spectrum
- ✅ You identified all 5 hallucination patterns and spotted at least one in a real AI output
- ✅ You scored three AI responses using the rubric and identified which prompt produced higher quality
- ✅ You performed cross-validation on at least one factual claim
- ✅ You have a quality checklist file ready to use and share

---

## Understanding Check

1. **AI gives you a SQL query. Where on the Trust spectrum does it belong?** *(Answer: Verify — run it against a test or staging database first. SQL mutations are irreversible on production.)*

2. **AI says "According to a 2024 Gartner report, 85% of developers use AI tools daily." How do you check this?** *(Answer: Search for the specific Gartner report by title. If you can't find it, treat the statistic as unverified. Gartner reports are usually paywalled but their titles are indexed.)*

3. **You asked two models the same question and they gave different answers. What should you do?** *(Answer: Go to an authoritative primary source — official documentation, RFC, peer-reviewed paper — rather than accepting either model's answer.)*

4. **A response scores 4/5 on Correctness, 2/5 on Completeness, 5/5 on Relevance, 4/5 on Safety. What is the composite? Should you accept it?** *(Answer: (4+2+5+4)/4 = 3.75. Borderline — the low completeness means the answer is missing something important. Ask a follow-up before accepting.)*

5. **Why does asking for "exactly 5 examples" increase hallucination risk?** *(Answer: The model will generate exactly 5 regardless of how many valid examples actually exist. If there are only 3 strong examples, it will invent 2 weaker or wrong ones.)*

---

## Troubleshooting

**"Both models gave wrong answers that sound convincing."**  
→ Model agreement doesn't guarantee correctness — both could be trained on the same wrong information. For critical facts, always verify against a primary source (official documentation, standards body, peer-reviewed work).

**"I don't know how to tell if an API function name is real."**  
→ The fastest check: paste the function name into an official documentation search (docs.python.org, developer.mozilla.org, etc.). If it doesn't appear there, it doesn't exist.

**"Scoring takes too long for every AI output."**  
→ Only score when the stakes are high (production code, customer-facing content, security decisions). For low-stakes outputs (draft text, exploratory code), the Trust/Verify/Reject quick check is sufficient.

---

## Next Steps

Continue to [Module 090 — AI Skills & Tools Creation](../090-ai-skills-tools-creation/about.md) where you will learn that parameterised tools eliminate entire categories of hallucinations by replacing AI judgment with deterministic execution — the ultimate quality guarantee.
