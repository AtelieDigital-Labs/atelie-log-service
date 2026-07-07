from datetime import datetime
from typing import Dict, Any

from pydantic import BaseModel

class ActorSchema(BaseModel):
    user_id: str

class AuditLogPayload(BaseModel):
    log_id: str
    timestamp: datetime  
    microservice: str
    actor: ActorSchema
    action: str
    resource: str
    resource_id: int
    changes: Dict[str, Any]
    reason: str