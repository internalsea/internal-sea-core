import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { StatusBadge } from '@/components/ui/StatusBadge'
import { ActivitySection } from '@/features/activity/components/ActivitySection'
import { CommentsSection } from '@/features/comments/components/CommentsSection'
import { AutomationSection } from '@/features/automation/components/AutomationSection'
import { ComplianceSection } from '@/features/compliance/components/ComplianceSection'
import { FilesSection } from '@/features/files/components/FilesSection'
import { NotificationsSection } from '@/features/notifications/components/NotificationsSection'
import { PerformanceSection } from '@/features/performance/components/PerformanceSection'
import { RelationshipsSection } from '@/features/relationships/components/RelationshipsSection'
import { DetailEntityField } from '@/features/entity-picker/components/DetailEntityField'
import type { DataProduct } from '@/features/data-products/types'
import { formatDateTime } from '@/features/data-products/utils'

interface DataProductDetailProps {
  dataProduct: DataProduct
}

function DetailField({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">{label}</dt>
      <dd className="mt-1 text-sm text-gray-700">{value}</dd>
    </div>
  )
}

export function DataProductDetail({ dataProduct }: DataProductDetailProps) {
  return (
    <div className="space-y-6">
      <PageHeader
        title={dataProduct.name}
        description={dataProduct.description ?? undefined}
        actions={
          <Link to="/data-products">
            <Button variant="secondary">Back to Data Products</Button>
          </Link>
        }
      />

      <Card title="Overview">
        <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Type</dt>
            <dd className="mt-1">
              <StatusBadge status={dataProduct.type} />
            </dd>
          </div>
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Status</dt>
            <dd className="mt-1">
              <StatusBadge status={dataProduct.status} />
            </dd>
          </div>
          <div>
            <dt className="text-xs font-medium uppercase tracking-wide text-gray-500">Quality</dt>
            <dd className="mt-1">
              <StatusBadge status={dataProduct.quality_status} />
            </dd>
          </div>
          <DetailField label="Refresh frequency" value={dataProduct.refresh_frequency ?? '—'} />
          <DetailField label="Documentation URL" value={dataProduct.documentation_url ?? '—'} />
        </dl>
      </Card>

      <Card title="Ownership">
        <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <DetailField label="Business domain ID" value={dataProduct.business_domain_id ?? '—'} />
          <DetailEntityField label="Business owner" entityType="person" entityId={dataProduct.business_owner_id} />
          <DetailEntityField label="Technical owner" entityType="person" entityId={dataProduct.technical_owner_id} />
          <DetailEntityField label="Capability" entityType="capability" entityId={dataProduct.capability_id} />
          <DetailEntityField label="Team" entityType="team" entityId={dataProduct.team_id} />
        </dl>
      </Card>

      {(dataProduct.source_systems || dataProduct.consumers) && (
        <Card title="Catalog metadata">
          <dl className="grid gap-4 sm:grid-cols-2">
            <DetailField label="Source systems" value={dataProduct.source_systems ?? '—'} />
            <DetailField label="Consumers" value={dataProduct.consumers ?? '—'} />
          </dl>
        </Card>
      )}

      <Card title="System info">
        <dl className="grid gap-4 sm:grid-cols-2">
          <DetailField label="Created" value={formatDateTime(dataProduct.created_at)} />
          <DetailField label="Updated" value={formatDateTime(dataProduct.updated_at)} />
          <DetailField label="ID" value={dataProduct.id} />
        </dl>
      </Card>

      <CommentsSection targetType="data_product" targetId={dataProduct.id} />
      <ActivitySection entityType="data_product" entityId={dataProduct.id} />

      <RelationshipsSection entityType="data_product" entityId={dataProduct.id} />
      <FilesSection entityType="data_product" entityId={dataProduct.id} title="Files" />
      <ComplianceSection subjectType="data_product" subjectId={dataProduct.id} />
      <PerformanceSection subjectType="data_product" subjectId={dataProduct.id} />
      <NotificationsSection entityType="data_product" entityId={dataProduct.id} />
      <AutomationSection targetType="data_product" targetId={dataProduct.id} />
    </div>
  )
}
