from typing import override
from PySide6 import QtCore, QtGui, QtWidgets

class MiniImage(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        QtWidgets.QLabel.__init__(self)
        self._pixmap = self.pixmap()
        self._resised= False
    
    @override
    def resizeEvent(self, event):
        self.setPixmap(self._pixmap)     

    @override
    def setPixmap(self, pixmap): #overiding setPixmap
        if not pixmap:
            return 
        self._pixmap = pixmap
        return QtWidgets.QLabel.setPixmap(self,self._pixmap.scaled(
                self.frameSize(),
                QtCore.Qt.KeepAspectRatio))