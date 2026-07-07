from faststream.rabbit import RabbitQueue
from .constants import RoutingKey, Queue

log_receiver_queue = RabbitQueue(
    name=Queue.LOG_REGISTER_QUEUE,
    routing_key=RoutingKey.LOG_REGISTER_ROUTING_KEY,
    durable=True
)