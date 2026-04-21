from typing import override

from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox, QButtonGroup
from PySide6.QtCore import Qt, Signal

from widgets.layers.layer_menu_static import LayerMenuStatic
from widgets.layers.layer_block import LayerBlock
from widgets.layers.layer import Layer

class LayerMenu(QWidget):
    delete_layer_validated = Signal(Layer)
    add_layer = Signal(Layer)
    switch_layer = Signal(Layer)

    def __init__(self):
        super().__init__()
        self.lifetime_layers = 0
        self.setFixedWidth(250)
        self.layer_blocks = []
        self.layout = QVBoxLayout(self)
        self.layer_menu_static = LayerMenuStatic()
        self.layout.addWidget(self.layer_menu_static)
        self.setFixedHeight(100)
        self.setMinimumHeight(self.layer_menu_static.height()+self.layer_menu_static.contentsMargins().top()+self.layer_menu_static.contentsMargins().bottom())
        self.layer_menu_static.add_layer.connect(self.addLayer)
        self.group = QButtonGroup()
        self.group.setExclusive(True)

    def addLayer(self):
        self.lifetime_layers+=1
        newLayer = Layer()
        newLayerBlock = LayerBlock("Layer_" + str(self.lifetime_layers), newLayer)
        selfY = self.height()+self.contentsMargins().top()+self.contentsMargins().bottom()
        newLayerBlockY = newLayerBlock.height()+newLayerBlock.contentsMargins().top()+newLayerBlock.contentsMargins().bottom()
        spacing = 22
        self.setMinimumHeight(selfY+newLayerBlockY+spacing)
        self.layer_blocks.append(newLayerBlock)
        newLayerBlock.delete_layer.connect(self.deleteLayer)
        self.group.addButton(newLayerBlock)
        newLayerBlock.clicked.connect(self.switchActiveLayer)
        self.layout.addWidget(newLayerBlock)
        self.add_layer.emit(newLayer)
        newLayerBlock.setChecked(True)

    def deleteLayer(self, Layer):
        if len(self.layer_blocks)<=1:
            message = QMessageBox(self)
            message.setText("The layer could not be deleted because there must always be at least one layer.")
            message.exec()
            return
        self.layer_blocks.remove(self.sender())
        if self.sender().isChecked():
            self.layer_blocks[len(self.layer_blocks)-1].setChecked(True)
        self.layout.removeWidget(self.sender())
        self.group.removeButton(self.sender())
        self.delete_layer_validated.emit(Layer)
        self.sender().hide()
    
    def switchActiveLayer(self):
        self.switch_layer.emit(self.sender().layer)