from moviefinder.resources import start_menu_image_path
from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class StartMenu(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__(main_window)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addSpacerItem(
            QtWidgets.QSpacerItem(1, 100, QtWidgets.QSizePolicy.Expanding)
        )
        image_pixmap = QtGui.QPixmap(start_menu_image_path)
        image_label = QtWidgets.QLabel(self)
        image_label.setPixmap(image_pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(image_label)
        title_label = QtWidgets.QLabel("<h1>Movie Finder</h1>", self)
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)
        self.create_account_button = QtWidgets.QPushButton("create account", self)
        self.create_account_button.clicked.connect(
            main_window.show_account_creation_menu
        )
        self.layout.addWidget(self.create_account_button)
        self.login_button = QtWidgets.QPushButton("login", self)
        self.login_button.clicked.connect(main_window.show_login_menu)
        self.layout.addWidget(self.login_button)
        self.about_button = QtWidgets.QPushButton("about", self)
        self.about_button.clicked.connect(main_window.show_about_dialog)
        self.layout.addWidget(self.about_button)
        self.layout.addSpacerItem(
            QtWidgets.QSpacerItem(1, 100, QtWidgets.QSizePolicy.Expanding)
        )
