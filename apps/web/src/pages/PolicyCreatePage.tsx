import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { PolicyForm } from '@/features/compliance/components/PolicyForm'
import { useCreatePolicy } from '@/features/compliance/hooks'
import { getApiErrorMessage } from '@/features/compliance/utils'

export function PolicyCreatePage() {
  const navigate = useNavigate()
  const createMutation = useCreatePolicy()
  const [submitError, setSubmitError] = useState<string | null>(null)

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Policy"
        description="Create a governance policy for products, projects or teams."
        actions={<Link to="/compliance"><Button variant="secondary">Back to Compliance</Button></Link>}
      />
      <Card>
        <PolicyForm
          mode="create"
          isSubmitting={createMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/compliance')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              const created = await createMutation.mutateAsync(payload)
              navigate(`/compliance/policies/${created.id}`)
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
