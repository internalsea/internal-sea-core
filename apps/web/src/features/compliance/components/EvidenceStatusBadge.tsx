import { Badge } from '@/components/ui/Badge'
import { EVIDENCE_STATUSES } from '@/features/compliance/constants'
import type { EvidenceStatus } from '@/features/compliance/types'
import { getEvidenceStatusVariant } from '@/features/compliance/utils'

const labels = Object.fromEntries(EVIDENCE_STATUSES.map((item) => [item.value, item.label]))

interface EvidenceStatusBadgeProps {
  status: EvidenceStatus
}

export function EvidenceStatusBadge({ status }: EvidenceStatusBadgeProps) {
  return <Badge variant={getEvidenceStatusVariant(status)}>{labels[status]}</Badge>
}
