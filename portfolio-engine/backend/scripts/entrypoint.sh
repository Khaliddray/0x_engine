#!/usr/bin/env sh
set -e

echo "==> Running Alembic database migrations..."
alembic upgrade head

echo "==> Ensuring initial portfolio seed data (if database is empty)..."
python3 scripts/seed_data.py --if-empty

PORT_TO_USE="${PORT:-8000}"
HOST_TO_USE="${HOST:-0.0.0.0}"

echo "==> Starting Portfolio Engine API on ${HOST_TO_USE}:${PORT_TO_USE}..."
exec uvicorn app.main:app --host "${HOST_TO_USE}" --port "${PORT_TO_USE}"
