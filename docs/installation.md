# Installation

JP OpenCode installs a global OpenCode configuration for software development and data analysis.

The installation includes:

- Code agents;
- Data agents;
- primary orchestrators;
- JP plugins;
- the `jp-opencode` CLI;
- local state and observability directories.

JP OpenCode is intentionally installed globally.

It does not require AI configuration files inside every project repository.

---

# Requirements

The current installation targets Linux and WSL environments.

Required:

- Bash;
- Git;
- OpenCode.

Recommended:

- Python 3.

Python is currently used by local statistics functionality.

The configured agents use models from:

- OpenCode Zen Free;
- OpenCode Go;
- OpenAI / Codex.

Provider authentication must already be configured in OpenCode.

JP OpenCode does not install, store, or distribute provider credentials.

---

# Quick Installation

Clone the repository:

```bash
git clone <repository-url>
cd jp-opencode
```

Make the installer executable if necessary:

```bash
chmod +x install.sh
```

Run:

```bash
./install.sh
```

The root installer will:

1. verify required commands;
2. inspect the environment;
3. execute the internal JP installer;
4. install agents;
5. install plugins;
6. install the CLI;
7. prepare local state;
8. run `jp-opencode doctor`.

---

# What Gets Installed

## Agents

Source:

```text
agents/
```

Destination:

```text
~/.config/opencode/agents/
```

Examples:

```text
jp-code-orchestrator.md
jp-data-orchestrator.md

jp-coder.md
jp-architect.md

jp-data-analyst.md
jp-data-coder.md
jp-sql.md
```

All JP agents use the `jp-` prefix.

---

# Primary Orchestrators

JP OpenCode currently provides two primary orchestrators.

## Code

```text
jp-code-orchestrator
```

Use for:

- software development;
- debugging;
- architecture;
- frontend/UI;
- implementation;
- testing;
- review;
- technical documentation.

## Data

```text
jp-data-orchestrator
```

Use for:

- data analysis;
- SQL;
- Pandas;
- analytical methodology;
- reconciliation;
- statistical reasoning;
- analytical pipelines;
- data verification;
- analytical documentation.

Users normally interact with an orchestrator rather than selecting individual subagents manually.

---

# Plugins

JP plugins are installed from:

```text
plugins/
```

to:

```text
~/.config/opencode/plugins/
```

Current plugins may include:

```text
jp-observability.ts
```

Restart OpenCode after changing or installing plugins.

---

# CLI

The CLI is available as:

```text
~/.local/bin/jp-opencode
```

The installer creates a symbolic link to:

```text
<repository>/bin/jp-opencode
```

This means development changes to the repository CLI are immediately reflected in the installed command.

Verify the link with:

```bash
readlink -f "$(which jp-opencode)"
```

It should resolve to:

```text
<repository>/bin/jp-opencode
```

---

# PATH

Your shell should include:

```text
~/.local/bin
```

Check:

```bash
echo "$PATH"
```

If necessary:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

For Zsh:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

For Bash:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Verify:

```bash
which jp-opencode
```

Expected:

```text
/home/<user>/.local/bin/jp-opencode
```

---

# Local State

JP OpenCode stores local runtime state under:

```text
~/.local/state/jp-opencode/
```

Current structure may include:

```text
~/.local/state/jp-opencode/
├── backups/
├── logs/
└── install-manifest.txt
```

These files do not belong to application repositories.

---

# Installation Manifest

JP OpenCode records installed managed files in:

```text
~/.local/state/jp-opencode/install-manifest.txt
```

The manifest allows uninstall to remove only files that belong to JP OpenCode.

It also prevents the uninstall command from deleting unrelated OpenCode configuration.

---

# Backups

When the installer replaces an existing managed file with different content, the previous version is preserved under:

```text
~/.local/state/jp-opencode/backups/
```

Example:

```text
install-20260906-143500/
```

Backups may contain previous:

- agent definitions;
- plugins;
- CLI entries.

Backups are not automatically deleted during normal uninstall.

---

# Verify Installation

Run:

```bash
jp-opencode doctor
```

The doctor command validates the JP OpenCode environment.

Depending on the current version, it checks:

- OpenCode;
- agents directory;
- plugins directory;
- installation manifest;
- CLI;
- primary orchestrators;
- Code agents;
- Data agents;
- required models;
- Python;
- observability components.

A healthy installation should end with:

```text
✓ Ready.
```

---

# Inspect Agents

Run:

```bash
jp-opencode agents
```

This displays installed agents grouped by family:

```text
Orchestrators
Code agents
Data agents
```

---

# Inspect Model Assignments

Run:

```bash
jp-opencode models
```

For more explanation about why each model is assigned to each role, see:

```text
docs/models.md
docs/agents.md
```

---

# Start OpenCode

Run:

```bash
opencode
```

Then use:

```text
jp-code-orchestrator
```

for software work.

Or:

```text
jp-data-orchestrator
```

for analytical work.

---

# Refresh Local Configuration

After editing agents or plugins in your local JP OpenCode repository:

```bash
jp-opencode install
```

Then:

```bash
jp-opencode doctor
```

You do not need to clone or reinstall the repository.

---

# Update

To retrieve repository updates:

```bash
jp-opencode update
```

The updater intentionally requires a clean Git working tree.

This protects local development work.

The normal update flow is:

```text
verify repository
-> verify clean working tree
-> git pull --ff-only
-> reinstall JP OpenCode
```

If you have uncommitted changes, commit, stash, or discard them before updating.

---

# Uninstall

Run:

```bash
jp-opencode uninstall
```

The uninstaller uses the installation manifest to remove managed JP files.

It should remove:

- installed JP agents;
- installed JP plugins;
- the JP CLI entry.

Local state is intentionally preserved.

That includes:

```text
logs/
backups/
```

This prevents uninstall from destroying historical information unexpectedly.

---

# Repository Safety

JP OpenCode is designed to avoid polluting user repositories.

Unless explicitly requested, JP agents must not create:

- `.opencode/`;
- `AGENTS.md`;
- SDD artifacts;
- OpenSpec artifacts;
- AI knowledge bases;
- AI workflow metadata;
- Git hooks;
- orchestration branches;
- orchestration worktrees.

Global configuration is preferred.

---

# Troubleshooting

## `jp-opencode: command not found`

Check:

```bash
ls -la ~/.local/bin/jp-opencode
```

Then:

```bash
echo "$PATH"
```

If necessary:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Reload the shell.

---

## Wrong JP repository detected

Check:

```bash
readlink -f "$(which jp-opencode)"
```

The result should point to the repository containing:

```text
bin/jp-opencode
```

The CLI resolves its symbolic link before calculating the JP repository root.

---

## Agent missing

Run:

```bash
jp-opencode install
jp-opencode doctor
```

---

## Required model missing

Inspect OpenCode:

```bash
opencode models
```

Then:

```bash
jp-opencode models
```

JP OpenCode does not configure provider credentials automatically.

---

## Plugin not loading

Restart OpenCode.

Then run:

```bash
jp-opencode doctor
```

---

# Security

Never commit:

- API keys;
- access tokens;
- passwords;
- provider credentials;
- private environment files.

Authentication belongs to the user's local OpenCode environment.