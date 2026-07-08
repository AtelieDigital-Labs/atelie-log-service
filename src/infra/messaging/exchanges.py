from faststream.rabbit import RabbitExchange, ExchangeType, RabbitBroker
from .constants import Exchange

exchange_log = RabbitExchange(
    name=Exchange.LOG_EXCHANGE,
    type=ExchangeType.TOPIC,
    durable=True
)

dlx_exchange = RabbitExchange(
    name=Exchange.DLX_EXCHANGE,
    type=ExchangeType.TOPIC,
    durable=True
)

async def declare_exchange(broker: RabbitBroker):
    await broker.declare_exchange(exchange_log)
    await broker.declare_exchange(dlx_exchange)