# Worker feature

UI for background worker status on the Automation page.

- `WorkerStatusCard` — config and due counts from `GET /worker/status`
- `DueWorkCard` — queue summary from `GET /worker/due-work`
- `RunWorkerOnceButton` — editor action calling `POST /worker/run-once`

The worker process itself runs separately (`make worker-dev` or Docker worker profile).
