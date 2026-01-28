from datetime import datetime
import os

LOG_FILE = "/tmp/compliance.log"

def log_decision(country_from, country_to, data_type, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {country_from} -> {country_to} | {data_type} | {status}\n"

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        # Silently fail on Vercel (or log to console)
        print(f"Logging failed: {e}")