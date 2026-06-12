import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { PersonForm } from '@/features/people/components/PersonForm'
import { useCreatePerson } from '@/features/people/hooks'
import { getApiErrorMessage } from '@/features/people/utils'

export function PersonCreatePage() {
  const navigate = useNavigate()
  const createMutation = useCreatePerson()
  const [submitError, setSubmitError] = useState<string | null>(null)

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Person"
        description="Add a team member or planned resource."
        actions={
          <Link to="/people">
            <Button variant="secondary">Back to People</Button>
          </Link>
        }
      />

      <Card>
        <PersonForm
          mode="create"
          isSubmitting={createMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/people')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              const created = await createMutation.mutateAsync(payload)
              navigate(`/people/${created.id}`)
            } catch (err) {
              setSubmitError(getApiErrorMessage(err))
            }
          }}
        />
      </Card>
    </div>
  )
}
