#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="${HOME}/.local/state/jp-opencode"
MANIFEST="${STATE_DIR}/install-manifest.txt"

AGENTS_DIR="${HOME}/.config/opencode/agents"
PLUGINS_DIR="${HOME}/.config/opencode/plugins"
CLI_PATH="${HOME}/.local/bin/jp-opencode"

printf 'Uninstalling JP OpenCode...\n\n'

if [[ ! -f "${MANIFEST}" ]]; then
    printf 'No installation manifest found:\n%s\n' "${MANIFEST}"
    printf '\nNothing was removed.\n'
    exit 0
fi

removed_count=0

while IFS= read -r path; do
    [[ -n "${path}" ]] || continue

    case "${path}" in
        "${AGENTS_DIR}/"jp-*.md)
            if [[ -f "${path}" ]]; then
                rm -- "${path}"
                printf 'Removed: %s\n' "${path}"
                removed_count=$((removed_count + 1))
            fi
            ;;

        "${PLUGINS_DIR}/"jp-*.ts)
            if [[ -f "${path}" ]]; then
                rm -- "${path}"
                printf 'Removed: %s\n' "${path}"
                removed_count=$((removed_count + 1))
            fi
            ;;

        "${CLI_PATH}")
            if [[ -L "${path}" || -f "${path}" ]]; then
                rm -- "${path}"
                printf 'Removed: %s\n' "${path}"
                removed_count=$((removed_count + 1))
            fi
            ;;

        *)
            printf 'Skipped unrecognized manifest path: %s\n' "${path}" >&2
            ;;
    esac
done < "${MANIFEST}"

rm -- "${MANIFEST}"

printf '\nRemoved %d installed item(s).\n' "${removed_count}"

printf '\nLocal state was preserved:\n%s\n' "${STATE_DIR}"
printf '%s\n' 'This includes logs and backups.'

printf '\nJP OpenCode uninstalled successfully.\n'