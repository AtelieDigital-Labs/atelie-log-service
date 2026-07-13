from faststream.rabbit import RabbitQueue

from .constants import Exchange, Queue, RoutingKey

log_receiver_queue = RabbitQueue(
    name=Queue.LOG_REGISTER_QUEUE,
    routing_key=RoutingKey.LOG_REGISTER_ROUTING_KEY,
    durable=True,
    arguments={
        'x-dead-letter-exchange': Exchange.DLX_EXCHANGE.value,
        'x-dead-letter-routing-key': RoutingKey.LOG_REGISTER_DLQ_ROUTING_KEY.value,
    },
)

dlq_queue = RabbitQueue(
    name=Queue.LOG_REGISTER_DLQ,
    routing_key=RoutingKey.LOG_REGISTER_DLQ_ROUTING_KEY,
    durable=True,
)
