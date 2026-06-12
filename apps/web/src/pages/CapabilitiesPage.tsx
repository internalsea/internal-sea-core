import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { Card } from '@/components/ui/Card'
import { EmptyState } from '@/components/ui/EmptyState'
import { Input } from '@/components/ui/Input'
import { PageHeader } from '@/components/ui/PageHeader'
import { CapabilitiesTable } from '@/features/capabilities/components/CapabilitiesTable'
import { confirmCapabilityDelete } from '@/features/capabilities/components/CapabilityDeleteDialog'
import { useCapabilities, useDeleteCapability } from '@/features/capabilities/hooks'
import type { CapabilityFilters, CapabilityListItem } from '@/features/capabilities/types'
import { getApiErrorMessage } from '@/features/capabilities/utils'

const DEFAULT_PAGE_SIZE = 20

const initialFilters: CapabilityFilters = {
  page: 1,
  page_size: DEFAULT_PAGE_SIZE,
}

export function CapabilitiesPage() {
  const navigate = useNavigate()
  const [filters, setFilters] = useState<CapabilityFilters>(initialFilters)
  const { data, isLoading, isError, error } = useCapabilities(filters)
  const deleteMutation = useDeleteCapability()

  const handleDelete = async (item: CapabilityListItem) => {
    if (!confirmCapabilityDelete(item.name)) {
      return
    }
    try {
      await deleteMutation.mutateAsync(item.id)
    } catch (err) {
      window.alert(getApiErrorMessage(err))
    }
  }

  const total = data?.total ?? 0
  const page = data?.page ?? 1
  const pages = data?.pages ?? 1

  return (
    <div className="space-y-6">
      <PageHeader
        title="Capabilities"
        description="Manage delivery capabilities such as Data Engineering, BI, AI, CloudOps and Governance."
        actions={
          <PermissionGate require="editor">
            <Link to="/capabilities/new">
              <Button>New Capability</Button>
            </Link>
          </PermissionGate>
        }
      />

      <Card>
        <div className="flex flex-wrap items-end gap-4">
          <div className="min-w-[240px] flex-1">
            <Input
              label="Search"
              placeholder="Search by name or description"
              value={filters.search ?? ''}
              onChange={(event) =>
                setFilters({ ...filters, search: event.target.value || undefined, page: 1 })
              }
            />
          </div>
          <Button type="button" variant="secondary" onClick={() => setFilters(initialFilters)}>
            Reset filters
          </Button>
        </div>
      </Card>

      {isError ? (
        <ErrorState message={getApiErrorMessage(error)} />
      ) : (
        <>
          <CapabilitiesTable
            items={data?.items ?? []}
            isLoading={isLoading}
            onOpen={(id) => navigate(`/capabilities/${id}`)}
            onEdit={(id) => navigate(`/capabilities/${id}/edit`)}
            onDelete={handleDelete}
          />

          {!isLoading && (data?.items.length ?? 0) === 0 ? (
            <EmptyState
              title="No capabilities yet"
              description="Create your first capability to organize skills and service lines."
              action={
                <PermissionGate require="editor">
                  <Link to="/capabilities/new">
                    <Button>New Capability</Button>
                  </Link>
                </PermissionGate>
              }
            />
          ) : null}

          {!isLoading && total > 0 ? (
            <div className="flex items-center justify-between text-sm text-gray-600">
              <p>
                {total} capabilit{total === 1 ? 'y' : 'ies'} · Page {page} of {pages}
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
