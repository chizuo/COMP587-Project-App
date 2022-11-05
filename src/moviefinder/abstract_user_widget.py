from abc import abstractmethod

from moviefinder.user import User
from PySide6 import QtWidgets


class AbstractUserWidget(QtWidgets.QWidget):
    @abstractmethod
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.user: User
