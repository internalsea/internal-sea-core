import { useState } from 'react'

import { Button } from '@/components/ui/Button'
import { EntityPicker } from '@/features/entity-picker/components/EntityPicker'
import type { EntityPickerType, EntityPickerValue } from '@/features/entity-picker/types'
import {
  ACTIVE_ENTITY_TYPES,
  ENTITY_LINK_TYPES,
  entityLinkTypeLabels,
  entityTypeLabels,
} from '@/features/relationships/constants'
import type { EntityLinkCreateInput, EntityLinkType, EntityType } from '@/features/relationships/types'
import {
  cleanRelationshipPayload,
  getApiErrorMessage,
  isSameEntity,
  isValidUuid,
} from '@/features/relationships/utils'

const RELATIONSHIP_PICKER_TYPES: EntityPickerType[] = [
  'data_product',
  'work_item',
  'project',
  'internal_project',
  'person',
  'team',
  'capability',
]

interface RelationshipFormProps {
  sourceType: EntityType
  sourceId: string
  onSubmit: (payload: EntityLinkCreateInput) => Promise<void>
  onCancel: () => void
  isSubmitting?: boolean
}

export function RelationshipForm({
  sourceType,
  sourceId,
  onSubmit,
  onCancel,
  isSubmitting = false,
}: RelationshipFormProps) {
  const [targetEntity, setTargetEntity] = useState<EntityPickerValue | null>(null)
  const [linkType, setLinkType] = useState<EntityLinkType>('relates_to')
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [targetType, setTargetType] = useState<EntityType>('work_item')
  const [targetId, setTargetId] = useState('')

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault()

    let resolvedTargetType: EntityType
    let resolvedTargetId: string

    if (showAdvanced) {
      const trimmedTargetId = targetId.trim()
      if (!trimmedTargetId) {
        setError('Target ID is required.')
        return
      }
      if (!isValidUuid(trimmedTargetId)) {
        setError('Target ID must be a valid UUID.')
        return
      }
      resolvedTargetType = targetType
      resolvedTargetId = trimmedTargetId
    } else {
      if (!targetEntity) {
        setError('Select a target entity.')
        return
      }
      resolvedTargetType = targetEntity.entity_type as EntityType
      resolvedTargetId = targetEntity.entity_id
    }

    if (isSameEntity(sourceType, sourceId, resolvedTargetType, resolvedTargetId)) {
      setError('Cannot link an object to itself.')
      return
    }

    setError(null)
    const payload = cleanRelationshipPayload({
      source_type: sourceType,
      source_id: sourceId,
      target_type: resolvedTargetType,
      target_id: resolvedTargetId,
      link_type: linkType,
      title: title || null,
      description: description || null,
    })

    try {
      await onSubmit(payload)
    } catch (submitError) {
      setError(getApiErrorMessage(submitError))
    }
  }

  return (
    <form onSubmit={(event) => void handleSubmit(event)} className="space-y-4 rounded-md border border-app-border bg-app-muted p-4">
      <div>
        <label htmlFor="link-type" className="mb-1 block text-xs font-medium uppercase tracking-wide text-gray-500">
          Link type
        </label>
        <select
          id="link-type"
          value={linkType}
          onChange={(event) => setLinkType(event.target.value as EntityLinkType)}
          className="w-full rounded-md border border-app-border bg-white px-3 py-2 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
        >
          {ENTITY_LINK_TYPES.map((type) => (
            <option key={type} value={type}>
              {entityLinkTypeLabels[type]}
            </option>
          ))}
        </select>
      </div>

      {!showAdvanced ? (
        <EntityPicker
          label="Target entity"
          allowedTypes={RELATIONSHIP_PICKER_TYPES}
          value={targetEntity}
          onChange={setTargetEntity}
          required
          helperText="Search by name to link an existing entity."
        />
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label htmlFor="target-type" className="mb-1 block text-xs font-medium uppercase tracking-wide text-gray-500">
              Target type
            </label>
            <select
              id="target-type"
              value={targetType}
              onChange={(event) => setTargetType(event.target.value as EntityType)}
              className="w-full rounded-md border border-app-border bg-white px-3 py-2 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
            >
              {ACTIVE_ENTITY_TYPES.map((type) => (
                <option key={type} value={type}>
                  {entityTypeLabels[type]}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="target-id" className="mb-1 block text-xs font-medium uppercase tracking-wide text-gray-500">
              Target ID
            </label>
            <input
              id="target-id"
              type="text"
              value={targetId}
              onChange={(event) => setTargetId(event.target.value)}
              placeholder="00000000-0000-0000-0000-000000000000"
              className="w-full rounded-md border border-app-border bg-white px-3 py-2 font-mono text-sm text-gray-900 placeholder:text-gray-400 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
            />
          </div>
        </div>
      )}

      <button
        type="button"
        onClick={() => setShowAdvanced((current) => !current)}
        className="text-xs text-core-blue hover:underline"
      >
        {showAdvanced ? 'Use entity picker' : 'Use manual ID'}
      </button>

      <div>
        <label htmlFor="link-title" className="mb-1 block text-xs font-medium uppercase tracking-wide text-gray-500">
          Title (optional)
        </label>
        <input
          id="link-title"
          type="text"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          maxLength={255}
          className="w-full rounded-md border border-app-border bg-white px-3 py-2 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
        />
      </div>

      <div>
        <label htmlFor="link-description" className="mb-1 block text-xs font-medium uppercase tracking-wide text-gray-500">
          Description (optional)
        </label>
        <textarea
          id="link-description"
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          rows={2}
          className="w-full rounded-md border border-app-border bg-white px-3 py-2 text-sm text-gray-900 focus:border-core-blue focus:outline-none focus:ring-1 focus:ring-core-blue"
        />
      </div>

      {error ? <p className="text-sm text-status-danger">{error}</p> : null}

      <div className="flex gap-2">
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Adding…' : 'Add relationship'}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel}>
          Cancel
        </Button>
      </div>
    </form>
  )
}
