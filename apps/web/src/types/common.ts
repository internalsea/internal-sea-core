export type UUID = string

export interface ApiErrorBody {
  error?: string
  message?: string
  details?: unknown
  request_id?: string | null
  /** @deprecated use message */
  detail?: string | Array<{ msg: string; loc: string[] }>
  /** @deprecated use error */
  code?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  page: number
  page_size: number
  total: number
  pages: number
}

export interface HealthResponse {
  status: string
  service: string
  version: string
  environment: string
}

export interface LiveHealthResponse {
  status: string
}
