import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget, QPushButton, QFileDialog, QApplication, QMainWindow, QLabel
from PySide6.QtGui import QPixmap, QColor, QPainter, QPen
from PySide6.QtCore import Qt, QPoint
from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtWidgets import QColorDialog

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
        
class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.image = QtGui.QImage(800, 500, QtGui.QImage.Format.Format_ARGB32)
        self.image.fill(Qt.GlobalColor.white)
        self.last_point = QPoint()
        self.drawing = False
        self.pen_color = QColor(Qt.GlobalColor.black)
        self.pen_width = 3

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()
    
    def mouseMoveEvent(self, event):
        if self.drawing and (event.buttons() & Qt.MouseButton.LeftButton):
            painter = QPainter(self.image)
            painter.setPen(QPen(self.pen_color, self.pen_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawLine(self.last_point, event.position().toPoint())
            self.last_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        QPainter(self).drawImage(self.rect(), self.image, self.image.rect())

    def set_color(self, color):
        self.pen_color = color


class ColorWheel(QWidget):
    color_change = Signal(QColor)
    
    def __init__(self):
        super().__init__()
        self.setMaximumHeight(30)
        self.current_color = QColor(Qt.GlobalColor.black)

        self.color_button = QPushButton("Choose Color")
        self.color_button.setFixedSize(150, 30)
        self.color_button.clicked.connect(self.choose_color)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(1,1,1,1)
        layout.addWidget(self.color_button)
    
    def choose_color(self):
        color = QColorDialog.getColor(self.current_color, self)
        if color.isValid():
            self.current_color = color
            self.color_change.emit(color)

if __name__=="__main__":
    app = QApplication([])
    widget = Drawable()
    widget.resize(800, 500)
    widget.show()
    sys.exit(app.exec())

    