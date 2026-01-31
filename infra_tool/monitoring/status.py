
import psutil
import time
from infra_tool.services.systemd import read_from_yaml

def cpu_display():
    current_cpu  = psutil.cpu_percent()
    current_ram  = psutil.virtual_memory()
    disk_usage   = psutil.disk_usage("/")
    ld, ld5, ld15 = psutil.getloadavg()

    print(f"CPU: {current_cpu}%")
    print(f"Memory: {current_ram.percent}%")
    print(f"Disk (/): {disk_usage.percent}%")
    print(f"Load Avg: {ld:.2f} {ld5:.2f} {ld15:.2f}")

#    cpu_threshold = parsed["thresholds"]["cpu"]
#    memory_threshold = parsed["thresholds"]["memory"]
#    disk_threshold = parsed["thresholds"]["disk"]

#    return current_cpu,current_ram,disk_threshold


if __name__ == "__main__":
    cpu_display()
