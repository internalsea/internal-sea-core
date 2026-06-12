import { useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { FileDetail } from '@/features/files/components/FileDetail'
import { useDeleteFile, useFile } from '@/features/files/hooks'
import { confirmFileDelete, getApiErrorMessage } from '@/features/files/utils'
import { ApiError } from '@/lib/apiClient'

export function FileDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: file, isLoading, isError, error } = useFile(id)
  const deleteMutation = useDeleteFile()

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
    <FileDetail
      file={file}
      onEdit={() => navigate(`/files/${file.id}/edit`)}
      onDelete={async () => {
        if (!confirmFileDelete(file.name)) {
          return
        }
        try {
          await deleteMutation.mutateAsync(file.id)
          navigate('/files')
        } catch {
          // mutation error
        }
      }}
    />
  )
}
