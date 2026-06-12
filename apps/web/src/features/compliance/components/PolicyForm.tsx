import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { POLICY_STATUSES, selectClassName } from '@/features/compliance/constants'
import type { PolicyFormValues } from '@/features/compliance/types'
import { cleanPolicyPayload } from '@/features/compliance/utils'

interface PolicyFormProps {
  initialValues?: Partial<PolicyFormValues>
  mode: 'create' | 'edit'
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (values: ReturnType<typeof cleanPolicyPayload>) => void
  onCancel: () => void
}

const defaultValues: PolicyFormValues = {
  name: '',
  description: '',
  status: 'draft',
  owner_id: '',
  effective_from: '',
  effective_to: '',
  version: '',
}

export function PolicyForm({
  initialValues,
  mode,
  isSubmitting = false,
  submitError,
  onSubmit,
  onCancel,
}: PolicyFormProps) {
  const [values, setValues] = useState<PolicyFormValues>({ ...defaultValues, ...initialValues })
  const [nameError, setNameError] = useState<string | null>(null)

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    if (!values.name.trim()) {
      setNameError('Name is required')
      return
    }
    setNameError(null)
    onSubmit(cleanPolicyPayload(values))
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="mb-1 block text-sm font-medium text-gray-700">Name *</label>
        <Input value={values.name} onChange={(e) => setValues((c) => ({ ...c, name: e.target.value }))} />
        {nameError ? <p className="mt-1 text-sm text-status-danger">{nameError}</p> : null}
      </div>
      <div>
        <label className="mb-1 block text-sm font-medium text-gray-700">Description</label>
        <textarea className="block min-h-24 w-full rounded-md border border-app-borderStrong px-3 py-2 text-sm" value={values.description} onChange={(e) => setValues((c) => ({ ...c, description: e.target.value }))} />
      </div>
      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Status</label>
          <select className={selectClassName} value={values.status} onChange={(e) => setValues((c) => ({ ...c, status: e.target.value as PolicyFormValues['status'] }))}>
            {POLICY_STATUSES.map((item) => <option key={item.value} value={item.value}>{item.label}</option>)}
          </select>
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Version</label>
          <Input value={values.version} onChange={(e) => setValues((c) => ({ ...c, version: e.target.value }))} />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Owner ID</label>
          <Input value={values.owner_id} onChange={(e) => setValues((c) => ({ ...c, owner_id: e.target.value }))} />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Effective from</label>
          <Input type="date" value={values.effective_from} onChange={(e) => setValues((c) => ({ ...c, effective_from: e.target.value }))} />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-gray-700">Effective to</label>
          <Input type="date" value={values.effective_to} onChange={(e) => setValues((c) => ({ ...c, effective_to: e.target.value }))} />
        </div>
      </div>
      {submitError ? <p className="text-sm text-status-danger">{submitError}</p> : null}
      <div className="flex gap-3">
        <Button type="submit" disabled={isSubmitting}>{isSubmitting ? 'Saving…' : mode === 'create' ? 'Create policy' : 'Save changes'}</Button>
        <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>
      </div>
    </form>
  )
}
