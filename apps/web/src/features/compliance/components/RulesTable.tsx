import { RuleSeverityBadge } from '@/features/compliance/components/RuleSeverityBadge'
import type { ComplianceRule } from '@/features/compliance/types'
import { formatSubjectType } from '@/features/compliance/utils'

interface RulesTableProps {
  items: ComplianceRule[]
}

export function RulesTable({ items }: RulesTableProps) {
  if (items.length === 0) {
    return <p className="text-sm text-gray-500">No rules defined for this policy.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-app-border text-sm">
        <thead className="bg-app-muted">
          <tr>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Code</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Name</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Severity</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Subject</th>
            <th className="px-4 py-3 text-left font-medium text-gray-600">Active</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border bg-app-surface">
          {items.map((item) => (
            <tr key={item.id}>
              <td className="px-4 py-3 font-mono text-xs">{item.code ?? '—'}</td>
              <td className="px-4 py-3">{item.name}</td>
              <td className="px-4 py-3"><RuleSeverityBadge severity={item.severity} /></td>
              <td className="px-4 py-3 text-gray-600">
                {item.subject_type ? formatSubjectType(item.subject_type) : '—'}
              </td>
              <td className="px-4 py-3 text-gray-600">{item.is_active ? 'Yes' : 'No'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
