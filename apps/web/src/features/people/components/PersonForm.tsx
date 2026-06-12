import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { EntityPicker } from '@/features/entity-picker/components/EntityPicker'
import type { EntityPickerValue } from '@/features/entity-picker/types'
import {
  SENIORITY_LEVELS,
  selectClassName,
} from '@/features/people/constants'
import type { PersonFormValues } from '@/features/people/types'
import { formValuesToPayload, validateEmail } from '@/features/people/utils'

interface PersonFormProps {
  initialValues?: Partial<PersonFormValues>
  mode: 'create' | 'edit'
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (values: ReturnType<typeof formValuesToPayload>) => void
  onCancel: () => void
}

function idToPickerValue(
  entityType: EntityPickerValue['entity_type'],
  entityId: string,
): EntityPickerValue | null {
  return entityId ? { entity_type: entityType, entity_id: entityId } : null
}

const defaultValues: PersonFormValues = {
  full_name: '',
  email: '',
  role_title: '',
  seniority_level: '',
  user_id: '',
  team_id: '',
  capability_id: '',
  availability_percent: '',
  location: '',
  is_active: true,
}

export function PersonForm({
  initialValues,
  mode,
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: PersonFormProps) {
  const [values, setValues] = useState<PersonFormValues>({
    ...defaultValues,
    ...initialValues,
  })
  const [team, setTeam] = useState<EntityPickerValue | null>(
    idToPickerValue('team', initialValues?.team_id ?? ''),
  )
  const [capability, setCapability] = useState<EntityPickerValue | null>(
    idToPickerValue('capability', initialValues?.capability_id ?? ''),
  )
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [nameError, setNameError] = useState<string | null>(null)
  const [emailError, setEmailError] = useState<string | null>(null)
  const [availabilityError, setAvailabilityError] = useState<string | null>(null)

  const updateField = <K extends keyof PersonFormValues>(field: K, value: PersonFormValues[K]) => {
    setValues((current) => ({ ...current, [field]: value }))
  }

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()

    const trimmedName = values.full_name.trim()
    if (!trimmedName) {
      setNameError('Full name is required')
      return
    }
    setNameError(null)

    const emailValidation = validateEmail(values.email)
    if (emailValidation) {
      setEmailError(emailValidation)
      return
    }
    setEmailError(null)

    if (values.availability_percent.trim() !== '') {
      const availability = Number.parseInt(values.availability_percent, 10)
      if (Number.isNaN(availability) || availability < 0 || availability > 100) {
        setAvailabilityError('Availability must be between 0 and 100')
        return
      }
    }
    setAvailabilityError(null)

    onSubmit(
      formValuesToPayload({
        ...values,
        full_name: trimmedName,
        team_id: team?.entity_id ?? '',
        capability_id: capability?.entity_id ?? '',
      }),
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2">
        <div className="md:col-span-2">
          <Input
            label="Full name"
            value={values.full_name}
            onChange={(event) => updateField('full_name', event.target.value)}
            error={nameError ?? undefined}
            required
          />
        </div>
        <Input
          label="Email"
          type="email"
          value={values.email}
          onChange={(event) => updateField('email', event.target.value)}
          error={emailError ?? undefined}
        />
        <Input
          label="Role title"
          value={values.role_title}
          onChange={(event) => updateField('role_title', event.target.value)}
        />
        <div className="space-y-1.5">
          <label htmlFor="seniority-level" className="block text-sm font-medium text-gray-700">
            Seniority level
          </label>
          <select
            id="seniority-level"
            className={selectClassName}
            value={values.seniority_level}
            onChange={(event) => updateField('seniority_level', event.target.value)}
          >
            <option value="">Not set</option>
            {SENIORITY_LEVELS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <Input
          label="Location"
          value={values.location}
          onChange={(event) => updateField('location', event.target.value)}
        />
        <Input
          label="Availability percent"
          type="number"
          min={0}
          max={100}
          value={values.availability_percent}
          onChange={(event) => updateField('availability_percent', event.target.value)}
          error={availabilityError ?? undefined}
          helpText="0–100"
        />
        <div className="space-y-1.5">
          <label htmlFor="is-active" className="block text-sm font-medium text-gray-700">
            Status
          </label>
          <select
            id="is-active"
            className={selectClassName}
            value={values.is_active ? 'true' : 'false'}
            onChange={(event) => updateField('is_active', event.target.value === 'true')}
          >
            <option value="true">Active</option>
            <option value="false">Inactive</option>
          </select>
        </div>
      </div>

      <div>
        <SectionHeader
          title="Organization"
          description="Primary team, capability and optional user account link."
        />
        <div className="grid gap-4 md:grid-cols-2">
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
          {showAdvanced ? (
            <Input
              label="User ID"
              value={values.user_id}
              onChange={(event) => updateField('user_id', event.target.value)}
              helpText="Optional user account UUID"
            />
          ) : null}
        </div>
        <button
          type="button"
          onClick={() => setShowAdvanced((current) => !current)}
          className="mt-2 text-xs text-core-blue hover:underline"
        >
          {showAdvanced ? 'Hide advanced fields' : 'Show advanced fields'}
        </button>
      </div>

      {submitError ? <p className="text-sm text-red-700">{submitError}</p> : null}

      <div className="flex items-center gap-2">
        <Button type="submit" disabled={isSubmitting}>
          {mode === 'create' ? 'Create Person' : 'Save Changes'}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
      </div>
    </form>
  )
}
