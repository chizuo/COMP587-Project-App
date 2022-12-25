from typing import NoReturn
from typing import Optional

import requests
from moviefinder.movie import CountryCode
from moviefinder.movie import DOMAIN_NAME
from moviefinder.movie import ServiceName
from moviefinder.movie import USE_MOCK_DATA
from moviefinder.validators import EmailValidator
from PySide6 import QtWidgets


def show_message_box(text: str) -> None:
    """Shows the user a message box and blocks until the user closes it."""
    msg = QtWidgets.QMessageBox()
    msg.setText(text)
    msg.exec()


class User:
    """A singleton object with the current user's info."""

    __instance: Optional["User"] = None

    def __new__(cls) -> "User":
        if cls.__instance is None:
            cls.__instance = super(User, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.name = ""
        self.email = ""
        self.password = ""
        self.region: CountryCode | None = None
        self.services: list[ServiceName] = []
        # Map genres to the number of times a movie in that genre has been liked.
        self.genre_habits = {
            "action": 0,
            "adult": 0,
            "adventure": 0,
            "animation": 0,
            "biography": 0,
            "comedy": 0,
            "crime": 0,
            "documentary": 0,
            "drama": 0,
            "family": 0,
            "fantasy": 0,
            "film noir": 0,
            "game show": 0,
            "historical": 0,
            "horror": 0,
            "musical": 0,
            "musical": 0,
            "mystery": 0,
            "news": 0,
            "reality": 0,
            "romance": 0,
            "science fiction": 0,
            "short": 0,
            "sport": 0,
            "talk show": 0,
            "thriller": 0,
            "war": 0,
            "western": 0,
        }

    def create(
        self,
        name: str,
        email: str,
        region: CountryCode,
        services: list[ServiceName],
        password: str,
    ) -> bool:
        """Creates a new account and saves it in the database.

        Returns True if the account was created successfully, False if the account
        already exists or if there was an error communicating to the service.
        """
        self.clear()
        self.name = name
        self.email = email
        self.region = region
        self.services = services
        self.password = password
        if USE_MOCK_DATA:
            return True
        try:
            response = requests.post(
                url=f"http://{DOMAIN_NAME}:1587/v1/register",
                json={
                    "name": self.name,
                    "email": self.email,
                    "country": self.region.name.lower(),
                    "services": [s.value for s in self.services],
                    "password": password,
                },
            )
        except requests.exceptions.ConnectionError as e:
            show_message_box(f"Error communicating with the service:\n\n{e}")
            return False
        if response.status_code == 403:
            show_message_box("An account with this email address already exists.")
            return False
        if response.status_code == 406:
            show_message_box("Error communicating with the service (status code 406).")
            return False
        if not response:
            show_message_box(
                f"Unknown error when creating. Status code: {response.status_code}"
            )
            return False
        print("Successfully created an account.")
        return True

    def update_and_save(
        self,
        name: str,
        region: CountryCode,
        services: list[ServiceName],
        # password: str,  # TODO
    ) -> bool:
        """Updates and saves the user's data to the db, not including genre habits.

        If the password is empty, it will not be saved. Returns True if the update
        was successful, False if there was an error communicating to the service, for
        example if the account no longer exists.
        """
        self.name = name
        self.region = region
        self.services = services
        data = {
            "country": self.region.name.lower(),
            "email": self.email,
            "name": self.name,
            "password": self.password,
            "services": [s.value for s in self.services],
        }
        # if password:  # TODO
        #     data["new_password"] = password
        #     self.password = password
        if not USE_MOCK_DATA:
            response = requests.put(
                url=f"http://{DOMAIN_NAME}:1587/v1/account",
                json=data,
            )
            if not response:
                show_message_box(
                    f"Unknown error when updating. Status code: {response.status_code}"
                )
                return False
            print("Successfully updated the account.")
        return True

    def save_genre_habits(self) -> None:
        """Saves the user's genre habits to the database.

        Assumes the account already exists.
        """
        data = {
            "email": self.email,
            "genre_habits": self.genre_habits,
            "password": self.password,
        }
        if not USE_MOCK_DATA:
            response = requests.put(
                url=f"http://{DOMAIN_NAME}:1587/v1/account",
                json=data,
            )
            if not response:
                raise RuntimeError(
                    f"Failed to save. The service returned {response.status_code}."
                )

    def clear(self) -> None:
        """Clears all of the user's data locally."""
        self.name = ""
        self.email = ""
        self.region = None
        self.services = []
        for genre in self.genre_habits:
            self.genre_habits[genre] = 0

    def __copy__(self) -> NoReturn:
        raise RuntimeError("The User singleton object cannot be copied.")

    def __deepcopy__(self, _) -> NoReturn:
        raise RuntimeError("The User singleton object cannot be copied.")

    def is_valid(self) -> bool:
        """Checks if the user object currently has valid data.

        Does not validate the user's password.
        """
        if not EmailValidator().validate(self.email):
            return False
        if not bool(self.name and self.region is not None and self.services):
            return False
        return self.region in CountryCode


user = User()
