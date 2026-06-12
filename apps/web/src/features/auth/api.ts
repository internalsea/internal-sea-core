import type { CurrentUser, LoginRequest, TokenResponse } from '@/features/auth/types'
import { apiGet, apiPost } from '@/lib/apiClient'

export function login(payload: LoginRequest): Promise<TokenResponse> {
  return apiPost<TokenResponse>('/auth/login', payload)
}

export function getMe(): Promise<CurrentUser> {
  return apiGet<CurrentUser>('/auth/me')
}

export async function logout(): Promise<void> {
  try {
    await apiPost<{ message: string }>('/auth/logout', {})
  } catch {
    // Client-side logout is sufficient for JWT MVP.
  }
}
