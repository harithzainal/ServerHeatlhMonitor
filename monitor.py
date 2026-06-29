import csv
import os
import socket
import logging
import platform
from datetime import datetime

import psutil

# ======================================================
# CONFIGURATION
# ======================================================

CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 90
DISK_THRESHOLD = 85

OUTPUT_FOLDER = "output"
LOG_FOLDER = "logs"

CSV_FILE = os.path.join(OUTPUT_FOLDER, "health_log.csv")
LOG_FILE = os.path.join(LOG_FOLDER, "application.log")

# ======================================================
# CREATE FOLDERS
# ======================================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# ======================================================
# LOGGING CONFIGURATION
# ======================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logging.info("=" * 60)
logging.info("SERVER HEALTH MONITOR STARTED")

# ======================================================
# SERVER INFORMATION
# ======================================================

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

hostname = platform.node()

try:
    ip_address = socket.gethostbyname(hostname)
except:
    ip_address = "Unknown"

operating_system = platform.system()
os_version = platform.release()

boot_time = datetime.fromtimestamp(
    psutil.boot_time()
).strftime("%Y-%m-%d %H:%M:%S")

cpu_core = psutil.cpu_count(logical=True)

memory_total = round(
    psutil.virtual_memory().total / (1024 ** 3), 2
)

disk_total = round(
    psutil.disk_usage("/").total / (1024 ** 3), 2
)

# ======================================================
# RESOURCE USAGE
# ======================================================

cpu = psutil.cpu_percent(interval=1)
memory = psutil.virtual_memory().percent
disk = psutil.disk_usage("/").percent

# ======================================================
# HEALTH STATUS
# ======================================================

cpu_status = "High" if cpu >= CPU_THRESHOLD else "Normal"
memory_status = "High" if memory >= MEMORY_THRESHOLD else "Normal"
disk_status = "High" if disk >= DISK_THRESHOLD else "Normal"

# ======================================================
# CONSOLE OUTPUT
# ======================================================

print("=" * 70)
print("                SERVER HEALTH MONITOR")
print("=" * 70)

print(f"Timestamp          : {timestamp}")
print(f"Hostname           : {hostname}")
print(f"IP Address         : {ip_address}")
print(f"Operating System   : {operating_system}")
print(f"OS Version         : {os_version}")
print(f"Boot Time          : {boot_time}")

print("-" * 70)

print(f"CPU Cores          : {cpu_core}")
print(f"CPU Usage          : {cpu:.2f}%")

print()

print(f"Total Memory       : {memory_total} GB")
print(f"Memory Usage       : {memory:.2f}%")

print()

print(f"Total Disk         : {disk_total} GB")
print(f"Disk Usage         : {disk:.2f}%")

print("-" * 70)

print(f"CPU Status         : {cpu_status}")
print(f"Memory Status      : {memory_status}")
print(f"Disk Status        : {disk_status}")

print("=" * 70)

# ======================================================
# LOGGING
# ======================================================

logging.info(f"Hostname : {hostname}")
logging.info(f"IP Address : {ip_address}")
logging.info(f"Operating System : {operating_system}")

logging.info(f"CPU Usage : {cpu:.2f}%")
logging.info(f"Memory Usage : {memory:.2f}%")
logging.info(f"Disk Usage : {disk:.2f}%")

logging.info(f"CPU Status : {cpu_status}")
logging.info(f"Memory Status : {memory_status}")
logging.info(f"Disk Status : {disk_status}")

if cpu_status == "High":
    logging.warning(f"CPU usage exceeded threshold ({cpu:.2f}%)")

if memory_status == "High":
    logging.warning(f"Memory usage exceeded threshold ({memory:.2f}%)")

if disk_status == "High":
    logging.warning(f"Disk usage exceeded threshold ({disk:.2f}%)")

# ======================================================
# SAVE CSV
# ======================================================

file_exists = os.path.isfile(CSV_FILE)

with open(CSV_FILE, "a", newline="") as file:

    writer = csv.writer(file)

    if not file_exists:

        writer.writerow([
            "Timestamp",
            "Hostname",
            "IP Address",
            "Operating System",
            "OS Version",
            "Boot Time",
            "CPU Cores",
            "Total Memory (GB)",
            "Total Disk (GB)",
            "CPU Usage",
            "Memory Usage",
            "Disk Usage",
            "CPU Status",
            "Memory Status",
            "Disk Status"
        ])

    writer.writerow([
        timestamp,
        hostname,
        ip_address,
        operating_system,
        os_version,
        boot_time,
        cpu_core,
        memory_total,
        disk_total,
        cpu,
        memory,
        disk,
        cpu_status,
        memory_status,
        disk_status
    ])

logging.info("Health information saved successfully.")
logging.info("=" * 60)

print("\nHealth information saved successfully.")
print(f"CSV File : {CSV_FILE}")
print(f"Log File : {LOG_FILE}")