from textwrap import dedent

from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class AboutMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)
        about_label = QtWidgets.QLabel(
            dedent(
                """\
                <h1>Movie Finder</h1>

                <p>v0.0.0</p>

                <p>More info here.</p>
                """
            ),
            self,
        )
        about_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(about_label)
        self.back_button = QtWidgets.QPushButton("back", self)
        self.layout.addWidget(self.back_button)
