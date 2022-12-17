from abc import abstractmethod

from PySide6 import QtWidgets


class AbstractItemWidget(QtWidgets.QWidget):
    @abstractmethod
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.heart_button: QtWidgets.QPushButton
        self.x_button: QtWidgets.QPushButton
        self.item_id: str | None
