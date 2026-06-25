import csv
import os
from datetime import datetime
import platform
import psutil

# ===========================
# Configuration
# ===========================

CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 90
DISK_THRESHOLD = 85

OUTPUT_FOLDER = "output"
CSV_FILE = os.path.join(OUTPUT_FOLDER, "health_log.csv")

# ===========================
# Collect Server Information
# ===========================

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

hostname = platform.node()
operating_system = platform.system()
os_version = platform.release()

cpu = psutil.cpu_percent(interval=1)
memory = psutil.virtual_memory().percent
disk = psutil.disk_usage("/").percent

# ===========================
# Health Status
# ===========================

cpu_status = "High" if cpu >= CPU_THRESHOLD else "Normal"
memory_status = "High" if memory >= MEMORY_THRESHOLD else "Normal"
disk_status = "High" if disk >= DISK_THRESHOLD else "Normal"

# ===========================
# Console Output
# ===========================

print("=" * 60)
print("        SERVER HEALTH MONITOR")
print("=" * 60)

print(f"Timestamp        : {timestamp}")
print(f"Hostname         : {hostname}")
print(f"Operating System : {operating_system}")
print(f"OS Version       : {os_version}")

print("-" * 60)

print(f"CPU Usage        : {cpu:.2f}%")
print(f"Memory Usage     : {memory:.2f}%")
print(f"Disk Usage       : {disk:.2f}%")

print("-" * 60)

print(f"CPU Status       : {cpu_status}")
print(f"Memory Status    : {memory_status}")
print(f"Disk Status      : {disk_status}")

print("=" * 60)

# ===========================
# Save CSV
# ===========================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

file_exists = os.path.isfile(CSV_FILE)

with open(CSV_FILE, "a", newline="") as file:

    writer = csv.writer(file)

    if not file_exists:

        writer.writerow([
            "Timestamp",
            "Hostname",
            "Operating System",
            "OS Version",
            "CPU",
            "Memory",
            "Disk",
            "CPU Status",
            "Memory Status",
            "Disk Status"
        ])

    writer.writerow([
        timestamp,
        hostname,
        operating_system,
        os_version,
        cpu,
        memory,
        disk,
        cpu_status,
        memory_status,
        disk_status
    ])

print("Health information saved successfully.")