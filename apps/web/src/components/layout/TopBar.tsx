import { useQuery } from '@tanstack/react-query'

import { useTenancy } from '@/app/TenancyProvider'
import { CurrentUserMenu } from '@/features/auth/components/CurrentUserMenu'
import { CurrentCompanyBadge } from '@/features/tenancy/components/CurrentCompanyBadge'
import { GlobalSearch } from '@/features/search/components/GlobalSearch'
import { apiGet } from '@/lib/apiClient'
import type { LiveHealthResponse } from '@/types/common'

export function TopBar() {
  const { company, workspace, isLoading: tenancyLoading } = useTenancy()
  const { data, isError, isLoading } = useQuery({
    queryKey: ['health', 'live'],
    queryFn: () => apiGet<LiveHealthResponse>('/health/live'),
    refetchInterval: 30_000,
    retry: 1,
  })

  const apiOnline = !isError && data?.status === 'live'

  return (
    <header className="flex h-topbar shrink-0 items-center justify-between gap-4 border-b border-app-border bg-app-surface px-6">
      <GlobalSearch />
      <div className="flex items-center gap-4">
        <CurrentCompanyBadge
          company={company}
          workspace={workspace}
          isLoading={tenancyLoading}
        />
        <span className="inline-flex items-center gap-2 text-sm text-gray-600">
          <span
            className={`h-2 w-2 rounded-full ${
              isLoading ? 'bg-gray-400' : apiOnline ? 'bg-status-success' : 'bg-status-danger'
            }`}
          />
          {isLoading ? 'Checking API…' : apiOnline ? 'API online' : 'API unavailable'}
        </span>
        <CurrentUserMenu />
      </div>
    </header>
  )
}
