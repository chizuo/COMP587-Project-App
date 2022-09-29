from moviefinder.user import User
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class BrowseMenu(QtWidgets.QWidget):
    def __init__(self, user: User, parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QGridLayout(self)
        self.user = user
        title_label = QtWidgets.QLabel("<h1>browse</h1>", self)
        title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layout.addWidget(title_label)
        # if not self.user.services:
        self.layout.addWidget(
            QtWidgets.QLabel(
                "To browse, choose your streaming services in settings.", self
            )
        )
        self.settings_button = QtWidgets.QPushButton("settings", self)
        self.layout.addWidget(self.settings_button)
