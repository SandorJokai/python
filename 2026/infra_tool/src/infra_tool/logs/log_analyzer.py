import sys
import re
import logging
import subprocess
from datetime import datetime
from time import time

last_hour = time() - 3600
year = 2026

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

formatter = logging.Formatter(
        "%(levelname)s - %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
        )

handler.setFormatter(formatter)

def show_logs(last_hour: bool=False):

    cmd = ["sudo", "journalctl", "-u", "apache2", "--no-pager"]

    if last_hour:
        cmd.extend(["--since", "1 hour ago"])

    apache_logs = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    for line in apache_logs.stdout.splitlines():

        if "Started The Apache" in line:
            match = re.search(r"(\w.{3,4}.\d\s\d.\:\d.\:\d.)", line)

            if match:
                match_str = match.group()
                MONTH_MAP = {           # Fix for febr as got ValueError error with converted variable previously
                    "febr": "feb",
                }

                parts = match_str.split()
                month = parts[0].lower()

                if month in MONTH_MAP:
                    parts[0] = MONTH_MAP[month].capitalize()

                normalized = f"{year} {' '.join(parts)}"
                converted = datetime.strptime(normalized, "%Y %b %d %H:%M:%S")
                convert_to_unix = float(converted.timestamp())

                if convert_to_unix > last_hour:
                    logger.info("Service restart detected - %s", line.strip())
