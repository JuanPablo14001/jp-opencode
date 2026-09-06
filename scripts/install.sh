#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd -P)"

SOURCE_AGENTS="${PROJECT_ROOT}/agents"
TARGET_AGENTS="${HOME}/.config/opencode/agents"

SOURCE_PLUGINS="${PROJECT_ROOT}/plugins"
TARGET_PLUGINS="${HOME}/.config/opencode/plugins"

STATE_DIR="${HOME}/.local/state/jp-opencode"
LOG_DIR="${STATE_DIR}/logs"

BACKUP_ROOT="${STATE_DIR}/backups"
MANIFEST="${STATE_DIR}/install-manifest.txt"

BIN_DIR="${HOME}/.local/bin"

CLI_SOURCE="${PROJECT_ROOT}/bin/jp-opencode"
CLI_TARGET="${BIN_DIR}/jp-opencode"

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="${BACKUP_ROOT}/install-${TIMESTAMP}"

if [[ ! -d "${SOURCE_AGENTS}" ]]; then
    printf 'ERROR: agents directory not found: %s\n' \
        "${SOURCE_AGENTS}" >&2
    exit 1
fi

if [[ ! -f "${CLI_SOURCE}" ]]; then
    printf 'ERROR: CLI not found: %s\n' \
        "${CLI_SOURCE}" >&2
    exit 1
fi

mkdir -p \
    "${TARGET_AGENTS}" \
    "${TARGET_PLUGINS}" \
    "${LOG_DIR}" \
    "${BACKUP_ROOT}" \
    "${BIN_DIR}"

printf 'Installing JP OpenCode...\n\n'

backup_created=false
installed_agents=0
installed_plugins=0

TMP_MANIFEST="$(mktemp)"

cleanup() {
    rm -f -- "${TMP_MANIFEST}"
}

trap cleanup EXIT

ensure_backup_dir() {
    if [[ "${backup_created}" == false ]]; then
        mkdir -p "${BACKUP_DIR}"
        backup_created=true
    fi
}

backup_file() {
    local source="$1"
    local backup_name="$2"

    ensure_backup_dir

    cp -a -- \
        "${source}" \
        "${BACKUP_DIR}/${backup_name}"
}

install_file() {
    local source="$1"
    local target="$2"
    local label="$3"
    local backup_name="$4"

    if [[ -f "${target}" ]] && ! cmp -s "${source}" "${target}"; then
        backup_file "${target}" "${backup_name}"
        printf 'Backup:    %s\n' "${label}"
    fi

    cp -- "${source}" "${target}"

    printf 'Installed: %s\n' "${label}"
    printf '%s\n' "${target}" >> "${TMP_MANIFEST}"
}

for source in "${SOURCE_AGENTS}"/jp-*.md; do
    [[ -e "${source}" ]] || continue

    filename="$(basename "${source}")"
    target="${TARGET_AGENTS}/${filename}"

    install_file \
        "${source}" \
        "${target}" \
        "${filename}" \
        "agent-${filename}"

    installed_agents=$((installed_agents + 1))
done

if [[ "${installed_agents}" -eq 0 ]]; then
    printf 'ERROR: no jp-*.md agents found in %s\n' \
        "${SOURCE_AGENTS}" >&2
    exit 1
fi

if [[ -d "${SOURCE_PLUGINS}" ]]; then
    for source in "${SOURCE_PLUGINS}"/jp-*.ts; do
        [[ -e "${source}" ]] || continue

        filename="$(basename "${source}")"
        target="${TARGET_PLUGINS}/${filename}"

        install_file \
            "${source}" \
            "${target}" \
            "${filename}" \
            "plugin-${filename}"

        installed_plugins=$((installed_plugins + 1))
    done
fi

chmod +x "${CLI_SOURCE}"

if [[ -e "${CLI_TARGET}" || -L "${CLI_TARGET}" ]]; then
    if [[ -L "${CLI_TARGET}" ]] &&
       [[ "$(readlink -f "${CLI_TARGET}")" == "$(readlink -f "${CLI_SOURCE}")" ]]; then
        :
    else
        backup_file \
            "${CLI_TARGET}" \
            "jp-opencode-cli"

        printf '%s\n' 'Backup:    existing jp-opencode CLI'
    fi
fi

ln -sfn \
    "${CLI_SOURCE}" \
    "${CLI_TARGET}"

printf '%s\n' "${CLI_TARGET}" >> "${TMP_MANIFEST}"

mv -- \
    "${TMP_MANIFEST}" \
    "${MANIFEST}"

trap - EXIT

printf '\n'
printf 'Installed %d agents.\n' "${installed_agents}"
printf 'Installed %d plugins.\n' "${installed_plugins}"

printf '\n'
printf 'Agents:   %s\n' "${TARGET_AGENTS}"
printf 'Plugins:  %s\n' "${TARGET_PLUGINS}"
printf 'Logs:     %s\n' "${LOG_DIR}"
printf 'CLI:      %s\n' "${CLI_TARGET}"
printf 'Manifest: %s\n' "${MANIFEST}"

if [[ "${backup_created}" == true ]]; then
    printf 'Backups:  %s\n' "${BACKUP_DIR}"
fi

if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
    printf '\n'
    printf 'WARNING: %s is not in PATH.\n' "${BIN_DIR}"

    printf '%s\n' 'Add this to your shell configuration:'
    printf '\n'
    printf '%s\n' '  export PATH="$HOME/.local/bin:$PATH"'
fi

printf '\n'
printf '%s\n' 'JP OpenCode installed successfully.'
printf '%s\n' 'Run: jp-opencode doctor'