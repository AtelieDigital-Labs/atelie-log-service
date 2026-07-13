from datetime import datetime
from typing import Any, Dict

from sqlalchemy import DateTime, Index, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from starlette_admin import ExportType
from starlette_admin.contrib.sqla import ModelView

from src.core.database import Base


class AuditLog(Base):
    __tablename__ = 'audit_log'

    log_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )  # log_id do evento
    user_id: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # actor.get(user_id)
    entity_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # ==resource
    entity_id: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # resource_id
    service_source: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # payload.microservice
    action: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True
    )  # action
    delta: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)  # changes
    reason: Mapped[str] = mapped_column(String, nullable=False)
    event_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )  # timestamp
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        Index('ix_audit_logs_user_entity', 'user_id', 'entity_type'),
        Index('ix_audit_logs_time_service', 'event_timestamp', 'service_source'),
    )


class AuditLogView(ModelView):
    label = 'Relatórios de Auditoria'
    name = 'Log'
    icon = 'fa fa-history'

    # 2. Quais colunas mostrar na tabela principal (Grid)
    fields = [
        'log_id',
        'event_timestamp',
        'service_source',
        'entity_type',
        'entity_id',
        'action',
        'user_id',
        'delta',
        'reason',
    ]

    exclude_fields_from_create = fields
    exclude_fields_from_edit = fields

    page_size = 10
    page_size_options = [10, 25, 50, 100]

    # 5. Configurar ordenação padrão pela data mais recente (beneficia-se do seu index)
    sortable_fields = ['log_id', 'event_timestamp', 'service_source', 'user_id']
    sort_default = [('event_timestamp', False)]

    # 6. Colunas que estarão disponíveis no botão "Filtrar" do topo da página
    searchable_fields = [
        'user_id',
        'service_source',
        'entity_type',
        'entity_id',
        'action',
        'event_timestamp',
    ]

    export_types = [ExportType.CSV, ExportType.EXCEL, ExportType.PDF]

    # Restringe a interface: Administrador não pode criar, editar ou deletar histórico!
    def can_create(self, request) -> bool:
        return False

    def can_edit(self, request) -> bool:
        return False

    def can_delete(self, request) -> bool:
        return False

    async def repr(self, obj: Any, request: Any) -> str:
        if isinstance(obj, AuditLog):
            return f'Evento #{obj.log_id} ({obj.action} em {obj.entity_type})'
        return super().repr(obj, request)
