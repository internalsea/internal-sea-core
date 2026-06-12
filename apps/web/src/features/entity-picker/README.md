# Entity Picker

Reusable search-and-select components for linking entities across forms.

## Components

- `EntityPicker` — single-entity search/select with debounced global search
- `EntityReference` — display readable entity name from ID (uses lookup endpoint)
- `EntityTypeBadge` — type label badge for picker results

## Usage

```tsx
<EntityPicker
  label="Assignee"
  allowedTypes={['person']}
  value={assignee}
  onChange={setAssignee}
  allowClear
/>
```

`EntityReference` resolves an ID to a title on detail pages:

```tsx
<EntityReference entityType="person" entityId={ownerId} />
```

## APIs

- `GET /api/v1/search?q=&types=&limit=` — picker search
- `GET /api/v1/search/entity/{type}/{id}` — entity lookup for display

Manual UUID entry remains available in advanced form sections where needed.
