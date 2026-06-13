import { Badge } from '@/components/ui/Badge'
import { Card } from '@/components/ui/Card'
import { useAuth } from '@/features/auth/hooks'
import { formatRoleLabel } from '@/features/auth/utils'

function DetailField({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">{label}</dt>
      <dd className="mt-1 text-sm text-gray-900">{value}</dd>
    </div>
  )
}

export function UserSettingsSection() {
  const { user } = useAuth()

  if (!user) {
    return <p className="text-sm text-gray-500">Sign in to view your profile.</p>
  }

  const displayName = user.full_name?.trim() || '—'

  return (
    <Card title="User profile">
      <dl className="grid gap-6 sm:grid-cols-2">
        <DetailField label="Full name" value={displayName} />
        <DetailField label="Email" value={user.email} />
        <div>
          <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Role</dt>
          <dd className="mt-1">
            <Badge
              variant={
                user.role === 'admin' ? 'success' : user.role === 'editor' ? 'info' : 'neutral'
              }
            >
              {formatRoleLabel(user.role)}
            </Badge>
          </dd>
        </div>
        <DetailField label="Status" value={user.is_active ? 'Active' : 'Inactive'} />
      </dl>
      <p className="mt-6 text-xs text-gray-500">
        Profile editing will be available in a future release.
      </p>
    </Card>
  )
}
