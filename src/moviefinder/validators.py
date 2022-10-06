import re

from PySide6 import QtGui
from PySide6 import QtWidgets


class EmailValidator(QtGui.QValidator):
    email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    def validate(self, email: str, cursor_position: int) -> QtGui.QValidator.State:
        if self.email_pattern.match(email):
            return QtGui.QValidator.Acceptable
        return QtGui.QValidator.Intermediate


class PasswordValidator(QtGui.QValidator):
    def validate(self, password: str, cursor_position: int) -> QtGui.QValidator.State:
        if 9 <= len(password) <= 50:
            return QtGui.QValidator.Acceptable
        return QtGui.QValidator.Intermediate


def valid_services(services_group_box: QtWidgets.QGroupBox) -> bool:
    service_checkboxes = services_group_box.findChildren(QtWidgets.QCheckBox)
    for service_checkbox in service_checkboxes:
        if service_checkbox.isChecked():
            return True
    msg = QtWidgets.QMessageBox()
    msg.setText("Please choose at least one service.")
    msg.exec()
    return False
