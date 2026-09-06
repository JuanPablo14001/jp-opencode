# JP OpenCode Model Strategy

JP OpenCode uses multiple independent model pools.

The objective is not to maximize usage of any single provider.

The objective is to distribute work according to:

- capability;
- specialization;
- cost;
- task complexity;
- task risk;
- methodological impact when working with data;
- available quota.

The system should preserve expensive model capacity for work where stronger reasoning or coding capability materially improves correctness.

Model selection follows one central rule:

> Use the cheapest model that can reliably complete the task correctly.

Cost optimization must never override engineering or analytical correctness.

---

# Available Model Pools

## OpenCode Zen Free

OpenCode Zen Free models should absorb high-volume, bounded, low-risk work whenever their quality is sufficient.

Currently available models include:

- Big Pickle;
- Ling 3.0 Flash Fin Free;
- MiMo V2.5 Free;
- Muse Spark 1.2 Contributor Free;
- Muse Spark 1.3 Contributor Free;
- Nemotron 3 Ultra Free;
- Nemotron 3.5 Lightning Free.

Zen Free is primarily intended for:

- Lite exploration;
- lightweight review;
- lightweight documentation;
- testing and verification;
- schema inspection;
- mechanical tasks;
- bounded low-risk work.

Free does not mean disposable.

A free model should still have:

- a clear role;
- a strict work budget;
- escalation rules;
- a concise output contract.

A free model must not compensate for insufficient capability by consuming excessive context or making unsupported assumptions.

---

# OpenCode Go

OpenCode Go is the primary paid daily-use pool.

Currently available models include:

- GPT-5.6 Luna;
- DeepSeek V4 Pro;
- DeepSeek V4 Flash;
- GLM-5.3;
- GLM-5.3 Flash;
- GLM-5.2;
- GLM-5.1;
- Kimi K3;
- Kimi K2.7 Code;
- Kimi K2.6;
- Qwen3.8 Max;
- Qwen3.8 Flash;
- Qwen3.7 Max;
- Qwen3.7 Plus;
- Qwen3.6 Plus;
- MiMo V2.5;
- MiMo V2.5 Pro;
- MiniMax M3;
- MiniMax M2.7;
- LongCat 2.0;
- Grok 4.6;
- other models available through the current Go plan.

OpenCode Go should absorb most everyday Full-agent work.

It should not become synonymous with GPT-5.6 Luna.

Different Go models should be selected according to role.

---

# OpenAI / Codex

ChatGPT Plus/Pro and Codex capacity form the premium reasoning and implementation pool.

Currently available models include:

- GPT-5.6 Luna;
- GPT-5.6 Luna Fast;
- GPT-5.6 Sol;
- GPT-5.6 Sol Fast;
- GPT-5.6 Terra;
- GPT-5.6 Terra Fast;
- other available OpenAI models.

JP OpenCode should avoid spending Codex capacity on:

- routine exploration;
- testing;
- simple documentation;
- mechanical transformations;
- straightforward UI work;
- small implementation tasks.

Codex should be selected because stronger capability materially improves the expected result.

---

# Provider Priority

Provider priority is capability-based rather than absolute.

A useful default is:

Zen Free
-> OpenCode Go
-> OpenAI / Codex

when capability allows.

This is not a mandatory escalation chain.

A task may route directly to Codex when its specialization or impact justifies it.

Examples:

- architecture may route directly to GPT-5.6 Sol;
- difficult implementation may route directly to Terra Fast;
- analytical methodology may route directly to Sol.

---

# Initial Code-Orchestrator Model Map

This is the initial working Code configuration.

