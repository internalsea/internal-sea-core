import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { FileForm } from '@/features/files/components/FileForm'
import { useCreateFile } from '@/features/files/hooks'
import { getApiErrorMessage } from '@/features/files/utils'

export function FileCreatePage() {
  const navigate = useNavigate()
  const createMutation = useCreateFile()
  const [submitError, setSubmitError] = useState<string | null>(null)

  return (
    <div className="space-y-6">
      <PageHeader
        title="New File"
        description="Register file metadata or an external document link."
        actions={
          <Link to="/files">
            <Button variant="secondary">Back to Files</Button>
          </Link>
        }
      />

      <Card>
        <FileForm
          mode="create"
          isSubmitting={createMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate('/files')}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              const created = await createMutation.mutateAsync(payload)
              navigate(`/files/${created.id}`)
            } catch (error) {
              setSubmitError(getApiErrorMessage(error))
            }
          }}
        />
      </Card>
    </div>
  )
}
