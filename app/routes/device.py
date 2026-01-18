from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.device import DeviceCreate, DeviceResponse
from app.models.device import Device
from app.database.db import SessionLocal
from app.services.security_engine import create_security_log
from fastapi import Request
from app.services.attack_detector import is_ddos_attack

router = APIRouter(prefix="/devices", tags=["Devices"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DeviceResponse)
def add_device(device: DeviceCreate, db: Session = Depends(get_db)):
    new_device = Device(
        name=device.name,
        type=device.type,
        ip=device.ip,
        status="active"
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    # Log device creation (info)
    create_security_log(
        db=db,
        device_id=new_device.id,
        message=f"Device {new_device.name} added",
        severity="info"
    )

    return new_device


@router.get("/")
def list_devices(request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host

    # Detect DDoS
    if is_ddos_attack(client_ip):
        create_security_log(
            db=db,
            device_id=0,
            message=f"Possible DDoS detected from IP {client_ip}",
            severity="critical"
        )
        return {"error": "Too many requests detected. Possible DDoS."}

    return db.query(Device).all()

@router.delete("/{device_id}")
def remove_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        return {"error": "Device not found"}

    # 🔥 SECURITY LOG: Unauthorized delete attempt
    create_security_log(
        db=db,
        device_id=device_id,
        message=f"Unauthorized delete attempt on device {device_id}",
        severity="critical"
    )

    db.delete(device)
    db.commit()

    return {"message": "Device removed and incident logged"}
