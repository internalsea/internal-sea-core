import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { EntityPicker } from '@/features/entity-picker/components/EntityPicker'
import type { EntityPickerValue } from '@/features/entity-picker/types'
import {
  PROJECT_HEALTH_STATUSES,
  PROJECT_PRIORITIES,
  PROJECT_STATUSES,
  PROJECT_TYPES,
  selectClassName,
} from '@/features/projects/constants'
import type { ProjectFormValues, ProjectVariant } from '@/features/projects/types'
import { formValuesToPayload } from '@/features/projects/utils'
import type { ProjectStatus, ProjectType } from '@/types/enums'

interface ProjectFormProps {
  initialValues?: Partial<ProjectFormValues>
  mode: 'create' | 'edit'
  variant?: ProjectVariant
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (values: ReturnType<typeof formValuesToPayload>) => void
  onCancel: () => void
}

const defaultValues: ProjectFormValues = {
  name: '',
  description: '',
  project_type: 'client_project',
  status: 'idea',
  health_status: '',
  priority: '',
  client_name: '',
  account_name: '',
  start_date: '',
  target_end_date: '',
  actual_end_date: '',
  budget_amount: '',
  budget_currency: 'EUR',
  owner_id: '',
  team_id: '',
  capability_id: '',
  delivery_notes: '',
}

function idToPickerValue(
  entityType: EntityPickerValue['entity_type'],
  entityId: string,
): EntityPickerValue | null {
  return entityId ? { entity_type: entityType, entity_id: entityId } : null
}

