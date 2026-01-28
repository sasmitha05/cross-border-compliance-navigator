from datetime import datetime
import os

LOG_FILE = "backend/compliance.log"

def log_decision(country_from, country_to, data_type, status):
    os.makedirs("backend", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {country_from} -> {country_to} | {data_type} | {status}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
