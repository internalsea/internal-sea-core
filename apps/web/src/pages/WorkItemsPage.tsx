import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { Card } from '@/components/ui/Card'
import { EmptyState } from '@/components/ui/EmptyState'
import { PageHeader } from '@/components/ui/PageHeader'
import { confirmWorkItemDelete } from '@/features/work-items/components/WorkItemDeleteDialog'
import { WorkItemFiltersBar } from '@/features/work-items/components/WorkItemFilters'
import { WorkItemTable } from '@/features/work-items/components/WorkItemTable'
import { DEFAULT_PAGE_SIZE } from '@/features/work-items/constants'
import { useDeleteWorkItem, useWorkItems } from '@/features/work-items/hooks'
import type { WorkItemFilters, WorkItemListItem } from '@/features/work-items/types'
import { getApiErrorMessage } from '@/features/work-items/utils'

const initialFilters: WorkItemFilters = {
  page: 1,
  page_size: DEFAULT_PAGE_SIZE,
}

export function WorkItemsPage() {
  const navigate = useNavigate()
  const [filters, setFilters] = useState<WorkItemFilters>(initialFilters)
  const { data, isLoading, isError, error } = useWorkItems(filters)
  const deleteMutation = useDeleteWorkItem()

  const handleDelete = async (item: WorkItemListItem) => {
    if (!confirmWorkItemDelete(item.title)) {
      return
    }
    try {
      await deleteMutation.mutateAsync(item.id)
    } catch {
      // Error surfaced via mutation state if needed
    }
  }

  const total = data?.total ?? 0
  const page = data?.page ?? 1
  const pages = data?.pages ?? 1

  return (
    <div className="space-y-6">
      <PageHeader
        title="Work Items"
        description="Manage tasks, risks, decisions, technical debt and delivery work."
        actions={
          <>
            <Link to="/work-board">
              <Button variant="secondary">Board View</Button>
            </Link>
            <PermissionGate require="editor">
              <Link to="/work-items/new">
                <Button>New Work Item</Button>
              </Link>
            </PermissionGate>
          </>
        }
      />

      <Card>
        <WorkItemFiltersBar
          filters={filters}
          onChange={setFilters}
          onReset={() => setFilters(initialFilters)}
        />
      </Card>

      {isError ? (
        <ErrorState message={getApiErrorMessage(error)} />
      ) : (
        <>
          <WorkItemTable
            items={data?.items ?? []}
            isLoading={isLoading}
            onOpen={(id) => navigate(`/work-items/${id}`)}
            onEdit={(id) => navigate(`/work-items/${id}/edit`)}
            onDelete={handleDelete}
          />

          {!isLoading && (data?.items.length ?? 0) === 0 ? (
            <EmptyState
              title="No work items yet"
              description="Create your first work item to track delivery tasks, bugs, risks and decisions."
              action={
                <PermissionGate require="editor">
                  <Link to="/work-items/new">
                    <Button>New Work Item</Button>
                  </Link>
                </PermissionGate>
              }
            />
          ) : null}

          {!isLoading && total > 0 ? (
            <div className="flex items-center justify-between text-sm text-gray-600">
              <p>
                {total} item{total === 1 ? '' : 's'} · Page {page} of {pages}
              </p>
              <div className="flex gap-2">
                <Button
                  type="button"
                  variant="secondary"
                  size="sm"
                  disabled={page <= 1}
                  onClick={() => setFilters((current) => ({ ...current, page: page - 1 }))}
                >
                  Previous
                </Button>
                <Button
                  type="button"
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
