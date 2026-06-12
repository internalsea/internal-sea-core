import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { TeamForm } from '@/features/teams/components/TeamForm'
import { useTeam, useUpdateTeam } from '@/features/teams/hooks'
import { getApiErrorMessage, teamToFormValues } from '@/features/teams/utils'
import { ApiError } from '@/lib/apiClient'

export function TeamEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data, isLoading, isError, error } = useTeam(id)
  const updateMutation = useUpdateTeam()
  const [submitError, setSubmitError] = useState<string | null>(null)

  if (isLoading) {
    return <LoadingState message="Loading team…" />
  }

  if (isError || !data) {
    const message =
      error instanceof ApiError && error.status === 404
        ? 'Team not found.'
        : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Edit Team"
        description={data.name}
        actions={
          <Link to={`/teams/${data.id}`}>
            <Button variant="secondary">Back to detail</Button>
          </Link>
        }
      />

      <Card>
        <TeamForm
          mode="edit"
          initialValues={teamToFormValues(data)}
          isSubmitting={updateMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate(`/teams/${data.id}`)}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              await updateMutation.mutateAsync({ id: data.id, payload })
              navigate(`/teams/${data.id}`)
            } catch (err) {
              setSubmitError(getApiErrorMessage(err))
            }
          }}
        />
      </Card>
    </div>
  )
}
