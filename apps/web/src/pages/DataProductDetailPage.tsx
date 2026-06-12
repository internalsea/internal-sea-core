import { useParams } from 'react-router-dom'

import { ErrorState } from '@/components/common/ErrorState'
import { LoadingState } from '@/components/common/LoadingState'
import { DataProductDetail } from '@/features/data-products/components/DataProductDetail'
import { useDataProduct } from '@/features/data-products/hooks'
import { getApiErrorMessage } from '@/features/data-products/utils'
import { ApiError } from '@/lib/apiClient'

export function DataProductDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data, isLoading, isError, error } = useDataProduct(id)

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

  return <DataProductDetail dataProduct={data} />
}
