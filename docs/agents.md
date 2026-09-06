# JP OpenCode Agents

JP OpenCode is built around specialized agents instead of assigning every task to the same model.

Each agent has:

- a clearly defined responsibility;
- a bounded scope;
- a model selected for that responsibility;
- an escalation path when the task exceeds its intended capability.

The objective is not to use the strongest model everywhere.

The objective is to use the cheapest model that can reliably complete each role without sacrificing engineering or analytical quality.

JP OpenCode currently contains two primary families:

- Code
- Data

Both families are coordinated by their own orchestrator.

---

# Agent Families

## Code

The Code family handles:

- repository exploration;
- software architecture;
- UI/UX design;
- implementation;
- review;
- documentation;
- testing.

Primary orchestrator:

```text
jp-code-orchestrator
```

---

## Data

The Data family handles:

- data exploration;
- analytical methodology;
- SQL;
- Pandas and analytical implementation;
- data review;
- analytical documentation;
- verification.

Primary orchestrator:

```text
jp-data-orchestrator
```

---

# Code Agents

## `jp-code-orchestrator`

**Provider:** OpenCode Go  
**Model:** `opencode-go/gpt-5.6-luna`  
**Level:** Orchestrator  
**Permissions:** Limited direct work + delegation

### Function

Coordinates software-development work and decides which specialist should handle each part of the task.

### Description

The Code Orchestrator is the main user-facing agent for software development.

It evaluates:

- scope;
- risk;
- ambiguity;
- specialization.

It decides whether work should be:

- handled directly;
- delegated to a Lite specialist;
- delegated to a Full specialist;
- escalated to Heavy implementation.

It preserves business and technical constraints while keeping the parent context small.

The orchestrator should not become the default coder, explorer, reviewer, or documenter.

### Why GPT-5.6 Luna

Orchestration requires broad reasoning rather than narrow specialization.

Luna is used because the role must:

- understand nuanced requirements;
- retain constraints;
- classify intent;
- judge task complexity;
- detect risky engineering decisions;
- coordinate several specialists;
- synthesize their results.

Using a weaker model here could produce poor routing decisions that increase cost later.

Using Sol for every orchestration turn would consume premium capacity unnecessarily.

Luna provides a strong balance between reasoning quality and daily-use cost.

---

## `jp-explorer-lite`

**Provider:** OpenCode Zen Free  
**Model:** `opencode/muse-spark-1.3-contributor-free`  
**Level:** Lite  
**Permissions:** Read-only

### Function

Performs small, localized repository investigations.

### Description

Explorer Lite is used when the relevant area is already mostly known and the investigation should remain bounded.

Typical work includes:

- locating validation;
- tracing one field;
- finding the controller for a route;
- identifying which service calls an API;
- understanding one local condition;
- locating a component or configuration value.

The expected scope is usually around five relevant files or fewer.

If the investigation expands, it must return `STATUS: ESCALATE`.

### Why Muse Spark 1.3 Contributor Free

Repository exploration is frequently high-volume but low-risk.

A capable free model is ideal because:

- many exploration tasks are mechanical;
- the role is read-only;
- mistakes do not directly modify source code;
- strict scope limits prevent the model from consuming excessive context.

If Muse cannot complete the investigation within its budget, escalation to the Full Explorer is cheaper than using an expensive model for every search.

---

## `jp-explorer`

**Provider:** OpenCode Go  
**Model:** `opencode-go/deepseek-v4-pro`  
**Level:** Full  
**Permissions:** Read-only

### Function

Performs broad repository exploration and complex root-cause investigation.

### Description

Explorer is used when:

- multiple modules interact;
- more than a few files must be traced;
- frontend and backend interact;
- database, jobs, middleware, or APIs must be inspected together;
- the root cause is unclear;
- Explorer Lite escalated.

It reconstructs flows and returns concise findings rather than dumping source code into the parent context.

### Why DeepSeek V4 Pro

Full exploration requires more reasoning and context handling than Lite exploration, but it usually does not require premium Codex capability.

