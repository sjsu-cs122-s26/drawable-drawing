from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QSlider, QLabel
from PySide6.QtCore import Signal, Qt

from widgets.layers.layer import Layer

class LayerBlock(QPushButton):
    delete_layer = Signal(Layer)
    update_opacity = Signal(Layer)
    def __init__(self, layerName, layer):
        super().__init__()
        self.setMaximumSize(200, 100)
        layerDisplayName = QLabel()
        layerDisplayName.setText(layerName)
        self.delete_layer_button = QPushButton("Delete")
        self.delete_layer_button.setMaximumWidth(50)
        self.delete_layer_button.clicked.connect(self.confirmDelete)
        self.layerName = layerName
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
        bottomLayout = QHBoxLayout()
        topLayout.addWidget(layerDisplayName)
        topLayout.addWidget(self.delete_layer_button)
        bottomLayout.addWidget(opacityText)
        bottomLayout.addWidget(self.opacity_slider)
        layout.addLayout(topLayout)
        layout.addLayout(bottomLayout)
        
    
    def confirmDelete(self):

        reply = QMessageBox.question(
            self,
            "Clear Canvas",
            "Are you sure you want to delete " + self.layerName + "?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_layer.emit(self.layer)
    def valueChanged(self, position):
        newOpacity = min(max(float(position)/100, 0), 1)
        self.layer.opacity=newOpacity
        self.update_opacity.emit(self.layer)