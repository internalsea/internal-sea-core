import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { EntityPicker } from '@/features/entity-picker/components/EntityPicker'
import type { EntityPickerType, EntityPickerValue } from '@/features/entity-picker/types'
import {
  COMPLIANCE_CHECK_TYPES,
  COMPLIANCE_STATUSES,
  COMPLIANCE_SUBJECT_TYPES,
  selectClassName,
} from '@/features/compliance/constants'
import type { ComplianceCheckFormValues, ComplianceSubjectType } from '@/features/compliance/types'
import { cleanComplianceCheckPayload } from '@/features/compliance/utils'

const SUBJECT_PICKER_TYPES: EntityPickerType[] = [
  'data_product',
  'project',
  'internal_project',
  'team',
  'capability',
]

interface ComplianceCheckFormProps {
  initialValues?: Partial<ComplianceCheckFormValues>
  mode: 'create' | 'edit'
  lockSubject?: { subjectType: ComplianceSubjectType; subjectId: string }
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (values: ReturnType<typeof cleanComplianceCheckPayload>) => void
  onCancel: () => void
}

const defaultValues: ComplianceCheckFormValues = {
  title: '',
  description: '',
  subject_type: 'data_product',
  subject_id: '',
  rule_id: '',
  control_id: '',
  check_type: 'manual',
  status: 'not_started',
  result_summary: '',
  owner_id: '',
  due_date: '',
}

function subjectToPickerValue(
  subjectType: ComplianceSubjectType,
  subjectId: string,
): EntityPickerValue | null {
  if (!subjectId) {
    return null
  }
  return { entity_type: subjectType as EntityPickerType, entity_id: subjectId }
}

function ownerToPickerValue(ownerId: string): EntityPickerValue | null {
  if (!ownerId) {
    return null
  }
  return { entity_type: 'person', entity_id: ownerId }
}

export function ComplianceCheckForm({
  initialValues,
  mode,
  lockSubject,
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: ComplianceCheckFormProps) {
  const mergedInitial = {
    ...defaultValues,
    ...initialValues,
    ...(lockSubject
      ? { subject_type: lockSubject.subjectType, subject_id: lockSubject.subjectId }
      : {}),
  }

  const [values, setValues] = useState<ComplianceCheckFormValues>(mergedInitial)
  const [subjectEntity, setSubjectEntity] = useState<EntityPickerValue | null>(
    subjectToPickerValue(mergedInitial.subject_type, mergedInitial.subject_id),
  )
  const [ownerEntity, setOwnerEntity] = useState<EntityPickerValue | null>(
    ownerToPickerValue(mergedInitial.owner_id),
  )
  const [titleError, setTitleError] = useState<string | null>(null)
  const [showAdvanced, setShowAdvanced] = useState(false)

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    if (!values.title.trim()) {
      setTitleError('Title is required')
      return
    }
    setTitleError(null)

    const payload = showAdvanced
      ? values
      : {
          ...values,
          subject_type: (subjectEntity?.entity_type ?? values.subject_type) as ComplianceSubjectType,
          subject_id: subjectEntity?.entity_id ?? values.subject_id,
          owner_id: ownerEntity?.entity_id ?? values.owner_id,
        }

    onSubmit(cleanComplianceCheckPayload(payload))
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="mb-1 block text-sm font-medium text-gray-700">Title *</label>
        <Input value={values.title} onChange={(e) => setValues((c) => ({ ...c, title: e.target.value }))} />
        {titleError ? <p className="mt-1 text-sm text-status-danger">{titleError}</p> : null}
      </div>
      <div>
        <label className="mb-1 block text-sm font-medium text-gray-700">Description</label>
        <textarea className="block min-h-20 w-full rounded-md border border-app-borderStrong px-3 py-2 text-sm" value={values.description} onChange={(e) => setValues((c) => ({ ...c, description: e.target.value }))} />
      </div>

      {!showAdvanced && !lockSubject ? (
        <EntityPicker
          label="Subject"
          allowedTypes={SUBJECT_PICKER_TYPES}
          value={subjectEntity}
          onChange={setSubjectEntity}
          required
          helperText="Entity this compliance check applies to."
        />
      ) : lockSubject ? (
        <EntityPicker
          label="Subject"
          allowedTypes={[lockSubject.subjectType as EntityPickerType]}
          value={subjectToPickerValue(lockSubject.subjectType, lockSubject.subjectId)}
          onChange={() => {}}
          disabled
          allowClear={false}
        />
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Subject type</label>
            <select className={selectClassName} value={values.subject_type} onChange={(e) => setValues((c) => ({ ...c, subject_type: e.target.value as ComplianceSubjectType }))}>
              {COMPLIANCE_SUBJECT_TYPES.map((item) => <option key={item.value} value={item.value}>{item.label}</option>)}
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Subject ID</label>
            <Input value={values.subject_id} onChange={(e) => setValues((c) => ({ ...c, subject_id: e.target.value }))} />
          </div>
        </div>
      )}

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Check type</label>
          <select className={selectClassName} value={values.check_type} onChange={(e) => setValues((c) => ({ ...c, check_type: e.target.value as ComplianceCheckFormValues['check_type'] }))}>
            {COMPLIANCE_CHECK_TYPES.map((item) => <option key={item.value} value={item.value}>{item.label}</option>)}
          </select>
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Status</label>
          <select className={selectClassName} value={values.status} onChange={(e) => setValues((c) => ({ ...c, status: e.target.value as ComplianceCheckFormValues['status'] }))}>
            {COMPLIANCE_STATUSES.map((item) => <option key={item.value} value={item.value}>{item.label}</option>)}
          </select>
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Rule ID</label>
          <Input value={values.rule_id} onChange={(e) => setValues((c) => ({ ...c, rule_id: e.target.value }))} />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Control ID</label>
          <Input value={values.control_id} onChange={(e) => setValues((c) => ({ ...c, control_id: e.target.value }))} />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Due date</label>
          <Input type="date" value={values.due_date} onChange={(e) => setValues((c) => ({ ...c, due_date: e.target.value }))} />
        </div>
        {!showAdvanced ? (
          <EntityPicker
            label="Owner"
            allowedTypes={['person']}
            value={ownerEntity}
            onChange={setOwnerEntity}
            allowClear
          />
        ) : (
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Owner ID</label>
            <Input value={values.owner_id} onChange={(e) => setValues((c) => ({ ...c, owner_id: e.target.value }))} />
          </div>
        )}
      </div>

      {!lockSubject ? (
        <button
          type="button"
          onClick={() => setShowAdvanced((current) => !current)}
          className="text-xs text-core-blue hover:underline"
        >
          {showAdvanced ? 'Use entity pickers' : 'Use manual IDs'}
        </button>
      ) : null}

      <div>
        <label className="mb-1 block text-sm font-medium text-gray-700">Result summary</label>
        <textarea className="block min-h-20 w-full rounded-md border border-app-borderStrong px-3 py-2 text-sm" value={values.result_summary} onChange={(e) => setValues((c) => ({ ...c, result_summary: e.target.value }))} />
      </div>
      {submitError ? <p className="text-sm text-status-danger">{submitError}</p> : null}
      <div className="flex gap-3">
        <Button type="submit" disabled={isSubmitting}>{isSubmitting ? 'Saving…' : mode === 'create' ? 'Create check' : 'Save changes'}</Button>
        <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>
      </div>
    </form>
  )
}
