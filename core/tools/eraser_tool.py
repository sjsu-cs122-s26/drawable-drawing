from typing import override
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from core.tools.base_tool import BaseTool

class EraserTool(BaseTool):
    def __init__(self):
        self.eraser_width = 20

    def _erase(self, canvas, point):
        painter = QPainter(canvas.currentLayer.image)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.setPen(Qt.NoPen)
        half = self.eraser_width // 2
        painter.drawEllipse(point.x() - half, point.y() - half, self.eraser_width, self.eraser_width)
        painter.end()
        canvas.update()

    @override
    def on_mouse_press(self, canvas, event):
        self._erase(canvas, event.position().toPoint())

    @override
    def on_mouse_move(self, canvas, event):
        self._erase(canvas, event.position().toPoint())