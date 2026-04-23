from typing import override

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter, QImage, QPixmap
from PySide6.QtCore import Qt, QPoint, Signal

from core.tools.bucket_tool import BucketTool
from core.tools.pen_tool import PenTool

class Layer(QWidget):
    layer_updated = Signal()
    def __init__(self):
        super().__init__()
        self.setMinimumSize(100,100)
        self.resize(1920,1080)
        self.image = QImage(self.size(), QImage.Format.Format_ARGB32)
        self.image.fill(Qt.GlobalColor.transparent)
        self.opacity=1

    def clear(self):
        self.image.fill(Qt.GlobalColor.transparent)
        self.update()
        self.layer_updated.emit()
    
    def updateOpacity(self, opacity):
        self.opacity = opacity
        self.layer_updated.emit()

    @override
    def paintEvent(self, event):
        QPainter(self).drawImage(self.rect(), self.image, self.image.rect())
        self.layer_updated.emit()

    @override
    def showEvent(self, event):
        if self.image.isNull():
            self.image = QImage(self.size(), QImage.Format.Format_ARGB32)
            self.image.fill(Qt.GlobalColor.transparent)
        super().showEvent(event)