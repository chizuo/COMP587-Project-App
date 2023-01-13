from moviefinder.resources import start_menu_image_path
from moviefinder.user import user
from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class LoggedInStartMenu(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__(main_window)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addSpacerItem(
            QtWidgets.QSpacerItem(1, 50, QtWidgets.QSizePolicy.Expanding)
        )
        image_pixmap = QtGui.QPixmap(start_menu_image_path)
        image_label = QtWidgets.QLabel(self)
        image_label.setPixmap(image_pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(image_label)
        title_label = QtWidgets.QLabel("<h1>Movie Finder</h1>", self)
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)
        self.layout.addWidget(
            QtWidgets.QLabel(f"Logged in as {user.name}", self), 0, Qt.AlignCenter
        )
        browse_button = QtWidgets.QPushButton("browse", self)
        browse_button.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        browse_button.clicked.connect(main_window.show_browse_menu)
        self.layout.addWidget(browse_button, alignment=Qt.AlignCenter)
        settings_button = QtWidgets.QPushButton("settings", self)
        settings_button.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        settings_button.clicked.connect(
            lambda: main_window.show_settings_menu("LoggedInStartMenu")
        )
        self.layout.addWidget(settings_button, alignment=Qt.AlignCenter)
        about_button = QtWidgets.QPushButton("about", self)
        about_button.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        about_button.clicked.connect(main_window.show_about_dialog)
        self.layout.addWidget(about_button, alignment=Qt.AlignCenter)
        log_out_button = QtWidgets.QPushButton("log out", self)
        log_out_button.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        log_out_button.clicked.connect(main_window.log_out)
        self.layout.addWidget(log_out_button, alignment=Qt.AlignCenter)
        self.layout.addSpacerItem(
            QtWidgets.QSpacerItem(1, 50, QtWidgets.QSizePolicy.Expanding)
        )
        self.setStyleSheet("QPushButton { width: 200px; }")
