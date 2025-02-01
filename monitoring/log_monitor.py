import time
import re

def monitor_logs(log_path="data/alert.log"):
    while True:
        with open(log_path, "r") as f:
            errors = re.findall(r"ORA-\d{5}", f.read())
            for error in set(errors):
                print(f"ALERT: Detected {error} in logs")
        time.sleep(3600)  # Check hourly
