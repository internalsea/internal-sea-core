import { apiDelete, apiGet, apiPatch, apiPost } from '@/lib/apiClient'
import type {
  WorkItem,
  WorkItemBoardResponse,
  WorkItemCreateInput,
  WorkItemFilters,
  WorkItemListResponse,
  WorkItemStatus,
  WorkItemUpdateInput,
} from '@/features/work-items/types'

function toQueryParams(
  filters?: WorkItemFilters,
): Record<string, string | number | boolean | undefined> | undefined {
  if (!filters) {
    return undefined
  }

  return {
    search: filters.search,
    type: filters.type,
    status: filters.status,
    priority: filters.priority,
    assignee_id: filters.assignee_id,
    data_product_id: filters.data_product_id,
    capability_id: filters.capability_id,
    team_id: filters.team_id,
    page: filters.page,
    page_size: filters.page_size,
  }
}

export function getWorkItems(filters?: WorkItemFilters): Promise<WorkItemListResponse> {
  return apiGet<WorkItemListResponse>('/work-items', toQueryParams(filters))
}

export function getWorkItem(id: string): Promise<WorkItem> {
  return apiGet<WorkItem>(`/work-items/${id}`)
}

export function createWorkItem(payload: WorkItemCreateInput): Promise<WorkItem> {
  return apiPost<WorkItem>('/work-items', payload)
}

export function updateWorkItem(id: string, payload: WorkItemUpdateInput): Promise<WorkItem> {
  return apiPatch<WorkItem>(`/work-items/${id}`, payload)
}

export function deleteWorkItem(id: string): Promise<void> {
  return apiDelete(`/work-items/${id}`)
}

export function getWorkItemBoard(filters?: WorkItemFilters): Promise<WorkItemBoardResponse> {
  return apiGet<WorkItemBoardResponse>('/work-items/board', toQueryParams(filters))
}

export function updateWorkItemStatus(id: string, status: WorkItemStatus): Promise<WorkItem> {
  return apiPatch<WorkItem>(`/work-items/${id}`, { status })
}
