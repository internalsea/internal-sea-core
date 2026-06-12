import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { EntityPicker } from '@/features/entity-picker/components/EntityPicker'
import type { EntityPickerValue } from '@/features/entity-picker/types'
import {
  selectClassName,
  WORK_ITEM_PRIORITIES,
  WORK_ITEM_STATUSES,
  WORK_ITEM_TYPES,
} from '@/features/work-items/constants'
import type { WorkItemFormValues } from '@/features/work-items/types'
import { formValuesToPayload } from '@/features/work-items/utils'

interface WorkItemFormProps {
  initialValues?: Partial<WorkItemFormValues>
  mode: 'create' | 'edit'
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (values: ReturnType<typeof formValuesToPayload>) => void
  onCancel: () => void
}

const defaultValues: WorkItemFormValues = {
  title: '',
  description: '',
  type: 'task',
  status: 'backlog',
  priority: 'medium',
  due_date: '',
  estimate_points: '',
  assignee_id: '',
  reporter_id: '',
  data_product_id: '',
  project_id: '',
  capability_id: '',
  team_id: '',
}

function idToPickerValue(
  entityType: EntityPickerValue['entity_type'],
  entityId: string,
): EntityPickerValue | null {
  return entityId ? { entity_type: entityType, entity_id: entityId } : null
}

export function WorkItemForm({
  initialValues,
  mode,
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: WorkItemFormProps) {
  const [values, setValues] = useState<WorkItemFormValues>({
    ...defaultValues,
    ...initialValues,
  })
  const [assignee, setAssignee] = useState<EntityPickerValue | null>(
    idToPickerValue('person', initialValues?.assignee_id ?? ''),
  )
  const [reporter, setReporter] = useState<EntityPickerValue | null>(
    idToPickerValue('person', initialValues?.reporter_id ?? ''),
  )
  const [dataProduct, setDataProduct] = useState<EntityPickerValue | null>(
    idToPickerValue('data_product', initialValues?.data_product_id ?? ''),
  )
  const [project, setProject] = useState<EntityPickerValue | null>(
    idToPickerValue('project', initialValues?.project_id ?? ''),
  )
  const [capability, setCapability] = useState<EntityPickerValue | null>(
    idToPickerValue('capability', initialValues?.capability_id ?? ''),
  )
  const [team, setTeam] = useState<EntityPickerValue | null>(
    idToPickerValue('team', initialValues?.team_id ?? ''),
  )
  const [titleError, setTitleError] = useState<string | null>(null)
  const [estimateError, setEstimateError] = useState<string | null>(null)

  const updateField = <K extends keyof WorkItemFormValues>(field: K, value: WorkItemFormValues[K]) => {
    setValues((current) => ({ ...current, [field]: value }))
  }

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()

    const trimmedTitle = values.title.trim()
    if (!trimmedTitle) {
      setTitleError('Title is required')
      return
    }
    setTitleError(null)

    if (values.estimate_points.trim() !== '') {
      const estimate = Number.parseInt(values.estimate_points, 10)
      if (Number.isNaN(estimate) || estimate < 0) {
        setEstimateError('Estimate must be zero or greater')
        return
      }
    }
    setEstimateError(null)

    onSubmit(
      formValuesToPayload({
        ...values,
        title: trimmedTitle,
        assignee_id: assignee?.entity_id ?? '',
        reporter_id: reporter?.entity_id ?? '',
        data_product_id: dataProduct?.entity_id ?? '',
        project_id: project?.entity_id ?? '',
        capability_id: capability?.entity_id ?? '',
        team_id: team?.entity_id ?? '',
      }),
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2">
        <div className="md:col-span-2">
          <Input
            label="Title"
            value={values.title}
            onChange={(event) => updateField('title', event.target.value)}
            error={titleError ?? undefined}
            required
          />
        </div>
        <div className="md:col-span-2">
          <label htmlFor="work-item-description" className="block text-sm font-medium text-gray-700">
            Description
          </label>
          <textarea
            id="work-item-description"
            rows={4}
            className="mt-1.5 block w-full rounded-md border border-app-borderStrong bg-app-surface px-3 py-2 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
            value={values.description}
            onChange={(event) => updateField('description', event.target.value)}
          />
        </div>
        <div className="space-y-1.5">
          <label htmlFor="work-item-type" className="block text-sm font-medium text-gray-700">
            Type
          </label>
          <select
            id="work-item-type"
            className={selectClassName}
            value={values.type}
            onChange={(event) =>
              updateField('type', event.target.value as WorkItemFormValues['type'])
            }
          >
            {WORK_ITEM_TYPES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div className="space-y-1.5">
          <label htmlFor="work-item-status" className="block text-sm font-medium text-gray-700">
            Status
          </label>
          <select
            id="work-item-status"
            className={selectClassName}
            value={values.status}
            onChange={(event) =>
              updateField('status', event.target.value as WorkItemFormValues['status'])
            }
          >
            {WORK_ITEM_STATUSES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div className="space-y-1.5">
          <label htmlFor="work-item-priority" className="block text-sm font-medium text-gray-700">
            Priority
          </label>
          <select
            id="work-item-priority"
            className={selectClassName}
            value={values.priority}
            onChange={(event) =>
              updateField('priority', event.target.value as WorkItemFormValues['priority'])
            }
          >
            {WORK_ITEM_PRIORITIES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <Input
          label="Due date"
          type="date"
          value={values.due_date}
          onChange={(event) => updateField('due_date', event.target.value)}
        />
        <Input
          label="Estimate points"
          type="number"
          min={0}
          value={values.estimate_points}
          onChange={(event) => updateField('estimate_points', event.target.value)}
          error={estimateError ?? undefined}
          helpText="Optional story points or effort estimate"
        />
      </div>

      <div>
        <SectionHeader
          title="Advanced links"
          description="Optional references to people, teams, capabilities and data products."
        />
        <div className="grid gap-4 md:grid-cols-2">
          <EntityPicker
            label="Assignee"
            allowedTypes={['person']}
            value={assignee}
            onChange={setAssignee}
            allowClear
          />
          <EntityPicker
            label="Reporter"
            allowedTypes={['person']}
            value={reporter}
            onChange={setReporter}
            allowClear
          />
          <EntityPicker
            label="Data product"
            allowedTypes={['data_product']}
            value={dataProduct}
            onChange={setDataProduct}
            allowClear
          />
          <EntityPicker
            label="Project"
            allowedTypes={['project', 'internal_project']}
            value={project}
            onChange={setProject}
            allowClear
          />
          <EntityPicker
            label="Capability"
            allowedTypes={['capability']}
            value={capability}
            onChange={setCapability}
            allowClear
          />
          <EntityPicker
            label="Team"
            allowedTypes={['team']}
            value={team}
            onChange={setTeam}
            allowClear
          />
        </div>
      </div>

      {submitError ? <p className="text-sm text-red-700">{submitError}</p> : null}

      <div className="flex items-center gap-2">
        <Button type="submit" disabled={isSubmitting}>
          {mode === 'create' ? 'Create Work Item' : 'Save Changes'}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
      </div>
    </form>
  )
}
