from typing import Any, Dict

from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base
from sqlalchemy import DateTime, Index, String, func
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class AuditLog(Base):
    __tablename__ = 'auditlog'

    log_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True) #log_id do evento
    user_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True) #actor.get(user_id)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) #==resource
    entity_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)#resource_id
    service_source: Mapped[str] = mapped_column(String(50), nullable=False) #payload.microservice
    action: Mapped[str] = mapped_column(String(20), nullable=False, index=True) #action
    delta: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False) #changes
    reason: Mapped[str] = mapped_column(String, nullable=False)
    event_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True) #timestamp
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('ix_audit_logs_user_entity', 'user_id', 'entity_type'),
        Index('ix_audit_logs_time_service', 'event_timestamp', 'service_source'),
    )