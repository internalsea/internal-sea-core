import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { FileForm } from '@/features/files/components/FileForm'
import { useFile, useUpdateFile } from '@/features/files/hooks'
import { fileToFormValues, getApiErrorMessage } from '@/features/files/utils'
import { ApiError } from '@/lib/apiClient'

export function FileEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: file, isLoading, isError, error } = useFile(id)
  const updateMutation = useUpdateFile()
  const [submitError, setSubmitError] = useState<string | null>(null)

  if (isLoading) {
    return <LoadingState message="Loading file…" />
  }

  if (isError || !file) {
    const message =
      error instanceof ApiError && error.status === 404
        ? 'File not found'
        : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title={`Edit: ${file.name}`}
        description="Update file metadata and location details."
        actions={
          <Link to={`/files/${file.id}`}>
            <Button variant="secondary">Back to detail</Button>
          </Link>
        }
      />

      <Card>
        <FileForm
          mode="edit"
          initialValues={fileToFormValues(file)}
          isSubmitting={updateMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate(`/files/${file.id}`)}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              await updateMutation.mutateAsync({ id: file.id, payload })
              navigate(`/files/${file.id}`)
            } catch (submitErr) {
              setSubmitError(getApiErrorMessage(submitErr))
            }
          }}
        />
      </Card>
    </div>
  )
}
