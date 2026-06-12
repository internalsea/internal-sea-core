# Files module

Metadata-first file and evidence layer for Internal Sea.

## Scope (MVP)

- `FileStorage` — where files live (external URL, SharePoint, S3, etc.)
- `FileAsset` — file/document metadata (no binary upload)
- `FileAttachment` — links files to core entities with optional evidence flags

## Supported attachment targets

- `data_product`
- `work_item`
- `project`
- `internal_project`

Other `FileEntityType` values exist for future compliance workflows.

## API

Base path: `/api/v1/files`

See OpenAPI docs at `/docs` for full endpoint list.
