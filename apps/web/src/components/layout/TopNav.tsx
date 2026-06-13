import { Link } from 'react-router-dom'

import { useTenancy } from '@/app/TenancyProvider'
import { NavDropdown } from '@/components/layout/NavDropdown'
import { APP_NAME } from '@/lib/config'
import { primaryNavGroups } from '@/lib/navigation'

export function TopNav() {
  const { company, isLoading } = useTenancy()

  const organizationSubtitle = isLoading
    ? 'Loading…'
    : company
      ? `of ${company.name}`
      : 'of —'

  return (
    <div className="flex min-w-0 flex-1 items-center gap-6">
      <Link
        to="/dashboard"
        className="shrink-0 rounded-md px-1 py-1 transition-colors hover:bg-auth-surface/60"
      >
        <span className="block text-base font-semibold text-gray-900">{APP_NAME}</span>
        <span className="block max-w-[10rem] truncate text-xs text-gray-600 sm:max-w-xs">
          {organizationSubtitle}
        </span>
      </Link>

      <nav
        aria-label="Primary"
        className="flex min-w-0 flex-1 items-center gap-1 overflow-x-auto pb-1 [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
      >
        {primaryNavGroups.map((group) => (
          <NavDropdown key={group.id} group={group} />
        ))}
      </nav>
    </div>
  )
}
