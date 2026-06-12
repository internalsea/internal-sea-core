import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { Card } from '@/components/ui/Card'
import { EmptyState } from '@/components/ui/EmptyState'
import { PageHeader } from '@/components/ui/PageHeader'
import { FileFiltersBar } from '@/features/files/components/FileFilters'
import { FilesTable } from '@/features/files/components/FilesTable'
import { DEFAULT_PAGE_SIZE } from '@/features/files/constants'
import { useDeleteFile, useFiles } from '@/features/files/hooks'
import type { FileAssetListItem, FileFilters } from '@/features/files/types'
import { confirmFileDelete, getApiErrorMessage } from '@/features/files/utils'

const initialFilters: FileFilters = {
  page: 1,
  page_size: DEFAULT_PAGE_SIZE,
}

export function FilesPage() {
  const navigate = useNavigate()
  const [filters, setFilters] = useState<FileFilters>(initialFilters)
  const { data, isLoading, isError, error } = useFiles(filters)
  const deleteMutation = useDeleteFile()

  const handleDelete = async (item: FileAssetListItem) => {
    if (!confirmFileDelete(item.name)) {
      return
    }
    try {
      await deleteMutation.mutateAsync(item.id)
    } catch {
      // surfaced via mutation if needed
    }
  }

  const total = data?.total ?? 0
  const page = data?.page ?? 1
  const pages = data?.pages ?? 1

  return (
    <div className="space-y-6">
      <PageHeader
        title="Files"
        description="Register documents, links and evidence used across products, work and projects."
        actions={
          <PermissionGate require="editor">
            <Link to="/files/new">
              <Button>New File</Button>
            </Link>
          </PermissionGate>
        }
      />

      <Card>
        <FileFiltersBar
          filters={filters}
          onChange={setFilters}
          onReset={() => setFilters(initialFilters)}
        />
      </Card>

      {isError ? (
        <ErrorState message={getApiErrorMessage(error)} />
      ) : (
        <>
          <FilesTable
            items={data?.items ?? []}
            isLoading={isLoading}
            onOpen={(id) => navigate(`/files/${id}`)}
            onEdit={(id) => navigate(`/files/${id}/edit`)}
            onDelete={handleDelete}
          />

          {!isLoading && (data?.items.length ?? 0) === 0 ? (
            <EmptyState
              title="No files yet"
              description="Register file metadata or external document links to get started."
              action={
                <PermissionGate require="editor">
                  <Link to="/files/new">
                    <Button>New File</Button>
                  </Link>
                </PermissionGate>
              }
            />
          ) : null}

          {pages > 1 ? (
            <div className="flex items-center justify-between text-sm text-gray-600">
              <span>
                Showing page {page} of {pages} ({total} total)
              </span>
              <div className="flex gap-2">
                <Button
                  variant="secondary"
                  size="sm"
                  disabled={page <= 1}
                  onClick={() => setFilters((current) => ({ ...current, page: page - 1 }))}
                >
                  Previous
                </Button>
                <Button
                  variant="secondary"
                  size="sm"
                  disabled={page >= pages}
                  onClick={() => setFilters((current) => ({ ...current, page: page + 1 }))}
                >
                  Next
                </Button>
              </div>
            </div>
          ) : null}
        </>
      )}
    </div>
  )
}
