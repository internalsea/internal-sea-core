import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import { useNavigate } from 'react-router-dom'

import * as authApi from '@/features/auth/api'
import type { CurrentUser, LoginRequest } from '@/features/auth/types'
import {
  clearStoredToken,
  getStoredToken,
  roleCanAdmin,
  roleCanWrite,
  setStoredToken,
} from '@/features/auth/utils'
import { ApiError, setUnauthorizedHandler } from '@/lib/apiClient'

interface AuthContextValue {
  user: CurrentUser | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (payload: LoginRequest) => Promise<void>
  logout: () => Promise<void>
  hasRole: (...roles: Array<CurrentUser['role']>) => boolean
  canWrite: boolean
  canAdmin: boolean
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function useAuthContext(): AuthContextValue {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuthContext must be used within AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const navigate = useNavigate()
  const [user, setUser] = useState<CurrentUser | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const clearSession = useCallback(() => {
    clearStoredToken()
    setToken(null)
    setUser(null)
  }, [])

  const logout = useCallback(async () => {
    try {
      await authApi.logout()
    } finally {
      clearSession()
      navigate('/login', { replace: true })
    }
  }, [clearSession, navigate])

  useEffect(() => {
    setUnauthorizedHandler(() => {
      clearSession()
      navigate('/login', { replace: true })
    })
    return () => setUnauthorizedHandler(null)
  }, [clearSession, navigate])

  useEffect(() => {
    let cancelled = false

    async function bootstrap() {
      const storedToken = getStoredToken()
      if (!storedToken) {
        if (!cancelled) setIsLoading(false)
        return
      }

      setToken(storedToken)
      try {
        const currentUser = await authApi.getMe()
        if (!cancelled) {
          setUser(currentUser)
        }
      } catch {
        if (!cancelled) {
          clearSession()
        }
      } finally {
        if (!cancelled) setIsLoading(false)
      }
    }

    void bootstrap()
    return () => {
      cancelled = true
    }
  }, [clearSession])

  const login = useCallback(
    async (payload: LoginRequest) => {
      const response = await authApi.login(payload)
      setStoredToken(response.access_token)
      setToken(response.access_token)
      setUser(response.user)
      navigate('/dashboard', { replace: true })
    },
    [navigate],
  )

  const hasRole = useCallback(
    (...roles: Array<CurrentUser['role']>) => {
      if (!user) return false
      if (user.is_superuser) return true
      return roles.includes(user.role)
    },
    [user],
  )

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      token,
      isAuthenticated: Boolean(user && token),
      isLoading,
      login,
      logout,
      hasRole,
      canWrite: user ? roleCanWrite(user.role, user.is_superuser) : false,
      canAdmin: user ? roleCanAdmin(user.role, user.is_superuser) : false,
    }),
    [user, token, isLoading, login, logout, hasRole],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function getApiErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    return error.message || `Request failed (${error.status})`
  }
  if (error instanceof Error) return error.message
  return 'An unexpected error occurred'
}
