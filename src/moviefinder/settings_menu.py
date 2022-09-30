from moviefinder.user import User
from moviefinder.validators import EmailValidator
from moviefinder.validators import PasswordValidator
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class SettingsMenu(QtWidgets.QWidget):
    def __init__(self, user: User, parent=None):
        super().__init__(parent)
        self.user = user
        self.layout = QtWidgets.QFormLayout(self)
        title_label = QtWidgets.QLabel("<h1>settings</h1>", self)
        title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layout.addRow(title_label)
        self.name_line_edit = QtWidgets.QLineEdit(self)
        self.name_line_edit.setText(self.user.name)
        self.layout.addRow("name:", self.name_line_edit)
        self.email_line_edit = QtWidgets.QLineEdit(self)
        self.email_line_edit.setValidator(EmailValidator())
        self.email_line_edit.setText(self.user.email)
        self.layout.addRow("email:", self.email_line_edit)
        self.password_line_edit = QtWidgets.QLineEdit(self)
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line_edit.setValidator(PasswordValidator())
        self.layout.addRow("new password:", self.password_line_edit)
        self.confirm_password_line_edit = QtWidgets.QLineEdit(self)
        self.confirm_password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addRow("confirm new password:", self.confirm_password_line_edit)
        self.layout.addRow(QtWidgets.QLabel("<h2>services</h2>", self))
        self.apple_tv_plus = QtWidgets.QCheckBox("Apple TV+", self)
        if "Apple TV+" in self.user.services:
            self.apple_tv_plus.setChecked(True)
        self.layout.addRow(self.apple_tv_plus)
        self.disney_plus_checkbox = QtWidgets.QCheckBox("Disney+", self)
        if "Disney+" in self.user.services:
            self.disney_plus_checkbox.setChecked(True)
        self.layout.addRow(self.disney_plus_checkbox)
        self.hbo_max_checkbox = QtWidgets.QCheckBox("HBO Max", self)
        if "HBO Max" in self.user.services:
            self.hbo_max_checkbox.setChecked(True)
        self.layout.addRow(self.hbo_max_checkbox)
        self.hulu_checkbox = QtWidgets.QCheckBox("Hulu", self)
        if "Hulu" in self.user.services:
            self.hulu_checkbox.setChecked(True)
        self.layout.addRow(self.hulu_checkbox)
        self.netflix_checkbox = QtWidgets.QCheckBox("Netflix", self)
        if "Netflix" in self.user.services:
            self.netflix_checkbox.setChecked(True)
        self.layout.addRow(self.netflix_checkbox)
        self.save_button = QtWidgets.QPushButton("save", self)
        self.layout.addRow(self.save_button)

    def get_services(self) -> list[str]:
        services = []
        if self.apple_tv_plus.isChecked():
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
