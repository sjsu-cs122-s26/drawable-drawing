from typing import override

from PySide6.QtGui import QPainter, QPen, QBrush, QPolygon
from PySide6.QtCore import Qt, QRect, QPoint

from core.tools.base_tool import BaseTool
from tests.cpu_test import log_action

class ShapesTool(BaseTool):
    def __init__(self):
        self.shape = "rectangle"
        self.start_point = QPoint()
        self.current_point = QPoint()

    def setShape(self, shape):
        self.shape = shape.lower()

    @override
    def on_mouse_press(self, canvas, event):
        self.start_point = event.position().toPoint()
        self.current_point = self.start_point

    @override
    def on_mouse_move(self, canvas, event):
        self.current_point = event.position().toPoint()
        canvas.update()

    @override
    def on_mouse_release(self, canvas, event):
        end_point = event.position().toPoint()
        self.draw_shape(canvas, canvas.currentLayer.image, end_point, Qt.PenStyle.SolidLine)
        canvas.update()

        rect = QRect(self.start_point, end_point).normalized()
        pixels_changed = rect.width() * rect.height()
        log_action(f"shape_{self.shape}", pixels_changed)

    def draw_preview(self, canvas):
        self.draw_shape(canvas, canvas, self.current_point, Qt.PenStyle.DashLine)
    
    def draw_shape(self, canvas, drawTo, end_point, style):
        painter = QPainter(drawTo)
        painter.setPen(QPen(canvas.color, 2, style))
        painter.setBrush(QBrush(canvas.color))

        rect = QRect(self.start_point, end_point).normalized()

        if self.shape == "rectangle":
            painter.drawRect(rect)
        elif self.shape == "ellipse":
            painter.drawEllipse(rect)
        elif self.shape == "line":
            painter.drawLine(self.start_point, end_point)
        elif self.shape == "triangle":
            triangle = QPolygon([
                self.start_point,
                QPoint(end_point.x(), self.start_point.y()),
                QPoint((self.start_point.x() + end_point.x()) // 2, end_point.y())
            ])
            painter.drawPolygon(triangle)
        painter.end()