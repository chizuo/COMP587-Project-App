from typing import Optional

from moviefinder.country_code import CountryCode
from moviefinder.item import ServiceName
from moviefinder.items import items
from moviefinder.user import user
from moviefinder.validators import EmailValidator
from moviefinder.validators import NameValidator
from moviefinder.validators import PasswordValidator
from moviefinder.validators import valid_services_groupbox
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class SettingsMenu(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__(main_window)
        self.main_window = main_window
        self.layout = QtWidgets.QFormLayout(self)
        title_label = QtWidgets.QLabel("<h1>settings</h1>", self)
        title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
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
        self.layout.addRow("new password:", self.password_line_edit)
        self.confirm_password_line_edit = QtWidgets.QLineEdit(self)
        self.confirm_password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addRow("confirm new password:", self.confirm_password_line_edit)
        self.region_combo_box = QtWidgets.QComboBox(self)
        self.region_combo_box.addItem(CountryCode.US.value)
        self.layout.addRow("region:", self.region_combo_box)
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
        self.save_button = QtWidgets.QPushButton("save", self)
        self.save_button.clicked.connect(self.__save_settings_and_show_browse_menu)
        buttons_layout.addWidget(self.save_button)
        self.cancel_button = QtWidgets.QPushButton("cancel", self)
        self.cancel_button.clicked.connect(self.__reset_settings_and_show_browse_menu)
        buttons_layout.addWidget(self.cancel_button)
        self.layout.addRow(buttons_layout)
        self.__set_widgets()

    def __set_widgets(self) -> None:
        """Initializes widgets with the values in the user object."""
        self.name_line_edit.setText(user.name)
        self.email_line_edit.setText(user.email)
        assert user.region is not None
        self.region_combo_box.setCurrentText(user.region.value)
        self.apple_tv_plus_checkbox.setChecked(
            ServiceName.APPLE_TV_PLUS in user.services
        )
        self.disney_plus_checkbox.setChecked(ServiceName.DISNEY_PLUS in user.services)
        self.hbo_max_checkbox.setChecked(ServiceName.HBO_MAX in user.services)
        self.hulu_checkbox.setChecked(ServiceName.HULU in user.services)
        self.netflix_checkbox.setChecked(ServiceName.NETFLIX in user.services)

    def __reset_settings_and_show_browse_menu(self) -> None:
        self.__set_widgets()
        self.main_window.show_browse_menu()

    def __get_services(self) -> list[ServiceName]:
        """Determines what services are selected in the service checkboxes."""
        services: list[ServiceName] = []
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

    def __save_settings_and_show_browse_menu(self) -> None:
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
        if (
            self.password_line_edit.text()
            and not self.password_line_edit.hasAcceptableInput()
        ):
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
        if not valid_services_groupbox(self.services_group_box):
            return
        name = self.name_line_edit.text()
        email = self.email_line_edit.text()
        password = self.password_line_edit.text()
        self.password_line_edit.clear()
        self.confirm_password_line_edit.clear()
        region = CountryCode(self.region_combo_box.currentText())
        services: list[ServiceName] = self.__get_services()
        must_reload_items = False
        if region != user.region or services != user.services:
            must_reload_items = True
            items.clear()
        user.update_and_save(name, email, region, services, password)
        if must_reload_items:
            ok: Optional[bool] = items.load()
            if ok is None:
                msg = QtWidgets.QMessageBox()
                msg.setText(
                    "Error: no movies or shows available from your chosen services."
                )
                msg.exec()
                self.show_settings_menu()
                return
            if not ok:
                msg = QtWidgets.QMessageBox()
                msg.setText("Error: unable to connect to the service.")
                msg.exec()
                self.show_settings_menu()
                return
        self.main_window.show_browse_menu()