DeepSeek V4 Pro is used because it is a strong fit for:

- codebase navigation;
- multi-file reasoning;
- dependency tracing;
- root-cause investigation;
- synthesizing technical evidence.

It keeps broad exploration inside the OpenCode Go pool instead of consuming Luna or Codex capacity.

---

## `jp-architect`

**Provider:** OpenAI / Codex  
**Model:** `openai/gpt-5.6-sol`  
**Level:** Full specialist  
**Permissions:** Read-only

### Function

Makes high-value architecture and system-design decisions.

### Description

Architect is used for meaningful decisions involving:

- system boundaries;
- database design;
- schema evolution;
- domain modeling;
- state machines;
- public APIs;
- integrations;
- concurrency;
- scalability;
- migration strategy;
- long-term coupling;
- important engineering trade-offs.

There is intentionally no Architect Lite.

Architecture mistakes can create long-term cost far beyond the price of a single model call.

### Why GPT-5.6 Sol

Architecture requires strong reasoning more than raw implementation speed.

Sol is reserved for this role because it provides better capability for:

- trade-off analysis;
- system decomposition;
- long-term design reasoning;
- responsibility boundaries;
- high-impact technical decisions.

Architecture is one of the areas where aggressively minimizing model cost would be counterproductive.

---

## `jp-designer-lite`

**Provider:** OpenCode Go  
**Model:** `opencode-go/qwen3.8-flash`  
**Level:** Lite  
**Permissions:** Read-only

### Function

Defines small UI/UX changes using an existing design language.

### Description

Designer Lite handles bounded UI work such as:

- one card;
- one badge;
- one small modal;
- one compact form;
- one responsive adjustment;
- one isolated component.

It does not implement source code by default.

Its responsibility is to define the visual and UX solution so a Coder can implement it.

### Why Qwen3.8 Flash

Small UI tasks benefit from:

- fast iteration;
- decent frontend understanding;
- low cost;
- sufficient reasoning for existing design systems.

Qwen3.8 Flash is used instead of a free model because UI interpretation can require more nuance than mechanical repository exploration.

The Lite scope still limits how much context the model should consume.

---

## `jp-designer`

**Provider:** OpenCode Go  
**Model:** `opencode-go/glm-5.3`  
**Level:** Full  
**Permissions:** Read-only

### Function

Handles substantial UI/UX design and multi-component interaction.

### Description

Designer is used when:

- several components interact;
- an entire section must be designed;
- UX behavior is ambiguous;
- visual hierarchy matters;
- responsive behavior is substantial;
- a design-system decision is required;
- a large Figma section must be interpreted.

Designer defines the intended experience.

Coder remains responsible for implementation.

### Why GLM-5.3

Full design work requires stronger reasoning about:

- visual hierarchy;
- component relationships;
- interaction states;
- responsive behavior;
- UX consistency.

GLM-5.3 provides stronger general design reasoning than the Lite model while remaining inside the Go pool.

This avoids spending premium Codex capacity on UI work that does not normally require it.

---

## `jp-coder-lite`

**Provider:** OpenCode Go  
**Model:** `opencode-go/qwen3.8-flash`  
**Level:** Lite  
**Permissions:** Write

### Function

Implements small, clearly defined code changes.

### Description

Coder Lite handles implementation when:

- the solution is already conceptually clear;
- approximately one or two related files are involved;
- the expected change is small;
- risk is low;
- no architecture decision is needed;
- no important public contract changes.

Typical work includes:

- small CRUD behavior;
- localized validation;
- mapper changes;
- small filtering logic;
- one small component.

It must escalate rather than attempting a large or risky implementation.

### Why Qwen3.8 Flash

Lite coding needs a model that is:

- fast;
- inexpensive;
- competent with code;
- suitable for bounded implementation.

Qwen3.8 Flash provides enough coding capability for localized work without consuming Full Coder or Codex capacity.

---

## `jp-coder`

