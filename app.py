from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QPixmap, QAction, QIcon, QActionGroup, QPalette, QColor
from PySide6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QPushButton, 
    QFileDialog, 
    QLabel, 
    QVBoxLayout, 
    QToolBar,
    QHBoxLayout,
    QScrollArea,
    QInputDialog,
    QComboBox
)

from widgets.color_wheel import ColorWheel
from widgets.canvas import Canvas
from widgets.clear import Clear
from widgets.layers.layer_menu import LayerMenu

class Drawable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drawable")
        icon = QIcon("media/drawable_icon.jpg")
        self.setWindowIcon(icon)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.createMenus()

        self.canvas = Canvas()
        self.scrollAreaCanvas = QScrollArea()
        self.scrollAreaCanvas.setWidget(self.canvas)
        self.scrollAreaCanvas.setBackgroundRole(QPalette.Dark)

        self.layer_menu = LayerMenu()
        self.layer_menu.delete_layer_validated.connect(self.canvas.deleteLayer)
        self.layer_menu.add_layer.connect(self.canvas.addLayer)
        self.layer_menu.switch_layer.connect(self.canvas.switchActiveLayer)
        self.layer_menu.swap_layer.connect(self.canvas.swapLayerOrder)
        self.layer_menu.addLayer()
        self.scrollAreaLayoutMenu = QScrollArea()
        self.scrollAreaLayoutMenu.setMaximumWidth(250)
        self.scrollAreaLayoutMenu.setWidget(self.layer_menu)
        self.scrollAreaLayoutMenu.setBackgroundRole(QPalette.Dark)

        self.central_layout = QHBoxLayout()
        self.central_layout.addWidget(self.scrollAreaLayoutMenu)
        self.central_layout.addWidget(self.scrollAreaCanvas)
        self.main_layout.addLayout(self.central_layout)
        
        toolbar = QToolBar("Toolbar")
        self.register_toolbar_widgets(toolbar)
        self.addToolBar(toolbar)

        self.color_wheel = ColorWheel()
        self.color_wheel.color_change.connect(self.canvas.setColor)
        self.main_layout.addWidget(self.color_wheel)

        self.clear = Clear()
        self.clear.cleared.connect(self.canvas.clear)
        self.main_layout.addWidget(self.clear)

        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["Rectangle", "Ellipse", "Triangle", "Line"])
        self.shape_combo.setFixedSize(150, 30)
        self.shape_combo.setVisible(False)
        self.shape_combo.currentTextChanged.connect(lambda name: self.canvas.shapes_tool.setShape(name))

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)
        bottom_layout.addWidget(self.color_wheel)
        bottom_layout.addWidget(self.clear)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.shape_combo)
        self.main_layout.addLayout(bottom_layout)

        

        


    def createMenus(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("&File")
        edit_menu = menu_bar.addMenu("&Edit")
        image_menu = menu_bar.addMenu("&Image")
        help_menu = menu_bar.addMenu("&Help")
        
        self.open_file_action = QAction("Open File")
        self.open_file_action.setShortcut("Ctrl+O")
        self.open_file_action.setStatusTip("Open an image file.")
        self.open_file_action.triggered.connect(self.openFile)
        file_menu.addAction(self.open_file_action)

        self.save_file_action = QAction("Save File")
        self.save_file_action.setShortcut("Ctrl+S")
        self.save_file_action.setStatusTip("Save current canvas as an image file.")
        self.save_file_action.triggered.connect(self.saveFile)
        file_menu.addAction(self.save_file_action)

        self.modify_bucket_action = QAction("Modify Bucket Tolerance")
        self.modify_bucket_action.setShortcut("Ctrl+Alt+B")
        self.modify_bucket_action.setStatusTip("Modify how similar pixels must be to be affected by the paint bucket tool.")
        self.modify_bucket_action.triggered.connect(self.modifyBucket)
        edit_menu.addAction(self.modify_bucket_action)

        self.resize_canvas_action = QAction("Resize Canvas")
        self.resize_canvas_action.setShortcut("Ctrl+Alt+C")
        self.resize_canvas_action.setStatusTip("Resize canvas with width & height values.")
        self.resize_canvas_action.triggered.connect(self.resizeCanvas)
        image_menu.addAction(self.resize_canvas_action)

        
    def register_toolbar_widgets(self, toolbar: QToolBar):
        self.group = QActionGroup(self)
        self.group.setExclusionPolicy(QActionGroup.ExclusionPolicy.ExclusiveOptional)
        for tool_name in self.canvas.tools.keys():
            action = toolbar.addAction(tool_name.capitalize())
            action.setCheckable(True)
            action.triggered.connect(lambda checked, name=tool_name: self.canvas.setActiveTool(name))
            if tool_name == "shapes":
                action.triggered.connect(lambda checked: self.shape_combo.setVisible(
                self.canvas.current_tool is not None and self.canvas.current_tool == self.canvas.shapes_tool
                ))
            else:
                action.triggered.connect(lambda checked: self.shape_combo.setVisible(False))
                self.group.addAction(action)
            self.group.addAction(action)


    @Slot()
    def openFile(self):
        dialog = QFileDialog(self)
        dialog.setNameFilter(("Images (*.png *.jpg)"))
        if not dialog.exec():
            return
        fileName = dialog.selectedFiles()[0]
        self.canvas.loadImage(fileName)
    
    @Slot()
    def saveFile(self):
        dialog = QFileDialog(self)
        fileName = dialog.getSaveFileName(filter=("Images (*.png)"))[0]
        if not fileName:
            return
        self.canvas.saveImage(fileName)

    @Slot()
    def resizeCanvas(self):
        dialog = QInputDialog(self)
        dialog.setIntRange(100, 8192)
        dialog.setLabelText("Resize Canvas")
        x, ok = dialog.getInt(self, "QInputDialog::getInt()", "Input x value:", 1920, 100, 8192, 2,)
        if not ok:
            return
        y, ok = dialog.getInt(self, "QInputDialog::getInt()", "Input y value:", 1080, 100, 8912, 2)
        if not ok:
            return
        self.canvas.resize(x, y)

    @Slot()
    def modifyBucket(self):
        dialog = QInputDialog(self)
        dialog.setIntRange(0, 255)
        dialog.setLabelText("Modify Bucket Tolerance")
        tolerance, ok = dialog.getInt(self, "QInputDialog::getInt()", "Input integer:", 0, 0, 255, 2,)
        if not ok:
            return
        self.canvas.bucket_tolerance = tolerance