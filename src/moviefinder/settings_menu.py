from moviefinder.buttons import add_services_groupbox
from moviefinder.checkable_combo_box import CheckableComboBox
from moviefinder.country_code import CountryCode
from moviefinder.movie import ServiceName
from moviefinder.movies import movies
from moviefinder.user import show_message_box
from moviefinder.user import user
from moviefinder.validators import NameValidator
from moviefinder.validators import PasswordValidator
from moviefinder.validators import valid_services_groupbox
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class SettingsMenu(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__(main_window)
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)
        self.options_button = main_window.create_options_button(self)
        self.layout.addWidget(self.options_button, alignment=Qt.AlignRight)
        settings_layout = QtWidgets.QFormLayout(self)
        title_label = QtWidgets.QLabel("<h1>settings</h1>", self)
        title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        settings_layout.addRow(title_label)
        settings_layout.addRow("email:", QtWidgets.QLabel(user.email, self))
        self.name_line_edit = QtWidgets.QLineEdit(self)
        self.name_line_edit.setValidator(NameValidator())
        settings_layout.addRow("name:", self.name_line_edit)
        self.password_line_edit = QtWidgets.QLineEdit(self)
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line_edit.setValidator(PasswordValidator())
        settings_layout.addRow("new password:", self.password_line_edit)
        self.confirm_password_line_edit = QtWidgets.QLineEdit(self)
        self.confirm_password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        settings_layout.addRow("confirm new password:", self.confirm_password_line_edit)
        self.genres_combo_box = CheckableComboBox(self)
        self.genres_combo_box.addItems(user.genre_habits.keys())
        self.genres_combo_box.setCurrentData(movies.genres)
        settings_layout.addRow("genres:", self.genres_combo_box)
        self.region_combo_box = QtWidgets.QComboBox(self)
        self.region_combo_box.addItem(CountryCode.US.value)
        settings_layout.addRow("region:", self.region_combo_box)
        add_services_groupbox(self)
        buttons_layout = QtWidgets.QHBoxLayout()
        self.save_button = QtWidgets.QPushButton("save", self)
        self.save_button.clicked.connect(self.__save_settings_and_show_browse_menu)
        buttons_layout.addWidget(self.save_button)
        self.cancel_button = QtWidgets.QPushButton("cancel", self)
        self.cancel_button.clicked.connect(self.__reset_settings_and_show_browse_menu)
        buttons_layout.addWidget(self.cancel_button)
        settings_layout.addRow(buttons_layout)
        self.__set_widgets()

    def __set_widgets(self) -> None:
        """Initializes widgets with the values in the user object."""
        self.name_line_edit.setText(user.name)
        assert user.region is not None
        self.genres_combo_box.setCurrentData(movies.genres)
        self.region_combo_box.setCurrentText(user.region.value)
        self.amazon_prime_checkbox.setChecked(ServiceName.AMAZON_PRIME in user.services)
        self.apple_tv_plus_checkbox.setChecked(
            ServiceName.APPLE_TV_PLUS in user.services
        )
        self.disney_plus_checkbox.setChecked(ServiceName.DISNEY_PLUS in user.services)
        self.hulu_checkbox.setChecked(ServiceName.HULU in user.services)
        self.netflix_checkbox.setChecked(ServiceName.NETFLIX in user.services)

    def __reset_settings_and_show_browse_menu(self) -> None:
        self.__set_widgets()
        self.main_window.show_browse_menu()

    def __get_services(self) -> list[ServiceName]:
        """Determines what services are selected in the service checkboxes."""
        services: list[ServiceName] = []
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

    def __save_settings_and_show_browse_menu(self) -> None:
        if not self.name_line_edit.hasAcceptableInput():
            show_message_box("Please enter a name up to 100 characters long.")
            return
        if (
            self.password_line_edit.text()
            and not self.password_line_edit.hasAcceptableInput()
        ):
            show_message_box(
                "Invalid password. The password must have 9 to 50 characters."
            )
            return
        if self.password_line_edit.text() != self.confirm_password_line_edit.text():
            self.confirm_password_line_edit.clear()
            show_message_box("The passwords do not match.")
            return
        new_genres = self.genres_combo_box.currentText().split(", ")
        if not new_genres:
            show_message_box("Please choose at least one genre.")
            return
        if not valid_services_groupbox(self.services_group_box):
            show_message_box("Please choose at least one service.")
            return
        new_name = self.name_line_edit.text()
        new_password = self.password_line_edit.text()
        self.password_line_edit.clear()
        self.confirm_password_line_edit.clear()
        new_region = CountryCode(self.region_combo_box.currentText())
        new_services: list[ServiceName] = self.__get_services()
        must_reload_movies = False
        if (
            new_genres != movies.genres
            or new_region != user.region
            or new_services != user.services
        ):
            movies.genres = new_genres
            must_reload_movies = True
        if not user.update_and_save(new_name, new_region, new_services, new_password):
            user.clear()
            self.main_window.clear_movies()
            self.main_window.show_login_menu()
            return
        if must_reload_movies:
            self.main_window.clear_movies()
            if not movies.load():
                show_message_box("Error: unable to connect to the service.")
                return
            self.main_window.browse_menu.reload_browse_widget()
        self.main_window.show_browse_menu()
