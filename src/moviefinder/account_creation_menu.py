import requests
from moviefinder.checkable_combo_box import CheckableComboBox
from moviefinder.country_code import CountryCode
from moviefinder.movie import ServiceName
from moviefinder.movie import USE_MOCK_DATA
from moviefinder.movies import movies
from moviefinder.user import user
from moviefinder.validators import EmailValidator
from moviefinder.validators import NameValidator
from moviefinder.validators import PasswordValidator
from moviefinder.validators import valid_services_groupbox
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class AccountCreationMenu(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__(main_window)
        self.main_window = main_window
        self.layout = QtWidgets.QFormLayout(self)
        title_label = QtWidgets.QLabel("<h1>create account</h1>", self)
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addRow(title_label)
        self.name_line_edit = QtWidgets.QLineEdit(self)
        self.name_line_edit.setValidator(NameValidator())
        self.layout.addRow("name:", self.name_line_edit)
        self.email_line_edit = QtWidgets.QLineEdit(self)
        self.email_line_edit.setValidator(EmailValidator())
        self.layout.addRow("email:", self.email_line_edit)
        self.password_line_edit = QtWidgets.QLineEdit(self)
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line_edit.setValidator(PasswordValidator())
        self.layout.addRow("password:", self.password_line_edit)
        self.confirm_password_line_edit = QtWidgets.QLineEdit(self)
        self.confirm_password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addRow("confirm password:", self.confirm_password_line_edit)
        self.region_combo_box = QtWidgets.QComboBox(self)
        self.region_combo_box.addItem("United States of America")
        self.layout.addRow("region:", self.region_combo_box)
        self.genres_combo_box = CheckableComboBox(self)
        self.genres_combo_box.addItems(user.genre_habits.keys())
        self.layout.addRow("favorite genres:", self.genres_combo_box)
        self.services_layout = QtWidgets.QVBoxLayout()
        self.services_group_box = QtWidgets.QGroupBox("services")
        self.apple_tv_plus_checkbox = QtWidgets.QCheckBox(
            ServiceName.APPLE_TV_PLUS.value, self
        )
        self.services_layout.addWidget(self.apple_tv_plus_checkbox)
        self.disney_plus_checkbox = QtWidgets.QCheckBox(
            ServiceName.DISNEY_PLUS.value, self
        )
        self.services_layout.addWidget(self.disney_plus_checkbox)
        self.hbo_max_checkbox = QtWidgets.QCheckBox(ServiceName.HBO_MAX.value, self)
        self.services_layout.addWidget(self.hbo_max_checkbox)
        self.hulu_checkbox = QtWidgets.QCheckBox(ServiceName.HULU.value, self)
        self.services_layout.addWidget(self.hulu_checkbox)
        self.netflix_checkbox = QtWidgets.QCheckBox(ServiceName.NETFLIX.value, self)
        self.services_layout.addWidget(self.netflix_checkbox)
        self.services_group_box.setLayout(self.services_layout)
        self.layout.addRow(self.services_group_box)
        buttons_layout = QtWidgets.QHBoxLayout()
        self.submit_button = QtWidgets.QPushButton("submit", self)
        self.submit_button.clicked.connect(self.__create_account_and_show_browse_menu)
        buttons_layout.addWidget(self.submit_button)
        self.cancel_button = QtWidgets.QPushButton("cancel", self)
        self.cancel_button.clicked.connect(main_window.show_start_menu)
        buttons_layout.addWidget(self.cancel_button)
        self.layout.addRow(buttons_layout)

    def __get_services(self) -> list[ServiceName]:
        """Determines what services are selected in the service checkboxes."""
        services = []
        if self.apple_tv_plus_checkbox.isChecked():
            services.append(ServiceName.APPLE_TV_PLUS)
        if self.disney_plus_checkbox.isChecked():
            services.append(ServiceName.DISNEY_PLUS)
        if self.hbo_max_checkbox.isChecked():
            services.append(ServiceName.HBO_MAX)
        if self.hulu_checkbox.isChecked():
            services.append(ServiceName.HULU)
        if self.netflix_checkbox.isChecked():
            services.append(ServiceName.NETFLIX)
        return services

    def __reset_services(self) -> None:
        """Unchecks all the service checkboxes."""
        service_checkboxes = self.services_group_box.findChildren(QtWidgets.QCheckBox)
        for service_checkbox in service_checkboxes:
            service_checkbox.setChecked(False)

    def __create_account_and_show_browse_menu(self) -> None:
        if not self.name_line_edit.hasAcceptableInput():
            msg = QtWidgets.QMessageBox()
            msg.setText("Please enter a name up to 100 characters long.")
            msg.exec()
            return
        if not self.email_line_edit.hasAcceptableInput():
            msg = QtWidgets.QMessageBox()
            msg.setText("Invalid email address format.")
            msg.exec()
            return
        if not self.password_line_edit.hasAcceptableInput():
            msg = QtWidgets.QMessageBox()
            msg.setText("Invalid password. The password must have 9 to 50 characters.")
            msg.exec()
            return
        if self.password_line_edit.text() != self.confirm_password_line_edit.text():
            self.confirm_password_line_edit.clear()
            msg = QtWidgets.QMessageBox()
            msg.setText("The passwords do not match.")
            msg.exec()
            return
        chosen_genres: str = self.genres_combo_box.currentText()
        if not chosen_genres:
            msg = QtWidgets.QMessageBox()
            msg.setText("Please choose at least one genre.")
            msg.exec()
            return
        if not valid_services_groupbox(self.services_group_box):
            return
        account_exists = self.__account_exists(self.email_line_edit.text().lower())
        if account_exists is None:
            msg = QtWidgets.QMessageBox()
            msg.setText("An error occurred while checking if the account exists.")
            msg.exec()
            return
        if account_exists:
            msg = QtWidgets.QMessageBox()
            msg.setText("An account with this email address already exists.")
            msg.exec()
            return
        name = self.name_line_edit.text()
        email = self.email_line_edit.text()
        password = self.password_line_edit.text()
        region = self.region_combo_box.currentText()
        services = self.__get_services()
        self.name_line_edit.clear()
        self.email_line_edit.clear()
        self.password_line_edit.clear()
        self.confirm_password_line_edit.clear()
        self.region_combo_box.setCurrentIndex(0)
        self.__reset_services()
        self.genres_combo_box.clear()
        user.create(name, email, CountryCode(region), services, password)
        movies.genres = chosen_genres.split(", ")
        self.main_window.show_browse_menu()

    def __account_exists(self, email: str) -> bool | None:
        """Checks the database for an account already using a given email address.

        Returns True if the account exists, False if it does not, and None if there was
        an error connecting to the service.
        """
        if USE_MOCK_DATA:
            return False
        response = requests.post(
            url="http://chuadevs.com:1587/v1/account",
            json={"email": email},
        )
        if response:
            return False
        if response.status_code == 406:
            return True
        return None
