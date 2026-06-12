/**
 * Frontend configuration (Vite build-time variables).
 * Set VITE_API_BASE_URL in apps/web/.env or root .env for non-default API hosts.
 */
export const APP_NAME = import.meta.env.VITE_APP_NAME ?? 'Internal Sea'

const configuredApiBaseUrl = import.meta.env.VITE_API_BASE_URL as string | undefined

export const API_BASE_URL =
  configuredApiBaseUrl && configuredApiBaseUrl.trim().length > 0
    ? configuredApiBaseUrl
    : 'http://localhost:8000/api/v1'

if (import.meta.env.PROD && !configuredApiBaseUrl) {
  console.warn(
    '[config] VITE_API_BASE_URL is not set — falling back to localhost. Configure before production build.',
  )
}
