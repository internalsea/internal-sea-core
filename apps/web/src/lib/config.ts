/**
 * Frontend configuration (Vite build-time variables).
 * Set VITE_API_BASE_URL in apps/web/.env or root .env for non-default API hosts.
 */
export const APP_NAME = import.meta.env.VITE_APP_NAME ?? 'Internal Sea'

const configuredApiBaseUrl = import.meta.env.VITE_API_BASE_URL as string | undefined

/** Same-origin API path when built for production behind Traefik (/api → backend). */
const PRODUCTION_DEFAULT_API_BASE_URL = '/api/v1'
const DEVELOPMENT_DEFAULT_API_BASE_URL = 'http://localhost:8000/api/v1'

export const API_BASE_URL =
  configuredApiBaseUrl && configuredApiBaseUrl.trim().length > 0
    ? configuredApiBaseUrl.trim()
    : import.meta.env.PROD
      ? PRODUCTION_DEFAULT_API_BASE_URL
      : DEVELOPMENT_DEFAULT_API_BASE_URL

if (import.meta.env.PROD && API_BASE_URL.includes('localhost')) {
  console.error(
    '[config] Production build must not use localhost for VITE_API_BASE_URL. Use /api/v1 (same-origin) or your public API URL.',
  )
}