**Provider:** OpenCode Go  
**Model:** `opencode-go/kimi-k2.7-code`  
**Level:** Full  
**Permissions:** Write

### Function

Acts as the primary implementation specialist for normal non-trivial software changes.

### Description

Coder handles:

- several related files;
- business logic;
- frontend/backend changes;
- focused refactors;
- broader implementation context;
- tasks escalated by Coder Lite.

It is usually the main implementation owner for a bounded feature or fix.

### Why Kimi K2.7 Code

The Full Coder benefits more from coding specialization than from a more expensive general reasoning model.

Kimi K2.7 Code is selected because it is suited for:

- multi-file implementation;
- code generation;
- refactoring;
- existing-code modification;
- following established architecture.

This keeps most day-to-day implementation inside OpenCode Go.

---

## `jp-coder-heavy`

**Provider:** OpenAI / Codex  
**Model:** `openai/gpt-5.6-terra-fast`  
**Level:** Heavy  
**Permissions:** Write

### Function

Handles unusually difficult or high-impact implementation.

### Description

Coder Heavy is used only when:

- implementation complexity is exceptional;
- important system behavior is involved;
- Coder identifies genuine difficulty;
- architectural constraints must be translated into intricate code;
- stronger coding capability materially improves correctness.

Heavy is not a synonym for "large task."

### Why GPT-5.6 Terra Fast

Terra Fast is reserved for difficult implementation because premium coding capability is most valuable when:

- several difficult constraints interact;
- implementation errors would be expensive;
- Full Coder confidence is insufficient;
- the code requires unusually strong synthesis.

Restricting Terra Fast to Heavy work protects Codex quota.

---

## `jp-reviewer-lite`

**Provider:** OpenCode Zen Free  
**Model:** `opencode/mimo-v2.5-free`  
**Level:** Lite  
**Permissions:** Read-only

### Function

Reviews small, low-risk code changes.

### Description

Reviewer Lite focuses on:

- correctness;
- obvious bugs;
- missing validation;
- basic edge cases;
- simple maintainability problems.

It is appropriate for small localized diffs.

If the change involves substantial business rules, security, public APIs, or broader regression risk, it escalates.

### Why MiMo V2.5 Free

Review benefits from an independent model perspective.

For small low-risk diffs, a free model can provide that second opinion economically.

MiMo V2.5 Free is assigned because:

- the work is read-only;
- the scope is bounded;
- independent review is valuable even when the model is inexpensive;
- larger problems can escalate to the Full Reviewer.

---

## `jp-reviewer`

**Provider:** OpenCode Go  
**Model:** `opencode-go/gpt-5.6-luna`  
**Level:** Full  
**Permissions:** Read-only

### Function

Performs full code review for meaningful or risky changes.

### Description

Reviewer evaluates:

- correctness;
- regressions;
- security;
- data integrity;
- business rules;
- public contracts;
- edge cases;
- testing gaps;
- maintainability;
- performance when relevant.

It is intended to provide a fresh perspective after substantive implementation.

### Why GPT-5.6 Luna

Full review requires broad reasoning across multiple dimensions.

Luna is used because review often requires understanding:

- user intent;
- business rules;
- implementation details;
- regression risk;
- cross-file interactions.

A general reasoning model is more appropriate here than a narrowly coding-focused model.

---

## `jp-documenter-lite`

**Provider:** OpenCode Zen Free  
**Model:** `opencode/mimo-v2.5-free`  
**Level:** Lite  
**Permissions:** Documentation-only write

### Function

Writes small, localized technical documentation.

### Description

Documenter Lite handles:

- one endpoint;
- one component;
- one small README section;
- docstrings;
- PHPDoc;
- JSDoc;
- small examples;
- changelog entries;
- localized technical comments.

It documents verified behavior.

It must not change executable behavior.

### Why MiMo V2.5 Free

Localized documentation is usually low-risk and high-volume.

A free model is sufficient when:

- the behavior is already understood;
- the documentation scope is small;
- no broad system reconstruction is needed.

