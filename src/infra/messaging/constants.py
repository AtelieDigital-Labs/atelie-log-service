from enum import StrEnum

class Exchange(StrEnum):
    LOG_EXCHANGE = "logs.events"

class Queue(StrEnum):
    LOG_REGISTER_QUEUE = "logs.receiver.queue" 

class RoutingKey(StrEnum):
    LOG_REGISTER_ROUTING_KEY = "logs.register"