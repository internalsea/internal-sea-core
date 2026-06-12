export type UserRole = 'admin' | 'editor' | 'viewer'

export interface CurrentUser {
  id: string
  email: string
  full_name: string | null
  role: UserRole
  is_active: boolean
  is_superuser: boolean
}

export interface LoginRequest {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: CurrentUser
}

export interface AuthState {
  user: CurrentUser | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
}
