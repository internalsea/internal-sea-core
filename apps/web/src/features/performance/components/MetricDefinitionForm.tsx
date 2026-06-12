import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { EntityPicker } from '@/features/entity-picker/components/EntityPicker'
import type { EntityPickerValue } from '@/features/entity-picker/types'
import {
  METRIC_DIRECTIONS,
  METRIC_FREQUENCIES,
  METRIC_STATUSES,
  METRIC_VALUE_TYPES,
  PERFORMANCE_SUBJECT_TYPES,
} from '@/features/performance/constants'
import type { MetricDefinitionFormValues } from '@/features/performance/types'
import { cleanMetricDefinitionPayload } from '@/features/performance/utils'

interface MetricDefinitionFormProps {
  initialValues?: Partial<MetricDefinitionFormValues>
  mode: 'create' | 'edit'
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (payload: ReturnType<typeof cleanMetricDefinitionPayload>) => void
  onCancel: () => void
}

const defaultValues: MetricDefinitionFormValues = {
  name: '',
  code: '',
  description: '',
  subject_type: 'data_product',
  value_type: 'number',
  direction: 'neutral',
  frequency: '',
  status: 'active',
  unit: '',
  target_value: '',
  warning_threshold: '',
  critical_threshold: '',
  owner_id: null,
}

export function MetricDefinitionForm({
  initialValues,
  mode,
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: MetricDefinitionFormProps) {
  const [values, setValues] = useState<MetricDefinitionFormValues>({
    ...defaultValues,
    ...initialValues,
  })
  const [nameError, setNameError] = useState<string | null>(null)
  const [owner, setOwner] = useState<EntityPickerValue | null>(
    values.owner_id ? { entity_type: 'person', entity_id: values.owner_id } : null,
  )

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    if (!values.name.trim()) {
      setNameError('Name is required')
      return
    }
    setNameError(null)
    onSubmit(
      cleanMetricDefinitionPayload({
        ...values,
        owner_id: owner?.entity_id ?? null,
      }),
    )
  }

  const selectClassName =
    'mt-1.5 block w-full rounded-md border border-app-borderStrong bg-app-surface px-3 py-2 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue'

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2">
        <Input
          label="Name"
          value={values.name}
          onChange={(event) => setValues((current) => ({ ...current, name: event.target.value }))}
          error={nameError ?? undefined}
          required
        />
        <Input
          label="Code"
          value={values.code}
          onChange={(event) => setValues((current) => ({ ...current, code: event.target.value }))}
        />
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700" htmlFor="metric-description">
            Description
          </label>
          <textarea
            id="metric-description"
            rows={3}
            className={selectClassName}
            value={values.description}
            onChange={(event) =>
              setValues((current) => ({ ...current, description: event.target.value }))
            }
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700" htmlFor="subject-type">
            Subject type
          </label>
          <select
            id="subject-type"
            className={selectClassName}
            value={values.subject_type}
            onChange={(event) =>
              setValues((current) => ({
                ...current,
                subject_type: event.target.value as MetricDefinitionFormValues['subject_type'],
              }))
            }
          >
            {PERFORMANCE_SUBJECT_TYPES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700" htmlFor="value-type">
            Value type
          </label>
          <select
            id="value-type"
            className={selectClassName}
            value={values.value_type}
            onChange={(event) =>
              setValues((current) => ({
                ...current,
                value_type: event.target.value as MetricDefinitionFormValues['value_type'],
              }))
            }
          >
            {METRIC_VALUE_TYPES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700" htmlFor="direction">
            Direction
          </label>
          <select
            id="direction"
            className={selectClassName}
            value={values.direction}
            onChange={(event) =>
              setValues((current) => ({
                ...current,
                direction: event.target.value as MetricDefinitionFormValues['direction'],
              }))
            }
          >
            {METRIC_DIRECTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700" htmlFor="frequency">
            Frequency
          </label>
          <select
            id="frequency"
            className={selectClassName}
            value={values.frequency}
            onChange={(event) =>
              setValues((current) => ({
                ...current,
                frequency: event.target.value as MetricDefinitionFormValues['frequency'],
              }))
            }
          >
            <option value="">Not set</option>
            {METRIC_FREQUENCIES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700" htmlFor="status">
            Status
          </label>
          <select
            id="status"
            className={selectClassName}
            value={values.status}
            onChange={(event) =>
              setValues((current) => ({
                ...current,
                status: event.target.value as MetricDefinitionFormValues['status'],
              }))
            }
          >
            {METRIC_STATUSES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <Input
          label="Unit"
          value={values.unit}
          onChange={(event) => setValues((current) => ({ ...current, unit: event.target.value }))}
        />
        <Input
          label="Target value"
          value={values.target_value}
          onChange={(event) =>
            setValues((current) => ({ ...current, target_value: event.target.value }))
          }
        />
        <Input
          label="Warning threshold"
          value={values.warning_threshold}
          onChange={(event) =>
            setValues((current) => ({ ...current, warning_threshold: event.target.value }))
          }
        />
        <Input
          label="Critical threshold"
          value={values.critical_threshold}
          onChange={(event) =>
            setValues((current) => ({ ...current, critical_threshold: event.target.value }))
          }
        />
        <div className="md:col-span-2">
          <EntityPicker
            label="Owner"
            allowedTypes={['person']}
            value={owner}
            onChange={setOwner}
            allowClear
          />
        </div>
      </div>

      {submitError ? <p className="text-sm text-red-700">{submitError}</p> : null}

      <div className="flex items-center gap-2">
        <Button type="submit" disabled={isSubmitting}>
          {mode === 'create' ? 'Create metric' : 'Save changes'}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel}>
          Cancel
        </Button>
      </div>
    </form>
  )
}
