from collections import defaultdict
import time

request_log = defaultdict(list)

def is_ddos_attack(ip):
    now = time.time()
    request_log[ip] = [t for t in request_log[ip] if now - t < 5]
    request_log[ip].append(now)

    return len(request_log[ip]) > 20
