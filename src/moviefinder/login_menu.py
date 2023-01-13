from moviefinder.movies import movies
from moviefinder.user import show_message_box
from PySide6 import QtCore
from PySide6 import QtWidgets


class LoginMenu(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__(main_window)
        self.main_window = main_window
        self.layout = QtWidgets.QFormLayout(self)
        title_label = QtWidgets.QLabel("<h1>log in</h1>", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addRow(title_label)
        self.email_line_edit = QtWidgets.QLineEdit(self)
        self.layout.addRow("email:", self.email_line_edit)
        self.password_line_edit = QtWidgets.QLineEdit(self)
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addRow("password:", self.password_line_edit)
        self.stay_logged_in_checkbox = QtWidgets.QCheckBox(self)
        self.layout.addRow("stay logged in: ", self.stay_logged_in_checkbox)
        buttons_layout = QtWidgets.QHBoxLayout()
        self.submit_button = QtWidgets.QPushButton("submit", self)
        self.submit_button.clicked.connect(self.__log_in_and_show_logged_in_start_menu)
        self.submit_button.setDefault(True)
        buttons_layout.addWidget(self.submit_button)
        self.cancel_button = QtWidgets.QPushButton("cancel", self)
        self.cancel_button.clicked.connect(main_window.show_start_menu)
        buttons_layout.addWidget(self.cancel_button)
        self.layout.addRow(buttons_layout)

    def __log_in_and_show_logged_in_start_menu(self) -> None:
        if not self.email_line_edit.hasAcceptableInput():
            show_message_box("Invalid email address.")
            print("The email address did not pass local validation.")
            return
        if not self.password_line_edit.hasAcceptableInput():
            self.password_line_edit.clear()
            show_message_box("Incorrect password.")
            print("The password did not pass local validation.")
            return
        email = self.email_line_edit.text()
        password = self.password_line_edit.text()
        self.password_line_edit.clear()
        if not self.main_window.load_user_data(email, password):
            return
        if self.stay_logged_in_checkbox.isChecked():
            print("Saving user login data to device config files...")
            settings = QtCore.QSettings()
            settings.setValue("user/email", email)
            settings.setValue("user/password", password)
            print("User login data saved.")
        movies.genres = self.main_window.get_top_3_genres()
        self.main_window.show_logged_in_start_menu()
