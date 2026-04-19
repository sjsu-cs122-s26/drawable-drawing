from typing import override

from PySide6 import QtGui
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter, QImage
from PySide6.QtCore import Qt, QPoint

from widgets.tools.PenTool import PenTool

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.image = QImage()
        self.color = QColor(Qt.GlobalColor.black)
        self.last_point = QPoint()
        self.drawing = False
        self.current_tool = PenTool()
        print(self.image.size())
        print(self.rect().size())
        
    def setColor(self, color):
        self.color = color

    def defineTools(self):
        self.tools = {
            "pen": PenTool()
        }
        self.current_tool = self.tools["pen"]

    @override
    def paintEvent(self, event):
        QPainter(self).drawImage(self.rect(), self.image, self.image.rect())
    
    @override
    def showEvent(self, event):
        if self.image.isNull():
            self.image = QImage(self.size(), QImage.Format.Format_ARGB32)
            self.image.fill(Qt.GlobalColor.white)
        super().showEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()
            self.current_tool.onMousePress(self, event)
    
    def mouseMoveEvent(self, event):
        if self.drawing and (event.buttons() & Qt.MouseButton.LeftButton):
            self.current_tool.onMouseMove(self, event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False
            self.current_tool.onMouseRelease(self, event)