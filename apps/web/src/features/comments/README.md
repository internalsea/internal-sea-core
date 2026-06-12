# Comments Feature

Plain-text comments on data products, work items, projects and internal projects.

## Components

- `CommentsSection` — loads comments, form and list for a target entity
- `CommentForm` — textarea with validation (max 5000 chars)
- `CommentList` / `CommentItem` — read-only comment display

## Usage

```tsx
<CommentsSection targetType="work_item" targetId={workItem.id} />
```
