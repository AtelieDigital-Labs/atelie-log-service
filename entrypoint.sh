#!/bin/sh
#Se qualquer comando aqui dentro der erro, pare tudo imediatamente"
set -e

echo "Executando migrações do banco de dados..."
alembic upgrade head

echo "Iniciando o FastStream..."
exec faststream run src.infra.messaging.broker:app