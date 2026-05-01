import sqlite3
import psutil
from datetime import datetime
import time
import os

def log_cpu():
    db_path = os.path.join(os.path.dirname(__file__), "..", "Notebooks", "database.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cpu_usage (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            usage REAL
        )
    """)
    conn.commit()
    
    while True:
        cpu = psutil.cpu_percent(interval=1)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO cpu_usage (timestamp, usage) VALUES (?, ?)", (timestamp, cpu))
        conn.commit()
        print(f"CPU: {cpu}% at {timestamp}")
        time.sleep(1)