import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { CapabilityForm } from '@/features/capabilities/components/CapabilityForm'
import { useCreateCapability } from '@/features/capabilities/hooks'
import { getApiErrorMessage } from '@/features/capabilities/utils'

export function CapabilityCreatePage() {
  const navigate = useNavigate()
  const createMutation = useCreateCapability()
  const [submitError, setSubmitError] = useState<string | null>(null)

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Capability"
        description="Create a delivery capability or service line."
        actions={
          <Link to="/capabilities">
            <Button variant="secondary">Back to Capabilities</Button>
          </Link>
        }
      />

      <Card>
        <CapabilityForm
          mode="create"
          isSubmitting={createMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/capabilities')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              const created = await createMutation.mutateAsync(payload)
              navigate(`/capabilities/${created.id}`)
            } catch (err) {
              setSubmitError(getApiErrorMessage(err))
            }
          }}
        />
      </Card>
    </div>
  )
}
