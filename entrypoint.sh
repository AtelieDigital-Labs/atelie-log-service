#!/bin/sh
#Se qualquer comando aqui dentro der erro, pare tudo imediatamente"
set -e

echo "Executando migrações do banco de dados..."
alembic upgrade head

echo "Iniciando o FastAPI..."
exec uvicorn --host 0.0.0.0 --port 8000 src.main:app --proxy-headers --forwarded-allow-ips=*
