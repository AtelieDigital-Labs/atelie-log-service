from faststream.rabbit import RabbitBroker
from faststream import FastStream
from src.core.config import settings
from contextlib import asynccontextmanager
from src.infra.messaging.exchanges import declare_exchange
from src.infra.messaging.queues import log_receiver_queue


broker = RabbitBroker(settings.MESSAGING_URL)
from .handlers.audit import saved_log_audit

@asynccontextmanager
async def lifespan():

    print("Conectando ao RabbitMQ...")
    await broker.connect()
    await broker.start()
    await declare_exchange(broker=broker)
    await broker.declare_queue(log_receiver_queue)

    try:
        yield
    finally:
        print("Desconectando do RabbitMQ...")
        await broker.stop()

app = FastStream(broker, lifespan=lifespan) 

