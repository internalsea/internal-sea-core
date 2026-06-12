import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createDataProduct,
  deleteDataProduct,
  getDataProduct,
  getDataProducts,
  updateDataProduct,
} from '@/features/data-products/api'
import type {
  DataProductCreateInput,
  DataProductListParams,
  DataProductUpdateInput,
} from '@/features/data-products/types'

export const dataProductKeys = {
  all: ['data-products'] as const,
  lists: () => [...dataProductKeys.all, 'list'] as const,
  list: (params: DataProductListParams) => [...dataProductKeys.lists(), params] as const,
  details: () => [...dataProductKeys.all, 'detail'] as const,
  detail: (id: string) => [...dataProductKeys.details(), id] as const,
}

export function useDataProducts(params: DataProductListParams = {}) {
  return useQuery({
    queryKey: dataProductKeys.list(params),
    queryFn: () => getDataProducts(params),
  })
}

export function useDataProduct(id: string | undefined) {
  return useQuery({
    queryKey: dataProductKeys.detail(id ?? ''),
    queryFn: () => getDataProduct(id!),
    enabled: Boolean(id),
  })
}

export function useCreateDataProduct() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: DataProductCreateInput) => createDataProduct(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: dataProductKeys.lists() })
    },
  })
}

export function useUpdateDataProduct() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: DataProductUpdateInput }) =>
      updateDataProduct(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: dataProductKeys.lists() })
      void queryClient.invalidateQueries({ queryKey: dataProductKeys.detail(variables.id) })
    },
  })
}

export function useDeleteDataProduct() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => deleteDataProduct(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: dataProductKeys.lists() })
    },
  })
}
