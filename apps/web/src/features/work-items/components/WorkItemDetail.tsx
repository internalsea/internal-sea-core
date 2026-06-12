import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { WorkItemPriorityBadge } from '@/features/work-items/components/WorkItemPriorityBadge'
import { WorkItemStatusBadge } from '@/features/work-items/components/WorkItemStatusBadge'
import { WorkItemTypeBadge } from '@/features/work-items/components/WorkItemTypeBadge'
import { ActivitySection } from '@/features/activity/components/ActivitySection'
import { CommentsSection } from '@/features/comments/components/CommentsSection'
import { FilesSection } from '@/features/files/components/FilesSection'
import { NotificationsSection } from '@/features/notifications/components/NotificationsSection'
import { AutomationSection } from '@/features/automation/components/AutomationSection'
import { RelationshipsSection } from '@/features/relationships/components/RelationshipsSection'
import { DetailEntityField } from '@/features/entity-picker/components/DetailEntityField'
import type { WorkItem } from '@/features/work-items/types'
import { formatDate, formatDateTime, isWorkItemOverdue } from '@/features/work-items/utils'
import { cn } from '@/lib/utils'

interface WorkItemDetailProps {
  workItem: WorkItem
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

export function WorkItemDetail({ workItem }: WorkItemDetailProps) {
  return (
    <div className="space-y-6">
      <PageHeader
        title={workItem.title}
        description={workItem.description ?? undefined}
        actions={
          <>
            <Link to="/work-items">
              <Button variant="secondary">Back to Work Items</Button>
            </Link>
            <Link to={`/work-items/${workItem.id}/edit`}>
              <Button>Edit</Button>
            </Link>
          </>
        }
      />

      <Card title="Overview">
        <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Type</dt>
            <dd className="mt-1">
              <WorkItemTypeBadge type={workItem.type} />
            </dd>
          </div>
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Status</dt>
            <dd className="mt-1">
              <WorkItemStatusBadge status={workItem.status} />
            </dd>
          </div>
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Priority</dt>
            <dd className="mt-1">
              <WorkItemPriorityBadge priority={workItem.priority} />
            </dd>
          </div>
          <DetailField label="Due date" value={formatDate(workItem.due_date)} />
          <DetailField
            label="Estimate points"
            value={workItem.estimate_points?.toString() ?? '—'}
          />
          {isWorkItemOverdue(workItem) ? (
            <div>
              <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Overdue</dt>
              <dd className={cn('mt-1 text-sm font-medium text-status-danger')}>Yes</dd>
            </div>
          ) : null}
        </dl>
      </Card>

      <Card title="Links">
        <dl className="grid gap-4 sm:grid-cols-2">
          <DetailEntityField label="Assignee" entityType="person" entityId={workItem.assignee_id} />
          <DetailEntityField label="Reporter" entityType="person" entityId={workItem.reporter_id} />
          <DetailEntityField label="Data product" entityType="data_product" entityId={workItem.data_product_id} />
          <DetailEntityField label="Project" entityType="project" entityId={workItem.project_id} />
          <DetailEntityField label="Capability" entityType="capability" entityId={workItem.capability_id} />
          <DetailEntityField label="Team" entityType="team" entityId={workItem.team_id} />
        </dl>
      </Card>

      <Card title="System info">
        <dl className="grid gap-4 sm:grid-cols-2">
          <DetailField label="Created" value={formatDateTime(workItem.created_at)} />
          <DetailField label="Updated" value={formatDateTime(workItem.updated_at)} />
          <DetailField label="ID" value={workItem.id} />
        </dl>
      </Card>

      <CommentsSection targetType="work_item" targetId={workItem.id} />
      <ActivitySection entityType="work_item" entityId={workItem.id} />
      <RelationshipsSection entityType="work_item" entityId={workItem.id} />
      <FilesSection entityType="work_item" entityId={workItem.id} title="Files" />
      <NotificationsSection entityType="work_item" entityId={workItem.id} />
      <AutomationSection targetType="work_item" targetId={workItem.id} />
      <PlaceholderSection title="Decisions / Risks" />
    </div>
  )
}
