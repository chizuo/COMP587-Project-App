from moviefinder.country_code import CountryCode
from moviefinder.item import ServiceName
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
        if not self.__valid_credentials(email, password):
            return
        if not self.__load_user_data(email):
            return
        self.main_window.show_browse_menu()

    def __valid_credentials(self, email: str, password: str) -> bool:
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

    def __load_user_data(self, email: str) -> bool:
        """Loads user data from the database.

        Returns True if successful, False otherwise.
        """
        # TODO
        # response = requests.get("http://chuadevs.com:1587/v1/account")
        # if not response:
        #     msg = QtWidgets.QMessageBox()
        #     msg.setText("Unable to connect to the service.")
        #     msg.exec()
        #     return False
        # if response.status_code == 404:
        #     msg = QtWidgets.QMessageBox()
        #     msg.setText("Invalid email and/or password.")
        #     msg.exec()
        #     return False
        # data = response.json()
        # user.name = data["name"]
        # user.email = email
        # user.region = CountryCode(data["country"].upper())
        # for s in data["service"]:
        #     user.services.append(ServiceName(s.upper()))

        user.name = "user's name here"
        user.email = email
        user.region = CountryCode.US
        user.services = [
            ServiceName.APPLE_TV_PLUS,
            ServiceName.DISNEY_PLUS,
            ServiceName.HBO_MAX,
            ServiceName.HULU,
            ServiceName.NETFLIX,
        ]
        return True
