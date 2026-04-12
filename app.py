import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget, QPushButton, QFileDialog, QApplication, QMainWindow, QLabel
from PySide6.QtGui import QPixmap
class Drawable(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drawable")
        self.openFileButton = QPushButton("Open File")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.openFileButton)
        self.openFileButton.clicked.connect(self.openFile)
        self.canvas = Canvas()
        self.layout.addWidget(self.canvas)

    @QtCore.Slot()
    def openFile(self):
        dialog = QFileDialog(self)
        dialog.setNameFilter(("Images (*.png *.jpg)")) #temporary feature to display images. will later be updated to load a previously saved QPainter state
        if not dialog.exec():
            return
        fileName = dialog.selectedFiles()[0]
        label = QLabel(self)
        label.setPixmap(QPixmap(fileName))
        self.layout.addWidget(label)
        
class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.image = QtGui.QImage(800, 500, QtGui.QImage.Format_ARGB32)
        self.image.fill(Qt.white)
        self.last_point = QPoint()
        self.drawing = False
        self.pen_color = QColor(Qt.black)
        self.pen_width = 3

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()
    
    def mouseMoveEvent(self, event):
        if self.drawing and (event.buttons() & Qt.LeftButton):
            painter = QPainter(self.image)
            painter.setPen(QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.last_point, event.position().toPoint())
            self.last_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        QPainter(self).drawImage(self.rect(), self.image, self.image.rect())
    

if __name__=="__main__":
    app = QApplication([])
    widget = Drawable()
    widget.resize(800, 500)
    widget.show()
    sys.exit(app.exec())

    