export interface WorkerStatus {
  worker_enabled: boolean
  worker_instance_id: string
  poll_interval_seconds: number
  batch_size: number
  automation_due_count: number
  notification_due_count: number
  last_checked_at: string | null
}

export interface DueWorkSummary {
  due_automation_triggers: number
  due_notifications: number
  locked_automation_triggers: number
  locked_notifications: number
}

export interface WorkerCycleResult {
  worker_instance_id: string
  started_at: string
  finished_at: string
  due_triggers_found: number
  automation_runs_created: number
  notification_messages_found: number
  notifications_processed: number
  failures: string[]
  summary: string
}
