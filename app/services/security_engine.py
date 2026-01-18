from app.models.log import Log
from datetime import datetime

def create_security_log(db, device_id, message, severity="critical"):
    log = Log(
        device_id=device_id,
        message=message,
        severity=severity,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
