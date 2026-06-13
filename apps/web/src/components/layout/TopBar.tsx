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
    <header className="relative z-40 flex h-topbar shrink-0 items-center gap-4 overflow-visible border-b border-auth-surfaceBorder bg-auth-nav px-4 lg:px-6">
      <TopNav />

      <div className="flex shrink-0 items-center gap-2 sm:gap-3">
        <div className="hidden w-72 xl:block">
          <GlobalSearch />
        </div>
        <div className="w-36 sm:w-44 xl:hidden">
          <GlobalSearch />
        </div>

        <CreateActionMenu />

        <Link
          to="/notifications"
          aria-label="Notifications"
          className={cn(
            'inline-flex h-9 w-9 items-center justify-center rounded-md transition-colors',
            notificationsActive
              ? 'bg-auth-surface text-gray-900'
              : 'text-gray-700 hover:bg-auth-surface/80 hover:text-gray-900',
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
              ? 'bg-auth-surface text-gray-900'
              : 'text-gray-700 hover:bg-auth-surface/80 hover:text-gray-900',
          )}
        >
          <SettingsIcon />
        </Link>

        <CurrentUserMenu />
      </div>
    </header>
  )
}
