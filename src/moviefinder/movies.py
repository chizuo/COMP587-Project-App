import json
from collections import UserDict
from random import shuffle
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
        self.total_pages: Optional[int] = None
        self.current_page: int = 0

    def __copy__(self) -> NoReturn:
        raise RuntimeError("The movies singleton object cannot be copied.")

    def __deepcopy__(self, _) -> NoReturn:
        raise RuntimeError("The movies singleton object cannot be copied.")

    def clear(self) -> None:
        """Clears all movies and shows.

        Always call ``browse_widget.movie_widgets.clear()`` immediately after or before
        calling this method (you can just use ``main_window.clear_movies`` to do both).
        """
        self.data.clear()
        self.total_pages = None
        self.current_page = 0

    def load(self) -> bool:
        """Loads movies and shows from the service.

        Assumes the user object has already been loaded and has valid data. Returns True
        if the movies were loaded successfully. Returns False if unable to get a valid
        response from the service. Calling this method will NOT clear any current data.
        """
        print("Loading movies...")
        assert self.genres, "Genres must be set before loading movies."
        if USE_MOCK_DATA:
            with open(sample_movies_json_path, "r", encoding="utf8") as file:
                response_dict: dict[str, Any] = json.load(file)
        else:
            if self.total_pages is not None and self.current_page >= self.total_pages:
                print("No more movies to load.")
                return False
            self.current_page += 1
            try:
                assert user.region is not None, "User region must be set."
                print("Sending request for movies...")
                response = requests.get(
                    url=f"http://{DOMAIN_NAME}:1587/v1/movie",
                    json={
                        "country": user.region.name.lower(),
                        "genre": [genre.title() for genre in self.genres],
                        "language": "en",
                        "orderBy": "year",  # "original_title" or "year"
                        "page": str(self.current_page),
                        "services": [
                            service.value.lower() for service in user.services
                        ],
                    },
                    verify=False,
                )
                print(f"movies {response = }")
            except Exception as e:
                print(f"Exception while loading movies: {e}")
                return False
            if not response:
                print(f"movies {response.content = }")
                print("Error: failed to load more movies. `response` is falsy.")
                return False
            response.encoding = "utf-8"
            response_dict = response.json()
        self.total_pages = response_dict["total_pages"]
        movies_data: list[dict] = response_dict["movies"]
        if not movies_data:
            print("Error: no movies were received from the service.")
            return False
        for movie_data in movies_data:
            new_movie = Movie(movie_data)
            if new_movie and self.__service_region_and_genres_match(new_movie):
                self.data[new_movie.id] = new_movie
        if not self.data:
            print("Error: none of the movies from the service were valid.")
            return False
        items = list(self.items())
        shuffle(items)
        self.data = dict(items)
        print("Movies loaded successfully.")
        return True

    def __service_region_and_genres_match(self, movie: Movie) -> bool:
        """Checks if the user has the service, region, & genres of the movie."""
        if user.region not in movie.regions:
            return False
        for service in user.services:
            if service in movie.services:
                break
        else:
            return False
        for genre in self.genres:
            if genre in movie.genres:
                break
        else:
            return False
        return True


movies = Movies()
