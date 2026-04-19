from typing import override

from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt

from widgets.tools.base_tool import BaseTool

class PenTool(BaseTool):
    def __init__(self):
        super().__init__()
        self.pen_width = 3
    
    @override
    def on_mouse_move(self, canvas, event):
        painter = QPainter(canvas.image)
        painter.setPen(QPen(canvas.color, self.pen_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.drawLine(canvas.last_point, event.position().toPoint())
        canvas.last_point = event.position().toPoint()
        canvas.update()
