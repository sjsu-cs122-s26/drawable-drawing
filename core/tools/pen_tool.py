from typing import override
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt
from core.tools.base_tool import BaseTool
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel

class PenTool(BaseTool):
    def __init__(self):
        self.pen_width = 3
        self.pixels_changed = 0
        self.sidebar = self._create_sidebar()
    
    def _create_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(60)
        layout = QVBoxLayout(sidebar)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.width_label = QLabel("3")
        self.width_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.width_label)

        slider = QSlider(Qt.Orientation.Vertical)
        slider.setRange(1, 100)
        slider.setValue(self.pen_width)
        slider.valueChanged.connect(self._on_width_changed)
        layout.addWidget(slider)

        return sidebar

    def _on_width_changed(self, value):
        self.pen_width = value
        self.width_label.setText(str(value))
    
    @override
    def on_mouse_move(self, canvas, event):
        painter = QPainter(canvas.currentLayer.image)
        painter.setPen(QPen(canvas.color, self.pen_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.drawLine(canvas.last_point, event.position().toPoint())
        painter.end()

        self.pixels_changed += self.pen_width * self.pen_width

        canvas.last_point = event.position().toPoint()
        canvas.update()

    @override
    def on_mouse_release(self, canvas, event):
        canvas.finishTest("drawing", self.pixels_changed)
        self.pixels_changed = 0