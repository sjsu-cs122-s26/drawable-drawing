from typing import override

from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QButtonGroup
from PySide6.QtCore import Qt, Signal

from core.snapshot import Snapshot
from widgets.layers.layer_menu_static import LayerMenuStatic
from widgets.layers.layer_block import LayerBlock
from widgets.layers.layer import Layer

class LayerMenu(QWidget):
    delete_layer_validated = Signal(Layer)
    add_layer = Signal(Layer)
    switch_layer = Signal(Layer)
    swap_layer = Signal(int, int)
    save_snapshot = Signal()
    
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
        
        referenceBlock = LayerBlock("Reference", Layer())
        self.heightPerBlock = referenceBlock.height() + referenceBlock.contentsMargins().bottom() + referenceBlock.contentsMargins().top() + 22

    def addLayer(self):
        self.save_snapshot.emit()
        self.lifetime_layers+=1
        newLayer = Layer()
        newLayerBlock = LayerBlock("Layer_" + str(self.lifetime_layers), newLayer)
        self.addLayerMain(newLayerBlock)
        self.addLayerCleanup()
        self.add_layer.emit(newLayer)
    
    def addLayerMain(self, newLayerBlock : LayerBlock):
        self.layer_blocks.append(newLayerBlock)
        newLayerBlock.delete_layer.connect(self.deleteLayer)
        newLayerBlock.clicked.connect(self.switchActiveLayer)
        newLayerBlock.update_block.connect(self.update)
        newLayerBlock.move_block.connect(self.moveLayerBlock)
        newLayerBlock.save_snapshot.connect(self.save_snapshot.emit)
        self.group.addButton(newLayerBlock)
        self.layout.addWidget(newLayerBlock)
        newLayerBlock.setChecked(True)

    def addLayerCleanup(self):
        self.setFixedHeight(self.height()+self.heightPerBlock)

    def deleteLayer(self, Layer):
        if len(self.layer_blocks)<=1:
            message = QMessageBox(self)
            message.setText("The layer could not be deleted because there must always be at least one layer.")
            message.exec()
            return
        self.save_snapshot.emit()
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
        toDelete.hide()
        self.setFixedHeight(self.height()-self.heightPerBlock)
    
    def switchActiveLayer(self):
        self.switch_layer.emit(self.sender().layer)

    def moveLayerBlock(self, int):
        sender = self.sender()
        senderDex = self.layer_blocks.index(sender)
        swapDex = senderDex+int
        
        if not self.checkMoveValidity(swapDex):
            return
        self.save_snapshot.emit()
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

    def setState(self, snapshot: Snapshot, layers : list):
        self.lifetime_layers = snapshot.lifetime_layers
        self.setBlocksToCount(snapshot)
        for menuBlock, snapshotBlock, layer in zip(self.layer_blocks, snapshot.blocks, layers):
            menuBlock.setState(layer, snapshotBlock["name"])
        self.update()

    def setBlocksToCount(self, snapshot: Snapshot):
        buttonList = self.group.buttons()
        if len(buttonList)<len(snapshot.blocks):
            for block in snapshot.blocks[len(buttonList):], :
                newLayerBlock = LayerBlock(layerName = block[0]["name"])
                self.layer_blocks.append(newLayerBlock)
                newLayerBlock.delete_layer.connect(self.deleteLayer)
                newLayerBlock.clicked.connect(self.switchActiveLayer)
                newLayerBlock.update_block.connect(self.update)
                newLayerBlock.move_block.connect(self.moveLayerBlock)
                newLayerBlock.save_snapshot.connect(self.save_snapshot.emit)
                self.group.addButton(newLayerBlock)
                self.layout.addWidget(newLayerBlock)
        self.group.buttons()[snapshot.currentLayerIndex].setChecked(True)
        if len(buttonList)>len(snapshot.blocks):
            for block in buttonList[len(snapshot.blocks):]:
                block.delete_layer.disconnect(self.deleteLayer)
                block.clicked.disconnect(self.switchActiveLayer)
                block.update_block.disconnect(self.update)
                block.move_block.disconnect(self.moveLayerBlock)
                block.save_snapshot.disconnect(self.save_snapshot.emit)
                self.group.removeButton(block)
                self.layer_blocks.remove(block)
                self.layout.removeWidget(block)
                block.hide()
        self.setFixedHeight(self.layer_menu_static.height()+50+len(self.group.buttons())*self.heightPerBlock)
