import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { StatusBadge } from '@/components/ui/StatusBadge'
import { EntityPicker } from '@/features/entity-picker/components/EntityPicker'
import type { EntityPickerValue } from '@/features/entity-picker/types'
import type { DataProductCreateInput } from '@/features/data-products/types'

interface DataProductFormValues {
  name: string
  description: string
  type: DataProductCreateInput['type']
  status: DataProductCreateInput['status']
  quality_status: DataProductCreateInput['quality_status']
  business_domain_id: string
  refresh_frequency: string
  source_systems: string
  consumers: string
  documentation_url: string
}

interface DataProductFormProps {
  initialValues?: Partial<DataProductFormValues> & {
    business_owner_id?: string
    technical_owner_id?: string
    capability_id?: string
    team_id?: string
  }
  mode: 'create' | 'edit'
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (payload: DataProductCreateInput) => void
  onCancel: () => void
}

const defaultValues: DataProductFormValues = {
  name: '',
  description: '',
  type: 'dashboard',
  status: 'draft',
  quality_status: 'unknown',
  business_domain_id: '',
  refresh_frequency: '',
  source_systems: '',
  consumers: '',
  documentation_url: '',
}

function idToPickerValue(
  entityType: EntityPickerValue['entity_type'],
  entityId: string | null | undefined,
): EntityPickerValue | null {
  return entityId ? { entity_type: entityType, entity_id: entityId } : null
}

function emptyToNull(value: string): string | null {
  const trimmed = value.trim()
  return trimmed || null
}

export function DataProductForm({
  initialValues,
  mode,
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: DataProductFormProps) {
  const [values, setValues] = useState<DataProductFormValues>({
    ...defaultValues,
    ...initialValues,
  })
  const [businessOwner, setBusinessOwner] = useState<EntityPickerValue | null>(
    idToPickerValue('person', initialValues?.business_owner_id),
  )
  const [technicalOwner, setTechnicalOwner] = useState<EntityPickerValue | null>(
    idToPickerValue('person', initialValues?.technical_owner_id),
  )
  const [capability, setCapability] = useState<EntityPickerValue | null>(
    idToPickerValue('capability', initialValues?.capability_id),
  )
  const [team, setTeam] = useState<EntityPickerValue | null>(
    idToPickerValue('team', initialValues?.team_id),
  )
  const [nameError, setNameError] = useState<string | null>(null)

  const updateField = <K extends keyof DataProductFormValues>(field: K, value: DataProductFormValues[K]) => {
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

    onSubmit({
      name: trimmedName,
      description: emptyToNull(values.description),
      type: values.type,
      status: values.status,
      quality_status: values.quality_status,
      business_domain_id: emptyToNull(values.business_domain_id),
      business_owner_id: businessOwner?.entity_id ?? null,
      technical_owner_id: technicalOwner?.entity_id ?? null,
      capability_id: capability?.entity_id ?? null,
      team_id: team?.entity_id ?? null,
      refresh_frequency: emptyToNull(values.refresh_frequency),
      source_systems: emptyToNull(values.source_systems),
      consumers: emptyToNull(values.consumers),
      documentation_url: emptyToNull(values.documentation_url),
    })
  }

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
          <label htmlFor="data-product-description" className="block text-sm font-medium text-gray-700">
            Description
          </label>
          <textarea
            id="data-product-description"
            rows={4}
            className="mt-1.5 block w-full rounded-md border border-app-borderStrong bg-app-surface px-3 py-2 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
            value={values.description}
            onChange={(event) => updateField('description', event.target.value)}
          />
        </div>
        <Input
          label="Refresh frequency"
          value={values.refresh_frequency}
          onChange={(event) => updateField('refresh_frequency', event.target.value)}
        />
        <Input
          label="Documentation URL"
          value={values.documentation_url}
          onChange={(event) => updateField('documentation_url', event.target.value)}
        />
      </div>

      <div>
        <SectionHeader title="Ownership" description="Business and technical ownership links." />
        <div className="grid gap-4 md:grid-cols-2">
          <EntityPicker
            label="Business owner"
            allowedTypes={['person']}
            value={businessOwner}
            onChange={setBusinessOwner}
            allowClear
          />
          <EntityPicker
            label="Technical owner"
            allowedTypes={['person']}
            value={technicalOwner}
            onChange={setTechnicalOwner}
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
          <Input
            label="Business domain ID"
            value={values.business_domain_id}
            onChange={(event) => updateField('business_domain_id', event.target.value)}
            helpText="Manual UUID until business domain API exists"
          />
        </div>
      </div>

      <div>
        <SectionHeader title="Catalog metadata" />
        <div className="grid gap-4 md:grid-cols-2">
          <Input
            label="Source systems"
            value={values.source_systems}
            onChange={(event) => updateField('source_systems', event.target.value)}
          />
          <Input
            label="Consumers"
            value={values.consumers}
            onChange={(event) => updateField('consumers', event.target.value)}
          />
        </div>
      </div>

      <div className="flex flex-wrap gap-2 text-sm text-gray-600">
        <span>Type:</span>
        <StatusBadge status={values.type ?? 'dashboard'} />
        <span>Status:</span>
        <StatusBadge status={values.status ?? 'draft'} />
        <span>Quality:</span>
        <StatusBadge status={values.quality_status ?? 'unknown'} />
      </div>

      {submitError ? <p className="text-sm text-red-700">{submitError}</p> : null}

      <div className="flex items-center gap-2">
        <Button type="submit" disabled={isSubmitting}>
          {mode === 'create' ? 'Create Data Product' : 'Save Changes'}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
      </div>
    </form>
  )
}
