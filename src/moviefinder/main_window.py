import sys
import webbrowser
from textwrap import dedent
from typing import Literal

import requests
from moviefinder.account_creation_menu import AccountCreationMenu
from moviefinder.browse_menu import BrowseMenu
from moviefinder.country_code import CountryCode
from moviefinder.loading_dialog import LoadingDialog
from moviefinder.logged_in_start_menu import LoggedInStartMenu
from moviefinder.login_menu import LoginMenu
from moviefinder.movie import SERVICE_BASE_URL
from moviefinder.movie import ServiceName
from moviefinder.movie import USE_MOCK_DATA
from moviefinder.movies import movies
from moviefinder.resources import settings_icon_path
from moviefinder.settings_menu import SettingsMenu
from moviefinder.start_menu import StartMenu
from moviefinder.user import show_message_box
from moviefinder.user import User
from moviefinder.user import user
from moviefinder.validators import EmailValidator
from moviefinder.validators import PasswordValidator
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie Finder")
        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.__init_menus()
        self.__load_settings_and_show_window()
        self.is_quitting = False
        qApp.aboutToQuit.connect(self.__on_quit)  # type: ignore # noqa: F821

    def __init_menus(self) -> None:
        self.start_menu = StartMenu(self)
        self.central_widget.addWidget(self.start_menu)
        self.central_widget.setCurrentWidget(self.start_menu)
        self.account_creation_menu = AccountCreationMenu(self)
        self.central_widget.addWidget(self.account_creation_menu)
        self.login_menu = LoginMenu(self)
        self.central_widget.addWidget(self.login_menu)
        self.logged_in_start_menu: SettingsMenu | None = None
        self.settings_menu: SettingsMenu | None = None
        self.browse_menu: BrowseMenu | None = None

    def __load_settings_and_show_window(self):
        """Reads the settings from the device's configuration files."""
        print("Loading settings...")
        settings = QtCore.QSettings()
        if settings.contains("user/email") and settings.contains("user/password"):
            user.email = str(settings.value("user/email"))
            user.password = str(settings.value("user/password"))
            print("Loaded user data from device settings.")
            if self.__log_in(user.email, user.password):
                self.show_logged_in_start_menu()
        if not settings.contains("main_window/geometry"):
            self.showMaximized()
        else:
            geometry_bytes: QtCore.QByteArray = settings.value("main_window/geometry")
            if geometry_bytes.isEmpty():
                self.showMaximized()
            else:
                self.adjustSize()
                self.restoreGeometry(geometry_bytes)
                self.show()

    def __save_window_geometry(self):
        """Saves the window's size and location to the device's configuration files."""
        QtCore.QSettings().setValue("main_window/geometry", self.saveGeometry())

    def __on_quit(self) -> None:
        """Called when the application is about to quit.

        Other code may run for a short time after this method runs.
        """
        self.is_quitting = True
        self.__save_window_geometry()
        if user:
            user.save_genre_habits()

    def load_user_data(self, email: str, password: str) -> bool:
        """Loads user data from the database.

        Returns True if successful, False otherwise.
        """
        if USE_MOCK_DATA:
            user.name = "user's name here"
            user.email = "a@b.c"
            user.region = CountryCode.US
            user.services = [
                ServiceName.AMAZON_PRIME,
                ServiceName.APPLE_TV_PLUS,
                ServiceName.DISNEY_PLUS,
                ServiceName.HULU,
                ServiceName.NETFLIX,
            ]
            return True
        try:
            response = requests.post(
                url=f"{SERVICE_BASE_URL}/account",
                json={
                    "email": email,
                    "password": password,
                },
            )
        except requests.exceptions.ConnectionError as e:
            show_message_box("Could not connect to the server.")
            print(e)
            return False
        if response.status_code == 401:
            show_message_box("Incorrect password.")
            return False
        if response.status_code == 404:
            show_message_box("No account is associated with this email address.")
            return False
        if not response:
            show_message_box(
                f"Unknown error when logging in. Status code: {response.status_code}"
            )
            return False
        data = response.json()
        user.name = data["name"]
        user.email = email
        user.password = password
        user.region = CountryCode[data["country"].upper()]
        for s in data["services"]:
            if ServiceName.contains(s):
                user.services.append(ServiceName(s))
            else:
                print(f"Unknown service: {s}")
        user.genre_habits = data["genre_habits"]
        print("Logged in successfully.")
        return True

    def show_start_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.start_menu)

    def show_account_creation_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.account_creation_menu)

    def show_login_menu(self) -> None:
        """Shows the login menu.

        This method should only be called while the start menu is visible. If the user's
        email and password were retrieved from their device's config files (if they
        chose to stay logged in), this method will show the browse menu instead.
        """
        self.central_widget.setCurrentWidget(self.login_menu)

    def show_logged_in_start_menu(self) -> None:
        if self.logged_in_start_menu is None:
            if not user.is_valid():
                show_message_box("Error: invalid user data.")
                print(f"{user.__dict__ = }")
                user.clear()
                self.show_start_menu()
                return
            self.logged_in_start_menu = LoggedInStartMenu(self)
            self.central_widget.addWidget(self.logged_in_start_menu)
        self.central_widget.setCurrentWidget(self.logged_in_start_menu)

    def show_settings_menu(
        self, from_menu_name: Literal["LoggedInStartMenu", "BrowseMenu"]
    ) -> None:
        if self.settings_menu is None:
            if not user.is_valid():
                show_message_box("Invalid user data.")
                print(f"{user.__dict__ = }")
                user.clear()
                self.show_start_menu()
                return
            self.settings_menu = SettingsMenu(self)
            self.central_widget.addWidget(self.settings_menu)
        self.settings_menu.from_menu_name = from_menu_name
        self.central_widget.setCurrentWidget(self.settings_menu)

    def show_browse_menu(self) -> None:
        if self.browse_menu is not None:
            self.browse_menu.update_movie_widgets()
        else:
            if not user.is_valid():
                show_message_box("Invalid user data.")
                print(f"    User: {user.__dict__}")
                self.show_start_menu()
                return
            with LoadingDialog():
                if not movies.load():
                    show_message_box("Cannot connect to the service.")
                    self.show_settings_menu("LoggedInStartMenu")
                    return
                self.browse_menu = BrowseMenu(self)
                self.central_widget.addWidget(self.browse_menu)
        self.central_widget.setCurrentWidget(self.browse_menu)

    def show_about_dialog(self) -> None:
        show_message_box(
            dedent(
                """\
                <h1>Movie Finder</h1>

                <p>v0.0.1</p>

                <p>See the source code <a href="https://github.com/chizuo/COMP587-MovieApplication">here</a>.</p>

                <p>Icons from lucide.dev</p>
                """  # noqa: E501
            )
        )

    def __log_in(self, email: str, password: str) -> bool:
        """Logs in the user.

        Returns True if the user was successfully logged in, False otherwise.
        """
        if EmailValidator().validate(user.email) != QtGui.QValidator.Acceptable:
            user.clear()
            print("Warning: invalid email format. Settings cleared.")
            return False
        elif PasswordValidator().validate(user.password) != QtGui.QValidator.Acceptable:
            user.clear()
            print("Warning: invalid password format. Settings cleared.")
            return False
        if not self.load_user_data(user.email, user.password):
            return False
        movies.genres = self.get_top_3_genres(user)
        return True

    def log_out(self) -> None:
        if self.browse_menu is not None:
            if self.browse_menu.browse_widget.movie_menu is not None:
                self.central_widget.removeWidget(
                    self.browse_menu.browse_widget.movie_menu
                )
            self.central_widget.removeWidget(self.browse_menu)
            self.browse_menu = None
        if self.settings_menu is not None:
            self.central_widget.removeWidget(self.settings_menu)
            self.settings_menu = None
        user.save_genre_habits()
        user.clear()
        self.clear_movies()
        settings = QtCore.QSettings()
        if settings.contains("user/email"):
            settings.remove("user/email")
        if settings.contains("user/password"):
            settings.remove("user/password")
        self.show_start_menu()

    def open_downloads_site(self) -> None:
        """Opens this app's downloads site in a new tab of the default browser."""
        webbrowser.open_new_tab(
            "https://github.com/chizuo/COMP587-MovieApplication/releases"
        )

    def create_options_button(self, parent: QtWidgets.QWidget) -> QtWidgets.QToolButton:
        """Creates and connects an options toolbutton.

        Parameters
        ----------
        parent : QtWidgets.QWidget
            The widget that will be the parent of the options button.
        """
        options_button = QtWidgets.QToolButton()
        options_button.setArrowType(QtCore.Qt.NoArrow)  # This doesn't seem to work?
        options_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        options_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
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
            lambda: self.show_settings_menu("BrowseMenu")
        )
        parent.log_out_action = QtGui.QAction("Log out")
        parent.options_menu.addAction(parent.log_out_action)
        parent.log_out_action.triggered.connect(self.log_out)
        parent.exit_action = QtGui.QAction("Exit")
        parent.options_menu.addAction(parent.exit_action)
        parent.exit_action.triggered.connect(lambda: sys.exit(0))
        options_button.setMenu(parent.options_menu)
        return options_button

    def clear_movies(self) -> None:
        if self.browse_menu is not None:
            self.browse_menu.browse_widget.movie_widgets.clear()
            movies.clear()

    def get_top_3_genres(self, user: User) -> list[str]:
        """Returns the 3 genres in which the user has liked the most movies.

        If the user has liked no movies, returns the first 3 genres in
        ``user.genre_habits``.
        """
        return [
            movie[0]
            for movie in sorted(
                list(user.genre_habits.items()),
                key=lambda movie: movie[1],
                reverse=True,
            )[:3]
        ]