| Agent | Provider | Model |
|---|---|---|
| `jp-code-orchestrator` | OpenCode Go | GPT-5.6 Luna |
| `jp-explorer-lite` | OpenCode Zen Free | Muse Spark 1.3 Contributor Free |
| `jp-explorer` | OpenCode Go | DeepSeek V4 Pro |
| `jp-architect` | OpenAI / Codex | GPT-5.6 Sol |
| `jp-designer-lite` | OpenCode Go | Qwen3.8 Flash |
| `jp-designer` | OpenCode Go | GLM-5.3 |
| `jp-coder-lite` | OpenCode Go | Qwen3.8 Flash |
| `jp-coder` | OpenCode Go | Kimi K2.7 Code |
| `jp-coder-heavy` | OpenAI / Codex | GPT-5.6 Terra Fast |
| `jp-reviewer-lite` | OpenCode Zen Free | MiMo V2.5 Free |
| `jp-reviewer` | OpenCode Go | GPT-5.6 Luna |
| `jp-documenter-lite` | OpenCode Zen Free | MiMo V2.5 Free |
| `jp-documenter` | OpenCode Go | Qwen3.7 Plus |
| `jp-tester` | OpenCode Zen Free | Muse Spark 1.3 Contributor Free |

---

# Initial Data-Orchestrator Model Map

Data uses the same pools but optimizes them differently.

Mechanical work remains inexpensive.

Methodological reasoning does not.

| Agent | Provider | Model |
|---|---|---|
| `jp-data-orchestrator` | OpenCode Go | GPT-5.6 Luna |
| `jp-data-explorer-lite` | OpenCode Zen Free | Muse Spark 1.3 Contributor Free |
| `jp-data-explorer` | OpenCode Go | DeepSeek V4 Pro |
| `jp-data-analyst` | OpenAI / Codex | GPT-5.6 Sol |
| `jp-sql-lite` | OpenCode Go | Qwen3.8 Flash |
| `jp-sql` | OpenCode Go | DeepSeek V4 Pro |
| `jp-data-coder-lite` | OpenCode Go | Qwen3.8 Flash |
| `jp-data-coder` | OpenCode Go | Kimi K2.7 Code |
| `jp-data-reviewer-lite` | OpenCode Zen Free | MiMo V2.5 Free |
| `jp-data-reviewer` | OpenCode Go | GPT-5.6 Luna |
| `jp-data-documenter-lite` | OpenCode Zen Free | MiMo V2.5 Free |
| `jp-data-documenter` | OpenCode Go | Qwen3.7 Plus |
| `jp-data-tester` | OpenCode Zen Free | Muse Spark 1.3 Contributor Free |

---

# Why Luna Is Limited

GPT-5.6 Luna is intentionally not assigned to every Full agent.

Its initial roles are:

## Code

- Code Orchestrator;
- Full Reviewer;
- fallback general reasoning.

## Data

- Data Orchestrator;
- Full Data Reviewer;
- fallback general reasoning.

The orchestrators benefit from Luna because they must:

- interpret nuanced requests;
- preserve business constraints;
- preserve technical or analytical constraints;
- classify intent;
- evaluate routing dimensions;
- challenge poor decisions;
- coordinate specialist handoffs;
- synthesize results.

The orchestrators should not:

- perform broad exploration;
- implement large features;
- perform large reviews inline;
- run extensive verification themselves;
- conduct full statistical methodology inline.

This keeps Luna high-value and relatively low-volume.

---

# Why Codex Is Restricted

Codex capacity is intentionally reserved for high-value work.

## GPT-5.6 Sol

Primary roles:

- `jp-architect`;
- `jp-data-analyst`.

Use Sol for:

- architecture;
- difficult system design;
- database design;
- complex state models;
- security-sensitive design;
- analytical methodology;
- KPI definition;
- statistical reasoning;
- population definition;
- important reconciliation methodology;
- high-impact engineering or analytical trade-offs.

Sol should reason about difficult decisions more often than it implements routine work.

## GPT-5.6 Terra Fast

Primary role:

- `jp-coder-heavy`.

Use Terra Fast for:

- unusually difficult implementation;
- complex multi-file coding;
- important refactors;
- intricate integration logic;
- implementation where Full Coder has insufficient confidence.

