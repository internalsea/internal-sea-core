import { useState } from 'react'
import { Link, Navigate } from 'react-router-dom'

import { getApiErrorMessage } from '@/app/AuthProvider'
import { Card } from '@/components/ui/Card'
import { RegisterForm } from '@/features/auth/components/RegisterForm'
import { useAuth } from '@/features/auth/hooks'

export function RegisterPage() {
  const { isAuthenticated, isLoading, register } = useAuth()
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
          <p className="mt-2 text-sm text-gray-600">Create an account to get started.</p>
        </div>
        <Card title="Create account">
          <RegisterForm
            isSubmitting={isSubmitting}
            submitError={submitError}
            onSubmit={async (payload) => {
              setSubmitError(null)
              setIsSubmitting(true)
              try {
                await register(payload)
              } catch (error) {
                setSubmitError(getApiErrorMessage(error))
              } finally {
                setIsSubmitting(false)
              }
            }}
          />
        </Card>
        <p className="text-center text-sm text-gray-600">
          Already have an account?{' '}
          <Link to="/login" className="font-medium text-core-blue hover:text-core-blueHover">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  )
}
