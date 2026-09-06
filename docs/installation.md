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

# Update Mechanics

This section explains the internal behavior of `jp-opencode update`.

## Pre-update checks

Before pulling changes, the updater verifies four conditions:

1. **Git availability** — the `git` command must be in PATH;
2. **Repository context** — the JP OpenCode root must be inside a Git work tree;
3. **Clean working tree** — `git status --porcelain` must return empty output;
4. **Active branch** — the repository must be on a named branch, not in detached HEAD state.

Any failure aborts the update with a specific error message and exits.

## Pull strategy

The updater runs:

```bash
git pull --ff-only
```

The `--ff-only` flag means:

- the pull succeeds only if the local branch can be fast-forwarded to the remote;
- if a merge commit would be required, the pull fails and the update aborts.

This ensures the local history stays linear and avoids unexpected merge conflicts during automated reinstallation.

## Reinstallation

After a successful pull, the updater calls `scripts/install.sh`.

This means the same installation logic runs during both first install and update:

- agents are reinstalled from the repository to `~/.config/opencode/agents/`;
- plugins are reinstalled from the repository to `~/.config/opencode/plugins/`;
- the CLI symlink is recreated or validated;
- the installation manifest is rebuilt.

If any file changed between the previous and current versions, the installer creates a backup before overwriting.

---

## Backup behavior

Backups are created during both fresh installation and update.

### When backups are created

A backup is created when:

- a target file already exists **and** its content differs from the source file;
- the CLI target exists as a regular file or a symlink pointing to a different source.

### When backups are skipped

No backup is created when:

- the target file does not exist (fresh install for that file);
- the target file has identical content to the source (verified with `cmp -s`);
- the CLI symlink already points to the current repository source.

### Backup location

All backups are stored under:

```text
~/.local/state/jp-opencode/backups/install-YYYYMMDD-HHMMSS/
```

Each install or update run creates at most one backup directory, named with a timestamp.

### Backup contents

A backup directory may contain any combination of:

- agent files (`agent-<name>.md`);
- plugin files (`plugin-<name>.ts`);
- CLI script entry (`jp-opencode-cli`).

If no files need backup, no directory is created at all.

### Backup lifecycle

Backups are:

- created automatically during install and update;
- never deleted automatically during uninstall;
- never deleted automatically during normal operation;
- preserved intentionally to allow manual recovery if a new version introduces issues.

---

## Installation manifest

The installation manifest records every file managed by JP OpenCode.

### Location

```text
~/.local/state/jp-opencode/install-manifest.txt
```

### Contents

The manifest contains one file path per line, including:

- all installed agent files in `~/.config/opencode/agents/`;
- all installed plugin files in `~/.config/opencode/plugins/`;
- the CLI symlink entry at `~/.local/bin/jp-opencode` (the link target is the repository's `bin/jp-opencode`).

### How it is built

During each install or update run:

1. the installer writes installed paths to a temporary file;
2. on successful completion, the temporary file replaces the previous manifest atomically (via `mv`);
3. if the installer fails mid-run, the previous manifest remains untouched.

This prevents a partial installation from corrupting the manifest used by uninstall.

### How uninstall uses it

The uninstaller reads the manifest line by line and:

- removes agent files matching `~/.config/opencode/agents/jp-*.md`;
- removes plugin files matching `~/.config/opencode/plugins/jp-*.ts`;
- removes the CLI symlink at `~/.local/bin/jp-opencode`;
- skips any path that does not match these patterns.

Unrecognized paths in the manifest are reported to stderr but not removed.

After processing, the manifest file itself is deleted.

---

## CLI symlink

The CLI is available as a symbolic link at:

```text
~/.local/bin/jp-opencode
```

### Symlink creation

During install or update, the installer:

1. runs `chmod +x` on the repository source (`<repo>/bin/jp-opencode`);
2. checks whether the target path already exists;
3. if the existing target is a symlink pointing to the same source, no backup is created;
4. if the existing target is a different symlink or a regular file, it is backed up first;
5. creates the symlink with `ln -sfn`, which:
   - removes the existing file or symlink if present (`-f`);
   - creates a symbolic link (`-s`);
   - does not follow the target when creating (`-n`).

### Link target

The symlink always points to the repository source file:

```text
<repository>/bin/jp-opencode
```

This means:

- development changes to the repository CLI are immediately available;
- no recompilation or separate copy step is needed;
- the installed command always runs the latest version of the CLI script.

### Resolving the repository root

The CLI script resolves its own location by following the symlink chain with `readlink -f`. It then computes the repository root as the parent directory of `bin/`.

This allows the CLI to find agents, plugins, scripts, and other repository resources regardless of where the symlink is located.

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
