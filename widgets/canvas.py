from typing import override
from collections import deque

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter, QImage
from PySide6.QtCore import Qt, QPoint, Signal

from core.tools.bucket_tool import BucketTool
from core.tools.pen_tool import PenTool
from core.tools.shapes_tool import ShapesTool
from core.tools.eraser_tool import EraserTool
from core.snapshot import Snapshot
from widgets.layers.layer import Layer

class Canvas(QWidget):
    save_snapshot = Signal()
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

        self.bucket_tolerance = 0
        
    def setColor(self, color):
        self.color = color

    def addLayer(self, layer : Layer):
        layer.image = QImage(self.size(), QImage.Format.Format_ARGB32)
        layer.image.fill(Qt.GlobalColor.transparent)
        self.layers.append(layer)
        self.currentLayerIndex = len(self.layers)-1
        self.currentLayer = self.layers[self.currentLayerIndex]
        layer.layer_updated.connect(lambda : self.update())
        
    def deleteLayer(self, layer):
        self.layers.remove(layer)
        if self.currentLayer == layer:
            self.currentLayerIndex = len(self.layers)-1
            self.currentLayer=self.layers[self.currentLayerIndex]
        self.update()
    
    def switchActiveLayer(self, layer):
        self.currentLayer = layer
        self.currentLayerIndex = self.layers.index(layer)
    
    def swapLayerOrder(self, index1, index2):
        layerHolder = self.layers[index1]
        self.layers[index1]=self.layers[index2]
        self.layers[index2]=layerHolder
        if index1 == self.currentLayerIndex:
            self.currentLayerIndex=index2
        elif index2 == self.currentLayerIndex:
            self.currentLayerIndex=index1
        self.update()

    def clear(self):
        self.save_snapshot.emit()
        for layer in self.layers:
            layer.clear()
        self.update()

    def defineTools(self):
        self.shapes_tool = ShapesTool()
        self.tools = {
            "pen": PenTool(),
            "eraser": EraserTool(),
            "bucket": BucketTool(),
            "shapes": self.shapes_tool
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
    
    def setState(self, snapshot : Snapshot):
        self.resize(snapshot.canvasSize)
        while(len(self.layers)<len(snapshot.blocks)):
            layer = Layer()
            self.layers.append(layer)
            layer.layer_updated.connect(lambda : self.update())
        while (len(self.layers)>len(snapshot.blocks)):
            layer : Layer = self.layers.pop()
            layer.layer_updated.disconnect()
        for layer, block in zip(self.layers, snapshot.blocks):
            layer.image = block["image"]
            layer.opacity = block["opacity"]
        self.currentLayerIndex : int = snapshot.currentLayerIndex
        self.currentLayer : Layer = self.layers[self.currentLayerIndex]
        self.update()
        return self.layers

    @override
    def paintEvent(self, event):
        self.compositeImage(self, QPainter.CompositionMode_SourceOver)
        if self.drawing and self.current_tool == self.shapes_tool:
            self.current_tool.draw_preview(self)

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
            self.save_snapshot.emit()
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