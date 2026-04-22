from typing import override

from PySide6.QtGui import QPainter, QPen, QBrush, QPolygon
from PySide6.QtCore import Qt, QRect, QPoint

from core.tools.base_tool import BaseTool

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
        painter = QPainter(canvas.currentLayer.image)
        painter.setPen(QPen(canvas.color, 2, Qt.PenStyle.SolidLine))
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
        canvas.update()

    def draw_preview(self, canvas):
        painter = QPainter(canvas)
        painter.setPen(QPen(canvas.color, 2, Qt.PenStyle.DashLine))
        painter.setBrush(QBrush(canvas.color))
        rect = QRect(self.start_point, self.current_point).normalized()
        if self.shape == "rectangle":
            painter.drawRect(rect)
        elif self.shape == "ellipse":
            painter.drawEllipse(rect)
        elif self.shape == "line":
            painter.drawLine(self.start_point, self.current_point)
        elif self.shape == "triangle":
            triangle = QPolygon([
                self.start_point,
                QPoint(self.current_point.x(), self.start_point.y()),
                QPoint((self.start_point.x() + self.current_point.x()) // 2, self.current_point.y())
            ])
            painter.drawPolygon(triangle)
        painter.end()