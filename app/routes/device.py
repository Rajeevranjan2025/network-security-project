from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.device import DeviceCreate, DeviceResponse
from app.models.device import Device
from app.database.db import SessionLocal
from app.services.security_engine import create_security_log
from app.services.attack_detector import is_ddos_attack
import threading
import requests

router = APIRouter(prefix="/devices", tags=["Devices"])

NETWORK_REBUILD_URL = "http://127.0.0.1:8000/network/rebuild"

def trigger_rebuild_async():
    def run():
        try:
            requests.post(NETWORK_REBUILD_URL, timeout=2)
            print("🔄 Network rebuild triggered")
        except Exception as e:
            print("⚠ Failed to rebuild network:", e)
    threading.Thread(target=run).start()

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

    create_security_log(
        db=db,
        device_id=new_device.id,
        message=f"Device {new_device.name} added",
        severity="info"
    )

    trigger_rebuild_async()

    return new_device

@router.get("/")
def list_devices(request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host

    if is_ddos_attack(client_ip):
        create_security_log(
            db=db,
            device_id=0,
            message=f"Possible DDoS detected from IP {client_ip}",
            severity="critical"
        )
        return []

    return db.query(Device).all()

@router.delete("/{device_id}")
def remove_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()

    if not device:
        return {"error": "Device not found"}

    create_security_log(
        db=db,
        device_id=device_id,
        message=f"Device {device.name} deleted",
        severity="warning"
    )

    db.delete(device)
    db.commit()

    trigger_rebuild_async()

    return {"message": "Device removed and network rebuilt"}
