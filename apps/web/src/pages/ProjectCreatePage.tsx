import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { ProjectForm } from '@/features/projects/components/ProjectForm'
import { useCreateProject } from '@/features/projects/hooks'
import { getApiErrorMessage } from '@/features/projects/utils'

export function ProjectCreatePage() {
  const navigate = useNavigate()
  const createMutation = useCreateProject()
  const [submitError, setSubmitError] = useState<string | null>(null)

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Project"
        description="Create a client project, POC, pilot, MVP or initiative."
        actions={
          <Link to="/projects">
            <Button variant="secondary">Back to Projects</Button>
          </Link>
        }
      />

      <Card>
        <ProjectForm
          mode="create"
          variant="projects"
          isSubmitting={createMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/projects')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              const created = await createMutation.mutateAsync(payload)
              navigate(`/projects/${created.id}`)
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
