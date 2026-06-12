import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { TeamForm } from '@/features/teams/components/TeamForm'
import { useCreateTeam } from '@/features/teams/hooks'
import { getApiErrorMessage } from '@/features/teams/utils'

export function TeamCreatePage() {
  const navigate = useNavigate()
  const createMutation = useCreateTeam()
  const [submitError, setSubmitError] = useState<string | null>(null)

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Team"
        description="Create a delivery team or ownership group."
        actions={
          <Link to="/teams">
            <Button variant="secondary">Back to Teams</Button>
          </Link>
        }
      />

      <Card>
        <TeamForm
          mode="create"
          isSubmitting={createMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/teams')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              const created = await createMutation.mutateAsync(payload)
              navigate(`/teams/${created.id}`)
            } catch (err) {
              setSubmitError(getApiErrorMessage(err))
            }
          }}
        />
      </Card>
    </div>
  )
}
