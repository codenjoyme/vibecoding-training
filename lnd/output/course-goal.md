# Course Goal and Learning Outcomes

## Goal

This course equips managers and non-engineering professionals with the
practical fluency, judgement, and tooling to thrive in a world where GenAI
is embedded into every layer of software work. By the end of the course
participants are not only able to vibe-code their own prototypes — they
also understand how the modern GenAI ecosystem operates, can intelligently
guide and support the engineers on their teams who are using these tools
day-to-day, can prototype managerial and analytical instruments themselves
without pulling engineering capacity, and can speak about and sell GenAI
solutions to clients with credibility grounded in hands-on experience.

The course deliberately blends three layers that are usually taught
separately:

1. **Hands-on practitioner skills** — using AI assistants inside an IDE,
   prompting, version control, debugging AI output, building reusable
   skills and MCP integrations.
2. **Ecosystem and architectural literacy** — how agent mode works under
   the hood, how models differ, what context windows and tool-calling do,
   how MCP servers extend an agent, what the cost trade-offs are.
3. **Managerial and commercial leverage** — how to support engineers
   adopting these tools, how to evaluate AI output quality, how to set
   team conventions via shared instructions, how to position GenAI work
   honestly to clients.

## Learning Outcomes

Upon completion of this course, you should be able to:

### Practitioner outcomes (vibe-coding)

- Work confidently with AI assistants inside an IDE without a developer
  background.
- Translate business or managerial intent into clear, structured
  instructions for AI agents.
- Apply safety mechanisms (version control, incremental changes, branch
  hygiene) to protect and recover work.
- Control AI output quality by defining constraints, structure, and
  instructions; verify generated changes before accepting them.
- Identify and correct common AI failure patterns such as hallucinations,
  unintended edits, and silent regressions.
- Reuse effective AI solutions through reusable skills, instructions, and
  prompt files instead of repeating ad-hoc prompts.
- Move from an idea to a working prototype using a structured,
  AI-assisted, iterative approach.

### Ecosystem-literacy outcomes

- Explain how an agent loop works: tools, context window, planning, file
  reads/writes, terminal calls.
- Compare premium and non-premium models on capability, latency, and cost,
  and choose the right one for a task.
- Understand what Model Context Protocol (MCP) is, why it exists, and
  install / configure / build MCP servers (including custom Python
  servers) to extend an agent's reach.
- Understand the role of skills, custom instructions, shared team
  instructions, prompt files, and memory files in shaping agent behaviour.
- Reason about token cost, premium-request budgets, and idle-time strategies
  (iterative-prompt loops, polling watchers).

### Leverage-multiplier outcomes (manager-as-enabler)

- Coach and unblock the engineers on your team who are adopting AI
  assistants — recognise productive vs unproductive usage patterns and
  intervene appropriately.
- Build internal team conventions (shared instructions, skill libraries,
  MCP toolkits) so the whole team benefits from one person's discoveries.
- Automate typical managerial workflows yourself — reports, analytics,
  integrations, document generation, repetitive cleanup — without queuing
  engineering tickets.
- Rapidly prototype POCs (e.g. via Spec Kit, custom MCP servers, browser
  automation) to validate ideas before involving engineering resources.
- Evaluate vendor and consultant claims about GenAI critically — you have
  built the same things yourself and know what is realistic.

### Commercial outcomes (selling GenAI)

- Speak about GenAI capabilities, limits, costs, and risks to clients
  with concrete examples drawn from your own hands-on work.
- Propose realistic GenAI engagements: scope, deliverables, success
  criteria, model and tool choices, and verification strategy.
- Demonstrate value through live prototyping rather than slideware.
- Position your team's GenAI maturity credibly because that maturity
  is real and visible in shared artefacts (skill libraries, MCP servers,
  team instructions, version-controlled prompt files).
