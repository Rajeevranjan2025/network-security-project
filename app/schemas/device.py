from pydantic import BaseModel
from typing import Optional

class DeviceCreate(BaseModel):
    name: str
    type: str   # switch, firewall, host
    ip: str

class DeviceResponse(BaseModel):
    id: int
    name: str
    type: str
    ip: str
    status: str
