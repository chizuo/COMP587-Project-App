from moviefinder.buttons import add_services_groupbox
from moviefinder.checkable_combo_box import CheckableComboBox
from moviefinder.country_code import CountryCode
from moviefinder.movie import ServiceName
from moviefinder.movies import movies
from moviefinder.user import show_message_box
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
        add_services_groupbox(self)
        buttons_layout = QtWidgets.QHBoxLayout()
        self.submit_button = QtWidgets.QPushButton("submit", self)
        self.submit_button.clicked.connect(
            self.__create_account_and_show_logged_in_start_menu
        )
        buttons_layout.addWidget(self.submit_button)
        self.cancel_button = QtWidgets.QPushButton("cancel", self)
        self.cancel_button.clicked.connect(main_window.show_start_menu)
        buttons_layout.addWidget(self.cancel_button)
        self.layout.addRow(buttons_layout)

    def __get_services(self) -> list[ServiceName]:
        """Determines what services are selected in the service checkboxes."""
        services = []
        if self.amazon_prime_checkbox.isChecked():
            services.append(ServiceName.AMAZON_PRIME)
        if self.apple_tv_plus_checkbox.isChecked():
            services.append(ServiceName.APPLE_TV_PLUS)
        if self.disney_plus_checkbox.isChecked():
            services.append(ServiceName.DISNEY_PLUS)
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

    def __create_account_and_show_logged_in_start_menu(self) -> None:
        if not self.name_line_edit.hasAcceptableInput():
            show_message_box("Please enter a name up to 100 characters long.")
            return
        if not self.email_line_edit.hasAcceptableInput():
            show_message_box("Invalid email address format.")
            return
        if not self.password_line_edit.hasAcceptableInput():
            show_message_box(
                "Invalid password. The password must have 9 to 50 characters."
            )
            return
        if self.password_line_edit.text() != self.confirm_password_line_edit.text():
            self.confirm_password_line_edit.clear()
            show_message_box("The passwords do not match.")
            return
        chosen_genres: str = self.genres_combo_box.currentText()
        if not chosen_genres:
            show_message_box("Please choose at least one genre.")
            return
        if not valid_services_groupbox(self.services_group_box):
            show_message_box("Please choose at least one service.")
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
        if not user.create(name, email, CountryCode(region), services, password):
            return
        movies.genres = chosen_genres.split(", ")
        self.main_window.show_logged_in_start_menu()
