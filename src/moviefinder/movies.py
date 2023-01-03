import json
from collections import UserDict
from random import shuffle
from typing import Any
from typing import NoReturn
from typing import Optional

import requests
from moviefinder.movie import Movie
from moviefinder.movie import SERVICE_BASE_URL
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
        """Loads movies from the service.

        Assumes the user object has already been loaded and has valid data. Returns True
        if the movies were loaded successfully, returns False otherwise. Calling this
        method will not clear any current data; the method can be called multiple times
        to load more movies.
        """
        print("Loading movies...")
        if not self.genres:
            print("Error: genres must be set before loading movies.")
            return False
        if not user.region:
            print("Error: user region must be set before loading movies.")
            return False
        if USE_MOCK_DATA:
            with open(sample_movies_json_path, "r", encoding="utf8") as file:
                return self.__add_movies(json.load(file))
        if self.total_pages is not None and self.current_page >= self.total_pages:
            print("No more movies to load.")
            return False
        self.current_page += 1
        try:
            print("Sending request for movies...")
            response = requests.get(
                url=f"{SERVICE_BASE_URL}/movie",
                json={
                    "country": user.region.name.lower(),
                    "genre": [genre.title() for genre in self.genres],
                    "language": "en",
                    "orderBy": "year",  # "original_title" or "year"
                    "page": str(self.current_page),
                    "services": [service.value.lower() for service in user.services],
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
        return self.__add_movies(response.json())

    def __add_movies(self, response_data: dict[str, Any]) -> bool:
        """Adds movies to ``self.data`` from a web request response.

        Returns True if the movies were added successfully, returns False otherwise.
        """
        self.total_pages = response_data["total_pages"]
        movies_data: list[dict] = response_data["movies"]
        if not movies_data:
            print("Error: no movies were received from the service.")
            return False
        new_movies: dict[str, Movie] = {}
        for movie_data in movies_data:
            new_movie = Movie(movie_data)
            if new_movie and self.__service_region_and_genres_match(new_movie):
                new_movies[new_movie.id] = new_movie
        if not new_movies:
            print("Error: none of the movies from the service were valid.")
            return False
        items = list(new_movies.items())
        shuffle(items)
        self.data.update(items)
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
