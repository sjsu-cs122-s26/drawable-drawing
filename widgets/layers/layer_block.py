from typing import override

from PySide6.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QSlider, QLabel
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Signal, Qt, QSize

from widgets.layers.layer import Layer
from widgets.layers.layer_mini_image import MiniImage

class LayerBlock(QPushButton):
    delete_layer = Signal(Layer)
    update_block = Signal()
    move = Signal(int)

    def __init__(self, layerName, layer):
        super().__init__()
        self.setFixedSize(229, 125)
        layerDisplayName = QLabel()
        layerDisplayName.setText(layerName)
        self.image = MiniImage()
        self.image.setMaximumSize(128, 72)
        self.image_opacity=1
        self.pixmap = self.image.pixmap()
        self.image.setPixmap(QPixmap("media/drawable_icon.jpg")) # temp image file. Will fix the issue of images not rendering later.

        self.move_up_button = QPushButton("Up")
        self.move_up_button.setMaximumSize(75, 25)
        self.move_up_button.clicked.connect(lambda x: self.move.emit(-1))
        self.move_down_button = QPushButton("Down")
        self.move_down_button.setMaximumSize(75, 25)
        self.move_down_button.clicked.connect(lambda x: self.move.emit(1))

        self.clear_layer_button = QPushButton("Clear layer")
        self.clear_layer_button.setMaximumSize(100, 25)
        self.clear_layer_button.clicked.connect(self.confirmClear)
        self.delete_layer_button = QPushButton("Delete layer")
        self.delete_layer_button.setMaximumSize(100, 25)
        self.delete_layer_button.clicked.connect(self.confirmDelete)
        self.layerName = layerName
        self.setCheckable(True)
        self.setStyleSheet('''
            QPushButton:checked {
            background-color: #144288;
            }
            ''')
        self.layer = layer

        opacityText = QLabel()
        opacityText.setText("Opacity")
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setMaximumWidth(150)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setSingleStep(1)
        self.opacity_slider.setSliderPosition(100)
        self.opacity_slider.valueChanged.connect(self.valueChanged)

        layout = QVBoxLayout(self)
        topLayout = QHBoxLayout()
        topLeftLayout = QVBoxLayout()
        middleLayout = QHBoxLayout()
        bottomLayout = QHBoxLayout()
        topLayout.addWidget(layerDisplayName)
        topLayout.addWidget(self.image)
        topLeftLayout.addWidget(self.move_up_button)
        topLeftLayout.addWidget(self.move_down_button)
        topLayout.addLayout(topLeftLayout)
        middleLayout.addWidget(self.clear_layer_button)
        middleLayout.addWidget(self.delete_layer_button)
        bottomLayout.addWidget(opacityText)
        bottomLayout.addWidget(self.opacity_slider)
        layout.addLayout(topLayout)
        layout.addLayout(middleLayout)
        layout.addLayout(bottomLayout)
    
    def confirmDelete(self):
        reply = QMessageBox.question(
            self,
            "Delete layer",
            "Are you sure you want to delete " + self.layerName + "?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_layer.emit(self.layer)
    
    def confirmClear(self):
        reply = QMessageBox.question(
            self,
            "Clear layer",
            "Are you sure you want to clear " + self.layerName + "?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.layer.clear()
    def valueChanged(self, position):
        self.image_opacity = min(max(float(position)/100, 0), 1)
        self.layer.updateOpacity(self.image_opacity)
        self.updateLayer()
    
    def setLayer(self, layer: Layer):
        if hasattr(self, "layer"):
            self.layer.layer_updated.disconnect(self.updateLayer)
        self.layer = layer
        self.layer.layer_updated.connect(self.updateLayer)
        self.layer.updateOpacity(self.image_opacity)
    
    def updateLayer(self):
        self.image.setPixmap(QPixmap(self.layer.image))
        self.update()
        self.update_block.emit()