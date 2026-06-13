import { Button } from '@/components/ui/Button'
import { useAuth } from '@/features/auth/hooks'
import { cn } from '@/lib/utils'

export function CurrentUserMenu() {
  const { user, logout, isLoading } = useAuth()

  if (!user) {
    return <span className="text-sm text-gray-600">Signed out</span>
  }

  const displayName = user.full_name?.trim() || user.email
  const initials = displayName
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? '')
    .join('')

  return (
    <div className="flex items-center gap-2 border-l border-auth-surfaceBorder pl-3">
      <div
        className={cn(
          'hidden h-8 w-8 items-center justify-center rounded-full bg-auth-surface text-xs font-semibold text-gray-800 sm:inline-flex',
        )}
        aria-hidden="true"
      >
        {initials || 'U'}
      </div>
      <div className="hidden min-w-0 lg:block">
        <p className="truncate text-sm font-medium text-gray-900">{displayName}</p>
        <p className="truncate text-xs text-gray-600">{user.email}</p>
      </div>
      <Button
        variant="ghost"
        size="sm"
        onClick={() => void logout()}
        disabled={isLoading}
        className="text-gray-700 hover:bg-auth-surface/80 hover:text-gray-900"
      >
        Log out
      </Button>
    </div>
  )
}
