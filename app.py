from collections import deque
from turtle import color

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
    QComboBox,
    QSlider,
    QColorDialog
)

from core.snapshot import Snapshot
from widgets.color_wheel import ColorWheel
from widgets.canvas import Canvas
from widgets.clear import Clear
from widgets.layers.layer_menu import LayerMenu

class Drawable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowParameters()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.createCentralLayout()
        self.createBottomLayout()
        self.createMenus()
        
        toolbar = QToolBar("Toolbar")
        self.register_toolbar_widgets(toolbar)
        self.addToolBar(toolbar)
        
        self._undo_stack = deque(maxlen=50)
        self._redo_stack = deque(maxlen=50)
        self.canvas.save_snapshot.connect(self.saveSnapshot)
        self.layer_menu.save_snapshot.connect(self.saveSnapshot)


    def setWindowParameters(self):
        self.setWindowTitle("Drawable")
        icon = QIcon("media/drawable_icon.jpg")
        self.setWindowIcon(icon)

    def createMenus(self):
        menu_bar = self.menuBar()

        self.createFileMenu(menu_bar)
        self.createEditMenu(menu_bar)
        self.createImageMenu(menu_bar)
        self.createHelpMenu(menu_bar)

    def createFileMenu(self, menu_bar):
        file_menu = menu_bar.addMenu("&File")
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

    def createEditMenu(self, menu_bar):
        edit_menu = menu_bar.addMenu("&Edit")

        self.undo_action = QAction("Undo")
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.triggered.connect(lambda : self.setState(self._undo_stack, self._redo_stack))
        edit_menu.addAction(self.undo_action)

        self.redo_action = QAction("Redo")
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.triggered.connect(lambda : self.setState(self._redo_stack, self._undo_stack))
        edit_menu.addAction(self.redo_action)

        self.modify_bucket_action = QAction("Modify Bucket Tolerance")
        self.modify_bucket_action.setShortcut("Ctrl+Alt+B")
        self.modify_bucket_action.setStatusTip("Modify how similar pixels must be to be affected by the paint bucket tool.")
        self.modify_bucket_action.triggered.connect(self.modifyBucket)
        edit_menu.addAction(self.modify_bucket_action)

    def createImageMenu(self, menu_bar):
        image_menu = menu_bar.addMenu("&Image")
        self.resize_canvas_action = QAction("Resize Canvas")
        self.resize_canvas_action.setShortcut("Ctrl+Alt+C")
        self.resize_canvas_action.setStatusTip("Resize canvas with width & height values.")
        self.resize_canvas_action.triggered.connect(self.resizeCanvas)
        image_menu.addAction(self.resize_canvas_action)

    def createHelpMenu(self, menu_bar):
        help_menu = menu_bar.addMenu("&Help")

    def createCentralLayout(self):
        self.canvas = Canvas()
        
        self.pen_sidebar = self.canvas.tools["pen"].sidebar
        self.pen_sidebar.setVisible(False)
        
        self.scrollAreaCanvas = QScrollArea()
        self.scrollAreaCanvas.setWidget(self.canvas)
        self.scrollAreaCanvas.setBackgroundRole(QPalette.Dark)

        self.layer_menu = LayerMenu()
        self.layer_menu.delete_layer_validated.connect(self.canvas.deleteLayer)
        self.layer_menu.add_layer.connect(self.canvas.addLayer)
        self.layer_menu.switch_layer.connect(self.canvas.switchActiveLayer)
        self.layer_menu.swap_layer.connect(self.canvas.swapLayerOrder)
        self.layer_menu.addLayer()
        self.scrollAreaLayerMenu = QScrollArea()
        self.scrollAreaLayerMenu.setMaximumWidth(250)
        self.scrollAreaLayerMenu.setWidget(self.layer_menu)
        self.scrollAreaLayerMenu.setBackgroundRole(QPalette.Dark)

        central_layout = QHBoxLayout()
        central_layout.addWidget(self.scrollAreaLayerMenu)
        central_layout.addWidget(self.scrollAreaCanvas)
        central_layout.addWidget(self.pen_sidebar)
        self.main_layout.addLayout(central_layout)

        

    def createBottomLayout(self):
        color_wheel = ColorWheel()
        color_wheel.color_change.connect(self.onColorPicked)

        clear = Clear()
        clear.cleared.connect(self.saveSnapshot)
        clear.cleared.connect(self.canvas.clear)

        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["Rectangle", "Ellipse", "Triangle", "Line"])
        self.shape_combo.setFixedSize(150, 30)
        self.shape_combo.setVisible(False)
        self.shape_combo.currentTextChanged.connect(lambda name: self.canvas.shapes_tool.setShape(name))

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)
        bottom_layout.addWidget(color_wheel)
        bottom_layout.addWidget(clear)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.shape_combo)
        
        self.primary_btn = QPushButton("Primary")
        self.secondary_btn = QPushButton("Secondary")
        
        self.primary_btn.clicked.connect(self.pickPrimaryColor)
        self.secondary_btn.clicked.connect(self.pickSecondaryColor)
        
        bottom_layout.addWidget(self.primary_btn)
        bottom_layout.addWidget(self.secondary_btn)
        
        self.primary_btn.setVisible(False)
        self.secondary_btn.setVisible(False)
        
        self.main_layout.addLayout(bottom_layout)
        
    def register_toolbar_widgets(self, toolbar: QToolBar):
        self.group = QActionGroup(self)
        self.group.setExclusionPolicy(QActionGroup.ExclusionPolicy.ExclusiveOptional)

        for tool_name in self.canvas.tools.keys():
            action = toolbar.addAction(tool_name.capitalize())
            action.setCheckable(True)

            action.triggered.connect(
                lambda checked, name=tool_name: self._on_tool_changed(name)
            )

            self.group.addAction(action)
    
    
    def saveSnapshot(self):
        snapshot = Snapshot(self.canvas.size(), self.layer_menu.layer_blocks, self.canvas.currentLayerIndex, self.layer_menu.lifetime_layers)
        self._undo_stack.append(snapshot)
        self._redo_stack.clear()
    
    def _on_tool_changed(self, tool_name):
        print("TOOL SWITCH:", tool_name)

        self.canvas.setActiveTool(tool_name)

        self.pen_sidebar.setVisible(tool_name == "pen")
        self.primary_btn.setVisible(tool_name == "gradient")
        self.secondary_btn.setVisible(tool_name == "gradient")
        self.shape_combo.setVisible(tool_name == "shapes")
    
    def pickPrimaryColor(self):
        color = QColorDialog.getColor(self.canvas.primary_color)
        if color.isValid():
            self.canvas.primary_color = color

    def pickSecondaryColor(self):
        color = QColorDialog.getColor(self.canvas.secondary_color)
        if color.isValid():
            self.canvas.secondary_color = color
    
    def onColorPicked(self, color):
        self.canvas.color = color

    @Slot()
    def setState(self, popStack, pushStack):
        if not popStack or self.canvas.drawing:
            return
        self.canvas.drawing = True
        pushStack.append(Snapshot(self.canvas.size(), self.layer_menu.layer_blocks, self.canvas.currentLayerIndex, self.layer_menu.lifetime_layers))
        snapshot = popStack.pop()
        layers = self.canvas.setState(snapshot)
        self.layer_menu.setState(snapshot, layers)
        self.canvas.drawing = False

    @Slot()
    def openFile(self):
        if self.canvas.drawing:
            return
        self.canvas.drawing = True
        dialog = QFileDialog(self)
        dialog.setNameFilter(("Images (*.png *.jpg)"))
        if not dialog.exec():
            return
        self.saveSnapshot
        fileName = dialog.selectedFiles()[0]
        self.canvas.loadImage(fileName)
        self.canvas.drawing = False
        
    
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
        x, ok = dialog.getInt(self, "QInputDialog::getInt()", "Input x value:", self.canvas.width(), 100, 8192, 2,)
        if not ok:
            return
        y, ok = dialog.getInt(self, "QInputDialog::getInt()", "Input y value:", self.canvas.height(), 100, 8912, 2)
        if not ok:
            return
        self.canvas.resize(x, y)

    @Slot()
    def modifyBucket(self):
        dialog = QInputDialog(self)
        dialog.setIntRange(0, 255)
        dialog.setLabelText("Modify Bucket Tolerance")
        tolerance, ok = dialog.getInt(self, "QInputDialog::getInt()", "Input integer:", self.canvas.bucket_tolerance, 0, 255, 2,)
        if not ok:
            return
        self.canvas.bucket_tolerance = tolerance