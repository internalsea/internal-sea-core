import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { COMPANY_SIZES, INDUSTRIES, selectClassName } from '@/features/tenancy/constants'
import type { FirstUserOnboardingFormValues } from '@/features/tenancy/types'
import { formValuesToOnboardingRequest } from '@/features/tenancy/utils'

interface FirstUserOnboardingFormProps {
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (payload: ReturnType<typeof formValuesToOnboardingRequest>) => void
}

const defaultValues: FirstUserOnboardingFormValues = {
  full_name: '',
  email: '',
  password: '',
  company_name: '',
  company_size: '',
  industry: '',
  country: '',
  team_name: 'Core Team',
  main_capability_name: '',
}

export function FirstUserOnboardingForm({
  isSubmitting = false,
  submitError,
  onSubmit,
}: FirstUserOnboardingFormProps) {
  const [values, setValues] = useState<FirstUserOnboardingFormValues>(defaultValues)

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    onSubmit(formValuesToOnboardingRequest(values))
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-4">
        <SectionHeader title="Account" />
        <Input
          label="Full name"
          value={values.full_name}
          onChange={(event) => setValues((current) => ({ ...current, full_name: event.target.value }))}
          required
        />
        <Input
          label="Email"
          type="email"
          autoComplete="username"
          value={values.email}
          onChange={(event) => setValues((current) => ({ ...current, email: event.target.value }))}
          required
        />
        <Input
          label="Password"
          type="password"
          autoComplete="new-password"
          value={values.password}
          onChange={(event) => setValues((current) => ({ ...current, password: event.target.value }))}
          required
          minLength={8}
        />
      </div>

      <div className="space-y-4">
        <SectionHeader title="Company" />
        <Input
          label="Company name"
          value={values.company_name}
          onChange={(event) => setValues((current) => ({ ...current, company_name: event.target.value }))}
          required
        />
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label htmlFor="onboarding-company-size" className="block text-sm font-medium text-gray-700">
              Company size
            </label>
            <select
              id="onboarding-company-size"
              className={`mt-1.5 ${selectClassName}`}
              value={values.company_size}
              onChange={(event) =>
                setValues((current) => ({ ...current, company_size: event.target.value }))
              }
            >
              <option value="">Select size</option>
              {COMPANY_SIZES.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="onboarding-industry" className="block text-sm font-medium text-gray-700">
              Industry
            </label>
            <select
              id="onboarding-industry"
              className={`mt-1.5 ${selectClassName}`}
              value={values.industry}
              onChange={(event) =>
                setValues((current) => ({ ...current, industry: event.target.value }))
              }
            >
              <option value="">Select industry</option>
              {INDUSTRIES.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>
        <Input
          label="Country"
          value={values.country}
          onChange={(event) => setValues((current) => ({ ...current, country: event.target.value }))}
        />
        <Input
          label="Default team name"
          value={values.team_name}
          onChange={(event) => setValues((current) => ({ ...current, team_name: event.target.value }))}
        />
        <Input
          label="Main capability name"
          value={values.main_capability_name}
          onChange={(event) =>
            setValues((current) => ({ ...current, main_capability_name: event.target.value }))
          }
        />
      </div>

      {submitError ? <p className="text-sm text-status-danger">{submitError}</p> : null}

      <Button type="submit" className="w-full" disabled={isSubmitting}>
        {isSubmitting ? 'Creating workspace…' : 'Create company & sign in'}
      </Button>
    </form>
  )
}