Terra Fast is not the default coding model.

---

# Lite Model Philosophy

Lite agents exist to absorb bounded work cheaply.

Typical Lite workloads include:

- small investigations;
- isolated UI work;
- localized code changes;
- straightforward SQL;
- mechanical data transformations;
- lightweight review;
- localized documentation;
- testing and verification.

Lite means bounded, not careless.

Lite agents must operate under explicit limits.

When those limits are exceeded:

`STATUS: ESCALATE`

is the correct result.

Escalation is expected behavior.

---

# Data Model Philosophy

Data work requires an additional distinction:

> Implementation complexity and methodological complexity are not the same thing.

Ten lines of Pandas or SQL can materially change:

- analytical population;
- denominators;
- time windows;
- duplicate handling;
- joins;
- missing-value treatment;
- financial reconciliation;
- statistical interpretation.

Therefore cheap models are appropriate for:

- schema inspection;
- simple SQL;
- file loading;
- mechanical transformations;
- basic plots;
- execution;
- lightweight documentation.

Stronger models should handle:

- methodology;
- analytical interpretation;
- statistical reasoning;
- important KPI definitions;
- reconciliation logic;
- population selection;
- meaningful business conclusions.

There is intentionally no `jp-data-analyst-lite`.

---

# Model Selection Is Role-Based

JP OpenCode must not assume that one model is best for every task.

Examples:

- Kimi K2.7 Code may be preferable to a more expensive general model for implementation;
- Muse may be sufficient for executing tests;
- DeepSeek V4 Pro may be more cost-effective for broad exploration than Luna;
- Sol is valuable for architecture and methodology but wasteful for mechanical work;
- MiMo Free may be sufficient for a bounded independent review.

Models are implementations of roles.

They are not the roles themselves.

---

# Agent Responsibilities Must Be Provider-Independent

Agent prompts should remain stable when model assignments change.

For example:

`jp-coder`

is a responsibility.

Its current implementation uses:

`opencode-go/kimi-k2.7-code`

A future configuration may assign another model without changing:

- its scope;
- its permissions;
- its escalation contract;
- its engineering responsibilities.

This separation allows JP OpenCode to evolve without rewriting its architecture around provider churn.

---

# Observability-Driven Tuning

The initial model maps are working defaults, not permanent truths.

JP OpenCode should evolve from real usage.

Useful signals include:

- agent usage frequency;
- model usage frequency;
- provider distribution;
- Lite escalation rate;
- Full-to-Heavy escalation rate;
- failed tasks;
- repeated exploration;
- latency;
- input/output tokens where available;
- cost where available;
- rerouting after apparently successful work.

Examples:

If `jp-explorer-lite` escalates most executions:

- its work budget may be too strict;
- its model may be insufficient;
- the orchestrator may be routing too aggressively to Lite.

If `jp-designer-lite` escalates frequently:

- its model may be inappropriate for the role;
- visual ambiguity thresholds may need adjustment.

If Luna dominates total calls:

- Full routing may be too aggressive;
- cheaper specialists may be underused;
- the orchestrator may be doing too much work.

If Codex dominates implementation:

- Heavy routing is probably too permissive.

If a cheap model rarely escalates and produces reliable work:

- its responsibility may safely expand.

Optimization should be based on working sessions rather than synthetic benchmarks alone.

---

# Future Model Profiles

JP OpenCode may later expose profiles such as:

- Free;
- Balanced;
- Premium;
- custom user profiles.

Profiles are intentionally deferred.

A profile should change model assignments without changing agent responsibilities or routing semantics.

The current system uses one opinionated model map optimized for the project's primary use case.

---

# Model Configuration Principle

Hardcoded model assignments in agent frontmatter are acceptable for the initial version.

Long term, the project should aim for:

responsibility
-> model mapping
-> generated/installed agent configuration

rather than coupling responsibilities permanently to one model.

This enables future profiles without redesigning the agents themselves.