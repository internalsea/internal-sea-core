import { apiGet } from '@/lib/apiClient'
import type {
  ActionableInsightsResponse,
  AdvancedDashboardResponse,
  AutomationHealth,
  CapabilityWorkloadItem,
  ComplianceInsights,
  DashboardSummary,
  DataProductHealthResponse,
  ExecutiveSummary,
  HighPriorityWorkItem,
  NotificationHealth,
  OperationalHealth,
  OwnershipGapItem,
  PerformanceInsights,
  ProjectHealthItem,
  ProjectInsightsResponse,
  RecentActivityResponse,
  RecentDataProductItem,
  WorkDeliverySummary,
} from '@/features/dashboard/types'

export function getDashboardSummary(): Promise<DashboardSummary> {
  return apiGet<DashboardSummary>('/dashboard/summary')
}

export function getExecutiveSummary(): Promise<ExecutiveSummary> {
  return apiGet<ExecutiveSummary>('/dashboard/executive-summary')
}

export function getOperationalHealth(): Promise<OperationalHealth> {
  return apiGet<OperationalHealth>('/dashboard/operational-health')
}

export function getDataProductHealth(limit = 10): Promise<DataProductHealthResponse> {
  return apiGet<DataProductHealthResponse>('/dashboard/data-product-health', { limit })
}

export function getWorkDelivery(): Promise<WorkDeliverySummary> {
  return apiGet<WorkDeliverySummary>('/dashboard/work-delivery')
}

export function getProjectInsights(limit = 10): Promise<ProjectInsightsResponse> {
  return apiGet<ProjectInsightsResponse>('/dashboard/project-insights', { limit })
}

export function getComplianceInsights(limit = 10): Promise<ComplianceInsights> {
  return apiGet<ComplianceInsights>('/dashboard/compliance-insights', { limit })
}

export function getPerformanceInsights(limit = 10): Promise<PerformanceInsights> {
  return apiGet<PerformanceInsights>('/dashboard/performance-insights', { limit })
}

export function getAutomationHealth(limit = 10): Promise<AutomationHealth> {
  return apiGet<AutomationHealth>('/dashboard/automation-health', { limit })
}

export function getNotificationHealth(limit = 10): Promise<NotificationHealth> {
  return apiGet<NotificationHealth>('/dashboard/notification-health', { limit })
}

export function getRecentActivity(limit = 15): Promise<RecentActivityResponse> {
  return apiGet<RecentActivityResponse>('/dashboard/recent-activity', { limit })
}

export function getActionableInsights(limit = 20): Promise<ActionableInsightsResponse> {
  return apiGet<ActionableInsightsResponse>('/dashboard/actionable-insights', { limit })
}

export function getAdvancedDashboard(): Promise<AdvancedDashboardResponse> {
  return apiGet<AdvancedDashboardResponse>('/dashboard/advanced')
}

export function getRecentDataProducts(limit = 8): Promise<RecentDataProductItem[]> {
  return apiGet<RecentDataProductItem[]>('/dashboard/recent-data-products', { limit })
}

export function getHighPriorityWorkItems(limit = 10): Promise<HighPriorityWorkItem[]> {
  return apiGet<HighPriorityWorkItem[]>('/dashboard/high-priority-work-items', { limit })
}

export function getProjectHealth(limit = 8): Promise<ProjectHealthItem[]> {
  return apiGet<ProjectHealthItem[]>('/dashboard/project-health', { limit })
}

export function getCapabilityWorkload(): Promise<CapabilityWorkloadItem[]> {
  return apiGet<CapabilityWorkloadItem[]>('/dashboard/capability-workload')
}

export function getOwnershipGaps(limit = 10): Promise<OwnershipGapItem[]> {
  return apiGet<OwnershipGapItem[]>('/dashboard/ownership-gaps', { limit })
}
