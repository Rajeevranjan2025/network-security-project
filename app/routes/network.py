from fastapi import APIRouter
import subprocess
import os
import signal
import time

router = APIRouter(prefix="/network", tags=["Network Control"])

TOPOLOGY_PATH = os.path.abspath("mininet_scripts/topology.py")

mininet_process = None
network_status = "stopped"

def kill_process(proc):
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except Exception as e:
        print("Kill error:", e)

@router.get("/status")
def get_status():
    return {"status": network_status}

@router.post("/start")
def start_network():
    global mininet_process, network_status

    if mininet_process and mininet_process.poll() is None:
        network_status = "running"
        return {"status": "already_running", "message": "Network already running"}

    try:
        network_status = "running"

        mininet_process = subprocess.Popen(
            ["sudo", "python3", TOPOLOGY_PATH],
            preexec_fn=os.setsid,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return {"status": "success", "message": "Network started"}

    except Exception as e:
        network_status = "error"
        return {"status": "error", "message": str(e)}

@router.post("/stop")
def stop_network():
    global mininet_process, network_status

    if not mininet_process:
        network_status = "stopped"
        return {"status": "not_running", "message": "Network not running"}

    try:
        kill_process(mininet_process)
        mininet_process = None
        network_status = "stopped"
        return {"status": "success", "message": "Network stopped"}

    except Exception as e:
        network_status = "error"
        return {"status": "error", "message": str(e)}

@router.post("/rebuild")
def rebuild_network():
    global mininet_process, network_status

    try:
        network_status = "rebuilding"

        if mininet_process:
            kill_process(mininet_process)
            time.sleep(1)

        mininet_process = subprocess.Popen(
            ["sudo", "python3", TOPOLOGY_PATH],
            preexec_fn=os.setsid,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        network_status = "running"
        return {"status": "success", "message": "Network rebuilt"}

    except Exception as e:
        network_status = "error"
        return {"status": "error", "message": str(e)}

@router.post("/simulate")
def simulate_attack():
    global network_status

    try:
        subprocess.Popen(
            ["sudo", "python3", TOPOLOGY_PATH],
            preexec_fn=os.setsid,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        network_status = "running"
        return {"status": "success", "message": "Attack simulation started"}

    except Exception as e:
        network_status = "error"
        return {"status": "error", "message": str(e)}
