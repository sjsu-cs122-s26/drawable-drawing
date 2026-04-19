from PySide6.QtGui import QMouseEvent

from widgets.canvas import Canvas

class BaseTool:
    def on_mouse_press(self, canvas: Canvas, event:QMouseEvent): pass
    def on_mouse_move(self, canva: Canvas, event: QMouseEvent): pass
    def on_mouse_release(self, canvas: Canvas, event: QMouseEvent): pass