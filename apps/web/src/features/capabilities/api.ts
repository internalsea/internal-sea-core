import { apiDelete, apiGet, apiPatch, apiPost } from '@/lib/apiClient'
import type {
  Capability,
  CapabilityCreateInput,
  CapabilityFilters,
  CapabilityListResponse,
  CapabilitySummary,
  CapabilityUpdateInput,
} from '@/features/capabilities/types'

function toQueryParams(
  filters?: CapabilityFilters,
): Record<string, string | number | boolean | undefined> | undefined {
  if (!filters) {
    return undefined
  }

  return {
    search: filters.search,
    page: filters.page,
    page_size: filters.page_size,
  }
}

export function getCapabilities(filters?: CapabilityFilters): Promise<CapabilityListResponse> {
  return apiGet<CapabilityListResponse>('/capabilities', toQueryParams(filters))
}

export function getCapability(id: string): Promise<Capability> {
  return apiGet<Capability>(`/capabilities/${id}`)
}

export function getCapabilitySummary(id: string): Promise<CapabilitySummary> {
  return apiGet<CapabilitySummary>(`/capabilities/${id}/summary`)
}

export function createCapability(payload: CapabilityCreateInput): Promise<Capability> {
  return apiPost<Capability>('/capabilities', payload)
}

export function updateCapability(
  id: string,
  payload: CapabilityUpdateInput,
): Promise<Capability> {
  return apiPatch<Capability>(`/capabilities/${id}`, payload)
}

export function deleteCapability(id: string): Promise<void> {
  return apiDelete(`/capabilities/${id}`)
}
