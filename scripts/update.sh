#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd -P)"

if ! command -v git >/dev/null 2>&1; then
    printf 'ERROR: git is not installed or not available in PATH.\n' >&2
    exit 1
fi

if ! git -C "${PROJECT_ROOT}" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    printf 'ERROR: JP OpenCode is not inside a Git repository.\n' >&2
    exit 1
fi

if [[ -n "$(git -C "${PROJECT_ROOT}" status --porcelain)" ]]; then
    printf 'ERROR: JP OpenCode has local changes.\n' >&2
    printf 'Commit, stash, or discard them before updating.\n'
    exit 1
fi

printf 'Updating JP OpenCode...\n\n'

CURRENT_BRANCH="$(git -C "${PROJECT_ROOT}" branch --show-current)"

if [[ -z "${CURRENT_BRANCH}" ]]; then
    printf 'ERROR: repository is in detached HEAD state.\n' >&2
    exit 1
fi

git -C "${PROJECT_ROOT}" pull --ff-only

printf '\nReinstalling configuration...\n\n'

"${SCRIPT_DIR}/install.sh"

printf '\nJP OpenCode updated successfully.\n'