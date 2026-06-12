import { useState } from 'react'
import { Link } from 'react-router-dom'

import { getApiErrorMessage } from '@/app/AuthProvider'
import { Card } from '@/components/ui/Card'
import { FirstUserOnboardingForm } from '@/features/tenancy/components/FirstUserOnboardingForm'
import { useFirstUserOnboarding } from '@/features/tenancy/hooks'
import { setStoredToken } from '@/features/auth/utils'
import { setStoredTenantIds } from '@/features/tenancy/utils'

export function FirstUserOnboardingPage() {
  const onboarding = useFirstUserOnboarding()
  const [submitError, setSubmitError] = useState<string | null>(null)

  return (
    <div className="flex min-h-screen items-center justify-center bg-app-background px-4 py-10">
      <div className="w-full max-w-2xl space-y-6">
        <div className="text-center">
          <h1 className="text-2xl font-semibold text-gray-900">Welcome to Internal Sea</h1>
          <p className="mt-2 text-sm text-gray-600">
            Set up your company, default workspace, and administrator account.
          </p>
        </div>
        <Card title="First-time setup">
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
