from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import Signal

class LayerMenuStatic(QWidget):
    add_layer = Signal()

    def __init__(self):
        super().__init__()
        self.setMaximumWidth(200)
        self.setMaximumHeight(50)
        self.layer_blocks = []

        self.add_layer_button = QPushButton("Add Layer")
        self.add_layer_button.clicked.connect(self.addLayer)

        layout = QVBoxLayout(self)
        layout.addWidget(self.add_layer_button)
    
    def addLayer(self):
        self.add_layer.emit()