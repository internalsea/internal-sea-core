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

import { useAuth } from '@/features/auth/hooks'
import { getCurrentTenant } from '@/features/tenancy/api'
import type { Company, CompanyMember, CompanyMemberRole, Workspace } from '@/features/tenancy/types'
import {
  clearStoredTenantIds,
  setStoredTenantIds,
} from '@/features/tenancy/utils'
import { ApiError } from '@/lib/apiClient'

interface TenancyContextValue {
  company: Company | null
  workspace: Workspace | null
  member: CompanyMember | null
  companyId: string | null
  workspaceId: string | null
  role: CompanyMemberRole | null
  isLoading: boolean
  refetch: () => Promise<void>
}

const TenancyContext = createContext<TenancyContextValue | null>(null)

export function useTenancy(): TenancyContextValue {
  const context = useContext(TenancyContext)
  if (!context) {
    throw new Error('useTenancy must be used within TenancyProvider')
  }
  return context
}

interface TenancyProviderProps {
  children: ReactNode
}

function isNoTenantError(error: unknown): boolean {
  return error instanceof ApiError && (error.status === 400 || error.status === 404)
}

export function TenancyProvider({ children }: TenancyProviderProps) {
  const { isAuthenticated, isLoading: authLoading } = useAuth()
  const navigate = useNavigate()

  const [company, setCompany] = useState<Company | null>(null)
  const [workspace, setWorkspace] = useState<Workspace | null>(null)
  const [member, setMember] = useState<CompanyMember | null>(null)
  const [tenantLoading, setTenantLoading] = useState(false)

  const clearTenant = useCallback(() => {
    setCompany(null)
    setWorkspace(null)
    setMember(null)
    clearStoredTenantIds()
  }, [])

  const loadTenant = useCallback(async () => {
    setTenantLoading(true)
    try {
      const context = await getCurrentTenant()
      setCompany(context.company)
      setWorkspace(context.workspace)
      setMember(context.member)
      setStoredTenantIds(context.company.id, context.workspace.id)
    } catch (error) {
      clearTenant()
      if (isNoTenantError(error)) {
        const path = window.location.pathname
        const skipRedirect =
          path === '/login' ||
          path === '/register' ||
          path === '/onboarding/first-user' ||
          path === '/onboarding/company-setup'
        if (!skipRedirect) {
          navigate('/onboarding/company-setup', { replace: true })
        }
      }
      throw error
    } finally {
      setTenantLoading(false)
    }
  }, [clearTenant, navigate])

  const refetch = useCallback(async () => {
    if (!isAuthenticated) return
    await loadTenant()
  }, [isAuthenticated, loadTenant])

  useEffect(() => {
    if (authLoading) return

    if (!isAuthenticated) {
      clearTenant()
      return
    }

    void loadTenant().catch(() => {
      // Redirect handled in loadTenant for no-tenant errors.
    })
  }, [authLoading, isAuthenticated, clearTenant, loadTenant])

  const value = useMemo<TenancyContextValue>(
    () => ({
      company,
      workspace,
      member,
      companyId: company?.id ?? null,
      workspaceId: workspace?.id ?? null,
      role: member ? (member.role as CompanyMemberRole) : null,
      isLoading: authLoading || (isAuthenticated && tenantLoading),
      refetch,
    }),
    [company, workspace, member, authLoading, isAuthenticated, tenantLoading, refetch],
  )

  return <TenancyContext.Provider value={value}>{children}</TenancyContext.Provider>
}
