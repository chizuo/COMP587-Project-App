from moviefinder.item import ServiceName
from moviefinder.user import User
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
        email = self.email_line_edit.text()
        password = self.password_line_edit.text()
        self.password_line_edit.clear()
        if not self.__valid_credentials(email, password):
            return
        user: User = self.__get_user_data(email)
        self.main_window.show_browse_menu(user)

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

    def __get_user_data(self, email: str) -> User:
        # TODO
        return User(
            "user's name here",
            email,
            "United States of America",
            [
                ServiceName.APPLE_TV_PLUS,
                ServiceName.DISNEY_PLUS,
                ServiceName.HBO_MAX,
                ServiceName.HULU,
                ServiceName.NETFLIX,
            ],
        )
