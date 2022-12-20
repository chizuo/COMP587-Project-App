from typing import NoReturn
from typing import Optional

import requests
from moviefinder.movie import CountryCode
from moviefinder.movie import ServiceName
from moviefinder.movie import USE_MOCK_DATA
from moviefinder.validators import EmailValidator
from PySide6 import QtWidgets


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
        already exists or if there was an error connecting to the service.
        """
        self.clear()
        self.name = name
        self.email = email
        self.region = region
        self.services = services
        if USE_MOCK_DATA:
            return True
        response = requests.post(
            url="http://chuadevs.com:1587/v1/register",
            json={
                "name": self.name,
                "email": self.email,
                "country": self.region.name.lower(),
                "services": [s.value for s in self.services],
                "password": password,
            },
        )
        if response.status_code == 403:
            msg = QtWidgets.QMessageBox()
            msg.setText("An account with this email address already exists.")
            msg.exec()
            return False
        if response.status_code == 406:
            msg = QtWidgets.QMessageBox()
            msg.setText("Error communicating with the service.")
            msg.exec()
            return False
        if not response:
            msg = QtWidgets.QMessageBox()
            msg.setText("Unable to connect to the service.")
            msg.exec()
            return False
        return True

    def update_and_save(
        self,
        name: str,
        region: CountryCode,
        services: list[ServiceName],
        password: str,
    ) -> None:
        """Updates and saves the user's data to the database.

        If the password is empty, it will not be saved. Assumes the account already
        exists.
        """
        self.name = name
        self.region = region
        self.services = services
        data = {
            "name": self.name,
            "country": self.region.name.lower(),
            "services": [s.value for s in self.services],
            "genres": self.genre_habits,
        }
        if password:
            data["password"] = password
        if not USE_MOCK_DATA:
            response = requests.put(
                url="http://chuadevs.com:1587/v1/account",
                json=data,
            )
            if not response:
                raise RuntimeError(
                    f"Failed to save. The service returned {response.status_code}."
                )

    def save(self) -> None:
        """Saves all of the user's data to the database.

        Assumes the account already exists.
        """
        assert self.region is not None
        data = {
            "name": self.name,
            "email": self.email,
            "country": self.region.name.lower(),
            "services": [s.value for s in self.services],
            "genres": self.genre_habits,
        }
        if not USE_MOCK_DATA:
            response = requests.put(
                url="http://chuadevs.com:1587/v1/account",
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
