from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap, QAction, QIcon, QActionGroup
from PySide6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QPushButton, 
    QFileDialog, 
    QLabel, 
    QVBoxLayout, 
    QToolBar,
    QHBoxLayout
)

from widgets.color_wheel import ColorWheel
from widgets.canvas import Canvas
from widgets.clear import Clear

class Drawable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drawable")
        icon = QIcon("media/drawable_icon.jpg")
        self.setWindowIcon(icon)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.create_menus()

        self.canvas = Canvas()
        self.main_layout.addWidget(self.canvas)
        
        toolbar = QToolBar("Toolbar")
        self.register_toolbar_widgets(toolbar)
        self.addToolBar(toolbar)

        self.color_wheel = ColorWheel()
        self.color_wheel.color_change.connect(self.canvas.set_color)
        self.main_layout.addWidget(self.color_wheel)

        self.clear = Clear()
        self.clear.cleared.connect(self.canvas.clear)
        self.main_layout.addWidget(self.clear)

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)
        bottom_layout.addWidget(self.color_wheel)
        bottom_layout.addWidget(self.clear)
        bottom_layout.addStretch()
        self.main_layout.addLayout(bottom_layout)


    def create_menus(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("&File")
        help_menu = menu_bar.addMenu("&Help")
        
        self.open_file_action = QAction("Open File")
        self.open_file_action.setShortcut("Ctrl+O")
        self.open_file_action.setStatusTip("Open an image file")
        self.open_file_action.triggered.connect(self.openFile)
        file_menu.addAction(self.open_file_action)

        self.save_file_action = QAction("Save File")
        self.save_file_action.setShortcut("Ctrl+S")
        self.save_file_action.setStatusTip("Save currnet canvas as an image file")
        self.save_file_action.triggered.connect(self.saveFile)
        file_menu.addAction(self.save_file_action)

        
    def register_toolbar_widgets(self, toolbar: QToolBar):
        self.group = QActionGroup(self)
        self.group.setExclusionPolicy(QActionGroup.ExclusionPolicy.ExclusiveOptional)
        for tool_name in self.canvas.tools.keys():
            action = toolbar.addAction(tool_name.capitalize())
            action.setCheckable(True)
            action.triggered.connect(lambda checked, name=tool_name: self.canvas.set_active_tool(name))
            self.group.addAction(action)


    @Slot()
    def openFile(self):
        dialog = QFileDialog(self)
        dialog.setNameFilter(("Images (*.png *.jpg)"))
        if not dialog.exec():
            return
        fileName = dialog.selectedFiles()[0]
        self.canvas.load_image(fileName)
    
    @Slot()
    def saveFile(self):
        dialog = QFileDialog(self)
        fileName = dialog.getSaveFileName(filter=("Images (*.png)"))[0]
        if not fileName:
            return
        self.canvas.save_image(fileName)