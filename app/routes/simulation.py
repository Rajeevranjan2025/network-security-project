from fastapi import APIRouter
import subprocess
import os
import signal

router = APIRouter(prefix="/simulate", tags=["Simulation"])

TOPOLOGY_PATH = os.path.abspath("mininet_scripts/topology.py")

@router.post("/")
def simulate_attack():
    try:
        subprocess.Popen(
            ["sudo", "python3", TOPOLOGY_PATH],
            preexec_fn=os.setsid,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return {"status": "success", "message": "Attack simulation started"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
