import sys
import threading
from PySide6.QtWidgets import QApplication
from app import Drawable 
from tests.cpu_test import log_cpu

def main():
    app = QApplication([])
    widget = Drawable()
    widget.showMaximized()
    
    thread = threading.Thread(target=log_cpu, daemon=True)
    thread.start()

    sys.exit(app.exec())
    
    

if __name__ == "__main__":
    main()