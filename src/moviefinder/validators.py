import re

from moviefinder.movie import ServiceName
from PySide6 import QtGui
from PySide6 import QtWidgets


class EmailValidator(QtGui.QValidator):
    email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    def validate(self, email: str, cursor_position: int = 0) -> QtGui.QValidator.State:
        if not email:
            return QtGui.QValidator.Intermediate
        if len(email) > 100:
            return QtGui.QValidator.Invalid
        if self.email_pattern.match(email):
            return QtGui.QValidator.Acceptable
        return QtGui.QValidator.Intermediate


class NameValidator(QtGui.QValidator):
    def validate(self, name: str, cursor_position: int) -> QtGui.QValidator.State:
        if not name:
            return QtGui.QValidator.Intermediate
        if len(name) > 100:
            return QtGui.QValidator.Invalid
        return QtGui.QValidator.Acceptable


class PasswordValidator(QtGui.QValidator):
    def validate(self, password: str, cursor_position: int) -> QtGui.QValidator.State:
        if len(password) > 50:
            return QtGui.QValidator.Invalid
        if len(password) >= 9:
            return QtGui.QValidator.Acceptable
        return QtGui.QValidator.Intermediate


valid_service_domain_names = [
    "disneyplus.com",
    "hbomax.com",
    "hulu.com",
    "netflix.com",
    "tv.apple.com",
]


def valid_services(services: dict[ServiceName, str]) -> bool:
    """Determines whether all of the movie URLs have valid service domain names."""
    for domain in services.values():
        for valid_domain in valid_service_domain_names:
            if valid_domain in domain:
                return True
    return False


def valid_services_groupbox(services_group_box: QtWidgets.QGroupBox) -> bool:
    """Determines whether at least one service is selected.

    Parameters
    ----------
    services_group_box : QtWidgets.QGroupBox
        A group box with at least one ``QtWidgets.QCheckBox``. Any other widgets in the
        group box will be ignored.
    """
    for service_checkbox in services_group_box.findChildren(QtWidgets.QCheckBox):
        if service_checkbox.isChecked():
            return True
    return False
