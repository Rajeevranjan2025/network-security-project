from mininet.net import Mininet
from mininet.node import OVSController
from mininet.log import setLogLevel
import requests
import time

API_BASE = "http://127.0.0.1:8000"
DEVICES_API = f"{API_BASE}/devices/"
LOG_API = f"{API_BASE}/logs/"

def send_log(device_id, message, severity):
    try:
        requests.post(LOG_API, json={
            "device_id": device_id,
            "message": message,
            "severity": severity
        }, timeout=3)
        print("📝 Log sent:", message)
    except Exception as e:
        print("Failed to send log:", e)

def fetch_devices():
    try:
        r = requests.get(DEVICES_API, timeout=3)
        devices = r.json()
        if isinstance(devices, dict) and devices.get("error"):
            return []
        return devices
    except Exception as e:
        print("Failed to fetch devices:", e)
        return []

def create_topology():
    print("\n🚀 Building Dynamic Mininet Topology from UI")

    devices = fetch_devices()

    if not devices:
        print("❌ No devices found")
        time.sleep(5)
        return

    net = Mininet(controller=OVSController)
    net.addController("c0")

    hosts = {}
    switches = {}

    for d in devices:
        dtype = d["type"].lower()
        name = f"d{d['id']}"

        if dtype in ["host", "firewall"]:
            hosts[d["id"]] = net.addHost(name)
            print("🖥 Host added:", name)

        elif dtype == "switch":
            switches[d["id"]] = net.addSwitch(name)
            print("🔀 Switch added:", name)

    if not switches and len(hosts) > 1:
        s_auto = net.addSwitch("s1")
        switches["auto"] = s_auto
        print("⚡ Auto switch created: s1")

    main_switch = list(switches.values())[0]

    for h in hosts.values():
        net.addLink(h, main_switch)

    print("⚡ Starting network...")
    net.start()

    print("📡 Testing connectivity...")
    net.pingAll()

    if len(hosts) >= 2:
        hlist = list(hosts.values())
        attacker = hlist[0]
        victim = hlist[1]

        print("⚠ Simulating attack traffic...")
        attacker.cmd(f"ping -f {victim.IP()} &")
        time.sleep(3)
        attacker.cmd("kill %ping")

        send_log(
            device_id=1,
            message=f"High traffic from {attacker.name} to {victim.name}",
            severity="critical"
        )

    print("✅ Network is LIVE")

    while True:
        time.sleep(5)

if __name__ == "__main__":
    setLogLevel("info")
    create_topology()
