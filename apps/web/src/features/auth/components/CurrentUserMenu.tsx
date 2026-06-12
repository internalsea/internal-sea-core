import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { useAuth } from '@/features/auth/hooks'
import { formatRoleLabel } from '@/features/auth/utils'

export function CurrentUserMenu() {
  const { user, logout, isLoading } = useAuth()

  if (!user) {
    return <span className="text-sm text-gray-600">Signed out</span>
  }

  const displayName = user.full_name?.trim() || user.email

  return (
    <div className="flex items-center gap-3">
      <div className="text-right">
        <p className="text-sm font-medium text-gray-900">{displayName}</p>
        <Badge variant={user.role === 'admin' ? 'success' : user.role === 'editor' ? 'info' : 'neutral'}>
          {formatRoleLabel(user.role)}
        </Badge>
      </div>
      <Button variant="ghost" size="sm" onClick={() => void logout()} disabled={isLoading}>
        Log out
      </Button>
    </div>
  )
}
