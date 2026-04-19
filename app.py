from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QPushButton, 
    QFileDialog, 
    QLabel, 
    QVBoxLayout, 
    QToolBar,
)

from widgets.color_wheel import ColorWheel
from widgets.canvas import Canvas

class Drawable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drawable")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.create_menus()

        self.openFileButton = QPushButton("Open File")

        self.main_layout.addWidget(self.openFileButton)
        self.openFileButton.clicked.connect(self.openFile)

        self.canvas = Canvas()
        self.main_layout.addWidget(self.canvas)
        
        toolbar = QToolBar("Toolbar")
        self.register_toolbar_widgets(toolbar)
        self.addToolBar(toolbar)

        self.color_wheel = ColorWheel()
        self.color_wheel.color_change.connect(self.canvas.set_color)
        self.main_layout.addWidget(self.color_wheel)

    def create_menus(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        help_menu = menu_bar.addMenu("&Help")
        
    def register_toolbar_widgets(self, toolbar: QToolBar):
        for tool_name in self.canvas.tools.keys():
            action = toolbar.addAction(tool_name.capitalize())
            action.setCheckable(True)
            action.triggered.connect(lambda checked, name=tool_name: self.canvas.set_active_tool(name))

    @Slot()
    def openFile(self):
        dialog = QFileDialog(self)
        dialog.setNameFilter(("Images (*.png *.jpg)")) #temporary feature to display images. will later be updated to load a previously saved QPainter state
        if not dialog.exec():
            return
        fileName = dialog.selectedFiles()[0]
        label = QLabel(self)
        label.setPixmap(QPixmap(fileName))
        self.main_layout.addWidget(label)
    