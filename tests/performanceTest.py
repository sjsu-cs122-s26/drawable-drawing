import sqlite3
import psutil
from datetime import datetime
from collections import deque
import time
import os
import threading

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "Notebooks", "database.db")

class CpuTest():
    def __init__(self, process: psutil.Process):
        self.process = process
        self.canvasArea = 0
        self.layers = 0
        self.lock = threading.Lock()

    def get_connection(self):
        conn = sqlite3.connect(DB_PATH)
        return conn

    def setup_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                cpu_usage REAL,
                rss INTEGER,
                vms INTEGER,
                action TEXT,
                pixels_changed INTEGER,
                canvas_area INTEGER,
                layers INTEGER
            )
        """) # rss = resident set size (non-swapped physical memory)
            # vms = virtual memory size (total amount of virtual memory used)
        conn.commit()
        conn.close()

    def updateParameters(self, area : int, layers : int):
        with self.lock: #To prevent values being updated while another thread is updating it
            self.canvasArea = area
            self.layers = layers

    def prep_log(self, infoSent : threading.Event, terminate : threading.Event, infoDeque : deque):
        try:
            with self.lock:
                conn = self.get_connection()
                cursor = conn.cursor()
                with self.process.oneshot():
                    cpu = self.process.cpu_percent(interval=None)/(psutil.cpu_count())
                    memory = list(self.process.memory_info())
                    rss = memory[0]
                    vms = memory[1]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    "INSERT INTO performance (timestamp, cpu_usage, rss, vms, action, pixels_changed, canvas_area, layers) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (timestamp, cpu, rss, vms, "preparing action", 0, self.canvasArea, self.layers)
                )
                conn.commit()
                print(f"Action: preparing action | Pixels: 0 | Canvas Size: {self.canvasArea} | Layers: {self.layers} | CPU: {cpu}% | RSS: {rss} | VMS: {vms}")
                conn.close
                while not (infoSent.is_set() or terminate.is_set()):
                    time.sleep(1)
                if terminate.is_set():
                    return
                self.log_action(infoDeque.pop(), infoDeque.pop())
        except Exception as e:
            print(f"DB ERROR: {e}")

    def log_action(self, action, pixels_changed=0):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            with self.process.oneshot():
                cpu = self.process.cpu_percent(interval=None)/(psutil.cpu_count())
                memory = list(self.process.memory_info())
                rss = memory[0]
                vms = memory[1]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO performance (timestamp, cpu_usage, rss, vms, action, pixels_changed, canvas_area, layers) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (timestamp, cpu, rss, vms, action, pixels_changed, self.canvasArea, self.layers)
            )
            conn.commit()
            print(f"Action: preparing action | Pixels: 0 | Canvas Size: {self.canvasArea} | Layers: {self.layers} | CPU: {cpu}% | RSS: {rss} | VMS: {vms}")
            conn.close
        except Exception as e:
            print(f"DB ERROR: {e}")

    def log_cpu(self):
        self.setup_db()
        conn = self.get_connection()
        cursor = conn.cursor()

        while True:
            try:
                with self.lock:
                    with self.process.oneshot():
                        cpu = self.process.cpu_percent(interval=None)/(psutil.cpu_count())
                        memory = list(self.process.memory_info())
                        rss = memory[0]
                        vms = memory[1]
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute(
                    "INSERT INTO performance (timestamp, cpu_usage, rss, vms, action, pixels_changed, canvas_area, layers) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (timestamp, cpu, rss, vms, "idle", 0, self.canvasArea, self.layers)
                    )
                    conn.commit()
                    print(f"CPU: {cpu}%, | RSS: {rss} | VMS: {vms} at {timestamp}")
            except Exception as e:
                print(f"DB ERROR: {e}")
            time.sleep(1)