from datetime import timedelta


class Item:
    def __init__(
        self,
        *,
        title: str,
        release_year: int,
        age_rating: str,
        rating: str,
        duration: timedelta,
        keywords: list[str],
        synopsis: str,
        cast: list[str],
        directors: list[str],
        writers: list[str],
        companies: list[str],
        poster_link: str,
        trailer_link: str,
        stream_link: str,
    ):
        self.title = title
        self.release_year = release_year
        self.age_rating = age_rating
        self.rating = rating
        self.duration = duration
        self.keywords = keywords
        self.synopsis = synopsis
        self.cast = cast
        self.directors = directors
        self.writers = writers
        self.companies = companies
        self.poster_link = poster_link
        self.trailer_link = trailer_link
        self.stream_link = stream_link
