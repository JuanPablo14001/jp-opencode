# JP OpenCode

My personal OpenCode setup for cost-aware software development and data analysis.

JP OpenCode combines:

- OpenCode Zen free models;
- OpenCode Go;
- OpenAI / Codex through ChatGPT Plus/Pro;

using specialized agents coordinated by two primary orchestrators:

- `jp-code-orchestrator`
- `jp-data-orchestrator`

## Goals

JP OpenCode is focused on:

- cost-aware routing;
- specialized sub-agents;
- Direct → Lite → Full → Heavy escalation where applicable;
- keeping expensive model usage focused on high-value work;
- minimal repository intrusion;
- engineering judgment over blind obedience;
- separate orchestration strategies for Code and Data;
- local observability for evaluating routing and model usage.

## How It Works

Users normally interact with one primary orchestrator.

For software development:

```text
jp-code-orchestrator
```

For data analysis:

```text
jp-data-orchestrator
```

The orchestrator evaluates the task and delegates work to specialized agents according to:

- scope;
- risk;
- ambiguity;
- specialization;
- methodological impact for Data work.

The objective is not to use the cheapest model possible.

The objective is to use the cheapest agent capable of completing the task correctly.

## Quick Install

```bash
git clone <repository-url>
cd jp-opencode
chmod +x install.sh
./install.sh
```

Then verify:

```bash
jp-opencode doctor
```

## Main Commands

```bash
jp-opencode install
jp-opencode update
jp-opencode uninstall

jp-opencode doctor
jp-opencode status
jp-opencode agents
jp-opencode models

jp-opencode logs
jp-opencode stats
```

See [`docs/commands.md`](docs/commands.md) for the full CLI reference.

## Documentation

- [`docs/architecture.md`](docs/architecture.md) — system structure and responsibilities
- [`docs/agents.md`](docs/agents.md) — agents, roles, models, and model rationale
- [`docs/models.md`](docs/models.md) — provider and model strategy
- [`docs/routing.md`](docs/routing.md) — Direct, Lite, Full, Heavy, Code, and Data routing
- [`docs/installation.md`](docs/installation.md) — installation and maintenance
- [`docs/commands.md`](docs/commands.md) — CLI reference

## Repository Philosophy

JP OpenCode keeps AI orchestration configuration outside normal application repositories.

Unless explicitly requested, agents should not create:

- project-local `.opencode`;
- `AGENTS.md`;
- AI workflow metadata;
- SDD/OpenSpec artifacts;
- orchestration branches or worktrees.

The goal is to keep application repositories focused on application code.

## Status

Current:

- Code Orchestrator
- Data Orchestrator
- specialized Code agents
- specialized Data agents
- global installer
- CLI
- model routing
- local observability foundation

Planned:

- MCP integrations
- observability refinement
- optional model profiles

## Contributions

This repository is maintained as my personal OpenCode configuration.

Feel free to fork and adapt it for your own workflow.

External pull requests are not currently accepted.

## License

MIT
