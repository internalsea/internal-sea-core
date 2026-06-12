.PHONY: help install api-dev api-test api-lint api-format api-typecheck api-check \
	web-install web-dev web-build web-lint web-typecheck web-check check format lint test \
	db-up db-migrate db-revision db-downgrade db-current db-history db-reset \
	seed db-seed demo-reset \
	docker-up docker-down docker-logs docker-reset \
	worker-once worker-dev docker-up-worker worker-status

API_DIR := apps/api
WEB_DIR := apps/web

help:
	@echo "Internal Sea — available commands:"
	@echo ""
	@echo "  make install          Install backend and frontend dependencies"
	@echo "  make check            Run api-check and web-check"
	@echo ""
	@echo "  make api-dev          Run FastAPI development server"
	@echo "  make api-test         Run API pytest suite (excludes integration)"
	@echo "  make api-lint         Run ruff check on API"
	@echo "  make api-format       Run ruff format on API"
	@echo "  make api-typecheck    Run mypy on API"
	@echo "  make api-check        Run lint, typecheck and tests"
	@echo ""
	@echo "  make web-install      Install frontend dependencies with pnpm"
	@echo "  make web-dev          Run Vite development server"
	@echo "  make web-build        Build frontend for production"
	@echo "  make web-lint         Run frontend ESLint"
	@echo "  make web-typecheck    Run frontend TypeScript check"
	@echo "  make web-check        Run lint, typecheck and build"
	@echo ""
	@echo "  make db-up            Start Postgres and Redis only"
	@echo "  make db-migrate       Run Alembic upgrade head"
	@echo "  make db-revision message=\"desc\"  Create autogenerate migration"
	@echo "  make db-downgrade     Alembic downgrade -1"
	@echo "  make db-current       Show current migration"
	@echo "  make db-history       Show migration history"
	@echo "  make db-reset         Reset DB volumes, start postgres/redis"
	@echo "  make seed             Populate local DB with demo data (idempotent)"
	@echo "  make db-seed          Alias for seed"
	@echo "  make demo-reset       Reset DB, migrate and seed demo data"
	@echo ""
	@echo "  make docker-up        Start Postgres, Redis, API and Web"
	@echo "  make docker-down      Stop Docker Compose services"
	@echo "  make docker-logs      Tail Docker Compose logs"
	@echo "  make docker-reset     Reset volumes and restart stack"
	@echo ""
	@echo "  make worker-once      Run one worker batch locally"
	@echo "  make worker-dev       Run worker loop locally"
	@echo "  make docker-up-worker Start stack with worker profile"
	@echo "  make worker-status    Curl worker status endpoint (auth may be required)"

install: web-install
	cd $(API_DIR) && uv sync --group dev

web-install:
	cd $(WEB_DIR) && pnpm install

api-dev:
	cd $(API_DIR) && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

api-test:
	cd $(API_DIR) && uv run pytest tests/ -v

api-lint:
	cd $(API_DIR) && uv run ruff check app tests alembic

api-format:
	cd $(API_DIR) && uv run ruff format app tests alembic

api-typecheck:
	cd $(API_DIR) && uv run mypy app

api-check: api-lint api-typecheck api-test

web-dev:
	cd $(WEB_DIR) && pnpm dev

web-build:
	cd $(WEB_DIR) && pnpm build

web-lint:
	cd $(WEB_DIR) && pnpm lint

web-typecheck:
	cd $(WEB_DIR) && pnpm typecheck

web-check: web-lint web-typecheck web-build

check: api-check web-check

format: api-format

lint: api-lint web-lint

test: api-test

db-up:
	docker compose up -d postgres redis

db-migrate:
	cd $(API_DIR) && uv run alembic upgrade head

db-revision:
	cd $(API_DIR) && uv run alembic revision --autogenerate -m "$(message)"

db-downgrade:
	cd $(API_DIR) && uv run alembic downgrade -1

db-current:
	cd $(API_DIR) && uv run alembic current

db-history:
	cd $(API_DIR) && uv run alembic history

db-reset:
	docker compose down -v
	docker compose up -d postgres redis
	@echo "Waiting for Postgres to become healthy..."
	@echo "Run 'make db-migrate' once the database is ready."

seed:
	cd $(API_DIR) && uv run python -m app.seed.seed

db-seed: seed

demo-reset:
	docker compose down -v
	docker compose up -d --wait postgres redis
	$(MAKE) db-migrate
	$(MAKE) seed

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

docker-reset:
	docker compose down -v
	docker compose up -d

worker-once:
	cd $(API_DIR) && uv run python -m app.worker.main run-once

worker-dev:
	cd $(API_DIR) && uv run python -m app.worker.main run-loop

docker-up-worker:
	docker compose --profile worker up -d

worker-status:
	curl -s http://localhost:8000/api/v1/worker/status || echo "Start API and provide auth token if AUTH_ENABLED=true"
