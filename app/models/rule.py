from sqlalchemy import Column, Integer, String
from app.database.db import Base

class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer)
    rule_type = Column(String)  # allow / deny
    target = Column(String)
    description = Column(String)
