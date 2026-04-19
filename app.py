from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QPushButton, QFileDialog, QLabel
from PySide6.QtGui import QPixmap

from widgets.color_wheel import ColorWheel
from widgets.canvas import Canvas

class Drawable(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drawable")
        self.openFileButton = QPushButton("Open File")
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.main_layout.addWidget(self.openFileButton)
        self.openFileButton.clicked.connect(self.openFile)

        self.canvas = Canvas()
        self.main_layout.addWidget(self.canvas)

        self.color_wheel = ColorWheel()
        self.color_wheel.color_change.connect(self.canvas.set_color)
        self.main_layout.addWidget(self.color_wheel)

    @QtCore.Slot()
    def openFile(self):
        dialog = QFileDialog(self)
        dialog.setNameFilter(("Images (*.png *.jpg)")) #temporary feature to display images. will later be updated to load a previously saved QPainter state
        if not dialog.exec():
            return
        fileName = dialog.selectedFiles()[0]
        label = QLabel(self)
        label.setPixmap(QPixmap(fileName))
        self.main_layout.addWidget(label)
    