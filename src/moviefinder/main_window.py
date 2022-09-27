from moviefinder.about_menu import AboutMenu
from moviefinder.account_creation_menu import AccountCreationMenu
from moviefinder.login_menu import LoginMenu
from moviefinder.start_menu import StartMenu
from PySide6 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie Finder")
        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.init_menus()
        self.show_start_menu()
        self.show()

    def init_menus(self) -> None:
        self.init_start_menu()
        self.init_account_creation_menu()
        self.init_login_menu()
        self.init_about_menu()

    def init_start_menu(self) -> None:
        self.start_menu = StartMenu(self)
        self.start_menu.create_account_button.clicked.connect(
            self.show_account_creation_menu
        )
        self.start_menu.login_button.clicked.connect(self.show_login_menu)
        self.start_menu.about_button.clicked.connect(self.show_about_menu)
        self.central_widget.addWidget(self.start_menu)

    def init_account_creation_menu(self) -> None:
        self.account_creation_menu = AccountCreationMenu(self)
        self.account_creation_menu.submit_button.clicked.connect(self.create_account)
        self.account_creation_menu.cancel_button.clicked.connect(self.show_start_menu)
        self.central_widget.addWidget(self.account_creation_menu)

    def init_login_menu(self) -> None:
        self.login_menu = LoginMenu(self)
        self.login_menu.submit_button.clicked.connect(self.log_in)
        self.login_menu.cancel_button.clicked.connect(self.show_start_menu)
        self.central_widget.addWidget(self.login_menu)

    def init_about_menu(self) -> None:
        self.about_menu = AboutMenu(self)
        self.about_menu.back_button.clicked.connect(self.show_start_menu)
        self.central_widget.addWidget(self.about_menu)

    def show_start_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.start_menu)

    def show_account_creation_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.account_creation_menu)

    def show_login_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.login_menu)

    def show_about_menu(self) -> None:
        self.central_widget.setCurrentWidget(self.about_menu)

    def create_account(self) -> None:
        print("create account menu's submit button clicked")
        name = self.account_creation_menu.name_line_edit.text()
        email = self.account_creation_menu.email_line_edit.text()
        password = self.account_creation_menu.password_line_edit.text()
        self.account_creation_menu.password_line_edit.clear()
        print(f"{name = }")
        print(f"{email = }")
        print(f"{password = }")

    def log_in(self) -> None:
        print("log in menu's submit button clicked")
        email = self.login_menu.email_line_edit.text()
        password = self.login_menu.password_line_edit.text()
        self.login_menu.password_line_edit.clear()
        print(f"{email = }")
        print(f"{password = }")
