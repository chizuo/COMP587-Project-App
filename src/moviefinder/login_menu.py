import requests
from moviefinder.country_code import CountryCode
from moviefinder.movie import ServiceName
from moviefinder.movie import USE_MOCK_DATA
from moviefinder.movies import movies
from moviefinder.user import User
from moviefinder.user import user
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class LoginMenu(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__(main_window)
        self.main_window = main_window
        self.layout = QtWidgets.QFormLayout(self)
        title_label = QtWidgets.QLabel("<h1>log in</h1>", self)
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addRow(title_label)
        self.email_line_edit = QtWidgets.QLineEdit(self)
        self.layout.addRow("email:", self.email_line_edit)
        self.password_line_edit = QtWidgets.QLineEdit(self)
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addRow("password:", self.password_line_edit)
        buttons_layout = QtWidgets.QHBoxLayout()
        self.submit_button = QtWidgets.QPushButton("submit", self)
        self.submit_button.clicked.connect(self.__log_in_and_show_browse_menu)
        buttons_layout.addWidget(self.submit_button)
        self.cancel_button = QtWidgets.QPushButton("cancel", self)
        self.cancel_button.clicked.connect(main_window.show_start_menu)
        buttons_layout.addWidget(self.cancel_button)
        self.layout.addRow(buttons_layout)

    def __log_in_and_show_browse_menu(self) -> None:
        """Logs in and shows the browse menu if successful."""
        email = self.email_line_edit.text()
        password = self.password_line_edit.text()
        self.password_line_edit.clear()
        if not self.__load_user_data(email, password):
            return
        movies.genres = self.get_top_3_genres(user)
        self.main_window.show_browse_menu()

    def __load_user_data(self, email: str, password: str) -> bool:
        """Loads user data from the database.

        Returns True if successful, False otherwise.
        """
        if USE_MOCK_DATA:
            user.name = "user's name here"
            user.email = "a@b.c"
            user.region = CountryCode.US
            user.services = [
                ServiceName.APPLE_TV_PLUS,
                ServiceName.DISNEY_PLUS,
                ServiceName.HBO_MAX,
                ServiceName.HULU,
                ServiceName.NETFLIX,
            ]
            return True
        response = requests.post(
            url="http://chuadevs.com:1587/v1/account",
            json={
                "email": email,
                "password": password,
            },
        )
        if response.status_code == 401:
            msg = QtWidgets.QMessageBox()
            msg.setText("Incorrect password.")
            msg.exec()
            return False
        if response.status_code == 404:
            msg = QtWidgets.QMessageBox()
            msg.setText("No account is associated with this email address.")
            msg.exec()
            return False
        if not response:
            msg = QtWidgets.QMessageBox()
            msg.setText("Error: unable to connect to the service.")
            msg.exec()
            return False
        data = response.json()
        user.name = data["name"]
        user.email = email
        user.region = CountryCode[data["country"].upper()]
        for s in data["service"]:
            user.services.append(ServiceName(s.upper()))
        return True

    def get_top_3_genres(self, user: User) -> list[str]:
        return [
            movie[0]
            for movie in sorted(
                list(user.genre_habits.items()),
                key=lambda movie: movie[1],
                reverse=True,
            )[:3]
        ]
