import { apiGet } from '@/lib/apiClient'
import type { ActivityEventListResponse, ActivityFilters } from '@/features/activity/types'

export function getEntityActivity(
  entityType: string,
  entityId: string,
  page = 1,
): Promise<ActivityEventListResponse> {
  return apiGet<ActivityEventListResponse>(`/activity/${entityType}/${entityId}`, { page })
}

export function getActivity(filters?: ActivityFilters): Promise<ActivityEventListResponse> {
  return apiGet<ActivityEventListResponse>(
    '/activity',
    filters as Record<string, string | number | boolean | undefined> | undefined,
  )
}
