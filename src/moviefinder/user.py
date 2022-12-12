from typing import NoReturn
from typing import Optional

from moviefinder.item import country_codes
from moviefinder.item import ServiceName
from moviefinder.validators import EmailValidator


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
        self.region = ""
        self.services: list[ServiceName] = []

    def save(
        self,
        name: str,
        email: str,
        region: str,
        services: list[ServiceName],
        password: str,
    ) -> None:
        """Saves all of the user's data to the database.

        If the password is empty, it will not be saved.
        """
        self.name = name
        self.email = email
        self.region = region
        self.services = services
        # TODO: check whether the password string is empty. If it is, don't save it.
        pass  # TODO

    def clear(self) -> None:
        """Clears all of the user's data."""
        self.name = ""
        self.email = ""
        self.region = ""
        self.services = []

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
        if not bool(self.name and self.region and self.services):
            return False
        return self.region in country_codes.values()


user = User()
