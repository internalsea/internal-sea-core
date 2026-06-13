import { useState } from 'react'
import { Navigate } from 'react-router-dom'

import { getApiErrorMessage } from '@/app/AuthProvider'
import { Card } from '@/components/ui/Card'
import { AuthLoadingScreen } from '@/features/auth/components/AuthLoadingScreen'
import { useAuth } from '@/features/auth/hooks'
import { createCompany, listWorkspaces } from '@/features/tenancy/api'
import { CompanySetupForm } from '@/features/tenancy/components/CompanySetupForm'
import { setStoredTenantIds } from '@/features/tenancy/utils'

export function CompanySetupPage() {
  const { isAuthenticated, isLoading } = useAuth()
  const [submitError, setSubmitError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  if (isLoading) {
    return <AuthLoadingScreen />
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-app-background px-4">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center">
          <h1 className="text-2xl font-semibold text-gray-900">Set up your company</h1>
          <p className="mt-2 text-sm text-gray-600">
            Create a company workspace to start using Internal Sea.
          </p>
        </div>
        <Card title="Company details">
          <CompanySetupForm
            isSubmitting={isSubmitting}
            submitError={submitError}
            onSubmit={async (companyName) => {
              setSubmitError(null)
              setIsSubmitting(true)
              try {
                const company = await createCompany({ name: companyName })
                const workspaces = await listWorkspaces(company.id)
                const workspace = workspaces.items[0]
                if (!workspace) {
                  throw new Error('Company was created but no workspace was found')
                }
                setStoredTenantIds(company.id, workspace.id)
                window.location.assign('/dashboard')
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
