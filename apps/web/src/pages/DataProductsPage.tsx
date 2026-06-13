import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { Button } from '@/components/ui/Button'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { Card } from '@/components/ui/Card'
import { EmptyState } from '@/components/ui/EmptyState'
import { Input } from '@/components/ui/Input'
import { PageHeader } from '@/components/ui/PageHeader'
import { confirmDataProductDelete } from '@/features/data-products/components/DataProductDeleteDialog'
import { DataProductsTable } from '@/features/data-products/components/DataProductsTable'
import { DEFAULT_PAGE_SIZE, selectClassName } from '@/features/data-products/constants'
import { useDataProducts, useDeleteDataProduct } from '@/features/data-products/hooks'
import type { DataProductListItem, DataProductListParams } from '@/features/data-products/types'
import { getApiErrorMessage } from '@/features/data-products/utils'
import {
  DATA_PRODUCT_STATUSES,
  DATA_PRODUCT_TYPES,
  QUALITY_STATUSES,
} from '@/types/enums'

const initialFilters: DataProductListParams = {
  page: 1,
  page_size: DEFAULT_PAGE_SIZE,
}

export function DataProductsPage() {
  const navigate = useNavigate()
  const [filters, setFilters] = useState<DataProductListParams>(initialFilters)
  const { data, isLoading, isError, error } = useDataProducts(filters)
  const deleteMutation = useDeleteDataProduct()

  const handleDelete = async (item: DataProductListItem) => {
    if (!confirmDataProductDelete(item.name)) {
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
        title="Data Products"
        description="Business-facing catalog of dashboards, datasets, metrics, APIs, AI agents, reports and automations."
        actions={
          <PermissionGate require="editor">
            <Link to="/data-products/new">
              <Button>New Data Product</Button>
            </Link>
          </PermissionGate>
        }
      />

      <Card>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <div className="md:col-span-2 lg:col-span-4">
            <Input
              label="Search"
              placeholder="Search by name or description"
              value={filters.search ?? ''}
              onChange={(event) =>
                setFilters({ ...filters, search: event.target.value || undefined, page: 1 })
              }
            />
          </div>
          <div>
            <label htmlFor="data-product-type-filter" className="block text-sm font-medium text-gray-700">
              Type
            </label>
            <select
              id="data-product-type-filter"
              className={selectClassName}
              value={filters.type ?? ''}
              onChange={(event) =>
                setFilters({
                  ...filters,
                  type: event.target.value ? (event.target.value as DataProductListParams['type']) : undefined,
                  page: 1,
                })
              }
            >
              <option value="">All types</option>
              {DATA_PRODUCT_TYPES.map((type) => (
                <option key={type} value={type}>
                  {type.replace(/_/g, ' ')}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="data-product-status-filter" className="block text-sm font-medium text-gray-700">
              Status
            </label>
            <select
              id="data-product-status-filter"
              className={selectClassName}
              value={filters.status ?? ''}
              onChange={(event) =>
                setFilters({
                  ...filters,
                  status: event.target.value
                    ? (event.target.value as DataProductListParams['status'])
                    : undefined,
                  page: 1,
                })
              }
            >
              <option value="">All statuses</option>
              {DATA_PRODUCT_STATUSES.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="data-product-quality-filter" className="block text-sm font-medium text-gray-700">
              Quality
            </label>
            <select
              id="data-product-quality-filter"
              className={selectClassName}
              value={filters.quality_status ?? ''}
              onChange={(event) =>
                setFilters({
                  ...filters,
                  quality_status: event.target.value
                    ? (event.target.value as DataProductListParams['quality_status'])
                    : undefined,
                  page: 1,
                })
              }
            >
              <option value="">All quality states</option>
              {QUALITY_STATUSES.map((quality) => (
                <option key={quality} value={quality}>
                  {quality}
                </option>
              ))}
            </select>
          </div>
          <div className="flex items-end">
            <Button type="button" variant="secondary" onClick={() => setFilters(initialFilters)}>
              Reset filters
            </Button>
          </div>
        </div>
      </Card>

      {isError ? (
        <ErrorState message={getApiErrorMessage(error)} />
      ) : (
        <>
          <DataProductsTable
            items={data?.items ?? []}
            isLoading={isLoading}
            onOpen={(id) => navigate(`/data-products/${id}`)}
            onEdit={(id) => navigate(`/data-products/${id}/edit`)}
            onDelete={handleDelete}
          />

          {!isLoading && (data?.items.length ?? 0) === 0 ? (
            <EmptyState
              title="No data products yet"
              description="Create your first catalog entry to track dashboards, datasets, metrics, APIs and reports."
              action={
                <PermissionGate require="editor">
                  <Link to="/data-products/new">
                    <Button>New Data Product</Button>
                  </Link>
                </PermissionGate>
              }
            />
          ) : null}

          {!isLoading && total > 0 ? (
            <div className="flex items-center justify-between text-sm text-gray-600">
              <p>
                {total} data product{total === 1 ? '' : 's'} · Page {page} of {pages}
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
