from typing import override

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter, QImage
from PySide6.QtCore import Qt, QPoint

from core.tools.bucket_tool import BucketTool
from core.tools.pen_tool import PenTool

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.image = QImage()
        self.color = QColor(Qt.GlobalColor.black)
        self.last_point = QPoint()
        self.drawing = False
        self.define_tools()
        
    def set_color(self, color):
        self.color = color

    def clear(self):
        self.image.fill(Qt.GlobalColor.white)
        self.update()

    def define_tools(self):
        self.tools = {
            "pen": PenTool(),
            "bucket": BucketTool()
        }
        self.current_tool = self.tools["pen"]

    def set_active_tool(self, tool_name):
        self.current_tool = self.tools[tool_name]

    @override
    def paintEvent(self, event):
        QPainter(self).drawImage(self.rect(), self.image, self.image.rect())
    
    @override
    def showEvent(self, event):
        if self.image.isNull():
            self.image = QImage(self.size(), QImage.Format.Format_ARGB32)
            self.image.fill(Qt.GlobalColor.white)
        super().showEvent(event)

    @override
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()
            self.current_tool.on_mouse_press(self, event)
    
    @override
    def mouseMoveEvent(self, event):
        if self.drawing and (event.buttons() & Qt.MouseButton.LeftButton):
            self.current_tool.on_mouse_move(self, event)

    @override
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False
            self.current_tool.on_mouse_release(self, event)