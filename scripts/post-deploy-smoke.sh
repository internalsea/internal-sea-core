#!/usr/bin/env bash
# Post-deploy HTTPS smoke checks for intsea.dev (GitHub Actions after deploy).
# Usage: scripts/post-deploy-smoke.sh

set -euo pipefail

BASE_URL="${SMOKE_BASE_URL:-https://intsea.dev}"
BASE_URL="${BASE_URL%/}"
WWW_URL="${SMOKE_WWW_URL:-https://www.intsea.dev}"
RETRIES="${SMOKE_CHECK_RETRIES:-10}"
RETRY_DELAY="${SMOKE_CHECK_RETRY_DELAY:-15}"

CURL_COMMON=(
  --fail
  --show-error
  --location
  --max-time 30
  -sS
  -o /dev/null
  -w '%{http_code} %{url_effective}\n'
)

log() {
  printf '==> %s\n' "$*"
}

host_from_url() {
  local url="$1"
  printf '%s' "${url#https://}" | cut -d/ -f1
}

has_public_dns() {
  local host="$1"
  if command -v dig >/dev/null 2>&1; then
    dig +short "${host}" A "${host}" AAAA 2>/dev/null | grep -q .
    return
  fi
  getent ahosts "${host}" >/dev/null 2>&1
}

print_tls_debug() {
  local url="$1"
  local host
  host="$(host_from_url "${url}")"
  log "TLS debug for ${host}"
  echo | openssl s_client -connect "${host}:443" -servername "${host}" 2>/dev/null \
    | openssl x509 -noout -issuer -subject -dates 2>/dev/null \
    || log "Could not read certificate for ${host}"
}

check_url() {
  local label="$1" url="$2"
  local attempt=1 code err_file

  err_file="$(mktemp)"
  while [ "${attempt}" -le "${RETRIES}" ]; do
    log "Check ${label}: ${url} (attempt ${attempt}/${RETRIES})"
    if code="$(curl "${CURL_COMMON[@]}" "${url}" 2>"${err_file}")"; then
      log "OK ${label} — HTTP ${code%% *}"
      rm -f "${err_file}"
      return 0
    fi
    if [ -s "${err_file}" ]; then
      log "curl error: $(tr '\n' ' ' < "${err_file}")"
    fi
    if [ "${attempt}" -eq "${RETRIES}" ]; then
      echo "::error::Failed ${label} after ${RETRIES} attempts: ${url}" >&2
      print_tls_debug "${url}"
      rm -f "${err_file}"
      return 1
    fi
    sleep "${RETRY_DELAY}"
    attempt=$((attempt + 1))
  done
  rm -f "${err_file}"
}

check_api_json() {
  local label="$1" url="$2" expected="$3"
  local attempt=1 body content_type err_file

  err_file="$(mktemp)"
  while [ "${attempt}" -le "${RETRIES}" ]; do
    log "Check ${label}: ${url} (attempt ${attempt}/${RETRIES})"
    body="$(mktemp)"
    if content_type="$(curl -fsS --max-time 30 -H 'Accept: application/json' -w '%{content_type}' -o "${body}" "${url}" 2>"${err_file}")"; then
      if [[ "${content_type}" == *application/json* ]] && grep -q "${expected}" "${body}"; then
        log "OK ${label} — JSON (${content_type})"
        rm -f "${body}" "${err_file}"
        return 0
      fi
      log "Expected JSON containing '${expected}', got content-type=${content_type} body=$(head -c 200 "${body}" | tr '\n' ' ')"
    elif [ -s "${err_file}" ]; then
      log "curl error: $(tr '\n' ' ' < "${err_file}")"
    fi
    rm -f "${body}"
    if [ "${attempt}" -eq "${RETRIES}" ]; then
      echo "::error::Failed ${label} — API must return JSON, not HTML (check Traefik routing and intsea-backend health)" >&2
      print_tls_debug "${url}"
      rm -f "${err_file}"
      return 1
    fi
    sleep "${RETRY_DELAY}"
    attempt=$((attempt + 1))
  done
  rm -f "${err_file}"
}