If broader synthesis is required, the task escalates to Full Documenter.

---

## `jp-documenter`

**Provider:** OpenCode Go  
**Model:** `opencode-go/qwen3.7-plus`  
**Level:** Full  
**Permissions:** Documentation-only write

### Function

Documents modules, workflows, architecture, and substantial implementation changes.

### Description

Documenter handles documentation that requires synthesis across:

- multiple files;
- several endpoints;
- complete modules;
- architecture;
- major workflows;
- refactors;
- installation;
- operations;
- reusable components.

It documents verified behavior rather than intended behavior.

### Why Qwen3.7 Plus

Full documentation requires:

- larger context synthesis;
- clear technical writing;
- understanding multiple interacting parts;
- preserving implementation accuracy.

Qwen3.7 Plus provides stronger synthesis capability than the Lite model without spending Luna or Codex capacity.

---

## `jp-tester`

**Provider:** OpenCode Zen Free  
**Model:** `opencode/muse-spark-1.3-contributor-free`  
**Level:** Verification  
**Permissions:** Execute safe checks, no source writes

### Function

Runs software verification commands.

### Description

Tester handles:

- unit tests;
- integration tests;
- linting;
- type checking;
- builds;
- static analysis;
- reproduction commands;
- targeted verification.

It reports failures and classifies whether they appear related to:

- code;
- tests;
- environment;
- tooling.

Tester does not silently fix implementation.

### Why Muse Spark 1.3 Contributor Free

Running and interpreting bounded verification commands usually does not require an expensive reasoning model.

A free model is ideal because testing can generate many repeated calls.

If deeper investigation is required, the orchestrator routes the failure to Explorer, Coder, or Reviewer instead of upgrading Tester.

---

# Data Agents

## `jp-data-orchestrator`

**Provider:** OpenCode Go  
**Model:** `opencode-go/gpt-5.6-luna`  
**Level:** Orchestrator  
**Permissions:** Limited direct work + delegation

### Function

Coordinates data-analysis work and protects methodological correctness.

### Description

The Data Orchestrator is the primary user-facing agent for analytical tasks.

It evaluates:

- scope;
- risk;
- ambiguity;
- specialization;
- methodological impact.

It distinguishes between:

- exploration;
- methodology;
- SQL;
- implementation;
- review;
- verification;
- documentation.

The Data Orchestrator is specifically designed to prevent short code or SQL from being incorrectly treated as low-risk when it changes analytical meaning.

### Why GPT-5.6 Luna

Data orchestration requires broad reasoning across technical and methodological concerns.

Luna is appropriate because the agent must:

- understand business questions;
- preserve analytical assumptions;
- reason about populations and metrics;
- decide when methodology requires a specialist;
- coordinate several data agents;
- prevent cheap mechanical work from silently changing analytical meaning.

Sol would be excessive for every orchestration turn.

Luna offers the appropriate balance.

---

## `jp-data-explorer-lite`

**Provider:** OpenCode Zen Free  
**Model:** `opencode/muse-spark-1.3-contributor-free`  
**Level:** Lite  
**Permissions:** Read-only

### Function

Performs bounded exploration of datasets, tables, schemas, notebooks, and metric sources.

### Description

Data Explorer Lite handles questions such as:

- which table contains a field;
- where a dataset is loaded;
- where a metric originates;
- which notebook performs a transformation;
- which date field is used;
- what columns exist.

It is intended for small structural investigations.

It does not decide whether methodology is analytically correct.

### Why Muse Spark 1.3 Contributor Free

Schema inspection and localized lineage tracing are often mechanical.

A free model can handle large volumes of this work efficiently.

Strict scope limits prevent the agent from attempting broad analytical reconstruction.

---

## `jp-data-explorer`

**Provider:** OpenCode Go  
**Model:** `opencode-go/deepseek-v4-pro`  
**Level:** Full  
**Permissions:** Read-only

### Function

Investigates complex data lineage and multi-source analytical flows.

### Description

