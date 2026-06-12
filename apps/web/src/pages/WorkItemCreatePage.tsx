import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { WorkItemForm } from '@/features/work-items/components/WorkItemForm'
import { useCreateWorkItem } from '@/features/work-items/hooks'
import { getApiErrorMessage } from '@/features/work-items/utils'

export function WorkItemCreatePage() {
  const navigate = useNavigate()
  const createMutation = useCreateWorkItem()
  const [submitError, setSubmitError] = useState<string | null>(null)

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Work Item"
        description="Create a task, bug, risk, decision or other delivery work item."
        actions={
          <Link to="/work-items">
            <Button variant="secondary">Back to Work Items</Button>
          </Link>
        }
      />

      <Card>
        <WorkItemForm
          mode="create"
          isSubmitting={createMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/work-items')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              const created = await createMutation.mutateAsync(payload)
              navigate(`/work-items/${created.id}`)
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
