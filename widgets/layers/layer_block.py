from typing import override

from PySide6.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QSlider, QLabel
from PySide6.QtCore import Signal, Qt, QSize

from widgets.layers.layer import Layer

class LayerBlock(QPushButton):
    delete_layer = Signal(Layer)
    def __init__(self, layerName, layer):
        super().__init__()
        self.setMaximumSize(200, 100)
        layerDisplayName = QLabel()
        layerDisplayName.setText(layerName)

        self.clear_layer_button = QPushButton("Clear layer")
        self.clear_layer_button.setMaximumWidth(100)
        self.clear_layer_button.clicked.connect(self.confirmClear)
        self.delete_layer_button = QPushButton("Delete layer")
        self.delete_layer_button.setMaximumWidth(100)
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
        middleLayout = QHBoxLayout()
        bottomLayout = QHBoxLayout()
        topLayout.addWidget(layerDisplayName)
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
        newOpacity = min(max(float(position)/100, 0), 1)
        self.layer.updateOpacity(newOpacity)