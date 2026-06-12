import { useState } from 'react'
import { Navigate } from 'react-router-dom'

import { Card } from '@/components/ui/Card'
import { LoginForm } from '@/features/auth/components/LoginForm'
import { useAuth } from '@/features/auth/hooks'
import { getApiErrorMessage } from '@/app/AuthProvider'

export function LoginPage() {
  const { isAuthenticated, isLoading, login } = useAuth()
  const [submitError, setSubmitError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  if (!isLoading && isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-app-background px-4">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center">
          <h1 className="text-2xl font-semibold text-gray-900">Internal Sea</h1>
          <p className="mt-2 text-sm text-gray-600">
            Sign in to manage data products, work, projects and compliance.
          </p>
        </div>
        <Card title="Sign in">
          <LoginForm
            isSubmitting={isSubmitting}
            submitError={submitError}
            onSubmit={async (payload) => {
              setSubmitError(null)
              setIsSubmitting(true)
              try {
                await login(payload)
              } catch (error) {
                setSubmitError(getApiErrorMessage(error))
              } finally {
                setIsSubmitting(false)
              }
            }}
          />
        </Card>
      </div>
    </div>
  )
}
