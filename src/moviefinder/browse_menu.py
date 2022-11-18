from moviefinder.abstract_user_widget import AbstractUserWidget
from moviefinder.browse_widget import BrowseWidget
from moviefinder.user import User
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class BrowseMenu(AbstractUserWidget):
    def __init__(self, user: User, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.user = user
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)
        self.options_button = main_window.create_options_button(self)
        self.layout.addWidget(self.options_button, alignment=Qt.AlignRight)
        title_label = QtWidgets.QLabel("<h1>browse</h1>", self)
        title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layout.addWidget(title_label)
        self.scroll_area = QtWidgets.QScrollArea()
        self.browse_widget = BrowseWidget(self.user, main_window)
        self.scroll_area.setWidget(self.browse_widget)
        self.layout.addWidget(self.scroll_area)
