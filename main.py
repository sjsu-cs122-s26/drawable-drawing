import sys
import threading

from PySide6.QtWidgets import QApplication
from psutil import Process

from tests.performanceTest import CpuTest
from app import Drawable 

def main():
    cpuTest = CpuTest(Process())
    thread = threading.Thread(target=cpuTest.log_cpu, daemon=True)
    thread.start()
    
    app = QApplication([])
    widget = Drawable(cpuTest)
    widget.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()