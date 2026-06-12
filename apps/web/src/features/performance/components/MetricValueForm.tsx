import { useEffect, useMemo, useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { EntityPicker } from '@/features/entity-picker/components/EntityPicker'
import type { EntityPickerType, EntityPickerValue } from '@/features/entity-picker/types'
import {
  METRIC_VALUE_STATUSES,
  PERFORMANCE_SUBJECT_PICKER_TYPES,
} from '@/features/performance/constants'
import { useMetricDefinitions } from '@/features/performance/hooks'
import type { MetricValueFormValues, PerformanceSubjectType } from '@/features/performance/types'
import { cleanMetricValuePayload } from '@/features/performance/utils'

interface MetricValueFormProps {
  initialValues?: Partial<MetricValueFormValues>
  mode: 'create' | 'edit'
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (payload: ReturnType<typeof cleanMetricValuePayload>) => void
  onCancel: () => void
}

const defaultValues: MetricValueFormValues = {
  metric_definition_id: '',
  subject_type: 'data_product',
  subject_id: '',
  period_start: '',
  period_end: '',
  value_numeric: '',
  value_text: '',
  value_bool: '',
  status: 'submitted',
  source: '',
  comment: '',
}

function subjectTypeToPickerType(subjectType: PerformanceSubjectType): EntityPickerType {
  return subjectType
}

export function MetricValueForm({
  initialValues,
  mode,
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: MetricValueFormProps) {
  const [values, setValues] = useState<MetricValueFormValues>({
    ...defaultValues,
    ...initialValues,
  })
  const [valueError, setValueError] = useState<string | null>(null)
  const [periodError, setPeriodError] = useState<string | null>(null)
  const [subject, setSubject] = useState<EntityPickerValue | null>(
    values.subject_id
      ? { entity_type: subjectTypeToPickerType(values.subject_type), entity_id: values.subject_id }
      : null,
  )

  const { data: definitionsData } = useMetricDefinitions({ page: 1, page_size: 100, status: 'active' })
  const definitions = useMemo(() => definitionsData?.items ?? [], [definitionsData?.items])

  const selectedDefinition = useMemo(
    () => definitions.find((item) => item.id === values.metric_definition_id),
    [definitions, values.metric_definition_id],
  )

  const subjectAllowedTypes = useMemo<EntityPickerType[]>(() => {
    if (selectedDefinition) {
      return [subjectTypeToPickerType(selectedDefinition.subject_type)]
    }
    return PERFORMANCE_SUBJECT_PICKER_TYPES
  }, [selectedDefinition])

  useEffect(() => {
    if (selectedDefinition && subject && subject.entity_type !== selectedDefinition.subject_type) {
      setSubject(null)
      setValues((current) => ({ ...current, subject_id: '', subject_type: selectedDefinition.subject_type }))
    }
  }, [selectedDefinition, subject])

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    setValueError(null)
    setPeriodError(null)

    if (!values.metric_definition_id) {
      setValueError('Metric definition is required')
      return
    }
    if (!subject?.entity_id) {
      setValueError('Subject is required')
      return
    }
    if (!values.value_numeric.trim() && !values.value_text.trim() && !values.value_bool) {
      setValueError('At least one value field is required')
      return
    }
    if (values.period_start && values.period_end && values.period_end < values.period_start) {
      setPeriodError('Period end must not be before period start')
      return
    }

    onSubmit(
      cleanMetricValuePayload({
        ...values,
        subject_type: (subject.entity_type as PerformanceSubjectType) ?? values.subject_type,
        subject_id: subject.entity_id,
      }),
    )
  }

  const selectClassName =
    'mt-1.5 block w-full rounded-md border border-app-borderStrong bg-app-surface px-3 py-2 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue'

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2">
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700" htmlFor="metric-definition">
            Metric definition
          </label>
          <select
            id="metric-definition"
            className={selectClassName}
            value={values.metric_definition_id}
            onChange={(event) =>
              setValues((current) => ({ ...current, metric_definition_id: event.target.value }))
            }
            required
          >
            <option value="">Select metric</option>
            {definitions.map((definition) => (
              <option key={definition.id} value={definition.id}>
                {definition.name} ({definition.code ?? definition.subject_type})
              </option>
            ))}
          </select>
        </div>
        <div className="md:col-span-2">
          <EntityPicker
            label="Subject"
            allowedTypes={subjectAllowedTypes}
            value={subject}
            onChange={setSubject}
            helperText={
              selectedDefinition
                ? `Subject type must match metric definition subject type (${selectedDefinition.subject_type}).`
                : 'Select a metric definition first to restrict subject type.'
            }
            required
          />
        </div>
        <Input
          label="Period start"
          type="date"
          value={values.period_start}
          onChange={(event) =>
            setValues((current) => ({ ...current, period_start: event.target.value }))
          }
        />
        <Input
          label="Period end"
          type="date"
          value={values.period_end}
          onChange={(event) =>
            setValues((current) => ({ ...current, period_end: event.target.value }))
          }
          error={periodError ?? undefined}
        />
        <Input
          label="Numeric value"
          value={values.value_numeric}
          onChange={(event) =>
            setValues((current) => ({ ...current, value_numeric: event.target.value }))
          }
        />
        <Input
          label="Text value"
          value={values.value_text}
          onChange={(event) =>
            setValues((current) => ({ ...current, value_text: event.target.value }))
          }
        />
        <div>
          <label className="block text-sm font-medium text-gray-700" htmlFor="value-bool">
            Boolean value
          </label>
          <select
            id="value-bool"
            className={selectClassName}
            value={values.value_bool}
            onChange={(event) =>
              setValues((current) => ({ ...current, value_bool: event.target.value }))
            }
          >
            <option value="">Not set</option>
            <option value="true">True</option>
            <option value="false">False</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700" htmlFor="value-status">
            Status
          </label>
          <select
            id="value-status"
            className={selectClassName}
            value={values.status}
            onChange={(event) =>
              setValues((current) => ({
                ...current,
                status: event.target.value as MetricValueFormValues['status'],
              }))
            }
          >
            {METRIC_VALUE_STATUSES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <Input
          label="Source"
          value={values.source}
          onChange={(event) => setValues((current) => ({ ...current, source: event.target.value }))}
        />
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700" htmlFor="value-comment">
            Comment
          </label>
          <textarea
            id="value-comment"
            rows={3}
            className={selectClassName}
            value={values.comment}
            onChange={(event) =>
              setValues((current) => ({ ...current, comment: event.target.value }))
            }
          />
        </div>
      </div>

      {valueError ? <p className="text-sm text-red-700">{valueError}</p> : null}
      {submitError ? <p className="text-sm text-red-700">{submitError}</p> : null}

      <div className="flex items-center gap-2">
        <Button type="submit" disabled={isSubmitting}>
          {mode === 'create' ? 'Create value' : 'Save changes'}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel}>
          Cancel
        </Button>
      </div>
    </form>
  )
}
