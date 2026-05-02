import sqlite3
import psutil
from datetime import datetime
import time
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "Notebooks", "database.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def setup_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cpu_usage (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            usage REAL,
            action TEXT,
            pixels_changed INTEGER
        )
    """)
    conn.commit()
    conn.close()

def log_action(action, pixels_changed=0):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cpu = psutil.cpu_percent(interval=None)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO cpu_usage (timestamp, usage, action, pixels_changed) VALUES (?, ?, ?, ?)",
            (timestamp, cpu, action, pixels_changed)
        )
        conn.commit()
        conn.close()
        print(f"Action: {action} | Pixels: {pixels_changed} | CPU: {cpu}%")
    except Exception as e:
        print(f"DB ERROR: {e}")

def log_cpu():
    setup_db()
    conn = get_connection()
    cursor = conn.cursor()

    while True:
        cpu = psutil.cpu_percent(interval=1)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO cpu_usage (timestamp, usage, action, pixels_changed) VALUES (?, ?, ?, ?)",
            (timestamp, cpu, "idle", 0)
        )
        conn.commit()
        print(f"CPU: {cpu}% at {timestamp}")
        time.sleep(1)