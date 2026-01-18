from mininet.net import Mininet
from mininet.node import OVSController
from mininet.log import setLogLevel
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

def send_log(device_id, message, severity):
    try:
        requests.post(LOG_API, json={
            "device_id": device_id,
            "message": message,
            "severity": severity
        }, timeout=3)
        print("📝 Log sent:", message)
    except:
        pass

def sanitize(name):
    return "".join(c for c in name if c.isalnum()).lower()

def fetch_devices():
    try:
        r = requests.get(DEVICES_API, timeout=3)
        return r.json()
    except:
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

    for d in devices:
        dtype = d["type"].lower()
        raw_name = d["name"]
        name = sanitize(raw_name)

        if dtype in ["host", "firewall"]:
            hosts[name] = net.addHost(name)
            print(f"🖥 Host added: {name}")

        elif dtype == "switch":
            switches[name] = net.addSwitch(name)
            print(f"🔀 Switch added: {name}")

    if not switches:
        switches["s1"] = net.addSwitch("s1")
        print("🔀 Auto switch created: s1")

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
