import enum
from typing import NoReturn

from moviefinder.country_code import CountryCode


USE_MOCK_DATA = False
if USE_MOCK_DATA:
    print("Using mock data.")
DOMAIN_NAME = "chuadevs.com"


class ServiceName(enum.Enum):
    AMAZON_PRIME = "amazon"
    APPLE_TV_PLUS = "apple"
    DISNEY_PLUS = "disney"
    HULU = "hulu"
    NETFLIX = "netflix"


class Movie:
    """A movie or a show."""

    def __init__(self, movie_info: dict):
        self.hearted = False
        self.xed = False
        self.id: str = movie_info["imdbID"]
        self.imdb_rating_percent: int = movie_info["imdbRating"]
        self.imdb_vote_count: int = movie_info["imdbVoteCount"]
        self.poster_url: str = movie_info["posterURL"]
        self.title: str = movie_info["title"]
        self.genres: list[str] = [genre.lower() for genre in movie_info["genres"]]
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

    def __hash__(self) -> int:
        return hash(self.id)

    def __copy__(self) -> NoReturn:
        raise RuntimeError("Movie objects cannot be copied.")

    def __deepcopy__(self, _) -> NoReturn:
        raise RuntimeError("Movie objects cannot be copied.")
