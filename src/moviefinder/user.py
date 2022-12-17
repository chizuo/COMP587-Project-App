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
    ) -> None:
        """Creates a new account and saves it in the database."""
        self.clear()
        self.name = name
        self.email = email
        self.region = region
        self.services = services
        # requests.post(  # TODO
        #     url="http://chuadevs.com:1587/v1/account",
        #     json={
        #         "name": self.name,
        #         "email": self.email,
        #         "region": self.region.name.lower(),
        #         "services": [service.value.lower() for service in self.services],
        #         "password": password,
        #     },
        # )

    def save(
        self,
        name: str,
        email: str,
        region: CountryCode,
        services: list[ServiceName],
        password: str,
    ) -> None:
        """Saves all of the user's data to the database except their genre habits.

        If the password is empty, it will not be saved. Assumes the account already
        exists.
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
        # response = requests.put(  # TODO
        #     url="http://chuadevs.com:1587/v1/account",
        #     json=data,
        # )
        # if not response:
        #     raise RuntimeError(
        #         f"Failed to save. The service returned {response.status_code}."
        #     )

    def __del__(self) -> None:
        self.save_genre_habits()

    def save_genre_habits(self) -> None:
        """Saves the user's genre habits to the database."""
        # TODO
        # response = requests.put(
        #     url="http://chuadevs.com:1587/v1/account",
        #     json={
        #         "genres": user.genre_habits,
        #     },
        # )
        # if not response:
        #     raise RuntimeError(
        #         f"Failed to save. The service returned {response.status_code}."
        #     )

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
