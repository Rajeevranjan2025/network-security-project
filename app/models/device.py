from sqlalchemy import Column, Integer, String
from app.database.db import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    ip = Column(String)
    status = Column(String, default="active")
