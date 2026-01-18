from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel
import threading
import time

class NetworkManager:
    def __init__(self):
        self.net = None
        self.running = False

    def start(self):
        if self.running:
            return "already_running"

        def run():
            setLogLevel("info")
            self.net = Mininet(controller=OVSController)
            self.net.addController("c0")

            h1 = self.net.addHost("h1")
            h2 = self.net.addHost("h2")
            s1 = self.net.addSwitch("s1")

            self.net.addLink(h1, s1)
            self.net.addLink(h2, s1)

            self.net.start()
            self.running = True

        threading.Thread(target=run).start()
        time.sleep(2)
        return "started"

    def stop(self):
        if not self.running or not self.net:
            return "not_running"

        self.net.stop()
        self.running = False
        self.net = None
        return "stopped"

    def rebuild(self):
        self.stop()
        return self.start()

    def status(self):
        return "running" if self.running else "stopped"

    def simulate_attack(self):
        if not self.running or not self.net:
            return "not_running"

        h1 = self.net.get("h1")
        h2 = self.net.get("h2")

        h1.cmd("ping -f " + h2.IP() + " &")
        time.sleep(3)
        h1.cmd("kill %ping")

        return "attack_simulated"


network_manager = NetworkManager()
