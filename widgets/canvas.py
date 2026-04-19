from PySide6 import QtGui
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtCore import Qt, QPoint

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