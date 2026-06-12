import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { WORKSPACE_STATUSES, selectClassName } from '@/features/tenancy/constants'
import type { WorkspaceFormValues } from '@/features/tenancy/types'
import { formValuesToWorkspaceUpdate } from '@/features/tenancy/utils'

interface WorkspaceSettingsFormProps {
  initialValues: WorkspaceFormValues
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (payload: ReturnType<typeof formValuesToWorkspaceUpdate>) => void
}

export function WorkspaceSettingsForm({
  initialValues,
  isSubmitting = false,
  submitError,
  onSubmit,
}: WorkspaceSettingsFormProps) {
  const [values, setValues] = useState<WorkspaceFormValues>(initialValues)
  const [nameError, setNameError] = useState<string | null>(null)

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    const trimmedName = values.name.trim()
    if (!trimmedName) {
      setNameError('Workspace name is required')
      return
    }
    setNameError(null)
    onSubmit(formValuesToWorkspaceUpdate({ ...values, name: trimmedName }))
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
        <Input
          label="Default timezone"
          value={values.default_timezone}
          onChange={(event) =>
            setValues((current) => ({ ...current, default_timezone: event.target.value }))
          }
        />
        <Input
          label="Default currency"
          value={values.default_currency}
          onChange={(event) =>
            setValues((current) => ({ ...current, default_currency: event.target.value }))
          }
        />
        <div>
          <label htmlFor="workspace-status" className="block text-sm font-medium text-gray-700">
            Status
          </label>
          <select
            id="workspace-status"
            className={`mt-1.5 ${selectClassName}`}
            value={values.status}
            onChange={(event) => setValues((current) => ({ ...current, status: event.target.value }))}
          >
            {WORKSPACE_STATUSES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div>
        <label htmlFor="workspace-description" className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          id="workspace-description"
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
        {isSubmitting ? 'Saving…' : 'Save workspace'}
      </Button>
    </form>
  )
}
