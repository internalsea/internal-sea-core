import { useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { ComplianceCheckForm } from '@/features/compliance/components/ComplianceCheckForm'
import { useCreateComplianceCheck } from '@/features/compliance/hooks'
import type { ComplianceSubjectType } from '@/features/compliance/types'
import { getApiErrorMessage } from '@/features/compliance/utils'

export function ComplianceCheckCreatePage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const subjectType = (searchParams.get('subject_type') as ComplianceSubjectType | null) ?? undefined
  const subjectId = searchParams.get('subject_id') ?? undefined
  const createMutation = useCreateComplianceCheck()
  const [submitError, setSubmitError] = useState<string | null>(null)

  const lockSubject =
    subjectType && subjectId ? { subjectType, subjectId } : undefined

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Compliance Check"
        description="Create a manual compliance check for a supported subject."
        actions={<Link to="/compliance"><Button variant="secondary">Back to Compliance</Button></Link>}
      />
      <Card>
        <ComplianceCheckForm
          mode="create"
          lockSubject={lockSubject}
          isSubmitting={createMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/compliance')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              const created = await createMutation.mutateAsync(payload)
              navigate(`/compliance/checks/${created.id}`)
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
