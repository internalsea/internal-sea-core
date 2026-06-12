import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { useCanWrite } from '@/features/auth/hooks'
import { PersonStatusBadge } from '@/features/people/components/PersonStatusBadge'
import { SeniorityBadge } from '@/features/people/components/SeniorityBadge'
import type { PersonListItem } from '@/features/people/types'
import { formatAvailability, formatDateTime } from '@/features/people/utils'
import { cn } from '@/lib/utils'

interface PeopleTableProps {
  items: PersonListItem[]
  isLoading?: boolean
  teamNames?: Record<string, string>
  capabilityNames?: Record<string, string>
  onOpen: (id: string) => void
  onEdit: (id: string) => void
  onDeactivate: (item: PersonListItem) => void
}

export function PeopleTable({
  items,
  isLoading = false,
  teamNames = {},
  capabilityNames = {},
  onOpen,
  onEdit,
  onDeactivate,
}: PeopleTableProps) {
  const canWrite = useCanWrite()

  if (isLoading) {
    return <LoadingState message="Loading people…" />
  }

  if (items.length === 0) {
    return null
  }

  const headers = [
    'Name',
    'Role',
    'Seniority',
    'Team',
    'Capability',
    'Availability',
    'Location',
    'Status',
    'Updated',
    'Actions',
  ]

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
            {items.map((item) => (
              <tr key={item.id} className="hover:bg-app-background">
                <td className="px-4 py-3">
                  <button
                    type="button"
                    onClick={() => onOpen(item.id)}
                    className="text-left text-sm font-medium text-gray-900 hover:text-core-blue"
                  >
                    {item.full_name}
                  </button>
                  {item.email ? (
                    <p className="mt-0.5 text-xs text-gray-500">{item.email}</p>
                  ) : null}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {item.role_title ?? '—'}
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <SeniorityBadge seniority={item.seniority_level} />
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {item.team_id ? (teamNames[item.team_id] ?? item.team_id) : '—'}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {item.capability_id
                    ? (capabilityNames[item.capability_id] ?? item.capability_id)
                    : '—'}
                </td>
                <td
                  className={cn(
                    'px-4 py-3 whitespace-nowrap text-sm',
                    item.availability_percent === null || item.availability_percent === undefined
                      ? 'text-gray-500'
                      : 'text-gray-700',
                  )}
                >
                  {formatAvailability(item.availability_percent)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {item.location ?? '—'}
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <PersonStatusBadge isActive={item.is_active} />
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {formatDateTime(item.updated_at)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-right text-sm">
                  <div className="inline-flex items-center gap-2">
                    <Button type="button" variant="ghost" size="sm" onClick={() => onOpen(item.id)}>
                      View
                    </Button>
                    {canWrite ? (
                      <Button type="button" variant="ghost" size="sm" onClick={() => onEdit(item.id)}>
                        Edit
                      </Button>
                    ) : null}
                    {item.is_active ? (
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="text-status-danger hover:text-status-danger"
                        onClick={() => onDeactivate(item)}
                      >
                        Deactivate
                      </Button>
                    ) : null}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
