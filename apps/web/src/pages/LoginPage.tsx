import { useState } from 'react'
import { Link, Navigate } from 'react-router-dom'

import { getApiErrorMessage } from '@/app/AuthProvider'
import { AuthCard } from '@/components/layout/AuthCard'
import { AuthLayout } from '@/components/layout/AuthLayout'
import { LoginForm } from '@/features/auth/components/LoginForm'
import { useAuth } from '@/features/auth/hooks'

export function LoginPage() {
  const { isAuthenticated, isLoading, login } = useAuth()
  const [submitError, setSubmitError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  if (!isLoading && isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <AuthLayout>
      <div className="space-y-6">
        <div className="text-center">
          <h1 className="text-2xl font-semibold tracking-tight text-gray-900">Internal Sea</h1>
          <p className="mt-2 text-sm text-gray-600">
            Sign in to manage data products, work, projects and compliance.
          </p>
        </div>
        <AuthCard title="Sign in">
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
          <div className="mt-4 border-t border-auth-surfaceBorder pt-4">
            <Link
              to="/register"
              className="inline-flex h-9 w-full items-center justify-center rounded-md border border-auth-inputBorder bg-auth-input px-4 text-sm font-medium text-gray-700 transition-colors hover:border-auth-surfaceBorder hover:bg-auth-surface"
            >
              Create account
            </Link>
          </div>
        </AuthCard>
        <p className="text-center text-sm text-gray-600">
          New to Internal Sea?{' '}
          <Link to="/register" className="font-medium text-core-blue hover:text-core-blueHover">
            Register
          </Link>
        </p>
      </div>
    </AuthLayout>
  )
}
