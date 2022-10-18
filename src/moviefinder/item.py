from moviefinder.user import User


class Item:
    def __init__(self, movie_info: dict, user: User):
        self.imdb_id: str = movie_info["imdbID"]
        self.imdb_rating_percent: int = movie_info["imdbRating"]
        self.imdb_vote_count: int = movie_info["imdbVoteCount"]
        self.poster_url: str = movie_info["posterURLs"]
        self.genres: list[str] = movie_info["genres"]
        self.release_year: int = movie_info["year"]
        self.runtime_minutes: int = movie_info["runtime"]
        self.cast: list[str] = movie_info["cast"]
        self.directors: list[str] = movie_info["directors"]
        self.title: str = movie_info["title"]
        self.overview: str = movie_info["overview"]
        self.tagline: str = movie_info["tagline"]
        self.streaming_services: dict[str, str] = {}  # maps names to URLs
        for name, info in movie_info["streamingInfo"].items():
            self.streaming_services[name] = info["us"]["link"]
            # TODO: use the user object's region instead of the literal "us".
        self.original_language: str = movie_info["originalLanguage"]
