FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./
COPY alembic.ini ./
COPY alembic ./alembic
COPY app ./app

# Install runtime deps from pyproject.toml (keep in sync with CI via uv sync).
RUN uv pip install --system .

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=90s --retries=10 \
  CMD python -c "import sys, urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health/live', timeout=4); sys.exit(0)" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
