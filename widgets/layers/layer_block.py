from typing import override

from PySide6.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QSlider, QLabel
from PySide6.QtGui import QPixmap, QPainter, QPalette, QImage
from PySide6.QtCore import Signal, Qt, QBuffer, QIODevice

from widgets.layers.layer import Layer
from widgets.layers.layer_mini_image import MiniImage

class LayerBlock(QPushButton):
    delete_layer = Signal(Layer)
    update_block = Signal()
    move = Signal(int)

    def __init__(self, layerName: str, layer: Layer):
        super().__init__()
        self.setFixedSize(229, 125)
        self.layerName = layerName
        self.layer = layer
        self.layer.layer_updated.connect(self.updateLayer)

        topLayout = self.createTopLayout(layerName, layer)
        middleLayout = self.createMiddleLayout()
        bottomLayout = self.createBottomLayout()

        layout = QVBoxLayout(self)
        layout.addLayout(topLayout)
        layout.addLayout(middleLayout)
        layout.addLayout(bottomLayout)
    def createTopLayout(self, layerName, layer):
        layerDisplayName = QLabel()
        layerDisplayName.setText(layerName)
        self.image = MiniImage()
        self.image.setMaximumSize(128, 72)
        self.image_opacity=1
        self.pixmap = self.image.pixmap()
        self.image.setPixmap(QPixmap("media/drawable_icon.jpg"))

        self.move_up_button = QPushButton("Up")
        self.move_up_button.setMaximumSize(75, 25)
        self.move_up_button.clicked.connect(lambda x: self.move.emit(-1))
        self.move_down_button = QPushButton("Down")
        self.move_down_button.setMaximumSize(75, 25)
        self.move_down_button.clicked.connect(lambda x: self.move.emit(1))
        
        topLayout = QHBoxLayout()
        topRightLayout = QVBoxLayout()
        topRightLayout.addWidget(self.move_up_button)
        topRightLayout.addWidget(self.move_down_button)
        topLayout.addWidget(layerDisplayName)
        topLayout.addWidget(self.image)
        topLayout.addLayout(topRightLayout)
        return topLayout
    
    def createMiddleLayout(self):
        self.clear_layer_button = QPushButton("Clear layer")
        self.clear_layer_button.setMaximumSize(100, 25)
        self.clear_layer_button.clicked.connect(lambda: self.confirmAction("clear", self.layer.clear, None))
        self.delete_layer_button = QPushButton("Delete layer")
        self.delete_layer_button.setMaximumSize(100, 25)
        self.delete_layer_button.clicked.connect(lambda: self.confirmAction("delete", self.delete_layer.emit, self.layer))
        self.setCheckable(True)
        self.setStyleSheet('''
            QPushButton:checked {
            background-color: #144288;
            }
            ''')
        
        middleLayout = QHBoxLayout()
        middleLayout.addWidget(self.clear_layer_button)
        middleLayout.addWidget(self.delete_layer_button)
        return middleLayout
    
    def createBottomLayout(self):
        opacityText = QLabel()
        opacityText.setText("Opacity")
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setMaximumWidth(150)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setSingleStep(1)
        self.opacity_slider.setSliderPosition(100)
        self.opacity_slider.valueChanged.connect(self.valueChanged)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(opacityText)
        bottomLayout.addWidget(self.opacity_slider)
        return bottomLayout
    
    def confirmAction(self, actionName: str, actionTrue, actionTrueParameter):
        reply = QMessageBox.question(
            self,
            actionName.capitalize()+ " layer",
            "Are you sure you want to " + actionName.lower() + " " + self.layerName + "?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if actionTrueParameter:
                actionTrue(actionTrueParameter)
                return
            actionTrue()

    def valueChanged(self, position):
        self.image_opacity = min(max(float(position)/100, 0), 1)
        self.layer.updateOpacity(self.image_opacity)
        self.updateLayer()
    
    def updateLayer(self):
        self.image.setPixmap(QPixmap(self.layer.image))
        self.update()
        self.update_block.emit()
    
    @override
    def paintEvent(self, event):
        self.updateLayer()
        super().paintEvent(event)