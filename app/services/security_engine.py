from app.models.log import Log

def create_security_log(db, device_id, message, severity):
    log = Log(
        device_id=device_id,
        message=message,
        severity=severity
    )
    db.add(log)
    db.commit()
