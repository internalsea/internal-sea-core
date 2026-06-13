import { Link, useLocation } from 'react-router-dom'

import { BellIcon } from '@/components/icons/BellIcon'
import { SettingsIcon } from '@/components/icons/SettingsIcon'
import { CreateActionMenu } from '@/components/layout/CreateActionMenu'
import { TopNav } from '@/components/layout/TopNav'
import { CurrentUserMenu } from '@/features/auth/components/CurrentUserMenu'
import { GlobalSearch } from '@/features/search/components/GlobalSearch'
import { isNotificationsPageActive, isSettingsPageActive } from '@/lib/navigation'
import { cn } from '@/lib/utils'

export function TopBar() {
  const location = useLocation()
  const settingsActive = isSettingsPageActive(location.pathname)
  const notificationsActive = isNotificationsPageActive(location.pathname)

  return (
    <header className="flex h-topbar shrink-0 items-center gap-4 border-b border-white/10 bg-core-navy px-4 lg:px-6">
      <TopNav />

      <div className="flex shrink-0 items-center gap-2 sm:gap-3">
        <div className="hidden w-72 xl:block">
          <GlobalSearch variant="dark" />
        </div>
        <div className="w-36 sm:w-44 xl:hidden">
          <GlobalSearch variant="dark" />
        </div>

        <CreateActionMenu />

        <Link
          to="/notifications"
          aria-label="Notifications"
          className={cn(
            'inline-flex h-9 w-9 items-center justify-center rounded-md transition-colors',
            notificationsActive
              ? 'bg-white/10 text-white'
              : 'text-gray-300 hover:bg-white/5 hover:text-white',
          )}
        >
          <BellIcon />
        </Link>

        <Link
          to="/settings"
          aria-label="Settings"
          className={cn(
            'inline-flex h-9 w-9 items-center justify-center rounded-md transition-colors',
            settingsActive
              ? 'bg-white/10 text-white'
              : 'text-gray-300 hover:bg-white/5 hover:text-white',
          )}
        >
          <SettingsIcon />
        </Link>

        <CurrentUserMenu />
      </div>
    </header>
  )
}
