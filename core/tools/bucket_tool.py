from typing import override

from core.tools.base_tool import BaseTool
from PySide6.QtGui import QColor
from tests.cpu_test import log_action

class BucketTool(BaseTool):
    @override
    def on_mouse_press(self, canvas, event):
        start_point = event.position().toPoint()
        x, y = start_point.x(), start_point.y()
        
        if not canvas.currentLayer.image.rect().contains(start_point):
            return

        self.target_color = canvas.currentLayer.image.pixelColor(x, y)
        self.fill_color = canvas.color
        self.tolerance = canvas.bucket_tolerance
        if self.fill_color == self.target_color:
            return

        width = canvas.currentLayer.image.width()
        height = canvas.currentLayer.image.height()
        
        pixels_changed = 0

        stack = [(x, y)]
        while stack:
            curr_x, curr_y = stack.pop()
            lx = curr_x
            while lx >= 0 and self.checkDistance(canvas.currentLayer.image.pixelColor(lx, curr_y)):
                canvas.currentLayer.image.setPixelColor(lx, curr_y, self.fill_color)
                lx -= 1
                pixels_changed += 1
            lx += 1

            rx = curr_x + 1
            while rx < width and self.checkDistance(canvas.currentLayer.image.pixelColor(rx, curr_y)):
                canvas.currentLayer.image.setPixelColor(rx, curr_y, self.fill_color)
                rx += 1
                pixels_changed += 1
            rx -= 1

            if curr_y > 0:
                self._scan_line(lx, rx, curr_y - 1, stack, canvas)
            if curr_y < height - 1:
                self._scan_line(lx, rx, curr_y + 1, stack, canvas)

        canvas.update()
        log_action("bucket", pixels_changed)

    def _scan_line(self, lx, rx, y, stack, canvas):
        added_seed = False
        for x in range(lx, rx + 1):
            if self.checkDistance(canvas.currentLayer.image.pixelColor(x, y)):
                if not added_seed:
                    stack.append((x, y))
                    added_seed = True
            else:
                added_seed = False

    def checkDistance(self, color1: QColor):
        return round(((color1.red() - self.target_color.red())**2
                      +(color1.blue() - self.target_color.blue())**2
                      +(color1.green() - self.target_color.green())**2
                      +(color1.alpha() - self.target_color.alpha())**2)
                      **(1/2))<=self.tolerance