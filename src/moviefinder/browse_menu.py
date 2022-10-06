from moviefinder.resources import settings_gear_png_path
from moviefinder.user import User
from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class BrowseMenu(QtWidgets.QWidget):
    def __init__(self, user: User, parent=None):
        super().__init__(parent)
        self.user = user
        self.layout = QtWidgets.QVBoxLayout(self)
        self.options_button = QtWidgets.QToolButton()
        self.options_button.setArrowType(Qt.NoArrow)  # This doesn't seem to work?
        self.options_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.options_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.options_button.setIcon(QtGui.QIcon(settings_gear_png_path))
        self.options_menu = QtWidgets.QMenu()
        self.about_action = QtGui.QAction("About")
        self.options_menu.addAction(self.about_action)
        self.update_action = QtGui.QAction("Check for updates")
        self.options_menu.addAction(self.update_action)
        self.settings_action = QtGui.QAction("Settings")
        self.options_menu.addAction(self.settings_action)
        self.log_out_action = QtGui.QAction("Log out")
        self.options_menu.addAction(self.log_out_action)
        self.exit_action = QtGui.QAction("Exit")
        self.options_menu.addAction(self.exit_action)
        self.options_button.setMenu(self.options_menu)
        self.layout.addWidget(self.options_button, alignment=Qt.AlignRight)
        self.browse_grid_layout = QtWidgets.QGridLayout()
        title_label = QtWidgets.QLabel("<h1>browse</h1>", self)
        title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.browse_grid_layout.addWidget(title_label)
        self.layout.addLayout(self.browse_grid_layout)
