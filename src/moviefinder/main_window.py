import json
import sys
import webbrowser
from textwrap import dedent
from typing import Any
from typing import Optional

from moviefinder.abstract_user_widget import AbstractUserWidget
from moviefinder.account_creation_menu import AccountCreationMenu
from moviefinder.browse_menu import BrowseMenu
from moviefinder.item import Item
from moviefinder.item_menu import ItemMenu
from moviefinder.login_menu import LoginMenu
from moviefinder.resources import sample_movies_json_path
from moviefinder.resources import settings_icon_path
from moviefinder.settings_menu import SettingsMenu
from moviefinder.start_menu import StartMenu
from moviefinder.user import User
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
        self.item_menu: Optional[ItemMenu] = None
        self.settings_menu: Optional[SettingsMenu] = None
        self.browse_menu: Optional[BrowseMenu] = None

    def show_start_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.start_menu)

    def show_account_creation_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.account_creation_menu)

    def show_login_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.login_menu)

    def show_settings_menu(self, user: User) -> None:
        if self.settings_menu is None:
            self.settings_menu = SettingsMenu(user, self)
            self.central_widget.addWidget(self.settings_menu)
        self.central_widget.setCurrentWidget(self.settings_menu)

    def show_browse_menu(self, user: User) -> None:
        if self.browse_menu is None:
            self.item_menu = ItemMenu(user, self)
            self.central_widget.addWidget(self.item_menu)
            items = self.__filter_items(self.__load_items(), user)
            self.browse_menu = BrowseMenu(user, items, self)
            self.central_widget.addWidget(self.browse_menu)
        else:
            self.browse_menu.user = user
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
        self.browse_menu = None
        self.settings_menu = None
        self.show_start_menu()

    def save_user_data(self, user: User, password: str) -> None:
        # TODO: check whether the password string is empty. If it is, don't save it.
        pass  # TODO

    def open_downloads_site(self) -> None:
        webbrowser.open_new_tab(
            "https://github.com/chizuo/COMP587-Project-App/releases"
        )

    def create_options_button(
        self, parent: AbstractUserWidget
    ) -> QtWidgets.QToolButton:
        """Creates and connects an options toolbutton.

        Parameters
        ----------
        parent : UserWidget
            The widget with a ``user`` attribute that will be the parent of the options
            button.
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
        parent.settings_action.triggered.connect(
            lambda self=self, user=parent.user: self.show_settings_menu(user)
        )
        parent.log_out_action = QtGui.QAction("Log out")
        parent.options_menu.addAction(parent.log_out_action)
        parent.log_out_action.triggered.connect(self.log_out)
        parent.exit_action = QtGui.QAction("Exit")
        parent.options_menu.addAction(parent.exit_action)
        parent.exit_action.triggered.connect(lambda: sys.exit(0))
        options_button.setMenu(parent.options_menu)
        return options_button

    def __load_items(self) -> list[Item]:
        items: list[Item] = []
        with open(sample_movies_json_path, "r", encoding="utf8") as file:
            service_obj: dict[str, Any] = json.load(file)
            # total_pages: int = service_obj["total_pages"]
            items_data: list[dict] = service_obj["movies"]
            for item_data in items_data:
                items.append(Item(item_data))
        return items

    def __filter_items(self, items: list[Item], user: User) -> list[Item]:
        # TODO
        return items
