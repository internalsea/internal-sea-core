import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { ProjectForm } from '@/features/projects/components/ProjectForm'
import { useProject, useUpdateProject } from '@/features/projects/hooks'
import { getApiErrorMessage, projectToFormValues } from '@/features/projects/utils'
import { ApiError } from '@/lib/apiClient'

export function ProjectEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data, isLoading, isError, error } = useProject(id)
  const updateMutation = useUpdateProject()
  const [submitError, setSubmitError] = useState<string | null>(null)

  if (isLoading) {
    return <LoadingState message="Loading project…" />
  }

  if (isError || !data) {
    const message =
      error instanceof ApiError && error.status === 404
        ? 'Project not found.'
        : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Edit Project"
        description={data.name}
        actions={
          <Link to={`/projects/${data.id}`}>
            <Button variant="secondary">Back to detail</Button>
          </Link>
        }
      />

      <Card>
        <ProjectForm
          mode="edit"
          variant="projects"
          initialValues={projectToFormValues(data)}
          isSubmitting={updateMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate(`/projects/${data.id}`)}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              await updateMutation.mutateAsync({ id: data.id, payload })
              navigate(`/projects/${data.id}`)
            } catch (submitErr) {
              setSubmitError(getApiErrorMessage(submitErr))
            }
          }}
        />
      </Card>
    </div>
  )
}
