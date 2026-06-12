# Files feature

Metadata-first file and evidence management for Internal Sea.

## Scope (MVP)

- Register file metadata and external document URLs
- Attach files to data products, work items, projects and internal projects
- Mark attachments as evidence with evidence type
- No binary upload, preview or cloud storage integration yet

## Key components

- `FilesSection` — embeddable section for entity detail pages
- `FileForm` — create/edit file metadata
- `FilesPage` — global file browser at `/files`

## API

Uses `/api/v1/files` endpoints. See `api.ts` for client functions.
