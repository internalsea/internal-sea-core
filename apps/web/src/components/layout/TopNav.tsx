import { Link } from 'react-router-dom'

import { NavDropdown } from '@/components/layout/NavDropdown'
import { APP_NAME } from '@/lib/config'
import { primaryNavGroups } from '@/lib/navigation'

export function TopNav() {
  return (
    <div className="flex min-w-0 flex-1 items-center gap-6">
      <Link
        to="/dashboard"
        className="shrink-0 rounded-md px-1 py-1 transition-colors hover:bg-white/5"
      >
        <span className="block text-base font-semibold text-white">{APP_NAME}</span>
        <span className="block text-xs text-gray-500">Core</span>
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
