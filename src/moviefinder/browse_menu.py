from moviefinder.user import User
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class BrowseMenu(QtWidgets.QWidget):
    def __init__(self, user: User, parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QGridLayout(self)
        title_label = QtWidgets.QLabel("<h1>browse</h1>", self)
        title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layout.addWidget(title_label)
