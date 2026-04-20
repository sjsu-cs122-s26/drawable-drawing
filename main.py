import sys
from PySide6.QtWidgets import QApplication
from app import Drawable 

def main():
    app = QApplication([])
    widget = Drawable()
    widget.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()