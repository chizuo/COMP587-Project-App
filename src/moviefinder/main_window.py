import sys
import webbrowser
from textwrap import dedent
from typing import Optional

from moviefinder.account_creation_menu import AccountCreationMenu
from moviefinder.browse_menu import BrowseMenu
from moviefinder.items import items
from moviefinder.login_menu import LoginMenu
from moviefinder.resources import settings_icon_path
from moviefinder.settings_menu import SettingsMenu
from moviefinder.start_menu import StartMenu
from moviefinder.user import user
from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie Finder")
        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.__init_menus()
        self.show_start_menu()
        self.showMaximized()

    def __init_menus(self) -> None:
        self.start_menu = StartMenu(self)
        self.central_widget.addWidget(self.start_menu)
        self.account_creation_menu = AccountCreationMenu(self)
        self.central_widget.addWidget(self.account_creation_menu)
        self.login_menu = LoginMenu(self)
        self.central_widget.addWidget(self.login_menu)
        self.settings_menu: Optional[SettingsMenu] = None
        self.browse_menu: Optional[BrowseMenu] = None

    def show_start_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.start_menu)

    def show_account_creation_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.account_creation_menu)

    def show_login_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.login_menu)

    def show_settings_menu(self) -> None:
        if self.settings_menu is None:
            if not user.is_valid():
                print("Invalid user data.")
                print(f"    User: {user}")
                self.show_start_menu()
                return
            self.settings_menu = SettingsMenu(self)
            self.central_widget.addWidget(self.settings_menu)
        self.central_widget.setCurrentWidget(self.settings_menu)

    def show_browse_menu(self) -> None:
        if self.browse_menu is None:
            if not user.is_valid():
                print("Invalid user data.")
                print(f"    User: {user}")
                self.show_start_menu()
                return
            ok: Optional[bool] = items.load()
            if ok is None:
                msg = QtWidgets.QMessageBox()
                msg.setText(
                    "Error: no movies or shows available from your chosen services."
                )
                msg.exec()
                self.show_settings_menu()
                return
            if not ok:
                msg = QtWidgets.QMessageBox()
                msg.setText("Error: unable to connect to the service.")
                msg.exec()
                self.show_settings_menu()
                return
            self.browse_menu = BrowseMenu(self)
            self.central_widget.addWidget(self.browse_menu)
        else:
            self.browse_menu.update_item_widgets()
        self.central_widget.setCurrentWidget(self.browse_menu)

    def show_about_dialog(self) -> None:
        msg = QtWidgets.QMessageBox()
        msg.setText(
            dedent(
                """\
                <h1>Movie Finder</h1>

                <p>v0.0.1</p>

                <p>Icons from lucide.dev</p>
                """
            )
        )
        msg.exec()

    def log_out(self) -> None:
        if self.browse_menu is not None:
            if self.browse_menu.browse_widget.item_menu is not None:
                self.central_widget.removeWidget(
                    self.browse_menu.browse_widget.item_menu
                )
            self.central_widget.removeWidget(self.browse_menu)
            self.browse_menu = None
        if self.settings_menu is not None:
            self.central_widget.removeWidget(self.settings_menu)
            self.settings_menu = None
        items.clear()
        user.clear()
        self.show_start_menu()

    def open_downloads_site(self) -> None:
        """Opens this app's downloads site in a new tab of the default browser."""
        webbrowser.open_new_tab(
            "https://github.com/chizuo/COMP587-Project-App/releases"
        )

    def create_options_button(self, parent: QtWidgets.QWidget) -> QtWidgets.QToolButton:
        """Creates and connects an options toolbutton.

        Parameters
        ----------
        parent : QtWidgets.QWidget
            The widget that will be the parent of the options button.
        """
        options_button = QtWidgets.QToolButton()
        options_button.setArrowType(Qt.NoArrow)  # This doesn't seem to work?
        options_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        options_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        options_button.setIcon(QtGui.QIcon(settings_icon_path))
        parent.options_menu = QtWidgets.QMenu()
        parent.about_action = QtGui.QAction("About")
        parent.options_menu.addAction(parent.about_action)
        parent.about_action.triggered.connect(self.show_about_dialog)
        parent.update_action = QtGui.QAction("Check for updates")
        parent.options_menu.addAction(parent.update_action)
        parent.update_action.triggered.connect(self.open_downloads_site)
        parent.settings_action = QtGui.QAction("Settings")
        parent.options_menu.addAction(parent.settings_action)
        parent.settings_action.triggered.connect(self.show_settings_menu)
        parent.log_out_action = QtGui.QAction("Log out")
        parent.options_menu.addAction(parent.log_out_action)
        parent.log_out_action.triggered.connect(self.log_out)
        parent.exit_action = QtGui.QAction("Exit")
        parent.options_menu.addAction(parent.exit_action)
        parent.exit_action.triggered.connect(lambda: sys.exit(0))
        options_button.setMenu(parent.options_menu)
        return options_button
