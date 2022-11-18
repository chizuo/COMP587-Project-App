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
        self.regions: list[str] = movie_info["countries"]
        self.release_year: int = movie_info["year"]
        self.runtime_minutes: int = movie_info["runtime"]
        self.cast: list[str] = movie_info["cast"]
        self.directors: list[str] = movie_info["director"]
        self.overview: str = movie_info["overview"]
        self.tagline: str = movie_info["tagline"]
        self.streaming_services: dict[str, str] = {}  # maps names to video URLs
        url: str = movie_info["videoURL"].lower()
        if "tv.apple.com" in url:
            self.streaming_services["Apple TV+"] = url
        elif "disneyplus.com" in url:
            self.streaming_services["Disney+"] = url
        elif "hbomax.com" in url:
            self.streaming_services["HBO Max"] = url
        elif "hulu.com" in url:
            self.streaming_services["Hulu"] = url
        elif "netflix.com" in url:
            self.streaming_services["Netflix"] = url

    def __hash__(self) -> int:
        return hash(self.id)
