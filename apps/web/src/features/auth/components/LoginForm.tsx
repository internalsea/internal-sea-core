import { useState, type FormEvent } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import type { LoginRequest } from '@/features/auth/types'

interface LoginFormProps {
  isSubmitting?: boolean
  submitError?: string | null
  onSubmit: (payload: LoginRequest) => void
}

export function LoginForm({ isSubmitting = false, submitError, onSubmit }: LoginFormProps) {
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('admin12345')

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    onSubmit({ email: email.trim(), password })
  }

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
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
        autoComplete="current-password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
        required
      />
      {submitError ? <p className="text-sm text-status-danger">{submitError}</p> : null}
      <Button type="submit" className="w-full" disabled={isSubmitting}>
        {isSubmitting ? 'Signing in…' : 'Sign in'}
      </Button>
      <div className="rounded-md border border-app-border bg-app-muted/40 p-3 text-xs text-gray-600">
        <p className="font-medium text-gray-700">Demo credentials</p>
        <ul className="mt-2 space-y-1">
          <li>admin@example.com / admin12345</li>
          <li>editor@example.com / editor12345</li>
          <li>viewer@example.com / viewer12345</li>
        </ul>
      </div>
    </form>
  )
}
