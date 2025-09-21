#!/usr/bin/env bash
set -euo pipefail

if [ ! -f .env ]; then
  cp .env.example .env
fi

echo "Starting FloatChat services..."
docker compose up -d --build

echo "Services starting:"
echo "- Backend: http://localhost:8000/docs"
echo "- Web:     http://localhost:5173"
echo "- Streamlit: http://localhost:8501"
