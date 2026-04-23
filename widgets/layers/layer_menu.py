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
    swap_layer = Signal(int, int)

    def __init__(self):
        super().__init__()
        self.lifetime_layers = 0
        self.setFixedWidth(250)
        self.layer_blocks = []
        self.layout = QVBoxLayout(self)
        self.layer_menu_static = LayerMenuStatic()
        self.layout.addWidget(self.layer_menu_static)
        self.setFixedHeight(100)
        self.setFixedHeight(self.layer_menu_static.height()+50)
        self.layer_menu_static.add_layer.connect(self.addLayer)
        self.group = QButtonGroup()
        self.group.setExclusive(True)

    def addLayer(self):
        self.lifetime_layers+=1
        newLayer = Layer()
        newLayerBlock = LayerBlock("Layer_" + str(self.lifetime_layers), newLayer)
        self.addLayerMain(newLayerBlock)
        self.addLayerCleanup(newLayerBlock)
        self.add_layer.emit(newLayer)
    
    def addLayerMain(self, newLayerBlock):
        self.layer_blocks.append(newLayerBlock)
        newLayerBlock.delete_layer.connect(self.deleteLayer)
        self.group.addButton(newLayerBlock)
        newLayerBlock.clicked.connect(self.switchActiveLayer)
        newLayerBlock.update_block.connect(self.update)
        newLayerBlock.move.connect(self.moveLayerBlock)
        self.layout.addWidget(newLayerBlock)
        newLayerBlock.setChecked(True)

    def addLayerCleanup(self, newLayerBlock):
        baseY = self.height()+newLayerBlock.height()
        contentMargins = newLayerBlock.contentsMargins().bottom()+newLayerBlock.contentsMargins().top()
        spacing=22
        self.setFixedHeight(baseY+contentMargins+spacing)

    def deleteLayer(self, Layer):
        if len(self.layer_blocks)<=1:
            message = QMessageBox(self)
            message.setText("The layer could not be deleted because there must always be at least one layer.")
            message.exec()
            return
        self.delete_layer_validated.emit(Layer)
        toDelete = self.sender()
        self.deleteLayerMain(toDelete)
        self.deleteLayerCleanup(toDelete)
        
    def deleteLayerMain(self, toDelete):
        self.layer_blocks.remove(toDelete)
        if toDelete.isChecked():
            self.layer_blocks[len(self.layer_blocks)-1].setChecked(True)
        self.layout.removeWidget(toDelete)
        self.group.removeButton(toDelete)

    def deleteLayerCleanup(self, toDelete):
        baseY = self.height()-toDelete.height()
        contentMargins = toDelete.contentsMargins().bottom()+toDelete.contentsMargins().top()
        spacing=22
        self.setFixedHeight(baseY-contentMargins-spacing)
    
    def switchActiveLayer(self):
        self.switch_layer.emit(self.sender().layer)

    def moveLayerBlock(self, int):
        sender = self.sender()
        senderDex = self.layer_blocks.index(sender)
        swapDex = senderDex+int
        
        if not self.checkMoveValidity(swapDex):
            return
        self.moveLayerBlockMenu(senderDex, swapDex, sender)

        self.update()
        self.swap_layer.emit(senderDex, swapDex)
    
    def checkMoveValidity(self, swapDex):
        if swapDex<0: #swap location is invalid
            message = QMessageBox(self)
            message.setText("The layer could not be moved up because the layer is already at the top.")
            message.exec()
            return False
        if swapDex>len(self.layer_blocks)-1: #swap location is invalid
            message = QMessageBox(self)
            message.setText("The layer could not be moved down because the layer is already at the bottom.")
            message.exec()
            return False
        return True
    
    def moveLayerBlockMenu(self, senderDex, swapDex, sender):
        blockSender = self.layer_blocks[senderDex]
        blockSwap = self.layer_blocks[swapDex]
        self.layer_blocks[senderDex]=self.layer_blocks[swapDex]
        self.layer_blocks[swapDex]=sender
        self.layout.removeWidget(blockSender)
        self.layout.removeWidget(blockSwap)
        if swapDex > senderDex:
            self.layout.insertWidget(senderDex+1, blockSwap)
            self.layout.insertWidget(swapDex+1, blockSender)
        else:
            self.layout.insertWidget(swapDex+1, blockSender)
            self.layout.insertWidget(senderDex+1, blockSwap)
