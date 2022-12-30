import enum
from html import escape
from typing import NoReturn

from moviefinder.country_code import CountryCode


USE_MOCK_DATA = False
if USE_MOCK_DATA:
    print("Using mock data.")
DOMAIN_NAME = "76.176.224.129"  # chuadevs.com


class ServiceName(enum.Enum):
    AMAZON_PRIME = "prime"
    APPLE_TV_PLUS = "apple"
    DISNEY_PLUS = "disney"
    HULU = "hulu"
    NETFLIX = "netflix"


class Movie:
    """A movie or a show."""

    def __init__(self, movie_info: dict):
        self.__ok = True
        self.hearted = False
        self.xed = False
        if (
            "imdbID" not in movie_info
            or "title" not in movie_info
            or "genres" not in movie_info
            or "countries" not in movie_info
            or "videoURL" not in movie_info
        ):
            self.__ok = False
            return
        self.id: str = movie_info["imdbID"]
        self.title: str = movie_info["title"]
        self.genres: list[str] = [genre.lower() for genre in movie_info["genres"]]
        self.regions: list[CountryCode] = []
        for region in movie_info["countries"]:
            region = region.upper()
            try:
                self.regions.append(CountryCode[region])
            except KeyError:
                print(f"Unknown region: {region}")
        self.services: dict[ServiceName, str] = {}  # maps names to video URLs
        url: str = movie_info["videoURL"].lower()
        if "amazon.com" in url:
            self.services[ServiceName.AMAZON_PRIME] = url
        elif "tv.apple.com" in url:
            self.services[ServiceName.APPLE_TV_PLUS] = url
        elif "disneyplus.com" in url:
            self.services[ServiceName.DISNEY_PLUS] = url
        elif "hulu.com" in url:
            self.services[ServiceName.HULU] = url
        elif "netflix.com" in url:
            self.services[ServiceName.NETFLIX] = url
        self.imdb_rating_percent: int = -1
        if "imdbRating" in movie_info:
            self.imdb_rating_percent = movie_info["imdbRating"]
        self.imdb_vote_count: int = -1
        if "imdbVoteCount" in movie_info:
            self.imdb_vote_count = movie_info["imdbVoteCount"]
        if "posterURL" in movie_info:
            self.poster_url: str = movie_info["posterURL"]
        else:
            t = escape(self.title)
            self.poster_url = f"https://via.placeholder.com/235x350.png?text={t}"
        self.release_year: int = -1
        if "year" in movie_info:
            self.release_year = movie_info["year"]
        self.runtime_minutes: int = -1
        if "runtime" in movie_info:
            self.runtime_minutes = movie_info["runtime"]
        self.cast: list[str] = []
        if "cast" in movie_info:
            self.cast = movie_info["cast"]
        self.directors: list[str] = []
        if "director" in movie_info:
            self.directors = movie_info["director"]
        self.writers: list[str] = []
        if "writer" in movie_info:
            self.writers = movie_info["writer"]
        self.overview: str = ""
        if "overview" in movie_info:
            self.overview = movie_info["overview"]
        self.tagline: str = ""
        if "tagline" in movie_info:
            self.tagline = movie_info["tagline"]

    def __bool__(self) -> bool:
        return self.__ok

    def __hash__(self) -> int:
        return hash(self.id)

    def __copy__(self) -> NoReturn:
        raise RuntimeError("Movie objects cannot be copied.")

    def __deepcopy__(self, _) -> NoReturn:
        raise RuntimeError("Movie objects cannot be copied.")
