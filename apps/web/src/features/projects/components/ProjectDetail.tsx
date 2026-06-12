import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { ProjectHealthBadge } from '@/features/projects/components/ProjectHealthBadge'
import { ProjectStatusBadge } from '@/features/projects/components/ProjectStatusBadge'
import { ProjectSummaryCards } from '@/features/projects/components/ProjectSummaryCards'
import { ProjectTypeBadge } from '@/features/projects/components/ProjectTypeBadge'
import { ActivitySection } from '@/features/activity/components/ActivitySection'
import { CommentsSection } from '@/features/comments/components/CommentsSection'
import { AutomationSection } from '@/features/automation/components/AutomationSection'
import { ComplianceSection } from '@/features/compliance/components/ComplianceSection'
import { FilesSection } from '@/features/files/components/FilesSection'
import { NotificationsSection } from '@/features/notifications/components/NotificationsSection'
import { PerformanceSection } from '@/features/performance/components/PerformanceSection'
import { RelationshipsSection } from '@/features/relationships/components/RelationshipsSection'
import { DetailEntityField } from '@/features/entity-picker/components/DetailEntityField'
import type { Project, ProjectSummary, ProjectVariant } from '@/features/projects/types'
import {
  formatCurrency,
  formatDate,
  formatDateTime,
  isProjectOverdue,
} from '@/features/projects/utils'
import { cn } from '@/lib/utils'

interface ProjectDetailProps {
  project: Project
  summary?: ProjectSummary
  summaryLoading?: boolean
  variant?: ProjectVariant
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

export function ProjectDetail({
  project,
  summary,
  summaryLoading = false,
  variant = 'projects',
}: ProjectDetailProps) {
  const isInternal = variant === 'internal-projects'
  const listPath = isInternal ? '/internal-projects' : '/projects'
  const editPath = `${listPath}/${project.id}/edit`
  const backLabel = isInternal ? 'Back to Internal Projects' : 'Back to Projects'

  return (
    <div className="space-y-6">
      <PageHeader
        title={project.name}
        description={project.description ?? undefined}
        actions={
          <>
            <Link to={listPath}>
              <Button variant="secondary">{backLabel}</Button>
            </Link>
            <Link to={editPath}>
              <Button>Edit</Button>
            </Link>
          </>
        }
      />

      <ProjectSummaryCards summary={summary} isLoading={summaryLoading} />

      <Card title="Overview">
        <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {!isInternal ? (
            <div>
              <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Type</dt>
              <dd className="mt-1">
                <ProjectTypeBadge type={project.project_type} />
              </dd>
            </div>
          ) : null}
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Status</dt>
            <dd className="mt-1">
              <ProjectStatusBadge status={project.status} />
            </dd>
          </div>
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Health</dt>
            <dd className="mt-1">
              <ProjectHealthBadge healthStatus={project.health_status} />
            </dd>
          </div>
          <DetailField label="Priority" value={project.priority ?? '—'} />
          {!isInternal ? (
            <>
              <DetailField label="Client name" value={project.client_name ?? '—'} />
              <DetailField label="Account name" value={project.account_name ?? '—'} />
            </>
          ) : null}
          {isProjectOverdue(project) ? (
            <div>
              <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Overdue</dt>
              <dd className={cn('mt-1 text-sm font-medium text-status-danger')}>Yes</dd>
            </div>
          ) : null}
        </dl>
      </Card>

      <Card title="Timeline">
        <dl className="grid gap-4 sm:grid-cols-3">
          <DetailField label="Start date" value={formatDate(project.start_date)} />
          <DetailField label="Target end date" value={formatDate(project.target_end_date)} />
          <DetailField label="Actual end date" value={formatDate(project.actual_end_date)} />
        </dl>
      </Card>

      <Card title="Ownership and delivery">
        <dl className="grid gap-4 sm:grid-cols-3">
          <DetailEntityField label="Owner" entityType="person" entityId={project.owner_id} />
          <DetailEntityField label="Team" entityType="team" entityId={project.team_id} />
          <DetailEntityField label="Capability" entityType="capability" entityId={project.capability_id} />
        </dl>
      </Card>

      <Card title="Budget">
        <dl className="grid gap-4 sm:grid-cols-2">
          <DetailField
            label="Amount"
            value={formatCurrency(project.budget_amount, project.budget_currency)}
          />
          <DetailField label="Currency" value={project.budget_currency ?? '—'} />
        </dl>
      </Card>

      {project.delivery_notes ? (
        <Card title="Delivery notes">
          <p className="text-sm text-gray-700 whitespace-pre-wrap">{project.delivery_notes}</p>
        </Card>
      ) : null}

      <Card title="System info">
        <dl className="grid gap-4 sm:grid-cols-2">
          <DetailField label="Created" value={formatDateTime(project.created_at)} />
          <DetailField label="Updated" value={formatDateTime(project.updated_at)} />
          <DetailField label="ID" value={project.id} />
        </dl>
      </Card>

      <RelationshipsSection
        entityType={isInternal ? 'internal_project' : 'project'}
        entityId={project.id}
      />

      <PlaceholderSection title="Work Items" />

      <PlaceholderSection title="Data Products" />
      <ComplianceSection
        subjectType={isInternal ? 'internal_project' : 'project'}
        subjectId={project.id}
        title="Compliance Checks"
      />
      <AutomationSection
        targetType={isInternal ? 'internal_project' : 'project'}
        targetId={project.id}
      />
      <PerformanceSection
        subjectType={isInternal ? 'internal_project' : 'project'}
        subjectId={project.id}
        title="Performance Metrics"
      />
      <NotificationsSection
        entityType={isInternal ? 'internal_project' : 'project'}
        entityId={project.id}
      />
      <PlaceholderSection title="Meetings" />
      <FilesSection
        entityType={isInternal ? 'internal_project' : 'project'}
        entityId={project.id}
        title="Files and Evidence"
      />
      <CommentsSection
        targetType={isInternal ? 'internal_project' : 'project'}
        targetId={project.id}
      />
      <ActivitySection
        entityType={isInternal ? 'internal_project' : 'project'}
        entityId={project.id}
      />
    </div>
  )
}
