from typing import override
from collections import deque

from widgets.tools.base_tool import BaseTool

class BucketTool(BaseTool):
    @override
    def on_mouse_press(self, canvas, event):
        start_point = event.position().toPoint()
        x, y = start_point.x(), start_point.y()
        
        if not canvas.image.rect().contains(start_point):
            return

        target_color = canvas.image.pixel(x, y)
        fill_color = canvas.color.rgba()

        if target_color == fill_color:
            return

        width = canvas.image.width()
        height = canvas.image.height()
        
        stack = [(x, y)]
        while stack:
            curr_x, curr_y = stack.pop()

            lx = curr_x
            while lx >= 0 and canvas.image.pixel(lx, curr_y) == target_color:
                canvas.image.setPixel(lx, curr_y, fill_color)
                lx -= 1
            lx += 1

            rx = curr_x + 1
            while rx < width and canvas.image.pixel(rx, curr_y) == target_color:
                canvas.image.setPixel(rx, curr_y, fill_color)
                rx += 1
            rx -= 1

            if curr_y > 0:
                self._scan_line(lx, rx, curr_y - 1, stack, canvas, target_color)
            if curr_y < height - 1:
                self._scan_line(lx, rx, curr_y + 1, stack, canvas, target_color)

        canvas.update()

    def _scan_line(self, lx, rx, y, stack, canvas, target_color):
        added_seed = False
        for x in range(lx, rx + 1):
            if canvas.image.pixel(x, y) == target_color:
                if not added_seed:
                    stack.append((x, y))
                    added_seed = True
            else:
                added_seed = False
            
