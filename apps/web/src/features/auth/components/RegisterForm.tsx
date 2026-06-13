import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import type { RegisterRequest } from '@/features/auth/types'

interface RegisterFormProps {
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (payload: RegisterRequest) => void
}

export function RegisterForm({ isSubmitting = false, submitError, onSubmit }: RegisterFormProps) {
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [validationError, setValidationError] = useState<string | null>(null)

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    if (password !== confirmPassword) {
      setValidationError('Passwords do not match')
      return
    }
    setValidationError(null)
    onSubmit({
      full_name: fullName.trim(),
      email: email.trim(),
      password,
    })
  }

  const displayError = validationError ?? submitError

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      <Input
        label="Full name"
        autoComplete="name"
        value={fullName}
        onChange={(event) => setFullName(event.target.value)}
        required
      />
      <Input
        label="Email"
        type="email"
        autoComplete="username"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
        required
      />
      <Input
        label="Password"
        type="password"
        autoComplete="new-password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
        required
        minLength={8}
      />
      <Input
        label="Confirm password"
        type="password"
        autoComplete="new-password"
        value={confirmPassword}
        onChange={(event) => setConfirmPassword(event.target.value)}
        required
        minLength={8}
      />
      {displayError ? <p className="text-sm text-status-danger">{displayError}</p> : null}
      <Button type="submit" className="w-full" disabled={isSubmitting}>
        {isSubmitting ? 'Creating account…' : 'Create account'}
      </Button>
    </form>
  )
}
