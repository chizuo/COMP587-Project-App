import json
from collections import UserDict
from typing import Any
from typing import NoReturn
from typing import Optional

from moviefinder.item import Item
from moviefinder.resources import sample_movies_json_path
from moviefinder.user import user


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
        self.genres: list[str] = []

    def __copy__(self) -> NoReturn:
        raise RuntimeError("The Items singleton object cannot be copied.")

    def __deepcopy__(self, _) -> NoReturn:
        raise RuntimeError("The Items singleton object cannot be copied.")

    def load(self) -> bool:
        """Loads movies and shows from the service.

        Assumes the user object has already been loaded and has valid data. Returns True
        if the items were loaded successfully. Returns False if unable to get a valid
        response from the service.
        """
        if self.data:
            raise RuntimeError(
                "Cannot load items when they are already loaded."
                " Use the clear function if needed."
            )
        print("Loading items...")
        assert self.genres, "Genres must be set before loading items."

        # try:
        #     response = requests.get(
        #         url="http://chuadevs.com:1587/v1/movie",
        #         json={
        #             "country": user.region.name.lower(),
        #             "genre": [genre.title() for genre in self.genres],
        #             "language": "en",
        #             "orderBy": "original_title",  # either "original_title" or "year"
        #             "page": "1",
        #             "service": [service.value.lower() for service in user.services],
        #         },
        #         verify=False,
        #     )
        # except Exception as e:
        #     print(e)
        #     return False
        # else:
        #     if not response:
        #         return False
        #     response.encoding = "utf-8"
        #     response_dict = response.json()
        #     # total_pages: int = response_dict["total_pages"]  # TODO
        #     items_data: list[dict] = response_dict["movies"]

        # TODO
        with open(sample_movies_json_path, "r", encoding="utf8") as file:
            service_obj: dict[str, Any] = json.load(file)
            # total_pages: int = service_obj["total_pages"]
            items_data: list[dict] = service_obj["movies"]

        for item_data in items_data:
            new_item = Item(item_data)
            if self.__service_region_and_genres_match(new_item):
                self.data[new_item.id] = new_item
        return True

    def __service_region_and_genres_match(self, item: Item) -> bool:
        """Checks if the user has the service, region, & genres of the item."""
        if user.region not in item.regions:
            print(f"\t{item.title} not loaded because there is no matching region.")
            return False
        for service in user.services:
            if service in item.services:
                break
        else:
            print(f"\t{item.title} not loaded because there is no matching service.")
            return False
        for genre in self.genres:
            if genre in item.genres:
                break
        else:
            print(f"\t{item.title} not loaded because there is no matching genre.")
            return False
        print(f"\t{item.title} loaded.")
        return True


items = Items()
