import { apiGet, apiPost } from '@/lib/apiClient'

import type { DueWorkSummary, WorkerCycleResult, WorkerStatus } from '@/features/worker/types'

export function getWorkerStatus() {
  return apiGet<WorkerStatus>('/worker/status')
}

export function getDueWorkSummary() {
  return apiGet<DueWorkSummary>('/worker/due-work')
}

export function runWorkerOnce() {
  return apiPost<WorkerCycleResult>('/worker/run-once')
}
