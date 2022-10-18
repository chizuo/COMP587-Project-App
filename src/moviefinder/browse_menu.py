from moviefinder.user import User
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class BrowseMenu(QtWidgets.QWidget):
    def __init__(self, user: User, main_window: QtWidgets.QMainWindow):
        super().__init__(main_window)
        self.user = user
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(main_window.options_button, alignment=Qt.AlignRight)
        self.browse_grid_layout = QtWidgets.QGridLayout()
        title_label = QtWidgets.QLabel("<h1>browse</h1>", self)
        title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.browse_grid_layout.addWidget(title_label)
        self.sample_item_menu_button = QtWidgets.QPushButton(
            "view sample item menu", self
        )
        self.browse_grid_layout.addWidget(self.sample_item_menu_button)
        self.layout.addLayout(self.browse_grid_layout)
