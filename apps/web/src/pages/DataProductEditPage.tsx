import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { PageHeader } from '@/components/ui/PageHeader'
import { DataProductForm } from '@/features/data-products/components/DataProductForm'
import { useDataProduct, useUpdateDataProduct } from '@/features/data-products/hooks'
import { dataProductToFormValues, getApiErrorMessage } from '@/features/data-products/utils'
import { ApiError } from '@/lib/apiClient'

export function DataProductEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data, isLoading, isError, error } = useDataProduct(id)
  const updateMutation = useUpdateDataProduct()
  const [submitError, setSubmitError] = useState<string | null>(null)

  if (isLoading) {
    return <LoadingState message="Loading data product…" />
  }

  if (isError || !data) {
    const message =
      error instanceof ApiError && error.status === 404
        ? 'Data product not found.'
        : getApiErrorMessage(error)
    return <ErrorState message={message} />
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Edit Data Product"
        description={data.name}
        actions={
          <Link to={`/data-products/${data.id}`}>
            <Button variant="secondary">Back to detail</Button>
          </Link>
        }
      />

      <Card>
        <DataProductForm
          mode="edit"
          initialValues={dataProductToFormValues(data)}
          isSubmitting={updateMutation.isPending}
          submitError={submitError}
          onCancel={() => navigate(`/data-products/${data.id}`)}
          onSubmit={async (payload) => {
            setSubmitError(null)
            try {
              await updateMutation.mutateAsync({ id: data.id, payload })
              navigate(`/data-products/${data.id}`)
            } catch (err) {
              setSubmitError(getApiErrorMessage(err))
            }
          }}
        />
      </Card>
    </div>
  )
}
