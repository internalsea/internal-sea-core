#!/usr/bin/env bash
# Build intsea-backend on the deploy host after update-repo internal-sea-core.
# compose-up runs migrate/seed in a one-off container before deploy_intsea_services()
# rebuilds the API; this ensures that one-off uses current source from /opt/internal-sea-core.

set -euo pipefail

SSH_HOST="${SSH_HOST:?SSH_HOST is required}"
SSH_USER="${SSH_USER:?SSH_USER is required}"
SSH_KEY="${SSH_KEY:?SSH_KEY is required}"
SSH_PORT="${SSH_PORT:-22}"
BASE_DIR="${DEPLOY_BASE_DIR:-/opt}"

mkdir -p ~/.ssh
chmod 700 ~/.ssh
umask 077
printf '%s\n' "${SSH_KEY}" > ~/.ssh/deploy_key
chmod 600 ~/.ssh/deploy_key

if ! ssh-keyscan -p "${SSH_PORT}" -H "${SSH_HOST}" >> ~/.ssh/known_hosts 2>/dev/null; then
  echo "::error::ssh-keyscan failed (check DEPLOY_HOST and DEPLOY_PORT)"
  exit 1
fi
chmod 644 ~/.ssh/known_hosts

COMPOSE_SCRIPT="${BASE_DIR}/shared-landing/scripts/compose.sh"
if ! ssh -i ~/.ssh/deploy_key -p "${SSH_PORT}" \
  -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -o BatchMode=yes \
  "${SSH_USER}@${SSH_HOST}" "test -f $(printf '%q' "${COMPOSE_SCRIPT}")"; then
  echo "::error::Missing ${COMPOSE_SCRIPT} — run update-repo shared-landing first" >&2
  exit 1
fi

echo "==> Building intsea-backend on deploy host (pre-migrate/seed)"
ssh -i ~/.ssh/deploy_key -p "${SSH_PORT}" \
  -o StrictHostKeyChecking=yes -o IdentitiesOnly=yes -o BatchMode=yes \
  "${SSH_USER}@${SSH_HOST}" \
  "bash $(printf '%q' "${COMPOSE_SCRIPT}") build intsea-backend"

rm -f ~/.ssh/deploy_key
