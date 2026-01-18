from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.db import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer)
    message = Column(String)
    severity = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
