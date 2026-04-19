from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QColorDialog, QVBoxLayout

class ColorWheel(QWidget):
    color_change = Signal(QColor)
    
    def __init__(self):
        super().__init__()
        self.setMaximumHeight(30)
        self.current_color = QColor(Qt.GlobalColor.black)

        self.color_button = QPushButton("Choose Color")
        self.color_button.setFixedSize(150, 30)
        self.color_button.clicked.connect(self.choose_color)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(1,1,1,1)
        layout.addWidget(self.color_button)
    
    def choose_color(self):
        color = QColorDialog.getColor(self.current_color, self)
        if color.isValid():
            self.current_color = color
            self.color_change.emit(color)