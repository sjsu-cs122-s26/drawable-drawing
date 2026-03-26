import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget, QPushButton, QFileDialog, QApplication, QMainWindow, QLabel
from PySide6.QtGui import QPixmap
class Drawable(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drawable")
        self.openFileButton = QPushButton("Open File")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.openFileButton)
        self.openFileButton.clicked.connect(self.openFile)
    @QtCore.Slot()
    def openFile(self):
        dialog = QFileDialog(self)
        dialog.setNameFilter(("Images (*.png *.jpg)")) #temporary feature to display images. will later be updated to load a previously saved QPainter state
        if not dialog.exec():
            return
        fileName = dialog.selectedFiles()[0]
        label = QLabel(self)
        label.setPixmap(QPixmap(fileName))
        self.layout.addWidget(label)
        

if __name__=="__main__":
    app=QApplication([])
    widget=Drawable()
    widget.resize(800,500)
    widget.show()

    sys.exit(app.exec())