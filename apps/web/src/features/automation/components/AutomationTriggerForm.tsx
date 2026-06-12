import { useEffect, useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { EntityPicker } from '@/features/entity-picker/components/EntityPicker'
import type { EntityPickerType, EntityPickerValue } from '@/features/entity-picker/types'
import {
  ACTION_CONFIG_EXAMPLES,
  AUTOMATION_ACTION_TYPES,
  AUTOMATION_STATUSES,
  AUTOMATION_TRIGGER_TYPES,
  MVP_ACTION_TYPES,
  selectClassName,
} from '@/features/automation/constants'
import { useAutomationSchedules } from '@/features/automation/hooks'
import type { AutomationActionType, AutomationTriggerFormValues } from '@/features/automation/types'
import type { AutomationTriggerCreateInput, AutomationTriggerUpdateInput } from '@/features/automation/types'
import {
  cleanTriggerCreatePayload,
  cleanTriggerUpdatePayload,
  getApiErrorMessage,
  isActionImplementedInMvp,
} from '@/features/automation/utils'

const TARGET_PICKER_TYPES: EntityPickerType[] = [
  'data_product',
  'work_item',
  'project',
  'internal_project',
  'compliance_check',
  'team',
  'capability',
]

interface AutomationTriggerFormProps {
  initialValues?: Partial<AutomationTriggerFormValues>
  initialTarget?: EntityPickerValue | null
  mode: 'create' | 'edit'
  lockTarget?: EntityPickerValue
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (values: AutomationTriggerCreateInput | AutomationTriggerUpdateInput) => void
  onCancel: () => void
}

const defaultValues: AutomationTriggerFormValues = {
  name: '',
  description: '',
  status: 'draft',
  trigger_type: 'schedule',
  action_type: 'create_work_item',
  schedule_id: '',
  conditionsJson: '',
  actionConfigJson: ACTION_CONFIG_EXAMPLES.create_work_item ?? '',
}

export function AutomationTriggerForm({
  initialValues,
  initialTarget,
  mode,
  lockTarget,
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: AutomationTriggerFormProps) {
  const [values, setValues] = useState<AutomationTriggerFormValues>({
    ...defaultValues,
    ...initialValues,
  })
  const [target, setTarget] = useState<EntityPickerValue | null>(lockTarget ?? initialTarget ?? null)
  const [nameError, setNameError] = useState<string | null>(null)
  const [jsonError, setJsonError] = useState<string | null>(null)
  const { data: schedulesData } = useAutomationSchedules({ page: 1, page_size: 100 })

  useEffect(() => {
    const example = ACTION_CONFIG_EXAMPLES[values.action_type]
    if (example && !values.actionConfigJson.trim()) {
      setValues((prev) => ({ ...prev, actionConfigJson: example }))
    }
  }, [values.action_type, values.actionConfigJson])

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    if (!values.name.trim()) {
      setNameError('Name is required')
      return
    }
    setNameError(null)
    try {
      if (values.conditionsJson.trim()) {
        JSON.parse(values.conditionsJson)
      }
      if (values.actionConfigJson.trim()) {
        JSON.parse(values.actionConfigJson)
      }
      setJsonError(null)
      onSubmit(
        mode === 'create'
          ? cleanTriggerCreatePayload(values, lockTarget ?? target)
          : cleanTriggerUpdatePayload(values, lockTarget ?? target),
      )
    } catch (error) {
      setJsonError(getApiErrorMessage(error))
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <Input
        label="Name"
        value={values.name}
        onChange={(event) => setValues((prev) => ({ ...prev, name: event.target.value }))}
        error={nameError ?? undefined}
        required
      />

      <div>
        <label className="mb-1 block text-sm font-medium text-gray-700">Description</label>
        <textarea
          value={values.description}
          onChange={(event) => setValues((prev) => ({ ...prev, description: event.target.value }))}
          rows={3}
          className="w-full rounded-md border border-app-border bg-white px-3 py-2 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
        />
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Status</label>
          <select
            value={values.status}
            onChange={(event) =>
              setValues((prev) => ({
                ...prev,
                status: event.target.value as AutomationTriggerFormValues['status'],
              }))
            }
            className={selectClassName}
          >
            {AUTOMATION_STATUSES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Trigger type</label>
          <select
            value={values.trigger_type}
            onChange={(event) =>
              setValues((prev) => ({
                ...prev,
                trigger_type: event.target.value as AutomationTriggerFormValues['trigger_type'],
              }))
            }
            className={selectClassName}
          >
            {AUTOMATION_TRIGGER_TYPES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div>
        <label className="mb-1 block text-sm font-medium text-gray-700">Action type</label>
        <select
          value={values.action_type}
          onChange={(event) =>
            setValues((prev) => ({
              ...prev,
              action_type: event.target.value as AutomationActionType,
              actionConfigJson: ACTION_CONFIG_EXAMPLES[event.target.value as AutomationActionType] ?? '',
            }))
          }
          className={selectClassName}
        >
          {AUTOMATION_ACTION_TYPES.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
              {!isActionImplementedInMvp(option.value) ? ' (not in MVP)' : ''}
            </option>
          ))}
        </select>
        {!isActionImplementedInMvp(values.action_type) ? (
          <p className="mt-1 text-xs text-status-warning">
            This action type cannot be executed in MVP. Simulation will show planned behavior only.
          </p>
        ) : null}
      </div>

      {values.trigger_type === 'schedule' ? (
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Schedule</label>
          <select
            value={values.schedule_id}
            onChange={(event) => setValues((prev) => ({ ...prev, schedule_id: event.target.value }))}
            className={selectClassName}
            required
          >
            <option value="">Select schedule…</option>
            {(schedulesData?.items ?? []).map((schedule) => (
              <option key={schedule.id} value={schedule.id}>
                {schedule.name}
              </option>
            ))}
          </select>
        </div>
      ) : null}

      <EntityPicker
        value={lockTarget ?? target}
        onChange={lockTarget ? () => undefined : setTarget}
        allowedTypes={TARGET_PICKER_TYPES}
        label="Target object"
        disabled={Boolean(lockTarget)}
      />

      <div>
        <label className="mb-1 block text-sm font-medium text-gray-700">Conditions (JSON)</label>
        <textarea
          value={values.conditionsJson}
          onChange={(event) => setValues((prev) => ({ ...prev, conditionsJson: event.target.value }))}
          rows={4}
          placeholder="{}"
          className="w-full rounded-md border border-app-border bg-white px-3 py-2 font-mono text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
        />
      </div>

      <div>
        <label className="mb-1 block text-sm font-medium text-gray-700">Action config (JSON)</label>
        <textarea
          value={values.actionConfigJson}
          onChange={(event) =>
            setValues((prev) => ({ ...prev, actionConfigJson: event.target.value }))
          }
          rows={8}
          className="w-full rounded-md border border-app-border bg-white px-3 py-2 font-mono text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
        />
        {MVP_ACTION_TYPES.includes(values.action_type) ? (
          <p className="mt-1 text-xs text-gray-500">
            Safe MVP actions: create work item, add comment, create activity event.
          </p>
        ) : null}
      </div>

      {jsonError ? <p className="text-sm text-status-danger">{jsonError}</p> : null}
      {submitError ? <p className="text-sm text-status-danger">{submitError}</p> : null}

      <div className="flex gap-3">
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Saving…' : mode === 'create' ? 'Create Trigger' : 'Save Changes'}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
      </div>
    </form>
  )
}
