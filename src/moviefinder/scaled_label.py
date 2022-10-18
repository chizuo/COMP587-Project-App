from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class ScaledLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        QtWidgets.QLabel.__init__(self)
        self._pixmap: QtGui.QPixmap = self.pixmap()
        self._resized: bool = False

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.setPixmap(self._pixmap)

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        self._pixmap = pixmap
        return QtWidgets.QLabel.setPixmap(
            self, self._pixmap.scaled(self.frameSize(), QtCore.Qt.KeepAspectRatio)
        )