export function ProjectForm({
  initialValues,
  mode,
  variant = 'projects',
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: ProjectFormProps) {
  const isInternal = variant === 'internal-projects'
  const [values, setValues] = useState<ProjectFormValues>({
    ...defaultValues,
    ...(isInternal ? { project_type: 'internal_project' as ProjectType } : {}),
    ...initialValues,
  })
  const [owner, setOwner] = useState<EntityPickerValue | null>(
    idToPickerValue('person', initialValues?.owner_id ?? ''),
  )
  const [team, setTeam] = useState<EntityPickerValue | null>(
    idToPickerValue('team', initialValues?.team_id ?? ''),
  )
  const [capability, setCapability] = useState<EntityPickerValue | null>(
    idToPickerValue('capability', initialValues?.capability_id ?? ''),
  )
  const [nameError, setNameError] = useState<string | null>(null)
  const [budgetError, setBudgetError] = useState<string | null>(null)
  const [dateError, setDateError] = useState<string | null>(null)

  const updateField = <K extends keyof ProjectFormValues>(field: K, value: ProjectFormValues[K]) => {
    setValues((current) => ({ ...current, [field]: value }))
  }

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()

    const trimmedName = values.name.trim()
    if (!trimmedName) {
      setNameError('Name is required')
      return
    }
    setNameError(null)

    if (values.budget_amount.trim() !== '') {
      const budget = Number.parseFloat(values.budget_amount)
      if (Number.isNaN(budget) || budget < 0) {
        setBudgetError('Budget must be zero or greater')
        return
      }
    }
    setBudgetError(null)

    if (values.start_date && values.target_end_date && values.target_end_date < values.start_date) {
      setDateError('Target end date cannot be before start date')
      return
    }
    if (values.start_date && values.actual_end_date && values.actual_end_date < values.start_date) {
      setDateError('Actual end date cannot be before start date')
      return
    }
    setDateError(null)

    onSubmit(
      formValuesToPayload(
        {
          ...values,
          name: trimmedName,
          project_type: isInternal ? 'internal_project' : values.project_type,
          owner_id: owner?.entity_id ?? '',
          team_id: team?.entity_id ?? '',
          capability_id: capability?.entity_id ?? '',
        },
        variant,
      ),
    )
  }

  const submitLabel =
    mode === 'create'
      ? isInternal
        ? 'Create Internal Project'
        : 'Create Project'
      : 'Save Changes'

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2">
        <div className="md:col-span-2">
          <Input
            label="Name"
            value={values.name}
            onChange={(event) => updateField('name', event.target.value)}
            error={nameError ?? undefined}
            required
          />
        </div>
        <div className="md:col-span-2">
          <label htmlFor="project-description" className="block text-sm font-medium text-gray-700">
            Description
          </label>
          <textarea
            id="project-description"
            rows={4}
            className="mt-1.5 block w-full rounded-md border border-app-borderStrong bg-app-surface px-3 py-2 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
            value={values.description}
            onChange={(event) => updateField('description', event.target.value)}
          />
        </div>
        {isInternal ? (
          <div className="space-y-1.5">
            <label htmlFor="project-type-readonly" className="block text-sm font-medium text-gray-700">
              Type
            </label>
            <input
              id="project-type-readonly"
              type="text"
              readOnly
              disabled
              className={selectClassName}
              value="Internal Project"
            />
          </div>
        ) : (
          <div className="space-y-1.5">
            <label htmlFor="project-type" className="block text-sm font-medium text-gray-700">
              Type
            </label>
            <select
              id="project-type"
              className={selectClassName}
              value={values.project_type}
              onChange={(event) =>
                updateField('project_type', event.target.value as ProjectType)
              }
            >
              {PROJECT_TYPES.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        )}
        <div className="space-y-1.5">
          <label htmlFor="project-status" className="block text-sm font-medium text-gray-700">
            Status
          </label>
          <select
            id="project-status"
            className={selectClassName}
            value={values.status}
            onChange={(event) =>
              updateField('status', event.target.value as ProjectStatus)
            }
          >
            {PROJECT_STATUSES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div className="space-y-1.5">
          <label htmlFor="project-health" className="block text-sm font-medium text-gray-700">
            Health status
          </label>
          <select
            id="project-health"
            className={selectClassName}
            value={values.health_status}
            onChange={(event) => updateField('health_status', event.target.value)}
          >
            <option value="">Not set</option>
            {PROJECT_HEALTH_STATUSES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div className="space-y-1.5">
          <label htmlFor="project-priority" className="block text-sm font-medium text-gray-700">
            Priority
          </label>
          <select
            id="project-priority"
            className={selectClassName}
            value={values.priority}
            onChange={(event) => updateField('priority', event.target.value)}
          >
            <option value="">Not set</option>
            {PROJECT_PRIORITIES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {!isInternal ? (
        <div>
          <SectionHeader
            title="Commercial / client"
            description="Client and account details for external delivery work."
          />
          <div className="grid gap-4 md:grid-cols-2">
            <Input
              label="Client name"
              value={values.client_name}
              onChange={(event) => updateField('client_name', event.target.value)}
            />
            <Input
              label="Account name"
              value={values.account_name}
              onChange={(event) => updateField('account_name', event.target.value)}
            />
          </div>
        </div>
      ) : null}

      <div>
        <SectionHeader title="Timeline" description="Planned and actual delivery dates." />
        <div className="grid gap-4 md:grid-cols-3">
          <Input
            label="Start date"
            type="date"
            value={values.start_date}
            onChange={(event) => updateField('start_date', event.target.value)}
          />
          <Input
            label="Target end date"
            type="date"
            value={values.target_end_date}
            onChange={(event) => updateField('target_end_date', event.target.value)}
          />
          <Input
            label="Actual end date"
            type="date"
            value={values.actual_end_date}
            onChange={(event) => updateField('actual_end_date', event.target.value)}
          />
        </div>
        {dateError ? <p className="mt-2 text-sm text-red-700">{dateError}</p> : null}
      </div>

      <div>
        <SectionHeader title="Budget" description="Optional budget tracking." />
        <div className="grid gap-4 md:grid-cols-2">
          <Input
            label="Budget amount"
            type="number"
            min={0}
            step="0.01"
            value={values.budget_amount}
            onChange={(event) => updateField('budget_amount', event.target.value)}
            error={budgetError ?? undefined}
          />
          <Input
            label="Budget currency"
            value={values.budget_currency}
            onChange={(event) => updateField('budget_currency', event.target.value)}
            helpText="ISO currency code, e.g. EUR"
          />
        </div>
      </div>

      <div>
        <SectionHeader
          title="Advanced links"
          description="Optional references to people, teams and capabilities."
        />
        <div className="grid gap-4 md:grid-cols-2">
          <EntityPicker
            label="Owner"
            allowedTypes={['person']}
            value={owner}
            onChange={setOwner}
            allowClear
          />
          <EntityPicker
            label="Team"
            allowedTypes={['team']}
            value={team}
            onChange={setTeam}
            allowClear
          />
          <EntityPicker
            label="Capability"
            allowedTypes={['capability']}
            value={capability}
            onChange={setCapability}
            allowClear
          />
        </div>
      </div>

      <div>
        <SectionHeader title="Delivery notes" description="Additional delivery context." />
        <textarea
          id="project-delivery-notes"
          rows={4}
          className="block w-full rounded-md border border-app-borderStrong bg-app-surface px-3 py-2 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
          value={values.delivery_notes}
          onChange={(event) => updateField('delivery_notes', event.target.value)}
        />
      </div>

      {submitError ? <p className="text-sm text-red-700">{submitError}</p> : null}

      <div className="flex items-center gap-2">
        <Button type="submit" disabled={isSubmitting}>
          {submitLabel}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
      </div>
    </form>
  )
}
