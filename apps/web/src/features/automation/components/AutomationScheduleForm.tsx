import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import {
  SCHEDULE_FREQUENCIES,
  selectClassName,
} from '@/features/automation/constants'
import type { AutomationScheduleFormValues } from '@/features/automation/types'
import {
  cleanScheduleCreatePayload,
  cleanScheduleUpdatePayload,
} from '@/features/automation/utils'
import type { AutomationScheduleCreateInput, AutomationScheduleUpdateInput } from '@/features/automation/types'

interface AutomationScheduleFormProps {
  initialValues?: Partial<AutomationScheduleFormValues>
  mode: 'create' | 'edit'
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (values: AutomationScheduleCreateInput | AutomationScheduleUpdateInput) => void
  onCancel: () => void
}

const defaultValues: AutomationScheduleFormValues = {
  name: '',
  description: '',
  frequency: 'monthly',
  timezone: 'UTC',
  start_at: '',
  end_at: '',
  next_run_at: '',
  cron_expression: '',
  is_active: true,
}

export function AutomationScheduleForm({
  initialValues,
  mode,
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: AutomationScheduleFormProps) {
  const [values, setValues] = useState<AutomationScheduleFormValues>({
    ...defaultValues,
    ...initialValues,
  })
  const [nameError, setNameError] = useState<string | null>(null)

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    if (!values.name.trim()) {
      setNameError('Name is required')
      return
    }
    setNameError(null)
    onSubmit(
      mode === 'create' ? cleanScheduleCreatePayload(values) : cleanScheduleUpdatePayload(values),
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <p className="text-sm text-gray-500">
        Schedules are stored now. Automatic background execution will be added later.
      </p>

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
          <label className="mb-1 block text-sm font-medium text-gray-700">Frequency</label>
          <select
            value={values.frequency}
            onChange={(event) =>
              setValues((prev) => ({
                ...prev,
                frequency: event.target.value as AutomationScheduleFormValues['frequency'],
              }))
            }
            className={selectClassName}
          >
            {SCHEDULE_FREQUENCIES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <Input
          label="Timezone"
          value={values.timezone}
          onChange={(event) => setValues((prev) => ({ ...prev, timezone: event.target.value }))}
        />
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <Input
          label="Start at"
          type="datetime-local"
          value={values.start_at}
          onChange={(event) => setValues((prev) => ({ ...prev, start_at: event.target.value }))}
        />
        <Input
          label="End at"
          type="datetime-local"
          value={values.end_at}
          onChange={(event) => setValues((prev) => ({ ...prev, end_at: event.target.value }))}
        />
        <Input
          label="Next run at"
          type="datetime-local"
          value={values.next_run_at}
          onChange={(event) => setValues((prev) => ({ ...prev, next_run_at: event.target.value }))}
        />
      </div>

      {values.frequency === 'custom' ? (
        <Input
          label="Cron expression"
          value={values.cron_expression}
          onChange={(event) =>
            setValues((prev) => ({ ...prev, cron_expression: event.target.value }))
          }
          helpText="Custom cron syntax. Background execution is not active yet."
        />
      ) : null}

      <label className="flex items-center gap-2 text-sm text-gray-700">
        <input
          type="checkbox"
          checked={values.is_active}
          onChange={(event) => setValues((prev) => ({ ...prev, is_active: event.target.checked }))}
          className="rounded border-app-borderStrong text-core-blue focus:ring-core-blue"
        />
        Active
      </label>

      {submitError ? <p className="text-sm text-status-danger">{submitError}</p> : null}

      <div className="flex gap-3">
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Saving…' : mode === 'create' ? 'Create Schedule' : 'Save Changes'}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
      </div>
    </form>
  )
}
