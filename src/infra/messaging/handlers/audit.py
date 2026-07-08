from src.infra.messaging.broker import broker
from src.infra.messaging.queues import log_receiver_queue, dlq_queue
from src.infra.messaging.exchanges import exchange_log, dlx_exchange
from src.infra.messaging.events.payload import AuditLogPayload
from sqlalchemy.ext.asyncio import AsyncSession
from faststream import Depends, Context
from faststream.rabbit import RabbitMessage
from src.core.database import get_session
from src.models.log import AuditLog
from src.core.logger import setup_trigger_logger
logger = setup_trigger_logger()

@broker.subscriber(
    queue=log_receiver_queue,
    exchange=exchange_log
)
async def saved_log_audit(
    data: AuditLogPayload,
    msg: RabbitMessage,
    session: AsyncSession = Depends(get_session)
):
    try:
        new_log = AuditLog(
            event_id=data.log_id,
            user_id=data.actor.user_id,
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
        logger.info(f"Log do serviço {new_log.service_source} salvo no banco com sucesso")
        await msg.ack()

    except Exception as e:
        await session.rollback()
        logger.error(f"Falha ao gravar AuditLog no banco: {str(e)}", exc_info=True)
        await msg.reject()

@broker.subscriber(
    queue=dlq_queue,
    exchange=dlx_exchange
)
async def reprocess_dlq_audit(
    data: AuditLogPayload,
    msg: RabbitMessage,
    session: AsyncSession = Depends(get_session)
):
    try:
        new_log = AuditLog(
            event_id=data.log_id,
            user_id=data.actor.user_id,
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
        logger.info(f"Log do serviço {new_log.service_source} salvo no banco com sucesso")
        await msg.ack()

    except Exception as e:
        await session.rollback()
        logger.error(f"Falha ao gravar AuditLog no banco: {str(e)}", exc_info=True)
        await msg.nack(requeue=True)
