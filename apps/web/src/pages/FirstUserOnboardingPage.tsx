import { useState } from 'react'
import { Link } from 'react-router-dom'

import { getApiErrorMessage } from '@/app/AuthProvider'
import { AuthCard } from '@/components/layout/AuthCard'
import { AuthLayout } from '@/components/layout/AuthLayout'
import { FirstUserOnboardingForm } from '@/features/tenancy/components/FirstUserOnboardingForm'
import { useFirstUserOnboarding } from '@/features/tenancy/hooks'
import { setStoredToken } from '@/features/auth/utils'
import { setStoredTenantIds } from '@/features/tenancy/utils'

export function FirstUserOnboardingPage() {
  const onboarding = useFirstUserOnboarding()
  const [submitError, setSubmitError] = useState<string | null>(null)

  return (
    <AuthLayout width="lg">
      <div className="space-y-6">
        <div className="text-center">
          <h1 className="text-2xl font-semibold tracking-tight text-gray-900">Welcome to Internal Sea</h1>
          <p className="mt-2 text-sm text-gray-600">
            Set up your company, default workspace, and administrator account.
          </p>
        </div>
        <AuthCard title="First-time setup">
          <FirstUserOnboardingForm
            isSubmitting={onboarding.isPending}
            submitError={submitError}
            onSubmit={async (payload) => {
              setSubmitError(null)
              try {
                const response = await onboarding.mutateAsync(payload)
                setStoredToken(response.access_token)
                setStoredTenantIds(response.company.id, response.workspace.id)
                window.location.assign('/dashboard')
              } catch (error) {
                setSubmitError(getApiErrorMessage(error))
              }
            }}
          />
        </AuthCard>
        <p className="text-center text-sm text-gray-600">
          Already have an account?{' '}
          <Link to="/login" className="font-medium text-core-blue hover:text-core-blueHover">
            Sign in
          </Link>
        </p>
      </div>
    </AuthLayout>
  )
}
