# JP OpenCode Architecture

JP OpenCode is a global OpenCode configuration designed around specialized agents, cost-aware routing, and minimal repository intrusion.

The system separates orchestration into two primary domains:

- Code
- Data

Each domain has its own orchestrator and specialist agents.

The architecture is designed so model assignments can change without changing agent responsibilities.

---

# High-Level Architecture

```text
User
│
├── jp-code-orchestrator
│   │
│   ├── exploration
│   ├── architecture
│   ├── design
│   ├── implementation
│   ├── review
│   ├── documentation
│   └── testing
│
└── jp-data-orchestrator
    │
    ├── data exploration
    ├── methodology / analysis
    ├── SQL
    ├── data implementation
    ├── review
    ├── documentation
    └── verification
```

Users normally interact with the orchestrators.

Specialist agents are primarily implementation details of the orchestration system.

---

# Core Design Principles

## Cost-Aware Routing

JP OpenCode does not assign the strongest model to every task.

Routing considers:

- capability;
- scope;
- risk;
- ambiguity;
- specialization;
- methodological impact for Data work;
- model cost;
- available quota.

The central rule is:

> Use the cheapest agent capable of completing the task correctly.

Correctness has priority over cost.

---

# Primary Orchestrators

## Code Orchestrator

```text
jp-code-orchestrator
```

Responsible for software-development coordination.

It evaluates:

- scope;
- risk;
- ambiguity;
- specialization.

It routes work to:

```text
Explorer
Architect
Designer
Coder
Reviewer
Documenter
Tester
```

The Code Orchestrator may perform very small Direct work, but it should not become the default implementation agent.

---

## Data Orchestrator

```text
jp-data-orchestrator
```

Responsible for analytical and data-processing coordination.

It evaluates:

- scope;
- risk;
- ambiguity;
- specialization;
- methodological impact.

The additional methodological dimension is important because a small amount of SQL or Python can materially change the meaning of an analysis.

It routes work to:

```text
Data Explorer
Data Analyst
SQL
Data Coder
Data Reviewer
Data Documenter
Data Tester
```

---

# Code Agent Architecture

```text
jp-code-orchestrator

├── Exploration
│   ├── jp-explorer-lite
│   └── jp-explorer
│
├── Architecture
│   └── jp-architect
│
├── Design
│   ├── jp-designer-lite
│   └── jp-designer
│
├── Coding
│   ├── jp-coder-lite
│   ├── jp-coder
│   └── jp-coder-heavy
│
├── Review
│   ├── jp-reviewer-lite
│   └── jp-reviewer
│
├── Documentation
│   ├── jp-documenter-lite
│   └── jp-documenter
│
└── Verification
    └── jp-tester
```

---

# Data Agent Architecture

```text
jp-data-orchestrator

├── Exploration
│   ├── jp-data-explorer-lite
│   └── jp-data-explorer
│
├── Methodology
│   └── jp-data-analyst
│
├── SQL
│   ├── jp-sql-lite
│   └── jp-sql
│
├── Implementation
│   ├── jp-data-coder-lite
│   └── jp-data-coder
│
├── Review
│   ├── jp-data-reviewer-lite
│   └── jp-data-reviewer
│
├── Documentation
│   ├── jp-data-documenter-lite
│   └── jp-data-documenter
│
└── Verification
    └── jp-data-tester
```

---

# Routing Levels

JP OpenCode uses:

```text
DIRECT
LITE
FULL
HEAVY
```

Not every domain uses every level.

Not every task passes through every level.

---

## Direct

The orchestrator handles very small work itself.

Use when:

- scope is tiny;
- risk is low;
- ambiguity is low;
- no specialist reasoning is required;
- delegation overhead exceeds the work.

Direct exists to avoid unnecessary agent creation.

---

## Lite

Lite agents are bounded, low-cost specialists.

They are intended for:

- small investigations;
- localized implementation;
- simple SQL;
- lightweight review;
- lightweight documentation;
- bounded design work.

Lite agents operate under strict budgets.

When the task exceeds their budget, they return:

```text
STATUS: ESCALATE
```

Escalation is expected behavior.

---

## Full

Full agents handle meaningful complexity.

They are used when:

- several files or datasets interact;
- reasoning is non-trivial;
- risk is meaningful;
- ambiguity exists;
- specialist judgment is required;
- a Lite agent escalated.

A task may route directly to Full.

---

## Heavy

Heavy is currently primarily used for difficult Code implementation.

```text
jp-coder-heavy
```

Heavy should be exceptional.

It is not simply a larger Full task.

It is used when stronger coding capability materially improves correctness.

---

# Specialist Responsibility Boundaries

JP OpenCode intentionally separates responsibilities.

For Code:

```text
Explorer
→ discovers

Architect
→ designs system structure

Designer
→ defines UI/UX

Coder
→ implements

Reviewer
→ evaluates

Tester
→ verifies

Documenter
→ communicates verified behavior
```

For Data:

```text
Data Explorer
→ discovers data structure and lineage

Data Analyst
→ defines or evaluates methodology

SQL
→ implements SQL

Data Coder
→ implements analytical processing

Data Reviewer
→ evaluates correctness and methodology

Data Tester
→ verifies execution and outputs

Data Documenter
→ communicates verified methodology and behavior
```

This separation helps prevent one agent from silently assuming responsibilities that belong to another specialist.

---

# Data Methodology Boundary

