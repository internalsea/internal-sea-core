import { Link } from 'react-router-dom'

import { SettingsIcon } from '@/components/icons/SettingsIcon'
import { Button } from '@/components/ui/Button'
import { useAuth } from '@/features/auth/hooks'
import { cn } from '@/lib/utils'

export function CurrentUserMenu() {
  const { user, logout, isLoading } = useAuth()

  if (!user) {
    return <span className="text-sm text-gray-600">Signed out</span>
  }

  const displayName = user.full_name?.trim() || user.email

  return (
    <div className="flex items-center gap-3">
      <p className="text-sm font-medium text-gray-900">{displayName}</p>
      <Link
        to="/settings"
        aria-label="Settings"
        className={cn(
          'inline-flex h-8 w-8 items-center justify-center rounded-md text-gray-600',
          'transition-colors hover:bg-app-muted hover:text-gray-900',
        )}
      >
        <SettingsIcon />
      </Link>
      <Button variant="ghost" size="sm" onClick={() => void logout()} disabled={isLoading}>
        Log out
      </Button>
    </div>
  )
}
