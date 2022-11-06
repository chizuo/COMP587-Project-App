from moviefinder.user import User
from moviefinder.validators import EmailValidator
from moviefinder.validators import PasswordValidator
from moviefinder.validators import valid_services
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
        self.region_combo_box.addItem("United States")
        self.layout.addRow("region:", self.region_combo_box)
        self.services_layout = QtWidgets.QVBoxLayout()
        self.services_group_box = QtWidgets.QGroupBox("services")
        self.apple_tv_plus_checkbox = QtWidgets.QCheckBox("Apple TV+", self)
        self.services_layout.addWidget(self.apple_tv_plus_checkbox)
        self.disney_plus_checkbox = QtWidgets.QCheckBox("Disney+", self)
        self.services_layout.addWidget(self.disney_plus_checkbox)
        self.hbo_max_checkbox = QtWidgets.QCheckBox("HBO Max", self)
        self.services_layout.addWidget(self.hbo_max_checkbox)
        self.hulu_checkbox = QtWidgets.QCheckBox("Hulu", self)
        self.services_layout.addWidget(self.hulu_checkbox)
        self.netflix_checkbox = QtWidgets.QCheckBox("Netflix", self)
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

    def __get_services(self) -> list[str]:
        services = []
        if self.apple_tv_plus_checkbox.isChecked():
            services.append("Apple TV+")
        if self.disney_plus_checkbox.isChecked():
            services.append("Disney+")
        if self.hbo_max_checkbox.isChecked():
            services.append("HBO Max")
        if self.hulu_checkbox.isChecked():
            services.append("Hulu")
        if self.netflix_checkbox.isChecked():
            services.append("Netflix")
        return services

    def __reset_services(self) -> None:
        service_checkboxes = self.services_group_box.findChildren(QtWidgets.QCheckBox)
        for service_checkbox in service_checkboxes:
            service_checkbox.setChecked(False)

    def __create_account_and_show_browse_menu(self) -> None:
        if not self.email_line_edit.hasAcceptableInput():
            msg = QtWidgets.QMessageBox()
            msg.setText("Invalid email address format.")
            msg.exec()
            return
        if self.__account_exists(self.email_line_edit.text()):
            msg = QtWidgets.QMessageBox()
            msg.setText("An account with this email address already exists.")
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
        if not valid_services(self.services_group_box):
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
        user = User(name, email, region, services)
        self.main_window.save_user_data(user, password)
        self.main_window.show_browse_menu(user)

    def __account_exists(self, email: str) -> bool:
        # TODO
        return False
