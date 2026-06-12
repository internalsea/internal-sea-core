import { useState } from 'react'

import { Button } from '@/components/ui/Button'
import { useCanWrite } from '@/features/auth/hooks'
import { Card } from '@/components/ui/Card'
import { ComplianceEvidenceForm } from '@/features/compliance/components/ComplianceEvidenceForm'
import { ComplianceEvidenceList } from '@/features/compliance/components/ComplianceEvidenceList'
import { ComplianceStatusBadge } from '@/features/compliance/components/ComplianceStatusBadge'
import {
  useAddComplianceEvidence,
  useComplianceCheckEvidence,
  useDeleteComplianceEvidence,
} from '@/features/compliance/hooks'
import { AutomationSection } from '@/features/automation/components/AutomationSection'
import { NotificationsSection } from '@/features/notifications/components/NotificationsSection'
import { DetailEntityField } from '@/features/entity-picker/components/DetailEntityField'
import type { ComplianceCheck } from '@/features/compliance/types'
import {
  formatDate,
  formatDateTime,
  formatSubjectType,
  getApiErrorMessage,
  isOverdueCheck,
} from '@/features/compliance/utils'

interface ComplianceCheckDetailProps {
  check: ComplianceCheck
  onEdit: () => void
  onDelete: () => void
}

export function ComplianceCheckDetail({ check, onEdit, onDelete }: ComplianceCheckDetailProps) {
  const canWrite = useCanWrite()
  const [showEvidenceForm, setShowEvidenceForm] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)
  const { data: evidence, isLoading } = useComplianceCheckEvidence(check.id)
  const addEvidence = useAddComplianceEvidence(check.id, check.subject_type, check.subject_id)
  const deleteEvidence = useDeleteComplianceEvidence(check.id, check.subject_type, check.subject_id)
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <h1 className="text-2xl font-semibold text-gray-900">{check.title}</h1>
            <ComplianceStatusBadge status={check.status} />
            {isOverdueCheck(check) ? <span className="text-xs font-medium text-status-danger">Overdue</span> : null}
          </div>
          {check.description ? <p className="text-gray-600">{check.description}</p> : null}
        </div>
        {canWrite ? (
          <div className="flex gap-2">
            <Button variant="secondary" onClick={onEdit}>Edit</Button>
            <Button variant="ghost" onClick={onDelete}>Delete</Button>
          </div>
        ) : null}
      </div>

      <Card title="Overview">
        <dl className="grid gap-4 sm:grid-cols-2">
          <DetailEntityField
            label={`Subject (${formatSubjectType(check.subject_type)})`}
            entityType={check.subject_type}
            entityId={check.subject_id}
          />
          <DetailEntityField label="Owner" entityType="person" entityId={check.owner_id} />
          <div><dt className="text-xs font-medium uppercase text-gray-500">Check type</dt><dd className="mt-1 text-sm">{check.check_type}</dd></div>
          <div><dt className="text-xs font-medium uppercase text-gray-500">Due date</dt><dd className="mt-1 text-sm">{formatDate(check.due_date)}</dd></div>
          <div><dt className="text-xs font-medium uppercase text-gray-500">Completed</dt><dd className="mt-1 text-sm">{formatDateTime(check.completed_at)}</dd></div>
          <div><dt className="text-xs font-medium uppercase text-gray-500">Rule ID</dt><dd className="mt-1 text-sm break-all">{check.rule_id ?? '—'}</dd></div>
          <div><dt className="text-xs font-medium uppercase text-gray-500">Control ID</dt><dd className="mt-1 text-sm break-all">{check.control_id ?? '—'}</dd></div>
        </dl>
      </Card>

      {check.result_summary ? (
        <Card title="Result summary">
          <p className="text-sm text-gray-700">{check.result_summary}</p>
        </Card>
      ) : null}

      <Card title="Evidence">
        {canWrite ? (
          <div className="mb-4 flex justify-end">
            <Button variant="secondary" size="sm" onClick={() => setShowEvidenceForm((c) => !c)}>
              {showEvidenceForm ? 'Cancel' : 'Add evidence'}
            </Button>
          </div>
        ) : null}
        {canWrite && showEvidenceForm ? (
          <ComplianceEvidenceForm
            isSubmitting={addEvidence.isPending}
            submitError={submitError}
            onCancel={() => setShowEvidenceForm(false)}
            onSubmit={async (payload) => {
              setSubmitError(null)
              try {
                await addEvidence.mutateAsync(payload)
                setShowEvidenceForm(false)
              } catch (error) {
                setSubmitError(getApiErrorMessage(error))
              }
            }}
          />
        ) : null}
        {isLoading ? (
          <p className="text-sm text-gray-500">Loading evidence…</p>
        ) : (
          <ComplianceEvidenceList
            items={evidence ?? []}
            isDeleting={canWrite && deleteEvidence.isPending}
            onDelete={
              canWrite
                ? async (item) => {
                    if (!window.confirm('Remove this evidence link?')) return
                    await deleteEvidence.mutateAsync(item.id)
                  }
                : undefined
            }
          />
        )}
      </Card>

      <AutomationSection targetType="compliance_check" targetId={check.id} />
      <NotificationsSection entityType="compliance_check" entityId={check.id} />
    </div>
  )
}
