import { LoadingState } from '@/components/common/LoadingState'
import { StatusBadge } from '@/components/ui/StatusBadge'
import { MemberRoleBadge } from '@/features/tenancy/components/MemberRoleBadge'
import { COMPANY_MEMBER_ROLES, selectClassName } from '@/features/tenancy/constants'
import type { CompanyMember, CompanyMemberRole } from '@/features/tenancy/types'
import { cn, formatLabel } from '@/lib/utils'

interface MembersTableProps {
  items: CompanyMember[]
  isLoading?: boolean
  canManage?: boolean
  isUpdatingId?: string | null
  onRoleChange?: (memberId: string, role: CompanyMemberRole) => void
}

export function MembersTable({
  items,
  isLoading = false,
  canManage = false,
  isUpdatingId = null,
  onRoleChange,
}: MembersTableProps) {
  if (isLoading) {
    return <LoadingState message="Loading members…" />
  }

  if (items.length === 0) {
    return (
      <p className="text-sm text-gray-500">No company members found.</p>
    )
  }

  const headers = ['User ID', 'Role', 'Status', 'Joined', ...(canManage ? ['Actions'] : [])]

  return (
    <div className="overflow-hidden rounded-card border border-app-border bg-app-surface">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-app-border">
          <thead className="bg-app-background">
            <tr>
              {headers.map((header) => (
                <th
                  key={header}
                  scope="col"
                  className={cn(
                    'px-4 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500',
                    header === 'Actions' && 'text-right',
                  )}
                >
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-app-border">
            {items.map((member) => (
              <tr key={member.id} className="hover:bg-app-muted/30">
                <td className="px-4 py-3 text-sm font-mono text-gray-700">{member.user_id}</td>
                <td className="px-4 py-3">
                  <MemberRoleBadge role={member.role} />
                </td>
                <td className="px-4 py-3">
                  <StatusBadge status={member.status} />
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">
                  {member.joined_at ? new Date(member.joined_at).toLocaleDateString() : '—'}
                </td>
                {canManage ? (
                  <td className="px-4 py-3 text-right">
                    <select
                      className={selectClassName}
                      value={member.role}
                      disabled={isUpdatingId === member.id || member.role === 'owner'}
                      onChange={(event) =>
                        onRoleChange?.(member.id, event.target.value as CompanyMemberRole)
                      }
                      aria-label={`Change role for member ${member.id}`}
                    >
                      {COMPANY_MEMBER_ROLES.map((option) => (
                        <option key={option.value} value={option.value}>
                          {formatLabel(option.value)}
                        </option>
                      ))}
                    </select>
                  </td>
                ) : null}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
