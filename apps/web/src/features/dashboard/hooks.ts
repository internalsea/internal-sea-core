import { useQuery } from '@tanstack/react-query'

import {
  getActionableInsights,
  getAutomationHealth,
  getCapabilityWorkload,
  getComplianceInsights,
  getDashboardSummary,
  getDataProductHealth,
  getExecutiveSummary,
  getHighPriorityWorkItems,
  getNotificationHealth,
  getOperationalHealth,
  getOwnershipGaps,
  getPerformanceInsights,
  getProjectHealth,
  getProjectInsights,
  getRecentActivity,
  getRecentDataProducts,
  getWorkDelivery,
} from '@/features/dashboard/api'

export const dashboardKeys = {
  all: ['dashboard'] as const,
  summary: ['dashboard', 'summary'] as const,
  executive: ['dashboard', 'executive-summary'] as const,
  operational: ['dashboard', 'operational-health'] as const,
  dataProductHealth: (limit: number) => ['dashboard', 'data-product-health', limit] as const,
  workDelivery: ['dashboard', 'work-delivery'] as const,
  projectInsights: (limit: number) => ['dashboard', 'project-insights', limit] as const,
  complianceInsights: (limit: number) => ['dashboard', 'compliance-insights', limit] as const,
  performanceInsights: (limit: number) => ['dashboard', 'performance-insights', limit] as const,
  automationHealth: (limit: number) => ['dashboard', 'automation-health', limit] as const,
  notificationHealth: (limit: number) => ['dashboard', 'notification-health', limit] as const,
  recentActivity: (limit: number) => ['dashboard', 'recent-activity', limit] as const,
  actionableInsights: (limit: number) => ['dashboard', 'actionable-insights', limit] as const,
  recentDataProducts: (limit: number) => ['dashboard', 'recent-data-products', limit] as const,
  highPriorityWorkItems: (limit: number) => ['dashboard', 'high-priority-work-items', limit] as const,
  projectHealth: (limit: number) => ['dashboard', 'project-health', limit] as const,
  capabilityWorkload: ['dashboard', 'capability-workload'] as const,
  ownershipGaps: (limit: number) => ['dashboard', 'ownership-gaps', limit] as const,
}

export function useDashboardSummary() {
  return useQuery({ queryKey: dashboardKeys.summary, queryFn: getDashboardSummary })
}

export function useExecutiveSummary() {
  return useQuery({ queryKey: dashboardKeys.executive, queryFn: getExecutiveSummary })
}

export function useOperationalHealth() {
  return useQuery({ queryKey: dashboardKeys.operational, queryFn: getOperationalHealth })
}

export function useDataProductHealth(limit = 10) {
  return useQuery({
    queryKey: dashboardKeys.dataProductHealth(limit),
    queryFn: () => getDataProductHealth(limit),
  })
}

export function useWorkDelivery() {
  return useQuery({ queryKey: dashboardKeys.workDelivery, queryFn: getWorkDelivery })
}

export function useProjectInsights(limit = 10) {
  return useQuery({
    queryKey: dashboardKeys.projectInsights(limit),
    queryFn: () => getProjectInsights(limit),
  })
}

export function useComplianceInsights(limit = 10) {
  return useQuery({
    queryKey: dashboardKeys.complianceInsights(limit),
    queryFn: () => getComplianceInsights(limit),
  })
}

export function usePerformanceInsights(limit = 10) {
  return useQuery({
    queryKey: dashboardKeys.performanceInsights(limit),
    queryFn: () => getPerformanceInsights(limit),
  })
}

export function useAutomationHealth(limit = 10) {
  return useQuery({
    queryKey: dashboardKeys.automationHealth(limit),
    queryFn: () => getAutomationHealth(limit),
  })
}

export function useNotificationHealth(limit = 10) {
  return useQuery({
    queryKey: dashboardKeys.notificationHealth(limit),
    queryFn: () => getNotificationHealth(limit),
  })
}

export function useRecentActivity(limit = 15) {
  return useQuery({
    queryKey: dashboardKeys.recentActivity(limit),
    queryFn: () => getRecentActivity(limit),
  })
}

export function useActionableInsights(limit = 20) {
  return useQuery({
    queryKey: dashboardKeys.actionableInsights(limit),
    queryFn: () => getActionableInsights(limit),
  })
}

export function useRecentDataProducts(limit = 8) {
  return useQuery({
    queryKey: dashboardKeys.recentDataProducts(limit),
    queryFn: () => getRecentDataProducts(limit),
  })
}

export function useHighPriorityWorkItems(limit = 10) {
  return useQuery({
    queryKey: dashboardKeys.highPriorityWorkItems(limit),
    queryFn: () => getHighPriorityWorkItems(limit),
  })
}

export function useProjectHealth(limit = 8) {
  return useQuery({
    queryKey: dashboardKeys.projectHealth(limit),
    queryFn: () => getProjectHealth(limit),
  })
}

export function useCapabilityWorkload() {
  return useQuery({
    queryKey: dashboardKeys.capabilityWorkload,
    queryFn: getCapabilityWorkload,
  })
}

export function useOwnershipGaps(limit = 10) {
  return useQuery({
    queryKey: dashboardKeys.ownershipGaps(limit),
    queryFn: () => getOwnershipGaps(limit),
  })
}
