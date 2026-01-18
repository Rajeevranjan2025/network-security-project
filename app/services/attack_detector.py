from datetime import datetime, timedelta
from collections import defaultdict

# Store request counts
request_tracker = defaultdict(list)

# Threshold settings
REQUEST_LIMIT = 5  # max 5 requests
TIME_WINDOW = 10   # in 10 seconds

def is_ddos_attack(client_ip: str):
    now = datetime.utcnow()
    request_tracker[client_ip].append(now)

    # Keep only recent requests
    request_tracker[client_ip] = [
        t for t in request_tracker[client_ip]
        if (now - t).seconds <= TIME_WINDOW
    ]

    # If too many requests in short time → suspicious
    if len(request_tracker[client_ip]) > REQUEST_LIMIT:
        return True

    return False
