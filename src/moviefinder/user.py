from typing import NoReturn
from typing import Optional

from moviefinder.item import CountryCode
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
        self.region: Optional[CountryCode] = None
        self.services: list[ServiceName] = []

    def save(
        self,
        name: str,
        email: str,
        region: CountryCode,
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
        data = {
            "name": self.name,
            "email": self.email,
            "region": self.region.name.lower(),
            "services": [service.value.lower() for service in self.services],
        }
        if password:
            data["password"] = password
        # requests.post("https://chuadevs.com:1587/v1/user/", json=data)  # TODO

    def clear(self) -> None:
        """Clears all of the user's data locally."""
        self.name = ""
        self.email = ""
        self.region = None
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
        if not bool(self.name and self.region is not None and self.services):
            return False
        return self.region in CountryCode


user = User()
