from typing import override

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter, QImage
from PySide6.QtCore import Qt, QPoint

from core.tools.bucket_tool import BucketTool
from core.tools.pen_tool import PenTool
from widgets.layers import layer

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(100,100)
        self.resize(1920,1080)

        self.drawing = False
        self.resizing = False
        self.compositing = False

        self.color = QColor(Qt.GlobalColor.black)
        self.last_point = QPoint()
        self.defineTools()
        self.layers = []
        self.currentLayerIndex = -1
        
    def setColor(self, color):
        self.color = color

    def addLayer(self, layer):
        self.layers.append(layer)
        self.currentLayerIndex = len(self.layers)
        self.currentLayer = self.layers[self.currentLayerIndex-1]
        
    def deleteLayer(self, layer):
        self.layers.remove(layer)
        if self.currentLayer == layer:
            self.currentLayerIndex = 0
            self.currentLayer=self.layers[self.currentLayerIndex-1]
    
    def switchLayer(self, layer):
        self.currentLayer = layer
        self.currentLayerIndex = self.layers.index(layer)

    def clear(self):
        self.currentLayer.image.fill(Qt.GlobalColor.transparent)
        self.update()

    def defineTools(self):
        self.tools = {
            "pen": PenTool(),
            "bucket": BucketTool()
        }
        self.current_tool = None

    def setActiveTool(self, tool_name):
        if self.current_tool!=self.tools[tool_name]:
            self.current_tool = self.tools[tool_name]
        else: #If button currently active is toggled, then it is deactivated.
            self.current_tool = None

    def loadImage(self, path):
        loaded = QImage(path)
        self.currentLayer.image = loaded.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.update()

    def saveImage(self, path):
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        image = QImage(self.size(), QImage.Format.Format_ARGB32_Premultiplied)
        self.compositeImage(image, QPainter.CompositionMode_SourceOver)
        self.render(image, renderFlags=QWidget.RenderFlag.DrawChildren)
        image.save(path, "PNG")
        self.setAttribute(Qt.WA_TranslucentBackground, False)
    
    def compositeImage(self, renderTo, mode):
        if self.compositing or not hasattr(self, "currentLayer"):
            return
        self.compositing = True
        painter=QPainter(renderTo)
        painter.setCompositionMode(mode)
        painter.fillRect(self.rect(), Qt.transparent)
        for layer in reversed(self.layers):
            painter.setOpacity(layer.opacity)
            painter.drawImage(self.rect(), layer.image, self.layers[0].image.rect())
        painter.setOpacity(0)
        painter.end
        self.compositing = False

    @override
    def paintEvent(self, event):
        self.compositeImage(self, QPainter.CompositionMode_SourceOver)

    @override
    def resizeEvent(self, event):
        if self.resizing:
            return
        self.resizing = True
        for layer in self.layers:
            original_image = layer.image
            new_image = QImage(event.size(), QImage.Format.Format_ARGB32)
            new_image.fill(Qt.GlobalColor.transparent)
            painter = QPainter(new_image)
            painter.drawImage(0, 0, original_image)
            painter.end()
            layer.image = new_image
        self.resizing = False

    @override
    def showEvent(self, event):
        super().showEvent(event)

    @override
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.current_tool:
            self.drawing = True
            self.last_point = event.position().toPoint()
            self.current_tool.on_mouse_press(self, event)
    
    @override
    def mouseMoveEvent(self, event):
        if self.drawing and (event.buttons() & Qt.MouseButton.LeftButton) and self.current_tool:
            self.current_tool.on_mouse_move(self, event)

    @override
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.current_tool:
            self.drawing = False
            self.current_tool.on_mouse_release(self, event)