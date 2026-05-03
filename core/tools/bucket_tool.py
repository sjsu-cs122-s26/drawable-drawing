import numpy as np
from scipy import ndimage
from typing import override
from core.tools.base_tool import BaseTool
from PySide6.QtGui import QImage

class BucketTool(BaseTool):
    @override
    def on_mouse_press(self, canvas, event):
        # 1. Capture the image and ensure it's in a predictable 32-bit format
        img = canvas.currentLayer.image
        if img.format() != QImage.Format.Format_RGBA8888:
            img = img.convertToFormat(QImage.Format.Format_RGBA8888)
            canvas.currentLayer.image = img

        point = event.position().toPoint()
        width, height = img.width(), img.height()
        
        if not img.rect().contains(point):
            canvas.finishTest("bucket", 0)

        ptr = img.bits()
        stride = img.bytesPerLine()
        arr = np.frombuffer(ptr, np.uint8).reshape((height, stride // 4, 4))
        arr = arr[:, :width, :]

        target_color = arr[point.y(), point.x()].astype(np.int32).copy()
        
        fill_color = np.array([
            canvas.color.red(), 
            canvas.color.green(), 
            canvas.color.blue(), 
            canvas.color.alpha()
        ], dtype=np.uint8)

        if np.array_equal(target_color.astype(np.uint8), fill_color):
            canvas.finishTest("bucket", 0)

        diff = arr.astype(np.int32) - target_color
        dist_sq = np.sum(diff**2, axis=2)
        
        mask = dist_sq <= (canvas.bucket_tolerance ** 2)

        structure = [[0, 1, 0],
                     [1, 1, 1],
                     [0, 1, 0]]
        
        labels, _ = ndimage.label(mask, structure=structure)
        
        target_label = labels[point.y(), point.x()]
        
        if target_label == 0:
            canvas.finishTest("bucket", 0)

        arr[labels == target_label] = fill_color

        changed_mask = (labels == target_label)
        pixels_changed = np.sum(changed_mask)
        canvas.update()
        canvas.finishTest("bucket", pixels_changed)