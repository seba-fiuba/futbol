#!/bin/bash
# Script de inicio para Railway - Ejecuta migraciones antes de iniciar el servidor

set -eu

echo "🚀 Ejecutando migraciones de Alembic..."
alembic upgrade head

echo "✅ Migraciones completadas"
echo "🌟 Iniciando servidor FastAPI..."

# Iniciar el servidor
uvicorn main:app --host 0.0.0.0 --port $PORT
