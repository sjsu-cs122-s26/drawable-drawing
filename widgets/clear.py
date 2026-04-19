from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtCore import Signal
class Clear(QWidget):
    cleared = Signal()

    def __init__(self):
        super().__init__()
        self.setMaximumHeight(30)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedSize(150, 30)
        self.clear_button.clicked.connect(self.confirm_clear)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(self.clear_button)


    def confirm_clear(self):
        reply = QMessageBox.question(
            self,
            "Clear Canvas",
            "Are you sure you want to clear the canvas?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.cleared.emit()