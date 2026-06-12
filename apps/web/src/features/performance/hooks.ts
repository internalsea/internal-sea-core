import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  createMetricDefinition,
  createMetricValue,
  deleteMetricDefinition,
  deleteMetricValue,
  getEntityPerformanceScorecard,
  getEntityPerformanceValues,
  getMetricDefinition,
  getMetricDefinitions,
  getMetricValue,
  getMetricValues,
  getPerformanceOverview,
  updateMetricDefinition,
  updateMetricValue,
} from '@/features/performance/api'
import type {
  MetricDefinitionFilters,
  MetricDefinitionFormValues,
  MetricValueFilters,
  PerformanceMetricDefinitionCreateInput,
  PerformanceMetricDefinitionUpdateInput,
  PerformanceMetricValueCreateInput,
  PerformanceMetricValueUpdateInput,
  PerformanceSubjectType,
} from '@/features/performance/types'

export const performanceKeys = {
  all: ['performance'] as const,
  overview: () => [...performanceKeys.all, 'overview'] as const,
  definitions: () => [...performanceKeys.all, 'definitions'] as const,
  definitionLists: () => [...performanceKeys.definitions(), 'list'] as const,
  definitionList: (filters: MetricDefinitionFilters) =>
    [...performanceKeys.definitionLists(), filters] as const,
  definitionDetails: () => [...performanceKeys.definitions(), 'detail'] as const,
  definitionDetail: (id: string) => [...performanceKeys.definitionDetails(), id] as const,
  values: () => [...performanceKeys.all, 'values'] as const,
  valueLists: () => [...performanceKeys.values(), 'list'] as const,
  valueList: (filters: MetricValueFilters) => [...performanceKeys.valueLists(), filters] as const,
  valueDetails: () => [...performanceKeys.values(), 'detail'] as const,
  valueDetail: (id: string) => [...performanceKeys.valueDetails(), id] as const,
  scorecard: (subjectType: PerformanceSubjectType, subjectId: string) =>
    [...performanceKeys.all, 'scorecard', subjectType, subjectId] as const,
  entityValues: (subjectType: PerformanceSubjectType, subjectId: string) =>
    [...performanceKeys.all, 'entity-values', subjectType, subjectId] as const,
}

export function usePerformanceOverview() {
  return useQuery({
    queryKey: performanceKeys.overview(),
    queryFn: getPerformanceOverview,
  })
}

export function useMetricDefinitions(filters: MetricDefinitionFilters) {
  return useQuery({
    queryKey: performanceKeys.definitionList(filters),
    queryFn: () => getMetricDefinitions(filters),
  })
}

export function useMetricDefinition(id: string | undefined) {
  return useQuery({
    queryKey: performanceKeys.definitionDetail(id ?? ''),
    queryFn: () => getMetricDefinition(id!),
    enabled: Boolean(id),
  })
}

export function useCreateMetricDefinition() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: PerformanceMetricDefinitionCreateInput) => createMetricDefinition(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: performanceKeys.definitionLists() })
      void queryClient.invalidateQueries({ queryKey: performanceKeys.overview() })
    },
  })
}

export function useUpdateMetricDefinition() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: PerformanceMetricDefinitionUpdateInput }) =>
      updateMetricDefinition(id, payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: performanceKeys.definitionLists() })
      void queryClient.invalidateQueries({ queryKey: performanceKeys.definitionDetail(variables.id) })
      void queryClient.invalidateQueries({ queryKey: performanceKeys.overview() })
    },
  })
}

export function useDeleteMetricDefinition() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => deleteMetricDefinition(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: performanceKeys.definitions() })
      void queryClient.invalidateQueries({ queryKey: performanceKeys.overview() })
    },
  })
}

export function useMetricValues(filters: MetricValueFilters) {
  return useQuery({
    queryKey: performanceKeys.valueList(filters),
    queryFn: () => getMetricValues(filters),
  })
}

export function useMetricValue(id: string | undefined) {
  return useQuery({
    queryKey: performanceKeys.valueDetail(id ?? ''),
    queryFn: () => getMetricValue(id!),
    enabled: Boolean(id),
  })
}

export function useCreateMetricValue() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: PerformanceMetricValueCreateInput) => createMetricValue(payload),
    onSuccess: (data) => {
      void queryClient.invalidateQueries({ queryKey: performanceKeys.valueLists() })
      void queryClient.invalidateQueries({ queryKey: performanceKeys.overview() })
      void queryClient.invalidateQueries({
        queryKey: performanceKeys.scorecard(data.subject_type, data.subject_id),
      })
      void queryClient.invalidateQueries({
        queryKey: performanceKeys.entityValues(data.subject_type, data.subject_id),
      })
    },
  })
}

export function useUpdateMetricValue() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: PerformanceMetricValueUpdateInput }) =>
      updateMetricValue(id, payload),
    onSuccess: (data) => {
      void queryClient.invalidateQueries({ queryKey: performanceKeys.valueLists() })
      void queryClient.invalidateQueries({ queryKey: performanceKeys.valueDetail(data.id) })
      void queryClient.invalidateQueries({ queryKey: performanceKeys.overview() })
      void queryClient.invalidateQueries({
        queryKey: performanceKeys.scorecard(data.subject_type, data.subject_id),
      })
      void queryClient.invalidateQueries({
        queryKey: performanceKeys.entityValues(data.subject_type, data.subject_id),
      })
    },
  })
}

export function useDeleteMetricValue() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => deleteMetricValue(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: performanceKeys.values() })
      void queryClient.invalidateQueries({ queryKey: performanceKeys.overview() })
      void queryClient.invalidateQueries({ queryKey: performanceKeys.all })
    },
  })
}

export function useEntityPerformanceScorecard(
  subjectType: PerformanceSubjectType,
  subjectId: string | undefined,
) {
  return useQuery({
    queryKey: performanceKeys.scorecard(subjectType, subjectId ?? ''),
    queryFn: () => getEntityPerformanceScorecard(subjectType, subjectId!),
    enabled: Boolean(subjectId),
  })
}

export function useEntityPerformanceValues(
  subjectType: PerformanceSubjectType,
  subjectId: string | undefined,
) {
  return useQuery({
    queryKey: performanceKeys.entityValues(subjectType, subjectId ?? ''),
    queryFn: () => getEntityPerformanceValues(subjectType, subjectId!),
    enabled: Boolean(subjectId),
  })
}

export type { MetricDefinitionFormValues }