check_demo_login() {
  local label="$1" url="$2" email="$3" password="$4"
  local attempt=1 body status err_file

  err_file="$(mktemp)"
  while [ "${attempt}" -le "${RETRIES}" ]; do
    log "Check ${label}: POST ${url} (attempt ${attempt}/${RETRIES})"
    body="$(mktemp)"
    status="$(curl -sS --max-time 30 \
      -H 'Content-Type: application/json' \
      -H 'Accept: application/json' \
      -o "${body}" \
      -w '%{http_code}' \
      -d "{\"email\":\"${email}\",\"password\":\"${password}\"}" \
      "${url}" 2>"${err_file}")" || status="000"

    if [ "${status}" = "200" ] && grep -q '"access_token"' "${body}"; then
      log "OK ${label} — HTTP 200 with access_token"
      rm -f "${body}" "${err_file}"
      return 0
    fi

    log "Expected HTTP 200 with access_token, got HTTP ${status} body=$(head -c 200 "${body}" | tr '\n' ' ')"
    rm -f "${body}"
    if [ "${attempt}" -eq "${RETRIES}" ]; then
      echo "::error::Failed ${label} — demo login failed (run seed on server or set INTSEA_SEED_ON_DEPLOY=true)" >&2
      rm -f "${err_file}"
      return 1
    fi
    sleep "${RETRY_DELAY}"
    attempt=$((attempt + 1))
  done
  rm -f "${err_file}"
}

check_www_redirect() {
  local label="$1" url="$2" expected_apex="$3"
  local attempt=1 status location apex_host

  apex_host="$(host_from_url "https://${expected_apex}")"
  if ! has_public_dns "$(host_from_url "${url}")"; then
    log "Skip ${label} — no public DNS"
    return 0
  fi

  while [ "${attempt}" -le "${RETRIES}" ]; do
    log "Check ${label} redirect: ${url} → https://${expected_apex}/ (attempt ${attempt}/${RETRIES})"
    status="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 30 "${url}")" || status="000"
    location="$(curl -sSI --max-time 30 "${url}" | tr -d '\r' | awk -F': ' 'tolower($1)=="location"{print $2; exit}')"

    case "${status}" in
      301|302|307|308)
        if [ -n "${location}" ] && [[ "${location}" == https://${expected_apex}* ]] \
          && [[ "${location}" != *:3000* ]]; then
          log "OK ${label} — HTTP ${status} → ${location}"
          return 0
        fi
        log "Unexpected redirect: HTTP ${status} Location: ${location:-<none>}"
        ;;
      200)
        log "OK ${label} — HTTP 200 (served on www)"
        return 0
        ;;
      *)
        log "Unexpected status: HTTP ${status}"
        ;;
    esac

    if [ "${attempt}" -eq "${RETRIES}" ]; then
      echo "::error::Failed ${label} after ${RETRIES} attempts: ${url}" >&2
      return 1
    fi
    sleep "${RETRY_DELAY}"
    attempt=$((attempt + 1))
  done
}

log "Running post-deploy smoke checks against ${BASE_URL}"

check_url "frontend home" "${BASE_URL}/"
check_url "login page" "${BASE_URL}/login"
check_api_json "API live" "${BASE_URL}/api/v1/health/live" '"status":"live"'
check_api_json "API ready" "${BASE_URL}/api/v1/health/ready" '"status"'
check_demo_login "demo admin login" "${BASE_URL}/api/v1/auth/login" \
  "${SMOKE_DEMO_EMAIL:-admin@example.com}" "${SMOKE_DEMO_PASSWORD:-admin12345}"
check_www_redirect "www redirect" "${WWW_URL}/" "$(host_from_url "${BASE_URL}")"

log "All post-deploy smoke checks passed"
