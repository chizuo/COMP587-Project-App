import json
from collections import UserDict
from typing import Any
from typing import NoReturn
from typing import Optional

import requests
from moviefinder.movie import DOMAIN_NAME
from moviefinder.movie import Movie
from moviefinder.movie import USE_MOCK_DATA
from moviefinder.resources import sample_movies_json_path
from moviefinder.user import user


class Movies(UserDict):
    """A singleton dictionary of movies and shows.

    The keys are IDs and the values are Movie objects.
    """

    __instance: Optional["Movies"] = None

    def __new__(cls) -> "Movies":
        if cls.__instance is None:
            cls.__instance = super(Movies, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__()
        self.genres: list[str] = []

    def __copy__(self) -> NoReturn:
        raise RuntimeError("The Movies singleton object cannot be copied.")

    def __deepcopy__(self, _) -> NoReturn:
        raise RuntimeError("The Movies singleton object cannot be copied.")

    def load(self) -> bool:
        """Loads movies and shows from the service.

        Assumes the user object has already been loaded and has valid data. Returns True
        if the movies were loaded successfully. Returns False if unable to get a valid
        response from the service.
        """
        if self.data:
            raise RuntimeError(
                "Cannot load movies when they are already loaded."
                " Use the clear function if needed."
            )
        print("Loading movies...")
        assert self.genres, "Genres must be set before loading movies."
        if USE_MOCK_DATA:
            with open(sample_movies_json_path, "r", encoding="utf8") as file:
                service_obj: dict[str, Any] = json.load(file)
                # total_pages: int = service_obj["total_pages"]  # TODO
                movies_data: list[dict] = service_obj["movies"]
        else:
            try:
                assert user.region is not None
                response = requests.get(
                    url=f"http://{DOMAIN_NAME}:1587/v1/movie",
                    json={
                        "country": user.region.name.lower(),
                        "genre": [genre.title() for genre in self.genres],
                        "language": "en",
                        "orderBy": "original_title",  # "original_title" or "year"
                        "page": "1",
                        "services": [
                            service.value.lower() for service in user.services
                        ],
                    },
                    verify=False,
                )
            except Exception as e:
                print(e)
                return False
            else:
                if not response:
                    return False
                response.encoding = "utf-8"
                response_dict = response.json()
                # total_pages: int = response_dict["total_pages"]  # TODO
                movies_data = response_dict["movies"]
        for movie_data in movies_data:
            new_movie = Movie(movie_data)
            if self.__service_region_and_genres_match(new_movie):
                self.data[new_movie.id] = new_movie
        return True

    def __service_region_and_genres_match(self, movie: Movie) -> bool:
        """Checks if the user has the service, region, & genres of the movie."""
        if user.region not in movie.regions:
            print(f"\t{movie.title} not loaded because there is no matching region.")
            return False
        for service in user.services:
            if service in movie.services:
                break
        else:
            print(f"\t{movie.title} not loaded because there is no matching service.")
            return False
        for genre in self.genres:
            if genre in movie.genres:
                break
        else:
            print(f"\t{movie.title} not loaded because there is no matching genre.")
            return False
        print(f"\t{movie.title} loaded.")
        return True


movies = Movies()
