from typing import override
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt
from core.tools.base_tool import BaseTool

class EraserTool(BaseTool):
    def __init__(self):
        self.eraser_width = 20

    def _erase(self, canvas, point):
        painter = QPainter(canvas.currentLayer.image)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.setPen(QPen(Qt.GlobalColor.transparent, self.eraser_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.drawLine(canvas.last_point, point)
        canvas.last_point = point
        painter.end()
        canvas.update()

    @override
    def on_mouse_press(self, canvas, event):
        self._erase(canvas, event.position().toPoint())

    @override
    def on_mouse_move(self, canvas, event):
        self._erase(canvas, event.position().toPoint())