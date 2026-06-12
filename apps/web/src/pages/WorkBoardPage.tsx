import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { Card } from '@/components/ui/Card'
import { EmptyState } from '@/components/ui/EmptyState'
import { PageHeader } from '@/components/ui/PageHeader'
import { WorkItemBoard } from '@/features/work-items/components/WorkItemBoard'
import { WorkItemFiltersBar } from '@/features/work-items/components/WorkItemFilters'
import { useUpdateWorkItemStatus, useWorkItemBoard } from '@/features/work-items/hooks'
import type { WorkItemFilters, WorkItemStatus } from '@/features/work-items/types'
import { getApiErrorMessage } from '@/features/work-items/utils'

const initialFilters: WorkItemFilters = {}

export function WorkBoardPage() {
  const navigate = useNavigate()
  const [filters, setFilters] = useState<WorkItemFilters>(initialFilters)
  const [updatingItemId, setUpdatingItemId] = useState<string | null>(null)
  const { data, isLoading, isError, error } = useWorkItemBoard(filters)
  const statusMutation = useUpdateWorkItemStatus()

  const handleStatusChange = async (id: string, status: WorkItemStatus) => {
    setUpdatingItemId(id)
    try {
      await statusMutation.mutateAsync({ id, status })
    } finally {
      setUpdatingItemId(null)
    }
  }

  const totalItems = data?.columns.reduce((sum, column) => sum + column.count, 0) ?? 0

  return (
    <div className="space-y-6">
      <PageHeader
        title="Work Board"
        description="Board view of active work grouped by status."
        actions={
          <>
            <Link to="/work-items">
              <Button variant="secondary">List View</Button>
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
          showStatus={false}
          showDataProductId
        />
      </Card>

      {isError ? (
        <ErrorState message={getApiErrorMessage(error)} />
      ) : (
        <>
          <WorkItemBoard
            columns={data?.columns ?? []}
            isLoading={isLoading}
            onOpenItem={(id) => navigate(`/work-items/${id}`)}
            onEditItem={(id) => navigate(`/work-items/${id}/edit`)}
            onStatusChange={handleStatusChange}
            updatingItemId={updatingItemId}
          />

          {!isLoading && totalItems === 0 ? (
            <EmptyState
              title="No work items on the board"
              description="Create a work item or adjust filters to see items grouped by status."
              action={
                <PermissionGate require="editor">
                  <Link to="/work-items/new">
                    <Button>New Work Item</Button>
                  </Link>
                </PermissionGate>
              }
            />
          ) : null}
        </>
      )}
    </div>
  )
}