Data Explorer is used when:

- multiple datasets interact;
- several tables or notebooks must be traced;
- source-of-truth is unclear;
- joins must be reconstructed;
- lineage crosses systems;
- Data Explorer Lite escalated.

It identifies what the system actually does before Analyst, SQL, or Data Coder make decisions.

### Why DeepSeek V4 Pro

Complex lineage investigation requires:

- multi-file context;
- code understanding;
- SQL understanding;
- source tracing;
- structured synthesis.

DeepSeek V4 Pro provides strong exploration capability while keeping this work in the Go pool.

---

## `jp-data-analyst`

**Provider:** OpenAI / Codex  
**Model:** `openai/gpt-5.6-sol`  
**Level:** Full specialist  
**Permissions:** Read-only by default

### Function

Defines and evaluates analytical methodology.

### Description

Data Analyst handles:

- KPI design;
- metric definitions;
- population selection;
- denominator selection;
- statistical reasoning;
- hypothesis testing;
- trend interpretation;
- comparative analysis;
- financial reconciliation methodology;
- business interpretation;
- methodological trade-offs.

There is intentionally no Data Analyst Lite.

The Analyst determines what should be calculated and how it should be interpreted.

### Why GPT-5.6 Sol

Methodological errors can invalidate an entire analysis even when the code is technically correct.

Sol is reserved for this role because it is valuable for:

- complex analytical reasoning;
- ambiguous methodology;
- statistical judgment;
- reconciliation logic;
- population design;
- high-impact interpretation.

This is one of the areas where stronger reasoning is worth premium model usage.

---

## `jp-sql-lite`

**Provider:** OpenCode Go  
**Model:** `opencode-go/qwen3.8-flash`  
**Level:** Lite  
**Permissions:** SQL write when requested

### Function

Handles simple SQL when schema and methodology are already established.

### Description

SQL Lite is used for:

- simple SELECT queries;
- filters;
- basic GROUP BY;
- straightforward aggregates;
- small joins with known cardinality;
- localized query fixes.

It must not silently decide:

- analytical population;
- denominator;
- date semantics;
- duplicate strategy.

If those are unclear, it escalates.

### Why Qwen3.8 Flash

SQL Lite needs fast, inexpensive coding capability rather than deep methodological reasoning.

Qwen3.8 Flash is a good match for:

- bounded SQL generation;
- syntax corrections;
- simple aggregation;
- small query modifications.

More difficult SQL goes to the Full SQL agent.

---

## `jp-sql`

**Provider:** OpenCode Go  
**Model:** `opencode-go/deepseek-v4-pro`  
**Level:** Full  
**Permissions:** SQL write when requested

### Function

Handles complex SQL, joins, reconciliation, temporal logic, and query performance.

### Description

SQL Full is used for:

- multiple joins;
- complex CTEs;
- window functions;
- non-trivial temporal logic;
- financial reconciliation;
- query optimization;
- aggregation across multiple levels;
- tasks escalated from SQL Lite.

It preserves methodology defined by Data Analyst.

### Why DeepSeek V4 Pro

Complex SQL requires strong reasoning about:

- join cardinality;
- aggregation;
- query structure;
- data flow;
- performance;
- temporal semantics.

DeepSeek V4 Pro provides sufficient reasoning for these tasks without requiring a premium Codex model.

---

## `jp-data-coder-lite`

**Provider:** OpenCode Go  
**Model:** `opencode-go/qwen3.8-flash`  
**Level:** Lite  
**Permissions:** Write

### Function

Implements small analytical transformations when methodology is already known.

### Description

Data Coder Lite handles:

- simple Pandas transformations;
- loading files;
- formatting;
- derived columns;
- basic charts;
- small cleaning rules;
- simple exports.

It must not invent analytical methodology.

### Why Qwen3.8 Flash

Bounded analytical implementation is similar to Lite software coding.

Qwen3.8 Flash provides:

- good code generation;
- fast response;
- low cost;
- sufficient capability for localized Pandas and Python work.

