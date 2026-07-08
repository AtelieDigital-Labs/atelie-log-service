from enum import StrEnum

class Exchange(StrEnum):
    LOG_EXCHANGE = "logs.events"
    DLX_EXCHANGE = "logs.dlx"

class Queue(StrEnum):
    LOG_REGISTER_QUEUE = "logs.receiver.queue" 
    LOG_REGISTER_DLQ = "logs.receiver.dlq"

class RoutingKey(StrEnum):
    LOG_REGISTER_ROUTING_KEY = "logs.register"
    LOG_REGISTER_DLQ_ROUTING_KEY = "logs.register.dlq"