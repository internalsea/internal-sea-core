import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import {
  COMPANY_SIZES,
  COMPANY_STATUSES,
  INDUSTRIES,
  selectClassName,
} from '@/features/tenancy/constants'
import type { CompanyFormValues } from '@/features/tenancy/types'
import { formValuesToCompanyUpdate } from '@/features/tenancy/utils'

interface CompanySettingsFormProps {
  initialValues: CompanyFormValues
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (payload: ReturnType<typeof formValuesToCompanyUpdate>) => void
}

export function CompanySettingsForm({
  initialValues,
  isSubmitting = false,
  submitError,
  onSubmit,
}: CompanySettingsFormProps) {
  const [values, setValues] = useState<CompanyFormValues>(initialValues)
  const [nameError, setNameError] = useState<string | null>(null)

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    const trimmedName = values.name.trim()
    if (!trimmedName) {
      setNameError('Company name is required')
      return
    }
    setNameError(null)
    onSubmit(formValuesToCompanyUpdate({ ...values, name: trimmedName }))
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2">
        <Input
          label="Name"
          value={values.name}
          onChange={(event) => setValues((current) => ({ ...current, name: event.target.value }))}
          error={nameError ?? undefined}
          required
        />
        <Input
          label="Slug"
          value={values.slug}
          onChange={(event) => setValues((current) => ({ ...current, slug: event.target.value }))}
        />
        <div>
          <label htmlFor="company-status" className="block text-sm font-medium text-gray-700">
            Status
          </label>
          <select
            id="company-status"
            className={`mt-1.5 ${selectClassName}`}
            value={values.status}
            onChange={(event) => setValues((current) => ({ ...current, status: event.target.value }))}
          >
            {COMPANY_STATUSES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="company-size" className="block text-sm font-medium text-gray-700">
            Company size
          </label>
          <select
            id="company-size"
            className={`mt-1.5 ${selectClassName}`}
            value={values.company_size}
            onChange={(event) =>
              setValues((current) => ({ ...current, company_size: event.target.value }))
            }
          >
            <option value="">Not set</option>
            {COMPANY_SIZES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="company-industry" className="block text-sm font-medium text-gray-700">
            Industry
          </label>
          <select
            id="company-industry"
            className={`mt-1.5 ${selectClassName}`}
            value={values.industry}
            onChange={(event) =>
              setValues((current) => ({ ...current, industry: event.target.value }))
            }
          >
            <option value="">Not set</option>
            {INDUSTRIES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <Input
          label="Country"
          value={values.country}
          onChange={(event) => setValues((current) => ({ ...current, country: event.target.value }))}
        />
        <div className="sm:col-span-2">
          <Input
            label="Website"
            type="url"
            value={values.website}
            onChange={(event) => setValues((current) => ({ ...current, website: event.target.value }))}
          />
        </div>
      </div>

      <div>
        <label htmlFor="company-description" className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          id="company-description"
          rows={4}
          className="mt-1.5 block w-full rounded-md border border-app-borderStrong bg-app-surface px-3 py-2 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
          value={values.description}
          onChange={(event) =>
            setValues((current) => ({ ...current, description: event.target.value }))
          }
        />
      </div>

      {submitError ? <p className="text-sm text-status-danger">{submitError}</p> : null}

      <Button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Saving…' : 'Save company'}
      </Button>
    </form>
  )
}
