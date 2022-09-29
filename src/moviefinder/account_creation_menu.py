import re

from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class EmailValidator(QtGui.QValidator):
    email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    def validate(self, email: str, cursor_position: int) -> QtGui.QValidator.State:
        # TODO: check if an account was already made with the given email address.
        # return QtGui.QValidator.Invalid
        if self.email_pattern.match(email):
            return QtGui.QValidator.Acceptable
        return QtGui.QValidator.Intermediate


class AccountCreationMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.layout.addRow("password:", self.password_line_edit)
        self.confirm_password_line_edit = QtWidgets.QLineEdit(self)
        self.confirm_password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addRow("confirm password:", self.confirm_password_line_edit)
        self.layout.addRow(QtWidgets.QLabel("<h2>services</h2>", self))
        self.amazon_prime_checkbox = QtWidgets.QCheckBox("Amazon Prime", self)
        self.layout.addRow(self.amazon_prime_checkbox)
        self.disney_plus_checkbox = QtWidgets.QCheckBox("Disney+", self)
        self.layout.addRow(self.disney_plus_checkbox)
        self.hbo_max_checkbox = QtWidgets.QCheckBox("HBO Max", self)
        self.layout.addRow(self.hbo_max_checkbox)
        self.hulu_checkbox = QtWidgets.QCheckBox("Hulu", self)
        self.layout.addRow(self.hulu_checkbox)
        self.netflix_checkbox = QtWidgets.QCheckBox("Netflix", self)
        self.layout.addRow(self.netflix_checkbox)
        buttons_layout = QtWidgets.QHBoxLayout()
        self.submit_button = QtWidgets.QPushButton("submit", self)
        buttons_layout.addWidget(self.submit_button)
        self.cancel_button = QtWidgets.QPushButton("cancel", self)
        buttons_layout.addWidget(self.cancel_button)
        self.layout.addRow(buttons_layout)

    def get_services(self) -> list[str]:
        services = []
        if self.amazon_prime_checkbox.isChecked():
            services.append("Amazon Prime")
        if self.amazon_prime_checkbox.isChecked():
            services.append("Disney+")
        if self.amazon_prime_checkbox.isChecked():
            services.append("HBO Max")
        if self.amazon_prime_checkbox.isChecked():
            services.append("Hulu")
        if self.amazon_prime_checkbox.isChecked():
            services.append("Netflix")
        return services
