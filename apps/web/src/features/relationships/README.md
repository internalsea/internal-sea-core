# Relationships Feature

Generic EntityLink UI for connecting core objects.

## Components

- `RelationshipsSection` — loads outgoing/incoming links, add and delete
- `RelationshipForm` — target type, target ID (UUID), link type
- `RelationshipList` / `RelationshipItem` — grouped display with badges

## Usage

```tsx
<RelationshipsSection entityType="data_product" entityId={dataProduct.id} />
```

Entity picker is not implemented yet — users paste target UUIDs.
