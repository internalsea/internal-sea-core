import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { PersonStatusBadge } from '@/features/people/components/PersonStatusBadge'
import { PersonSummaryCards } from '@/features/people/components/PersonSummaryCards'
import { SeniorityBadge } from '@/features/people/components/SeniorityBadge'
import { PerformanceSection } from '@/features/performance/components/PerformanceSection'
import { RelationshipsSection } from '@/features/relationships/components/RelationshipsSection'
import { DetailEntityField } from '@/features/entity-picker/components/DetailEntityField'
import type { Person, PersonSummary } from '@/features/people/types'
import { formatAvailability, formatDateTime } from '@/features/people/utils'

interface PersonDetailProps {
  person: Person
  summary?: PersonSummary
  summaryLoading?: boolean
}

function DetailField({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">{label}</dt>
      <dd className="mt-1 text-sm text-gray-700">{value}</dd>
    </div>
  )
}

function PlaceholderSection({ title }: { title: string }) {
  return (
    <Card>
      <SectionHeader title={title} description="Coming in a later prompt." />
    </Card>
  )
}

export function PersonDetail({
  person,
  summary,
  summaryLoading = false,
}: PersonDetailProps) {
  const description = person.role_title ?? person.email ?? undefined

  return (
    <div className="space-y-6">
      <PageHeader
        title={person.full_name}
        description={description}
        actions={
          <>
            <Link to="/people">
              <Button variant="secondary">Back to People</Button>
            </Link>
            <PermissionGate require="editor">
              <Link to={`/people/${person.id}/edit`}>
                <Button>Edit</Button>
              </Link>
            </PermissionGate>
          </>
        }
      />

      <PersonSummaryCards summary={summary} isLoading={summaryLoading} />

      <Card title="Overview">
        <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <DetailField label="Full name" value={person.full_name} />
          <DetailField label="Email" value={person.email ?? '—'} />
          <DetailField label="Role title" value={person.role_title ?? '—'} />
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Seniority</dt>
            <dd className="mt-1">
              <SeniorityBadge seniority={person.seniority_level} />
            </dd>
          </div>
          <DetailField label="Location" value={person.location ?? '—'} />
          <DetailField
            label="Availability"
            value={formatAvailability(person.availability_percent)}
          />
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Status</dt>
            <dd className="mt-1">
              <PersonStatusBadge isActive={person.is_active} />
            </dd>
          </div>
        </dl>
      </Card>

      <Card title="Organization">
        <dl className="grid gap-4 sm:grid-cols-3">
          <DetailEntityField label="Team" entityType="team" entityId={person.team_id} />
          <DetailEntityField label="Capability" entityType="capability" entityId={person.capability_id} />
          <DetailField label="User ID" value={person.user_id ?? '—'} />
        </dl>
      </Card>

      <Card title="System info">
        <dl className="grid gap-4 sm:grid-cols-2">
          <DetailField label="Created" value={formatDateTime(person.created_at)} />
          <DetailField label="Updated" value={formatDateTime(person.updated_at)} />
          <DetailField label="ID" value={person.id} />
        </dl>
      </Card>

      <RelationshipsSection entityType="person" entityId={person.id} />

      <PlaceholderSection title="Skills" />
      <PlaceholderSection title="Allocations" />
      <PerformanceSection subjectType="person" subjectId={person.id} title="Performance Metrics" />
      <PlaceholderSection title="Assigned Work Items" />
      <PlaceholderSection title="Owned Data Products" />
      <PlaceholderSection title="Activity" />
    </div>
  )
}
