import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { CapabilitySummaryCards } from '@/features/capabilities/components/CapabilitySummaryCards'
import { AutomationSection } from '@/features/automation/components/AutomationSection'
import { ComplianceSection } from '@/features/compliance/components/ComplianceSection'
import { PerformanceSection } from '@/features/performance/components/PerformanceSection'
import { RelationshipsSection } from '@/features/relationships/components/RelationshipsSection'
import type { Capability, CapabilitySummary } from '@/features/capabilities/types'
import { formatDateTime } from '@/features/capabilities/utils'

interface CapabilityDetailProps {
  capability: Capability
  summary?: CapabilitySummary
  summaryLoading?: boolean
}

function PlaceholderSection({ title }: { title: string }) {
  return (
    <Card>
      <SectionHeader title={title} description="Coming in a later prompt." />
    </Card>
  )
}

export function CapabilityDetail({
  capability,
  summary,
  summaryLoading = false,
}: CapabilityDetailProps) {
  return (
    <div className="space-y-6">
      <PageHeader
        title={capability.name}
        description={capability.description ?? undefined}
        actions={
          <>
            <Link to="/capabilities">
              <Button variant="secondary">Back to Capabilities</Button>
            </Link>
            <Link to={`/capabilities/${capability.id}/edit`}>
              <Button>Edit</Button>
            </Link>
          </>
        }
      />

      <CapabilitySummaryCards summary={summary} isLoading={summaryLoading} />

      <Card title="Overview">
        <dl className="grid gap-4">
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Name</dt>
            <dd className="mt-1 text-sm text-gray-700">{capability.name}</dd>
          </div>
          {capability.description ? (
            <div>
              <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">
                Description
              </dt>
              <dd className="mt-1 text-sm text-gray-700 whitespace-pre-wrap">
                {capability.description}
              </dd>
            </div>
          ) : null}
        </dl>
      </Card>

      <Card title="System info">
        <dl className="grid gap-4 sm:grid-cols-2">
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Created</dt>
            <dd className="mt-1 text-sm text-gray-700">{formatDateTime(capability.created_at)}</dd>
          </div>
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Updated</dt>
            <dd className="mt-1 text-sm text-gray-700">{formatDateTime(capability.updated_at)}</dd>
          </div>
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">ID</dt>
            <dd className="mt-1 text-sm text-gray-700">{capability.id}</dd>
          </div>
        </dl>
      </Card>

      <RelationshipsSection entityType="capability" entityId={capability.id} />

      <PlaceholderSection title="People" />
      <PlaceholderSection title="Data Products" />
      <PlaceholderSection title="Work Items" />
      <PlaceholderSection title="Projects" />
      <PlaceholderSection title="Skill Gaps" />
      <ComplianceSection subjectType="capability" subjectId={capability.id} />
      <AutomationSection targetType="capability" targetId={capability.id} />
      <PerformanceSection subjectType="capability" subjectId={capability.id} />
      <PlaceholderSection title="Activity" />
    </div>
  )
}
