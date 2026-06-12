import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { TeamSummaryCards } from '@/features/teams/components/TeamSummaryCards'
import { AutomationSection } from '@/features/automation/components/AutomationSection'
import { ComplianceSection } from '@/features/compliance/components/ComplianceSection'
import { PerformanceSection } from '@/features/performance/components/PerformanceSection'
import { RelationshipsSection } from '@/features/relationships/components/RelationshipsSection'
import type { Team, TeamSummary } from '@/features/teams/types'
import { formatDateTime } from '@/features/teams/utils'

interface TeamDetailProps {
  team: Team
  summary?: TeamSummary
  summaryLoading?: boolean
}

function PlaceholderSection({ title }: { title: string }) {
  return (
    <Card>
      <SectionHeader title={title} description="Coming in a later prompt." />
    </Card>
  )
}

export function TeamDetail({ team, summary, summaryLoading = false }: TeamDetailProps) {
  return (
    <div className="space-y-6">
      <PageHeader
        title={team.name}
        description={team.description ?? undefined}
        actions={
          <>
            <Link to="/teams">
              <Button variant="secondary">Back to Teams</Button>
            </Link>
            <Link to={`/teams/${team.id}/edit`}>
              <Button>Edit</Button>
            </Link>
          </>
        }
      />

      <TeamSummaryCards summary={summary} isLoading={summaryLoading} />

      <Card title="Overview">
        <dl className="grid gap-4">
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Name</dt>
            <dd className="mt-1 text-sm text-gray-700">{team.name}</dd>
          </div>
          {team.description ? (
            <div>
              <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">
                Description
              </dt>
              <dd className="mt-1 text-sm text-gray-700 whitespace-pre-wrap">{team.description}</dd>
            </div>
          ) : null}
        </dl>
      </Card>

      <Card title="System info">
        <dl className="grid gap-4 sm:grid-cols-2">
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Created</dt>
            <dd className="mt-1 text-sm text-gray-700">{formatDateTime(team.created_at)}</dd>
          </div>
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Updated</dt>
            <dd className="mt-1 text-sm text-gray-700">{formatDateTime(team.updated_at)}</dd>
          </div>
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">ID</dt>
            <dd className="mt-1 text-sm text-gray-700">{team.id}</dd>
          </div>
        </dl>
      </Card>

      <RelationshipsSection entityType="team" entityId={team.id} />

      <PlaceholderSection title="People" />
      <PlaceholderSection title="Data Products" />
      <PlaceholderSection title="Work Items" />
      <PlaceholderSection title="Projects" />
      <ComplianceSection subjectType="team" subjectId={team.id} />
      <AutomationSection targetType="team" targetId={team.id} />
      <PerformanceSection subjectType="team" subjectId={team.id} />
      <PlaceholderSection title="Activity" />
    </div>
  )
}
