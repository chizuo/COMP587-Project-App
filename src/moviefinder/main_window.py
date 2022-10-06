import webbrowser
from textwrap import dedent
from typing import Optional

from moviefinder.account_creation_menu import AccountCreationMenu
from moviefinder.browse_menu import BrowseMenu
from moviefinder.login_menu import LoginMenu
from moviefinder.settings_menu import SettingsMenu
from moviefinder.start_menu import StartMenu
from moviefinder.user import User
from moviefinder.validators import valid_services
from PySide6 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie Finder")
        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.init_menus()
        self.show_start_menu()
        self.show()

    def init_menus(self) -> None:
        self.init_start_menu()
        self.init_account_creation_menu()
        self.init_login_menu()
        self.settings_menu: Optional[SettingsMenu] = None
        self.browse_menu: Optional[BrowseMenu] = None

    def init_start_menu(self) -> None:
        self.start_menu = StartMenu(self)
        self.start_menu.create_account_button.clicked.connect(
            self.show_account_creation_menu
        )
        self.start_menu.login_button.clicked.connect(self.show_login_menu)
        self.start_menu.about_button.clicked.connect(self.show_about_dialog)
        self.central_widget.addWidget(self.start_menu)

    def init_account_creation_menu(self) -> None:
        self.account_creation_menu = AccountCreationMenu(self)
        self.account_creation_menu.submit_button.clicked.connect(
            self.create_account_and_show_browse_menu
        )
        self.account_creation_menu.cancel_button.clicked.connect(self.show_start_menu)
        self.central_widget.addWidget(self.account_creation_menu)

    def init_login_menu(self) -> None:
        self.login_menu = LoginMenu(self)
        self.login_menu.submit_button.clicked.connect(self.log_in_and_show_browse_menu)
        self.login_menu.cancel_button.clicked.connect(self.show_start_menu)
        self.central_widget.addWidget(self.login_menu)

    def show_start_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.start_menu)

    def show_account_creation_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.account_creation_menu)

    def show_login_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.login_menu)

    def show_settings_menu(self) -> None:
        """Shows the settings menu.

        Assumes the browse menu has a user object.
        """
        if self.settings_menu is None:
            assert self.browse_menu is not None
            self.settings_menu = SettingsMenu(self.browse_menu.user, self)
            self.settings_menu.save_button.clicked.connect(
                self.save_settings_and_show_browse_menu
            )
            self.settings_menu.cancel_button.clicked.connect(
                self.reset_settings_and_show_browse_menu
            )
            self.central_widget.addWidget(self.settings_menu)
        self.central_widget.setCurrentWidget(self.settings_menu)

    def show_browse_menu(self, user: User) -> None:
        if self.browse_menu is None:
            self.browse_menu = BrowseMenu(user, self)
            self.browse_menu.about_action.triggered.connect(self.show_about_dialog)
            self.browse_menu.update_action.triggered.connect(self.open_downloads_site)
            self.browse_menu.settings_action.triggered.connect(self.show_settings_menu)
            self.browse_menu.log_out_action.triggered.connect(self.log_out)
            self.browse_menu.exit_action.triggered.connect(lambda: exit(0))
            self.central_widget.addWidget(self.browse_menu)
        self.central_widget.setCurrentWidget(self.browse_menu)

    def create_account_and_show_browse_menu(self) -> None:
        menu = self.account_creation_menu
        if not menu.email_line_edit.hasAcceptableInput():
            msg = QtWidgets.QMessageBox()
            msg.setText("Invalid email address format.")
            msg.exec()
            return
        if self.account_exists(menu.email_line_edit.text()):
            msg = QtWidgets.QMessageBox()
            msg.setText("An account with this email address already exists.")
            msg.exec()
            return
        if not menu.password_line_edit.hasAcceptableInput():
            msg = QtWidgets.QMessageBox()
            msg.setText("Invalid password. The password must have 9 to 50 characters.")
            msg.exec()
            return
        if menu.password_line_edit.text() != menu.confirm_password_line_edit.text():
            menu.confirm_password_line_edit.clear()
            msg = QtWidgets.QMessageBox()
            msg.setText("The passwords do not match.")
            msg.exec()
            return
        if not valid_services(menu.services_group_box):
            return
        name = menu.name_line_edit.text()
        email = menu.email_line_edit.text()
        password = menu.password_line_edit.text()
        region = menu.region_combo_box.currentText()
        services = menu.get_services()
        menu.name_line_edit.clear()
        menu.email_line_edit.clear()
        menu.password_line_edit.clear()
        menu.confirm_password_line_edit.clear()
        menu.region_combo_box.setCurrentIndex(0)
        menu.reset_services()
        user = User(name, email, region, services)
        self.save_user_data(user, password)
        self.show_browse_menu(user)

    def log_in_and_show_browse_menu(self) -> None:
        email = self.login_menu.email_line_edit.text()
        password = self.login_menu.password_line_edit.text()
        self.login_menu.password_line_edit.clear()
        if not self.valid_credentials(email, password):
            return
        user: User = self.get_user_data(email)
        self.show_browse_menu(user)

    def log_out(self) -> None:
        self.browse_menu = None
        self.settings_menu = None
        self.show_start_menu()

    def save_settings_and_show_browse_menu(self) -> None:
        menu = self.settings_menu
        assert menu is not None
        if not menu.email_line_edit.hasAcceptableInput():
            msg = QtWidgets.QMessageBox()
            msg.setText("Invalid email address format.")
            msg.exec()
            return
        if (
            menu.password_line_edit.text()
            and not menu.password_line_edit.hasAcceptableInput()
        ):
            msg = QtWidgets.QMessageBox()
            msg.setText("Invalid password. The password must have 9 to 50 characters.")
            msg.exec()
            return
        if menu.password_line_edit.text() != menu.confirm_password_line_edit.text():
            menu.confirm_password_line_edit.clear()
            msg = QtWidgets.QMessageBox()
            msg.setText("The passwords do not match.")
            msg.exec()
            return
        if not valid_services(menu.services_group_box):
            return
        name = menu.name_line_edit.text()
        email = menu.email_line_edit.text()
        password = menu.password_line_edit.text()
        menu.password_line_edit.clear()
        menu.confirm_password_line_edit.clear()
        region = menu.region_combo_box.currentText()
        services = menu.get_services()
        user = User(name, email, region, services)
        self.save_user_data(user, password)
        assert self.browse_menu is not None
        assert self.settings_menu is not None
        self.browse_menu.user = self.settings_menu.user = user
        self.show_browse_menu(user)

    def valid_credentials(self, email: str, password: str) -> bool:
        # if ?:  # TODO
        # msg = QtWidgets.QMessageBox()
        # msg.setText("Unable to connect to the service.")
        # msg.exec()
        # return False
        # if ?:  # TODO
        # msg = QtWidgets.QMessageBox()
        # msg.setText("Invalid email and/or password.")
        # msg.exec()
        # return False
        return True

    def account_exists(self, email: str) -> bool:
        # TODO
        return False

    def get_user_data(self, email: str) -> User:
        # TODO
        return User("user's name here", email, "United States", [])

    def save_user_data(self, user: User, password: str) -> None:
        # TODO: check whether the password string is empty. If it is, don't save it.
        pass  # TODO

    def reset_settings_and_show_browse_menu(self) -> None:
        assert self.settings_menu is not None
        self.settings_menu.set_widgets()
        self.show_browse_menu(self.settings_menu.user)

    def open_downloads_site(self) -> None:
        webbrowser.open("https://github.com/chizuo/COMP587-Project-App/releases", 1)

    def show_about_dialog(self) -> None:
        msg = QtWidgets.QMessageBox()
        msg.setText(
            dedent(
                """\
                <h1>Movie Finder</h1>

                <p>v0.0.1</p>

                <p>Icons provided by https://icons8.com</p>
                """
            )
        )
        msg.exec()
