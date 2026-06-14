import { PowerOffIcon } from '@/components/icons/PowerOffIcon'
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
          'inline-flex h-8 w-8 items-center justify-center rounded-full bg-auth-surface text-xs font-semibold text-gray-800',
        )}
        aria-label={displayName}
        title={displayName}
      >
        {initials || 'U'}
      </div>
      <Button
        type="button"
        variant="ghost"
        size="sm"
        onClick={() => void logout()}
        disabled={isLoading}
        aria-label="Log out"
        title="Log out"
        className="h-9 w-9 p-0 text-gray-700 hover:bg-auth-surface/80 hover:text-gray-900"
      >
        <PowerOffIcon />
      </Button>
    </div>
  )
}
