import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { ProjectForm } from '@/features/projects/components/ProjectForm'
import { useCreateInternalProject } from '@/features/projects/hooks'
import { getApiErrorMessage } from '@/features/projects/utils'

export function InternalProjectCreatePage() {
  const navigate = useNavigate()
  const createMutation = useCreateInternalProject()
  const [submitError, setSubmitError] = useState<string | null>(null)

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Internal Project"
        description="Create an internal product, capability or improvement initiative."
        actions={
          <Link to="/internal-projects">
            <Button variant="secondary">Back to Internal Projects</Button>
          </Link>
        }
      />

      <Card>
        <ProjectForm
          mode="create"
          variant="internal-projects"
          isSubmitting={createMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/internal-projects')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              const created = await createMutation.mutateAsync(payload)
              navigate(`/internal-projects/${created.id}`)
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
