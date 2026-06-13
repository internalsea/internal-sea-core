import { useTenancy } from '@/app/TenancyProvider'
import { CurrentUserMenu } from '@/features/auth/components/CurrentUserMenu'
import { CurrentCompanyBadge } from '@/features/tenancy/components/CurrentCompanyBadge'
import { GlobalSearch } from '@/features/search/components/GlobalSearch'

export function TopBar() {
  const { company, workspace, isLoading: tenancyLoading } = useTenancy()

  return (
    <header className="flex h-topbar shrink-0 items-center justify-between gap-4 border-b border-app-border bg-app-surface px-6">
      <GlobalSearch />
      <div className="flex items-center gap-4">
        <CurrentCompanyBadge
          company={company}
          workspace={workspace}
          isLoading={tenancyLoading}
        />
        <CurrentUserMenu />
      </div>
    </header>
  )
}
