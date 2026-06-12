import type { UserRole } from '@/features/auth/types'

export const TOKEN_STORAGE_KEY = 'internal_sea_core_access_token'

export function getStoredToken(): string | null {
  return localStorage.getItem(TOKEN_STORAGE_KEY)
}

export function setStoredToken(token: string): void {
  localStorage.setItem(TOKEN_STORAGE_KEY, token)
}

export function clearStoredToken(): void {
  localStorage.removeItem(TOKEN_STORAGE_KEY)
}

export function roleCanWrite(role: UserRole, isSuperuser = false): boolean {
  if (isSuperuser) return true
  return role === 'editor' || role === 'admin'
}

export function roleCanAdmin(role: UserRole, isSuperuser = false): boolean {
  if (isSuperuser) return true
  return role === 'admin'
}

export function formatRoleLabel(role: UserRole): string {
  switch (role) {
    case 'admin':
      return 'Admin'
    case 'editor':
      return 'Editor'
    case 'viewer':
      return 'Viewer'
    default:
      return role
  }
}
