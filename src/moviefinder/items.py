import json
from collections import UserDict
from typing import Any
from typing import NoReturn
from typing import Optional

from moviefinder.item import Item
from moviefinder.resources import sample_movies_json_path
from moviefinder.user import User


class Items(UserDict):
    """A singleton dictionary of movies and shows.

    The keys are IDs and the values are Item objects.
    """

    __instance: Optional["Items"] = None

    def __new__(cls) -> "Items":
        if cls.__instance is None:
            cls.__instance = super(Items, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__()
        self.user: Optional[User] = None

    def __copy__(self) -> NoReturn:
        raise RuntimeError("The Items singleton object cannot be copied.")

    def __deepcopy__(self, _) -> NoReturn:
        raise RuntimeError("The Items singleton object cannot be copied.")

    def load(self, user: User) -> None:
        self.user = user
        if self.data:
            raise RuntimeError(
                "Cannot load items when they are already loaded."
                " Use the clear function if needed."
            )
        with open(sample_movies_json_path, "r", encoding="utf8") as file:
            service_obj: dict[str, Any] = json.load(file)
            # total_pages: int = service_obj["total_pages"]
            items_data: list[dict] = service_obj["movies"]
            for item_data in items_data:
                new_item = Item(item_data)
                if self.__service_and_region_match(user, new_item):
                    self.data[new_item.id] = new_item

    def __service_and_region_match(self, user: User, item: Item) -> bool:
        """Checks if the user has the service & region of the item."""
        # TODO
        return True


items = Items()