If the transformation becomes multi-stage or methodologically complex, it escalates.

---

## `jp-data-coder`

**Provider:** OpenCode Go  
**Model:** `opencode-go/kimi-k2.7-code`  
**Level:** Full  
**Permissions:** Write

### Function

Implements non-trivial analytical workflows and data pipelines.

### Description

Data Coder handles:

- multiple interacting transformations;
- several datasets;
- Pandas pipelines;
- SQLAlchemy workflows;
- reusable scripts;
- notebooks;
- ingestion/transformation/export flows;
- tasks escalated by Data Coder Lite.

It implements methodology defined elsewhere.

### Why Kimi K2.7 Code

This role is implementation-heavy.

Kimi K2.7 Code is selected because it is optimized for:

- multi-file coding;
- Python;
- refactoring;
- pipeline implementation;
- modifying existing code.

Using a coding-specialized model here is more cost-effective than assigning Luna or Sol.

---

## `jp-data-reviewer-lite`

**Provider:** OpenCode Zen Free  
**Model:** `opencode/mimo-v2.5-free`  
**Level:** Lite  
**Permissions:** Read-only

### Function

Reviews small analytical changes for obvious correctness issues.

### Description

Data Reviewer Lite checks:

- calculation errors;
- incorrect columns;
- simple filter mistakes;
- obvious join problems;
- accidental row loss;
- duplicate expansion;
- basic date errors;
- simple null-handling problems.

It is not intended for substantial methodology review.

### Why MiMo V2.5 Free

Small reviews benefit from cheap independent scrutiny.

Because the agent is:

- read-only;
- bounded;
- focused on obvious defects;

a free model is sufficient for many cases.

More important analytical review escalates to the Full Data Reviewer.

---

## `jp-data-reviewer`

**Provider:** OpenCode Go  
**Model:** `opencode-go/gpt-5.6-luna`  
**Level:** Full  
**Permissions:** Read-only

### Function

Reviews analytical implementations for both technical and methodological correctness.

### Description

Data Reviewer evaluates:

- population;
- unit of analysis;
- denominator;
- join cardinality;
- filters;
- date fields;
- time windows;
- aggregation;
- duplicates;
- missing data;
- outliers;
- statistical validity;
- interpretation;
- reproducibility.

It provides an independent review after substantial analytical work.

### Why GPT-5.6 Luna

Full analytical review requires broad reasoning across:

- business intent;
- methodology;
- implementation;
- statistics;
- data integrity.

Luna is strong enough to combine these dimensions without spending Sol capacity on every review.

Sol remains reserved for defining or resolving difficult methodology.

---

## `jp-data-documenter-lite`

**Provider:** OpenCode Zen Free  
**Model:** `opencode/mimo-v2.5-free`  
**Level:** Lite  
**Permissions:** Documentation-only write

### Function

Documents small analytical procedures and metric definitions.

### Description

Data Documenter Lite handles:

- one metric;
- one query;
- one notebook section;
- one chart explanation;
- one methodology note;
- localized comments.

It documents verified analytical behavior.

### Why MiMo V2.5 Free

Small analytical documentation is usually well-bounded.

A free model can efficiently convert already-understood behavior into clear documentation.

Broad data-lineage or methodology documentation escalates to the Full Data Documenter.

---

## `jp-data-documenter`

**Provider:** OpenCode Go  
**Model:** `opencode-go/qwen3.7-plus`  
**Level:** Full  
**Permissions:** Documentation-only write

### Function

Documents substantial analyses, methodologies, pipelines, and data lineage.

### Description

Data Documenter handles:

- full methodology;
- complete analyses;
- metric definitions;
- reconciliation procedures;
- data lineage;
- reusable analytical pipelines;
- multi-step notebooks;
- operational data workflows.

It should distinguish:

- source data;
- transformations;
- assumptions;
- methodology;
- results;
- interpretation;
- limitations.

### Why Qwen3.7 Plus

