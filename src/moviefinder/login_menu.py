from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class LoginMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QFormLayout(self)
        title_label = QtWidgets.QLabel("<h1>log in</h1>", self)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addRow(title_label)
        self.username_line_edit = QtWidgets.QLineEdit(self)
        layout.addRow("username:", self.username_line_edit)
        self.password_line_edit = QtWidgets.QLineEdit(self)
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addRow("password:", self.password_line_edit)
        buttons_layout = QtWidgets.QHBoxLayout()
        self.submit_button = QtWidgets.QPushButton("submit", self)
        buttons_layout.addWidget(self.submit_button)
        self.cancel_button = QtWidgets.QPushButton("cancel", self)
        buttons_layout.addWidget(self.cancel_button)
        layout.addRow(buttons_layout)
        self.setLayout(layout)
