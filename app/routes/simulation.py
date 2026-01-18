from fastapi import APIRouter
import paramiko

router = APIRouter(prefix="/simulate", tags=["Simulation"])

UBUNTU_IP = "192.168.29.97"
USERNAME = "rajeev"
PASSWORD = "Rajeev@2025"
SCRIPT_PATH = "/home/rajeev/mininet_scripts/topology.py"

@router.post("/")
def simulate_attack():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(UBUNTU_IP, username=USERNAME, password=PASSWORD)

        command = f"sudo python3 {SCRIPT_PATH}"
        stdin, stdout, stderr = ssh.exec_command(command)

        output = stdout.read().decode()
        error = stderr.read().decode()

        ssh.close()

        if error:
            return {"status": "error", "message": error}

        return {
            "status": "success",
            "message": "Attack simulation executed successfully",
            "output": output
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
