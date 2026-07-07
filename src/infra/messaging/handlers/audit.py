from src.infra.messaging.broker import broker
from src.infra.messaging.queues import log_receiver_queue
from src.infra.messaging.exchanges import exchange_log
from src.infra.messaging.events.payload import AuditLogPayload
from sqlalchemy.ext.asyncio import AsyncSession
from faststream import Depends
from src.core.database import get_session
from src.models.log import AuditLog

@broker.subscriber(
    queue=log_receiver_queue,
    exchange=exchange_log
)
async def saved_log_audit(
    data: AuditLogPayload,
    session: AsyncSession = Depends(get_session)
):
    try:
        new_log = AuditLog(
            event_id=data.log_id,
            user_id=data.actor,
            entity_type=data.resource,
            entity_id=str(data.resource_id),
            service_source=data.microservice,
            action=data.action,
            delta=data.changes,
            reason=data.reason,
            event_timestamp=data.timestamp
        )

        session.add(new_log)

        await session.commit()

    except Exception as e:
        await session.rollback()
