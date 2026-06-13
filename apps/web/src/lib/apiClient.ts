import { getStoredToken } from '@/features/auth/utils'
import { getStoredCompanyId, getStoredWorkspaceId } from '@/features/tenancy/utils'
import { API_BASE_URL } from '@/lib/config'
import type { ApiErrorBody } from '@/types/common'

export class ApiError extends Error {
  status: number
  body?: ApiErrorBody
  requestId?: string | null

  constructor(
    status: number,
    message: string,
    body?: ApiErrorBody,
    requestId?: string | null,
  ) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.body = body
    this.requestId = requestId
  }
}

let unauthorizedHandler: (() => void) | null = null
let handlingUnauthorized = false

export function setUnauthorizedHandler(handler: (() => void) | null): void {
  unauthorizedHandler = handler
}

function buildUrl(path: string, params?: Record<string, string | number | boolean | undefined>): string {
  const base = API_BASE_URL.replace(/\/$/, '')
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  const combinedPath = `${base.startsWith('/') || /^https?:\/\//i.test(base) ? base : `/${base}`}${normalizedPath}`

  // Relative bases like /api/v1 need an origin; single-arg URL() rejects path-only strings.
  const url = /^https?:\/\//i.test(base)
    ? new URL(combinedPath)
    : new URL(combinedPath, window.location.origin)

  if (params) {
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined && value !== '') {
        url.searchParams.set(key, String(value))
      }
    }
  }

  return url.toString()
}

const TENANT_HEADER_SKIP_PATHS = [
  '/auth/login',
  '/auth/register',
  '/tenancy/onboarding/first-user',
  '/health',
]

function shouldSkipTenantHeaders(path: string): boolean {
  return TENANT_HEADER_SKIP_PATHS.some((skipPath) => path.includes(skipPath))
}

function buildHeaders(path: string, includeJson = false): HeadersInit {
  const headers: Record<string, string> = {
    Accept: 'application/json',
  }
  if (includeJson) {
    headers['Content-Type'] = 'application/json'
  }
  const token = getStoredToken()
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }
  if (!shouldSkipTenantHeaders(path)) {
    const companyId = getStoredCompanyId()
    const workspaceId = getStoredWorkspaceId()
    if (companyId) {
      headers['X-Company-ID'] = companyId
    }
    if (workspaceId) {
      headers['X-Workspace-ID'] = workspaceId
    }
  }
  return headers
}

function extractErrorMessage(body: ApiErrorBody | undefined, fallback: string): string {
  if (!body) return fallback
  if (typeof body.message === 'string' && body.message) return body.message
  if (typeof body.detail === 'string' && body.detail) return body.detail
  if (Array.isArray(body.detail)) {
    return body.detail.map((item) => item.msg).join('; ') || fallback
  }
  if (Array.isArray(body.details)) {
    return body.details
      .map((item) => (typeof item === 'object' && item && 'msg' in item ? String(item.msg) : String(item)))
      .join('; ') || fallback
  }
  return fallback
}

async function parseResponse<T>(response: Response): Promise<T> {
  const requestId = response.headers.get('X-Request-ID')
  const contentType = response.headers.get('content-type')
  const isJson = contentType?.includes('application/json')
  let body: ApiErrorBody | undefined

  if (isJson) {
    try {
      body = (await response.json()) as ApiErrorBody
    } catch {
      body = undefined
    }
  }

  if (!response.ok) {
    if (response.status === 401 && unauthorizedHandler && !handlingUnauthorized) {
      handlingUnauthorized = true
      try {
        unauthorizedHandler()
      } finally {
        handlingUnauthorized = false
      }
    }
    const message = extractErrorMessage(body, response.statusText || 'Request failed')
    throw new ApiError(
      response.status,
      message,
      body,
      body?.request_id ?? requestId,
    )
  }

  if (response.status === 204) {
    return undefined as T
  }

  if (!isJson) {
    throw new ApiError(response.status, 'Expected JSON response', body, requestId)
  }

  return body as T
}

async function request<T>(
  path: string,
  init: RequestInit,
  params?: Record<string, string | number | boolean | undefined>,
): Promise<T> {
  try {
    const response = await fetch(buildUrl(path, params), init)
    return await parseResponse<T>(response)
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }
    if (error instanceof TypeError) {
      throw new ApiError(0, 'Network error — check API connectivity and CORS settings')
    }
    throw error
  }
}

export async function apiGet<T>(
  path: string,
  params?: Record<string, string | number | boolean | undefined>,
): Promise<T> {
  return request<T>(path, { headers: buildHeaders(path) }, params)
}

export async function apiPost<T>(path: string, body: unknown = {}): Promise<T> {
  return request<T>(path, {
    method: 'POST',
    headers: buildHeaders(path, true),
    body: JSON.stringify(body),
  })
}

export async function apiPatch<T>(path: string, body: unknown): Promise<T> {
  return request<T>(path, {
    method: 'PATCH',
    headers: buildHeaders(path, true),
    body: JSON.stringify(body),
  })
}

export async function apiDelete(path: string): Promise<void> {
  await request<void>(path, { method: 'DELETE', headers: buildHeaders(path) })
}
