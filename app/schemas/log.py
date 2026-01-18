from pydantic import BaseModel
from datetime import datetime

class LogCreate(BaseModel):
    device_id: int
    message: str
    severity: str  # info, warning, critical

class LogResponse(BaseModel):
    id: int
    device_id: int
    message: str
    severity: str
    timestamp: datetime
