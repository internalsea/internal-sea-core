import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import type { TeamFormValues } from '@/features/teams/types'
import { formValuesToPayload } from '@/features/teams/utils'

interface TeamFormProps {
  initialValues?: Partial<TeamFormValues>
  mode: 'create' | 'edit'
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (values: ReturnType<typeof formValuesToPayload>) => void
  onCancel: () => void
}

const defaultValues: TeamFormValues = {
  name: '',
  description: '',
}

export function TeamForm({
  initialValues,
  mode,
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: TeamFormProps) {
  const [values, setValues] = useState<TeamFormValues>({
    ...defaultValues,
    ...initialValues,
  })
  const [nameError, setNameError] = useState<string | null>(null)

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()

    const trimmedName = values.name.trim()
    if (!trimmedName) {
      setNameError('Name is required')
      return
    }
    setNameError(null)

    onSubmit(formValuesToPayload({ ...values, name: trimmedName }))
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid gap-4">
        <Input
          label="Name"
          value={values.name}
          onChange={(event) => setValues((current) => ({ ...current, name: event.target.value }))}
          error={nameError ?? undefined}
          required
        />
        <div>
          <label htmlFor="team-description" className="block text-sm font-medium text-gray-700">
            Description
          </label>
          <textarea
            id="team-description"
            rows={4}
            className="mt-1.5 block w-full rounded-md border border-app-borderStrong bg-app-surface px-3 py-2 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
            value={values.description}
            onChange={(event) =>
              setValues((current) => ({ ...current, description: event.target.value }))
            }
          />
        </div>
      </div>

      {submitError ? <p className="text-sm text-red-700">{submitError}</p> : null}

      <div className="flex items-center gap-2">
        <Button type="submit" disabled={isSubmitting}>
          {mode === 'create' ? 'Create Team' : 'Save Changes'}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
      </div>
    </form>
  )
}
