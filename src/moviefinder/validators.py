import re

from PySide6 import QtGui


class EmailValidator(QtGui.QValidator):
    email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    def validate(self, email: str, cursor_position: int) -> QtGui.QValidator.State:
        # TODO: check if an account was already made with the given email address.
        # return QtGui.QValidator.Invalid
        if self.email_pattern.match(email):
            return QtGui.QValidator.Acceptable
        return QtGui.QValidator.Intermediate


class PasswordValidator(QtGui.QValidator):
    def validate(self, password: str, cursor_position: int) -> QtGui.QValidator.State:
        if 9 <= len(password) <= 50:
            return QtGui.QValidator.Acceptable
        return QtGui.QValidator.Intermediate
