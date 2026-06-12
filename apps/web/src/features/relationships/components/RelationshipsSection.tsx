import { useState } from 'react'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { SectionHeader } from '@/components/ui/SectionHeader'
import { RelationshipForm } from '@/features/relationships/components/RelationshipForm'
import { RelationshipList } from '@/features/relationships/components/RelationshipList'
import {
  useCreateRelationship,
  useDeleteRelationship,
  useEntityRelationships,
} from '@/features/relationships/hooks'
import type { EntityType } from '@/features/relationships/types'
import { PermissionGate } from '@/features/auth/components/PermissionGate'
import { useCanWrite } from '@/features/auth/hooks'
import { getApiErrorMessage } from '@/features/relationships/utils'

interface RelationshipsSectionProps {
  entityType: EntityType
  entityId: string
  title?: string
}

export function RelationshipsSection({
  entityType,
  entityId,
  title = 'Relationships',
}: RelationshipsSectionProps) {
  const [showForm, setShowForm] = useState(false)
  const [deletingLinkId, setDeletingLinkId] = useState<string | null>(null)
  const { data, isLoading, isError, error } = useEntityRelationships(entityType, entityId)
  const canWrite = useCanWrite()
  const createRelationship = useCreateRelationship(entityType, entityId)
  const deleteRelationship = useDeleteRelationship(entityType, entityId)

  async function handleCreate(payload: Parameters<typeof createRelationship.mutateAsync>[0]) {
    await createRelationship.mutateAsync(payload)
    setShowForm(false)
  }

  async function handleDelete(linkId: string) {
    setDeletingLinkId(linkId)
    try {
      await deleteRelationship.mutateAsync(linkId)
    } finally {
      setDeletingLinkId(null)
    }
  }

  return (
    <Card>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <SectionHeader
          title={title}
          description="Connect this object to related products, work, projects, people, teams or capabilities."
        />
        {!showForm ? (
          <PermissionGate require="editor">
            <Button variant="secondary" onClick={() => setShowForm(true)}>
              Add relationship
            </Button>
          </PermissionGate>
        ) : null}
      </div>

      <div className="mt-4 space-y-4">
        {showForm ? (
          <RelationshipForm
            sourceType={entityType}
            sourceId={entityId}
            onSubmit={handleCreate}
            onCancel={() => setShowForm(false)}
            isSubmitting={createRelationship.isPending}
          />
        ) : null}

        {isLoading ? (
          <p className="text-sm text-gray-500">Loading relationships…</p>
        ) : isError ? (
          <p className="text-sm text-status-danger">{getApiErrorMessage(error)}</p>
        ) : (
          <RelationshipList
            outgoing={data?.outgoing ?? []}
            incoming={data?.incoming ?? []}
            onDelete={canWrite ? (linkId) => void handleDelete(linkId) : undefined}
            deletingLinkId={deletingLinkId}
          />
        )}
      </div>
    </Card>
  )
}
