from faststream.rabbit import RabbitExchange, ExchangeType, RabbitBroker
from .constants import Exchange

exchange_log = RabbitExchange(
    name=Exchange.LOG_EXCHANGE,
    type=ExchangeType.TOPIC,
    durable=True
)


async def declare_exchange(broker: RabbitBroker):
    await broker.declare_exchange(exchange_log)