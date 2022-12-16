import enum
from typing import NoReturn

from moviefinder.country_code import CountryCode


class ServiceName(enum.Enum):
    APPLE_TV_PLUS = "Apple TV+"
    DISNEY_PLUS = "Disney+"
    HBO_MAX = "HBO Max"
    HULU = "Hulu"
    NETFLIX = "Netflix"


genres = [
    "all genres",
    "action",
    "adult",
    "adventure",
    "animation",
    "biography",
    "comedy",
    "crime",
    "documentary",
    "drama",
    "family",
    "fantasy",
    "film noir",
    "game show",
    "historical",
    "horror",
    "musical",
    "musical",
    "mystery",
    "news",
    "reality",
    "romance",
    "science fiction",
    "short",
    "sport",
    "talk show",
    "thriller",
    "war",
    "western",
]


class Item:
    """A movie or a show."""

    def __init__(self, movie_info: dict):
        self.hearted = False
        self.xed = False
        self.id: str = movie_info["imdbID"]
        self.imdb_rating_percent: int = movie_info["imdbRating"]
        self.imdb_vote_count: int = movie_info["imdbVoteCount"]
        self.poster_url: str = movie_info["posterURL"]
        self.title: str = movie_info["title"]
        self.genres: list[str] = movie_info["genres"]
        self.regions: list[CountryCode] = []
        for region in movie_info["countries"]:
            region = region.upper()
            try:
                self.regions.append(CountryCode[region])
            except KeyError:
                print(f"Unknown region: {region}")
        self.release_year: int = movie_info["year"]
        self.runtime_minutes: int = movie_info["runtime"]
        self.cast: list[str] = movie_info["cast"]
        self.directors: list[str] = movie_info["director"]
        self.overview: str = movie_info["overview"]
        self.tagline: str = movie_info["tagline"]
        self.services: dict[ServiceName, str] = {}  # maps names to video URLs
        url: str = movie_info["videoURL"].lower()
        if "tv.apple.com" in url:
            self.services[ServiceName.APPLE_TV_PLUS] = url
        elif "disneyplus.com" in url:
            self.services[ServiceName.DISNEY_PLUS] = url
        elif "hbomax.com" in url:
            self.services[ServiceName.HBO_MAX] = url
        elif "hulu.com" in url:
            self.services[ServiceName.HULU] = url
        elif "netflix.com" in url:
            self.services[ServiceName.NETFLIX] = url

    def __hash__(self) -> int:
        return hash(self.id)

    def __copy__(self) -> NoReturn:
        raise RuntimeError("Item objects cannot be copied.")

    def __deepcopy__(self, _) -> NoReturn:
        raise RuntimeError("Item objects cannot be copied.")
