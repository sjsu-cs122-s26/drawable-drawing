from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt, Signal

from widgets.layers.layer_menu_static import LayerMenuStatic
from widgets.layers.layer_block import LayerBlock
from widgets.layers.layer import Layer

class LayerMenu(QWidget):
    delete_layer_validated = Signal(Layer)
    add_layer = Signal(Layer)
    switch_layer = Signal(Layer)
    update_opacity_validated = Signal(Layer)

    def __init__(self):
        super().__init__()
        self.lifetime_layers = 0
        self.setMaximumWidth(400)
        self.layer_blocks = []
        self.layout = QVBoxLayout(self)
        self.layer_menu_static = LayerMenuStatic()
        self.layout.addWidget(self.layer_menu_static)
        self.layer_menu_static.add_layer.connect(self.addLayer)

    def addLayer(self):
        self.lifetime_layers+=1
        newLayer = Layer()
        newLayerBlock = LayerBlock("Layer_" + str(self.lifetime_layers), newLayer)

        self.layer_blocks.append(newLayerBlock)
        newLayerBlock.delete_layer.connect(self.deleteLayer)
        newLayerBlock.update_opacity.connect(self.updateOpacity)
        newLayerBlock.clicked.connect(self.switchActiveLayer)
        self.layout.addWidget(newLayerBlock)
        self.add_layer.emit(newLayer)

    def deleteLayer(self, Layer):
        if len(self.layer_blocks)<=1:
            message = QMessageBox(self)
            message.setText("The layer could not be deleted because there must always be at least one layer.")
            message.exec()
            return
        self.layer_blocks.remove(self.sender())
        self.layout.removeWidget(self.sender())
        self.delete_layer_validated.emit(Layer)
    
    def switchActiveLayer(self):
        self.switch_layer.emit(self.sender().layer)

    def updateOpacity(self, Layer):
        self.update_opacity_validated.emit(Layer)

    