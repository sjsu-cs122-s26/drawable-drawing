import sys
from PySide6.QtWidgets import QApplication
from app import Drawable 

def main():
    app = QApplication([])
    widget = Drawable()
    widget.resize(800, 500)
    widget.show() 
    sys.exit(app.exec())

if __name__ == "__main__":
    main()