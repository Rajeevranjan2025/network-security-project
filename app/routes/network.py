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
    except:
        pass

@router.get("/status")
def get_status():
    return {"status": network_status}

@router.post("/start")
def start_network():
    global mininet_process, network_status

    if mininet_process and mininet_process.poll() is None:
        network_status = "running"
        return {"status": "already_running"}

    try:
        mininet_process = subprocess.Popen(
            ["sudo", "python3", TOPOLOGY_PATH],
            preexec_fn=os.setsid
        )
        network_status = "running"
        return {"status": "success"}
    except Exception as e:
        network_status = "error"
        return {"status": "error", "message": str(e)}

@router.post("/stop")
def stop_network():
    global mininet_process, network_status

    if mininet_process:
        kill_process(mininet_process)
        mininet_process = None

    network_status = "stopped"
    return {"status": "success"}

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
            preexec_fn=os.setsid
        )

        network_status = "running"
        return {"status": "success"}

    except Exception as e:
        network_status = "error"
        return {"status": "error", "message": str(e)}

@router.post("/simulate")
def simulate_attack():
    return rebuild_network()
