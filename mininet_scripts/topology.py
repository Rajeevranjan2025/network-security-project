from mininet.net import Mininet
from mininet.node import OVSController
from mininet.log import setLogLevel
from mininet.cli import CLI
import requests
import time
import os

API_BASE = "http://127.0.0.1:8000"
DEVICES_API = f"{API_BASE}/devices/"
LOG_API = f"{API_BASE}/logs/"

def clean_mininet():
    print("🧹 Cleaning old Mininet...")
    os.system("sudo mn -c > /dev/null 2>&1")
    os.system("sudo killall ovs-testcontroller > /dev/null 2>&1")
    os.system("sudo killall ovs-controller > /dev/null 2>&1")
    os.system("sudo systemctl restart openvswitch-switch > /dev/null 2>&1")

def send_log(device_id, message, severity):
    try:
        requests.post(LOG_API, json={
            "device_id": device_id,
            "message": message,
            "severity": severity
        }, timeout=3)
        print("📝 Log sent:", message)
    except Exception as e:
        print("⚠ Log failed:", e)

def fetch_devices():
    try:
        r = requests.get(DEVICES_API, timeout=3)
        devices = r.json()
        if isinstance(devices, dict) and devices.get("error"):
            return []
        return devices
    except Exception as e:
        print("⚠ Fetch devices failed:", e)
        return []

def create_topology():
    print("\n🚀 Building Dynamic Mininet Topology from UI")

    clean_mininet()

    devices = fetch_devices()
    if not devices:
        print("❌ No devices found")
        return

    net = Mininet(controller=OVSController)
    net.addController("c0")

    hosts = {}
    switches = {}

    # --- Create Nodes using UI names ---
    for d in devices:
        dtype = d["type"].lower()
        name = d["name"]

        if dtype in ["host", "firewall"]:
            hosts[name] = net.addHost(name)
            print(f"🖥 Host added: {name}")

        elif dtype == "switch":
            switches[name] = net.addSwitch(name)
            print(f"🔀 Switch added: {name}")

    # Auto switch if none
    if not switches:
        s_auto = net.addSwitch("s1")
        switches["s1"] = s_auto
        print("🔀 Auto switch created: s1")

    main_switch = list(switches.values())[0]

    # --- Links ---
    for h in hosts.values():
        net.addLink(h, main_switch)

    print("⚡ Starting network...")
    net.start()

    print("📡 Testing connectivity...")
    net.pingAll()

    # --- Attack Simulation ---
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
    print("🖥 Entering Mininet CLI...")
    print("Type: nodes | net | pingall | exit")

    CLI(net)

    print("🛑 Stopping network...")
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    create_topology()
