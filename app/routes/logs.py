from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.log import LogCreate, LogResponse
from app.models.log import Log
from app.database.db import SessionLocal

router = APIRouter(prefix="/logs", tags=["Logs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=LogResponse)
def create_log(log: LogCreate, db: Session = Depends(get_db)):
    new_log = Log(
        device_id=log.device_id,
        message=log.message,
        severity=log.severity
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.get("/")
def get_logs(db: Session = Depends(get_db)):
    return db.query(Log).all()
