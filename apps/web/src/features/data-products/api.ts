import { apiDelete, apiGet, apiPatch, apiPost } from '@/lib/apiClient'
import type {
  DataProduct,
  DataProductCreateInput,
  DataProductListParams,
  DataProductListResponse,
  DataProductUpdateInput,
} from '@/features/data-products/types'

export function getDataProducts(params?: DataProductListParams): Promise<DataProductListResponse> {
  return apiGet<DataProductListResponse>(
    '/data-products',
    params as Record<string, string | number | boolean | undefined> | undefined,
  )
}

export function getDataProduct(id: string): Promise<DataProduct> {
  return apiGet<DataProduct>(`/data-products/${id}`)
}

export function createDataProduct(payload: DataProductCreateInput): Promise<DataProduct> {
  return apiPost<DataProduct>('/data-products', payload)
}

export function updateDataProduct(
  id: string,
  payload: DataProductUpdateInput,
): Promise<DataProduct> {
  return apiPatch<DataProduct>(`/data-products/${id}`, payload)
}

export function deleteDataProduct(id: string): Promise<void> {
  return apiDelete(`/data-products/${id}`)
}