Full analytical documentation requires substantial context synthesis and clear technical writing.

Qwen3.7 Plus provides enough capability for:

- multi-source documentation;
- analytical explanation;
- workflow synthesis;
- structured writing;

without consuming Luna or Codex capacity.

---

## `jp-data-tester`

**Provider:** OpenCode Zen Free  
**Model:** `opencode/muse-spark-1.3-contributor-free`  
**Level:** Verification  
**Permissions:** Execute safe checks, no source writes

### Function

Verifies analytical implementations and data-processing workflows.

### Description

Data Tester runs:

- Python tests;
- notebooks;
- scripts;
- schema checks;
- SQL validation;
- row-count checks;
- shape assertions;
- reproducibility checks;
- pipeline execution;
- linting;
- type checking.

It classifies failures as:

- CODE;
- DATA;
- TEST;
- ENVIRONMENT;
- TOOLING;
- METHODOLOGY;
- UNKNOWN.

It does not silently modify implementation or methodology.

### Why Muse Spark 1.3 Contributor Free

Verification work can generate many repetitive calls.

Most execution and basic validation work does not justify a paid reasoning model.

Muse Spark allows these checks to remain free while escalation handles deeper investigation when necessary.

---

# Model Distribution

Current model usage across JP OpenCode:

| Model | Primary responsibilities |
|---|---|
| `opencode-go/gpt-5.6-luna` | Code orchestration, Data orchestration, Full Code review, Full Data review |
| `opencode/muse-spark-1.3-contributor-free` | Lite exploration and testing |
| `opencode-go/deepseek-v4-pro` | Full Code exploration, Full Data exploration, Full SQL |
| `openai/gpt-5.6-sol` | Architecture and analytical methodology |
| `opencode-go/qwen3.8-flash` | Lite design, Lite coding, Lite SQL, Lite data coding |
| `opencode-go/glm-5.3` | Full UI/UX design |
| `opencode-go/kimi-k2.7-code` | Full Code implementation and Full Data implementation |
| `openai/gpt-5.6-terra-fast` | Heavy Code implementation |
| `opencode/mimo-v2.5-free` | Lite review and Lite documentation |
| `opencode-go/qwen3.7-plus` | Full documentation |

---

# Why Agents Share Models

A model may serve multiple agents when its strengths fit several responsibilities.

For example:

```text
Qwen3.8 Flash
```

is currently used for:

- Code Coder Lite;
- Designer Lite;
- SQL Lite;
- Data Coder Lite.

This does not mean those agents are interchangeable.

Their prompts, permissions, work budgets, and escalation rules remain different.

The model is only the runtime capability assigned to the role.

---

# Why Roles Are More Important Than Models

JP OpenCode treats:

```text
agent responsibility
```

and:

```text
model assignment
```

as separate concepts.

For example:

```text
jp-coder
```

is the Full Code implementation role.

Its current model is:

```text
opencode-go/kimi-k2.7-code
```

If a future model performs better, JP OpenCode can change the assignment without redesigning the Coder role.

The same principle applies to every specialist.

---

# Escalation Philosophy

Lite agents are expected to escalate.

An escalation does not automatically mean the model failed.

It may mean:

- the orchestrator correctly tried the cheaper option first;
- scope grew beyond the original estimate;
- new risk was discovered;
- ambiguity increased;
- methodological impact became significant.

Example:

```text
jp-coder-lite
-> jp-coder
```

or:

```text
jp-data-explorer-lite
-> jp-data-explorer
```

Escalation statistics should therefore be interpreted as routing signals, not simply failure rates.

---

# Future Model Changes

The current assignments are initial working defaults.

They should evolve based on real use.

Useful signals include:

- agent usage;
- model usage;
- escalation rates;
- failed tasks;
- repeated work;
- latency;
- context size;
- token usage;
- cost.

A model should be replaced when evidence shows that another option offers a better balance of:

- capability;
- reliability;
- cost;
- latency;
- available quota.

Agent responsibilities should remain stable even when model assignments change.
