from typing import override

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter, QImage
from PySide6.QtCore import Qt, QPoint

from core.tools.bucket_tool import BucketTool
from core.tools.pen_tool import PenTool
from core.tools.base_tool import BaseTool

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(100,100)
        self.resize(800,400)
        self.image = QImage(self.size(), QImage.Format.Format_ARGB32)
        self.image.fill(Qt.GlobalColor.transparent)
        self.color = QColor(Qt.GlobalColor.black)
        self.last_point = QPoint()
        self.drawing = False
        self.define_tools()
        
    def set_color(self, color):
        self.color = color

    def clear(self):
        self.image.fill(Qt.GlobalColor.transparent)
        self.update()

    def define_tools(self):
        self.tools = {
            "pen": PenTool(),
            "bucket": BucketTool()
        }
        self.current_tool = None

    def set_active_tool(self, tool_name):
        if self.current_tool!=self.tools[tool_name]:
            self.current_tool = self.tools[tool_name]
        else: #If button currently active is toggled, then it is deactivated.
            self.current_tool = None

    def load_image(self, path):
        loaded = QImage(path)
        self.image = loaded.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.update()

    def save_image(self, path):
        image = QImage(self.size(), QImage.Format.Format_ARGB32)
        self.render(image)
        image.save(path)

    @override
    def paintEvent(self, event):
        QPainter(self).drawImage(self.rect(), self.image, self.image.rect())

    @override
    def resizeEvent(self, event):
        original_image = self.image
        new_image = QImage(event.size(), QImage.Format.Format_ARGB32)
        new_image.fill(Qt.GlobalColor.transparent)
        painter = QPainter(new_image)
        painter.drawImage(0, 0, original_image)
        painter.end()
        self.image = new_image

    @override
    def showEvent(self, event):
        if self.image.isNull():
            self.image = QImage(self.size(), QImage.Format.Format_ARGB32)
            self.image.fill(Qt.GlobalColor.transparent)
        super().showEvent(event)

    @override
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.current_tool:
            self.drawing = True
            self.last_point = event.position().toPoint()
            self.current_tool.on_mouse_press(self, event)
    
    @override
    def mouseMoveEvent(self, event):
        if self.drawing and (event.buttons() & Qt.MouseButton.LeftButton) and self.current_tool:
            self.current_tool.on_mouse_move(self, event)

    @override
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.current_tool:
            self.drawing = False
            self.current_tool.on_mouse_release(self, event)