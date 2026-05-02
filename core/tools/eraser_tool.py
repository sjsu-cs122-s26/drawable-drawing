from typing import override
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt
from core.tools.base_tool import BaseTool
from tests.cpu_test import log_action

class EraserTool(BaseTool):
    def __init__(self):
        self.eraser_width = 20
        self.pixels_changed = 0

    def _erase(self, canvas, point):
        painter = QPainter(canvas.currentLayer.image)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.setPen(QPen(Qt.GlobalColor.transparent, self.eraser_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.drawLine(canvas.last_point, point)
        canvas.last_point = point
        painter.end()
        canvas.update()

        self.pixels_changed += self.eraser_width * self.eraser_width

    @override
    def on_mouse_press(self, canvas, event):
        self.pixels_changed = 0
        self._erase(canvas, event.position().toPoint())

    @override
    def on_mouse_move(self, canvas, event):
        self._erase(canvas, event.position().toPoint())

    @override
    def on_mouse_release(self, canvas, event):
        log_action("erasing", self.pixels_changed)
        self.pixels_changed = 0