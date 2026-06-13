import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'

interface CompanySetupFormProps {
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (companyName: string) => void
}

export function CompanySetupForm({
  isSubmitting = false,
  submitError,
  onSubmit,
}: CompanySetupFormProps) {
  const [companyName, setCompanyName] = useState('')

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    onSubmit(companyName.trim())
  }

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      <Input
        label="Company name"
        value={companyName}
        onChange={(event) => setCompanyName(event.target.value)}
        required
      />
      {submitError ? <p className="text-sm text-status-danger">{submitError}</p> : null}
      <Button type="submit" className="w-full" disabled={isSubmitting}>
        {isSubmitting ? 'Creating company…' : 'Create company & continue'}
      </Button>
    </form>
  )
}