Data has an important architectural rule:

```text
Analyst defines methodology.
SQL/Data Coder implement methodology.
Reviewer evaluates methodology.
Tester verifies execution.
```

Implementation agents should not silently decide:

- population;
- denominator;
- date semantics;
- deduplication strategy;
- outlier rules;
- statistical interpretation.

If methodology is unresolved, control returns to the orchestrator and can be routed to:

```text
jp-data-analyst
```

---

# Model Architecture

Agent responsibility and model assignment are separate concerns.

For example:

```text
jp-coder
```

is a role.

Its current model is:

```text
opencode-go/kimi-k2.7-code
```

The role should remain stable if the model changes later.

Conceptually:

```text
Agent responsibility
        ↓
Model assignment
        ↓
Provider runtime
```

This allows JP OpenCode to adapt to new models without redesigning its agent architecture.

---

# Provider Architecture

JP OpenCode currently uses three independent model pools.

```text
OpenCode Zen Free
OpenCode Go
OpenAI / Codex
```

General intended use:

```text
Zen Free
→ bounded, high-volume, low-risk work

OpenCode Go
→ normal daily specialist work

OpenAI / Codex
→ high-value architecture, methodology, and difficult implementation
```

This is a capability strategy, not a mandatory escalation chain.

A task may route directly to a premium model when its responsibility requires it.

---

# Context Architecture

The orchestrator is responsible for protecting parent-session context.

Subagents should return conclusions rather than large evidence dumps.

Preferred flow:

```text
Parent context
     ↓
small specialist handoff
     ↓
specialist work
     ↓
concise result
     ↓
parent retains conclusions
```

Avoid transferring:

- complete source files;
- entire notebooks;
- large query outputs;
- raw datasets;
- unnecessary conversation history.

The parent should retain:

- conclusions;
- relevant paths;
- important constraints;
- methodology;
- risks;
- decisions.

---

# Write Ownership

Avoid overlapping writers.

For a bounded implementation task, prefer one implementation owner.

Example:

```text
jp-coder
```

or:

```text
jp-data-coder
```

Reviewers and explorers remain read-only.

Designers are read-only by default.

Documenters may only modify documentation-related content.

Testers execute verification but do not silently fix implementation.

---

# Repository Isolation

JP OpenCode configuration is installed globally.

Agents:

```text
~/.config/opencode/agents/
```

Plugins:

```text
~/.config/opencode/plugins/
```

CLI:

```text
~/.local/bin/jp-opencode
```

Runtime state:

```text
~/.local/state/jp-opencode/
```

This architecture intentionally avoids requiring AI workflow files in normal application repositories.

---

# Repository Safety

Unless explicitly requested, JP OpenCode should not create:

- project-local `.opencode`;
- `AGENTS.md`;
- SDD artifacts;
- OpenSpec artifacts;
- AI knowledge bases;
- AI workflow metadata;
- Git hooks;
- orchestration branches;
- orchestration worktrees.

Read-only Git inspection is allowed.

Application repositories should remain focused on application code.

---

# Installation Architecture

The public entry point is:

```bash
./install.sh
```

The root installer performs:

```text
environment validation
        ↓
scripts/install.sh
        ↓
global agent/plugin installation
        ↓
CLI installation
        ↓
manifest / backups / local state
        ↓
jp-opencode doctor
```

The internal installer remains responsible for actual file installation.

This separates installation UX from installation mechanics.

---

# CLI Architecture

The CLI is:

```text
bin/jp-opencode
```

and is exposed globally as:

```text
~/.local/bin/jp-opencode
```

through a symbolic link.

Main responsibilities include:

- install;
- update;
- uninstall;
- validation;
- status inspection;
- agent inspection;
- model inspection;
- observability inspection.

The CLI resolves its symbolic link before determining the repository root.

---

# Installation Manifest

Installed managed files are recorded in:

```text
~/.local/state/jp-opencode/install-manifest.txt
```

Uninstall uses this manifest to remove only JP-managed files.

This reduces the risk of deleting unrelated OpenCode configuration.

---

# Backups

Changed managed files are backed up before replacement.

Backups are stored under:

```text
~/.local/state/jp-opencode/backups/
```

Backups are preserved during normal uninstall.

---

# Observability Architecture

JP OpenCode includes a local observability foundation.

Runtime data is stored under:

```text
~/.local/state/jp-opencode/logs/
```

The long-term goal is to evaluate real usage such as:

- model frequency;
- agent frequency;
- escalation rates;
- provider distribution;
- failures;
- latency;
- tokens;
- cost where available.

Observability should not store unnecessary sensitive content.

Raw prompts, source files, and secrets should not be persisted merely for analytics.

Observability refinement remains independent from the core orchestration architecture.

---

# Current Architecture Boundaries

Currently implemented:

```text
Code orchestration
Data orchestration
specialized agents
cost-aware routing
provider distribution
global installation
CLI
local observability foundation
```

Currently deferred:

```text
MCP integrations
model profiles
specialized ML family
specialized visualization family
advanced observability
```

Deferred features should not complicate the core architecture until real usage justifies them.

---

# Architectural Principle

JP OpenCode should remain understandable.

A new agent, model layer, integration, or abstraction should only be introduced when it solves a recurring responsibility that does not fit cleanly into the existing architecture.

The goal is not to maximize the number of agents.

The goal is to maintain clear ownership, efficient routing, and reliable results.