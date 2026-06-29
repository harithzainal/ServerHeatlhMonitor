import os
from datetime import datetime, timedelta

import pandas as pd

# ======================================================
# CONFIGURATION
# ======================================================

CSV_FILE = "output/health_log.csv"
REPORT_FILE = "output/weekly_report.txt"

# ======================================================
# CHECK FILE
# ======================================================

if not os.path.exists(CSV_FILE):
    print("Health log not found.")
    exit()

# ======================================================
# READ CSV
# ======================================================

df = pd.read_csv(CSV_FILE)

# Convert Timestamp column to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Filter only last 7 days
one_week_ago = datetime.now() - timedelta(days=7)
weekly_df = df[df["Timestamp"] >= one_week_ago]

if weekly_df.empty:
    print("No data found for the last 7 days.")
    exit()

# ======================================================
# SERVER INFORMATION
# ======================================================

latest = weekly_df.iloc[-1]

hostname = latest["Hostname"]
ip_address = latest["IP Address"]
operating_system = latest["Operating System"]
os_version = latest["OS Version"]
boot_time = latest["Boot Time"]
cpu_core = latest["CPU Cores"]
memory_total = latest["Total Memory (GB)"]
disk_total = latest["Total Disk (GB)"]

# ======================================================
# CPU SUMMARY
# ======================================================

avg_cpu = weekly_df["CPU Usage"].mean()
max_cpu = weekly_df["CPU Usage"].max()
min_cpu = weekly_df["CPU Usage"].min()

# ======================================================
# MEMORY SUMMARY
# ======================================================

avg_memory = weekly_df["Memory Usage"].mean()
max_memory = weekly_df["Memory Usage"].max()
min_memory = weekly_df["Memory Usage"].min()

# ======================================================
# DISK SUMMARY
# ======================================================

avg_disk = weekly_df["Disk Usage"].mean()
max_disk = weekly_df["Disk Usage"].max()
min_disk = weekly_df["Disk Usage"].min()

# ======================================================
# WARNING SUMMARY
# ======================================================

cpu_warning = (weekly_df["CPU Status"] == "High").sum()
memory_warning = (weekly_df["Memory Status"] == "High").sum()
disk_warning = (weekly_df["Disk Status"] == "High").sum()

total_warning = cpu_warning + memory_warning + disk_warning

# ======================================================
# OVERALL STATUS
# ======================================================

if total_warning == 0:
    overall = "HEALTHY"
elif total_warning <= 5:
    overall = "WARNING"
else:
    overall = "CRITICAL"

# ======================================================
# GENERATE REPORT
# ======================================================

report = f"""
======================================================================
                    WEEKLY SERVER HEALTH REPORT
======================================================================

Report Generated : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Monitoring Period: Last 7 Days

======================================================================
SERVER INFORMATION
======================================================================

Hostname          : {hostname}
IP Address        : {ip_address}
Operating System  : {operating_system}
OS Version        : {os_version}
Boot Time         : {boot_time}

CPU Cores         : {cpu_core}
Total Memory      : {memory_total} GB
Total Disk        : {disk_total} GB

Total Health Logs : {len(weekly_df)}

======================================================================
CPU SUMMARY
======================================================================

Average CPU Usage : {avg_cpu:.2f} %
Highest CPU Usage : {max_cpu:.2f} %
Lowest CPU Usage  : {min_cpu:.2f} %

CPU Warnings      : {cpu_warning}

======================================================================
MEMORY SUMMARY
======================================================================

Average Memory    : {avg_memory:.2f} %
Highest Memory    : {max_memory:.2f} %
Lowest Memory     : {min_memory:.2f} %

Memory Warnings   : {memory_warning}

======================================================================
DISK SUMMARY
======================================================================

Average Disk      : {avg_disk:.2f} %
Highest Disk      : {max_disk:.2f} %
Lowest Disk       : {min_disk:.2f} %

Disk Warnings     : {disk_warning}

======================================================================
OVERALL HEALTH
======================================================================

Total Warnings    : {total_warning}

Overall Status    : {overall}

======================================================================
END OF REPORT
======================================================================
"""

# ======================================================
# SAVE REPORT
# ======================================================

with open(REPORT_FILE, "w") as file:
    file.write(report)

print(report)
print(f"\nWeekly report saved to: {REPORT_FILE}")