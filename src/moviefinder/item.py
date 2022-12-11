import enum
import json
from typing import NoReturn

from moviefinder.resources import country_codes_json_path


class ServiceName(enum.Enum):
    APPLE_TV_PLUS = "Apple TV+"
    DISNEY_PLUS = "Disney+"
    HBO_MAX = "HBO Max"
    HULU = "Hulu"
    NETFLIX = "Netflix"


# country_codes is a dict of country ISO 3166 Alpha-2 codes mapped to country names.
with open(country_codes_json_path, "r", encoding="utf8") as file:
    country_codes: dict[str, str] = json.load(file)


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
        self.regions: list[str] = []
        for region in movie_info["countries"]:
            self.regions.append(country_codes[region])
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
