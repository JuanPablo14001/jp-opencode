# JP OpenCode CLI

JP OpenCode includes the `jp-opencode` command for installation, validation, inspection, updates, and local observability.

General usage:

```bash
jp-opencode <command>
```

---

# `jp-opencode install`

Install or refresh the JP OpenCode global configuration.

```bash
jp-opencode install
```

Use this after changing:

- agents;
- orchestrators;
- plugins;
- CLI code.

The command installs managed configuration from the current JP OpenCode repository.

Changed existing managed files are backed up.

---

# `jp-opencode update`

Update the JP OpenCode repository and reinstall.

```bash
jp-opencode update
```

The updater normally:

1. verifies Git;
2. verifies the repository;
3. requires a clean working tree;
4. rejects detached HEAD;
5. executes `git pull --ff-only`;
6. reinstalls JP OpenCode.

This behavior protects local repository changes.

---

# `jp-opencode uninstall`

Remove managed JP OpenCode files.

```bash
jp-opencode uninstall
```

The command uses:

```text
~/.local/state/jp-opencode/install-manifest.txt
```

to determine which files are owned by JP OpenCode.

Local state such as logs and backups is preserved by default.

---

# `jp-opencode doctor`

Validate the JP OpenCode installation.

```bash
jp-opencode doctor
```

Depending on the installed version, Doctor checks:

- OpenCode;
- CLI;
- installation manifest;
- agent directory;
- plugin directory;
- Code Orchestrator;
- Data Orchestrator;
- Code subagents;
- Data subagents;
- required models;
- Python;
- observability support.

Typical healthy result:

```text
✓ Ready.
```

Run Doctor after:

- installation;
- updates;
- adding agents;
- changing model assignments;
- provider changes;
- plugin changes.

---

# `jp-opencode status`

Display a quick installation overview.

```bash
jp-opencode status
```

Useful for checking:

- OpenCode version;
- JP configuration state;
- CLI path;
- orchestrator availability;
- observability status.

---

# `jp-opencode version`

Display the current JP OpenCode version and, when available, the installed
OpenCode version.

```bash
jp-opencode version
```

The JP OpenCode version is read from the `VERSION` file in the repository
root.

---

# `jp-opencode agents`

List installed JP agents.

```bash
jp-opencode agents
```

Agents are grouped into:

```text
Orchestrators
Code agents
Data agents
```

The primary orchestrators are:

```text
jp-code-orchestrator
jp-data-orchestrator
```

---

# `jp-opencode models`

Display current agent-to-model assignments.

```bash
jp-opencode models
```

This gives a quick operational view.

For the reasoning behind those assignments, see:

```text
docs/models.md
docs/agents.md
```

---

# `jp-opencode logs`

Display recent local observability events.

```bash
jp-opencode logs
```

Observability data is stored locally under:

```text
~/.local/state/jp-opencode/logs/
```

Depending on the active plugin version, logs may contain metadata about:

- sessions;
- tools;
- routing;
- agents;
- models.

Raw prompts, source code, credentials, and unnecessary sensitive data should not be stored.

---

# `jp-opencode stats`

Display the general observability summary.

```bash
jp-opencode stats
```

Potential metrics include:

- agent executions;
- model executions;
- provider usage;
- escalation rate;
- errors;
- tokens;
- duration;
- cost when exposed by the provider/runtime.

---

# `jp-opencode stats models`

Display statistics grouped by model.

```bash
jp-opencode stats models
```

This is useful for evaluating questions such as:

- Which model receives the most work?
- Is GPT-5.6 Luna being overused?
- Are Zen Free agents absorbing enough work?
- Is Codex usage unusually high?
- Which models frequently escalate?

---

# `jp-opencode stats agents`

Display usage grouped by agent.

```bash
jp-opencode stats agents
```

Useful metrics may include:

- runs;
- successful completions;
- escalations;
- escalation rate;
- errors;
- average duration;
- token usage.

This helps evaluate whether an agent's model or routing threshold should change.

---

# `jp-opencode stats providers`

Display usage grouped by provider.

```bash
jp-opencode stats providers
```

Current pools include:

```text
OpenCode Zen Free
OpenCode Go
OpenAI / Codex
```

This helps determine whether work is being distributed according to the project's cost strategy.

---

# `jp-opencode stats escalations`

Display Lite escalation behavior.

```bash
jp-opencode stats escalations
```

Examples of escalation routes:

```text
jp-explorer-lite
-> jp-explorer
```

```text
jp-coder-lite
-> jp-coder
```

```text
jp-data-explorer-lite
-> jp-data-explorer
```

```text
jp-sql-lite
-> jp-sql
```

A high escalation rate does not automatically indicate a bad model.

Possible causes include:

- Lite routing is too aggressive;
- Lite budget is too restrictive;
- tasks are naturally more complex;
- the model is insufficient for the role.

The metric should be interpreted together with task quality.

---

# `jp-opencode help`

Display CLI help.

```bash
jp-opencode help
```

Also:

```bash
jp-opencode -h
```

or:

```bash
jp-opencode --help
```

---

# Recommended First Run

After cloning JP OpenCode:

```bash
./install.sh
```

Then:

```bash
jp-opencode doctor
```

Inspect agents:

```bash
jp-opencode agents
```

Inspect models:

```bash
jp-opencode models
```

Then start:

```bash
opencode
```

Use:

```text
jp-code-orchestrator
```

for software-development work.

Use:

```text
jp-data-orchestrator
```

for data-analysis work.

---

# Development Workflow

When developing JP OpenCode itself:

```bash
jp-opencode install
jp-opencode doctor
```

Because the CLI is symlinked to the repository, CLI-only modifications normally become available immediately.

Agent and plugin modifications must be reinstalled into the global OpenCode configuration.

---

# Command Summary

| Command | Purpose |
|---|---|
| `jp-opencode install` | Install or refresh JP OpenCode |
| `jp-opencode update` | Pull updates and reinstall |
| `jp-opencode uninstall` | Remove managed JP files |
| `jp-opencode doctor` | Validate the installation |
| `jp-opencode status` | Show installation status |
| `jp-opencode version` | Show JP OpenCode and OpenCode versions |
| `jp-opencode agents` | List installed agents |
| `jp-opencode models` | Show model assignments |
| `jp-opencode logs` | Show recent observability events |
| `jp-opencode stats` | Show usage summary |
| `jp-opencode stats models` | Show model usage |
| `jp-opencode stats agents` | Show agent usage |
| `jp-opencode stats providers` | Show provider usage |
| `jp-opencode stats escalations` | Show escalation statistics |
| `jp-opencode help` | Show command help |
