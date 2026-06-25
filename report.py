import os
import pandas as pd

CSV_FILE = "output/health_log.csv"
REPORT_FILE = "output/weekly_report.txt"

if not os.path.exists(CSV_FILE):
    print("No monitoring data found.")
    exit()

df = pd.read_csv(CSV_FILE)

avg_cpu = df["CPU"].mean()
max_cpu = df["CPU"].max()
min_cpu = df["CPU"].min()

avg_memory = df["Memory"].mean()
max_memory = df["Memory"].max()

avg_disk = df["Disk"].mean()
max_disk = df["Disk"].max()

cpu_warning = len(df[df["CPU Status"] == "High"])
memory_warning = len(df[df["Memory Status"] == "High"])
disk_warning = len(df[df["Disk Status"] == "High"])

total_warning = cpu_warning + memory_warning + disk_warning

if total_warning == 0:
    overall = "Healthy"
elif total_warning <= 5:
    overall = "Warning"
else:
    overall = "Critical"

report = f"""
==========================================================
              WEEKLY SERVER HEALTH REPORT
==========================================================

Total Records : {len(df)}

---------------- CPU ----------------

Average CPU Usage : {avg_cpu:.2f} %
Highest CPU Usage : {max_cpu:.2f} %
Lowest CPU Usage  : {min_cpu:.2f} %

--------------- MEMORY ---------------

Average Memory Usage : {avg_memory:.2f} %
Highest Memory Usage : {max_memory:.2f} %

---------------- DISK -----------------

Average Disk Usage : {avg_disk:.2f} %
Highest Disk Usage : {max_disk:.2f} %

-------------- WARNINGS --------------

CPU High Warning    : {cpu_warning}

Memory High Warning : {memory_warning}

Disk High Warning   : {disk_warning}

---------------------------------------

Overall Health : {overall}

==========================================================
"""

print(report)

with open(REPORT_FILE, "w") as file:
    file.write(report)

print(f"Report saved into {REPORT_FILE}")
