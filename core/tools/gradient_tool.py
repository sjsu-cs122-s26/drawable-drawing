from PySide6.QtGui import QPainter, QLinearGradient, QBrush
from PySide6.QtCore import QPoint

from core.tools.base_tool import BaseTool
from tests.cpu_test import log_action


class GradientTool(BaseTool):
    def __init__(self):
        self.start_point = None
        self.end_point = None

    def on_mouse_press(self, canvas, event):
        self.start_point = event.position().toPoint()
        self.end_point = None

    def on_mouse_move(self, canvas, event):
        self.end_point = event.position().toPoint()
        canvas.update()

    def on_mouse_release(self, canvas, event):
        self.end_point = event.position().toPoint()
        self.apply_gradient(canvas)

    def apply_gradient(self, canvas):
        if self.start_point is None or self.end_point is None:
            return

        gradient = QLinearGradient(self.start_point, self.end_point)

        gradient.setColorAt(0.0, canvas.primary_color)
        gradient.setColorAt(1.0, canvas.secondary_color)

        painter = QPainter(canvas.currentLayer.image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(
            canvas.currentLayer.image.rect(),
            QBrush(gradient)
        )

        painter.end()
        canvas.update()

        width = canvas.currentLayer.image.width()
        height = canvas.currentLayer.image.height()
        log_action("gradient", width * height)