from pydantic import BaseModel

class RuleCreate(BaseModel):
    device_id: int
    rule_type: str   # allow / deny
    target: str      # IP, port, protocol
    description: str

class RuleResponse(BaseModel):
    id: int
    device_id: int
    rule_type: str
    target: str
    description: str
