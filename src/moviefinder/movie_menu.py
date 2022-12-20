import webbrowser
from textwrap import dedent

from moviefinder.abstract_movie_widget import AbstractMovieWidget
from moviefinder.buttons import init_buttons
from moviefinder.country_code import CountryCode
from moviefinder.movie import Movie
from moviefinder.movie import ServiceName
from moviefinder.movies import movies
from moviefinder.resources import corner_up_left_arrow_icon_path
from moviefinder.scaled_label import ScaledLabel
from moviefinder.validators import valid_services
from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class MovieMenu(AbstractMovieWidget):
    """A menu that displays info about one movie or show.

    After creating an MovieMenu object, call ``update_movie_data`` to choose which movie
    or show it should display when opened.
    """

    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.movie_id: str | None = None
        top_buttons_layout = QtWidgets.QHBoxLayout()
        self.back_button = QtWidgets.QPushButton()
        self.back_button.setIcon(QtGui.QIcon(corner_up_left_arrow_icon_path))
        self.back_button.clicked.connect(main_window.show_browse_menu)
        top_buttons_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        self.options_button = main_window.create_options_button(self)
        top_buttons_layout.addWidget(self.options_button, alignment=Qt.AlignRight)
        self.layout.addLayout(top_buttons_layout)
        self.movie_layout = QtWidgets.QHBoxLayout()
        self.poster_label = ScaledLabel()
        self.movie_layout.addWidget(self.poster_label)
        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_text_browser = QtWidgets.QTextBrowser(self)
        self.right_text_browser.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        self.right_layout.addWidget(self.right_text_browser)
        self.heart_button = QtWidgets.QPushButton()
        heart_and_x_buttons_layout = QtWidgets.QHBoxLayout()
        heart_and_x_buttons_layout.addWidget(self.heart_button)
        self.x_button = QtWidgets.QPushButton()
        heart_and_x_buttons_layout.addWidget(self.x_button)
        self.right_layout.addLayout(heart_and_x_buttons_layout)
        self.apple_tv_plus_button = QtWidgets.QPushButton(
            ServiceName.APPLE_TV_PLUS.value
        )
        stream_buttons_layout = QtWidgets.QHBoxLayout()
        stream_buttons_layout.addWidget(self.apple_tv_plus_button)
        self.disney_plus_button = QtWidgets.QPushButton(ServiceName.DISNEY_PLUS.value)
        stream_buttons_layout.addWidget(self.disney_plus_button)
        self.hbo_max_button = QtWidgets.QPushButton(ServiceName.HBO_MAX.value)
        stream_buttons_layout.addWidget(self.hbo_max_button)
        self.hulu_button = QtWidgets.QPushButton(ServiceName.HULU.value)
        stream_buttons_layout.addWidget(self.hulu_button)
        self.netflix_button = QtWidgets.QPushButton(ServiceName.NETFLIX.value)
        stream_buttons_layout.addWidget(self.netflix_button)
        self.right_layout.addLayout(stream_buttons_layout)
        self.movie_layout.addLayout(self.right_layout)
        self.layout.addLayout(self.movie_layout)

    def update_movie_data(self, movie_id: str, poster_pixmap: QtGui.QPixmap) -> bool:
        """Returns True if successful, False otherwise.

        This function may fail if the movie's data does not make sense.
        """
        if not movie_id or not self.is_valid_movie(movie_id):
            return False
        self.movie_id = movie_id
        init_buttons(self, self.movie_id)
        self.poster_label.setPixmap(poster_pixmap)
        hours = movies[self.movie_id].runtime_minutes // 60
        minutes = movies[self.movie_id].runtime_minutes % 60
        duration = f"{hours}h {minutes}m" if hours else f"{minutes}m"
        rating = f"{movies[self.movie_id].imdb_rating_percent}/100"
        self.right_text_browser.setText(
            dedent(
                f"""\
                <h1>{movies[self.movie_id].title}</h1>
                <p><em>{movies[self.movie_id].tagline}</em></p>
                <p>{"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join(
                    (str(movies[self.movie_id].release_year), rating, duration)
                )}</p>
                <p>{", ".join(movies[self.movie_id].genres)}</p>
                <h2>Overview</h2>
                {movies[self.movie_id].overview}
                <h2>Cast</h2>
                {", ".join(movies[self.movie_id].cast)}
                <h2>Directors</h2>
                {", ".join(movies[self.movie_id].directors)}
                """
            )
        )
        service_names = movies[self.movie_id].services.keys()
        if ServiceName.APPLE_TV_PLUS in service_names:
            self.apple_tv_plus_button.setVisible(True)
            try:
                self.apple_tv_plus_button.clicked.disconnect()
            except RuntimeError:
                pass
            self.apple_tv_plus_button.clicked.connect(
                lambda: webbrowser.open_new_tab(
                    movies[self.movie_id].services[ServiceName.APPLE_TV_PLUS]
                )
            )
        else:
            self.apple_tv_plus_button.setVisible(False)
        if ServiceName.DISNEY_PLUS in service_names:
            self.disney_plus_button.setVisible(True)
            try:
                self.disney_plus_button.clicked.disconnect()
            except RuntimeError:
                pass
            self.disney_plus_button.clicked.connect(
                lambda: webbrowser.open_new_tab(
                    movies[self.movie_id].services[ServiceName.DISNEY_PLUS]
                )
            )
        else:
            self.disney_plus_button.setVisible(False)
        if ServiceName.HBO_MAX in service_names:
            self.hbo_max_button.setVisible(True)
            try:
                self.hbo_max_button.clicked.disconnect()
            except RuntimeError:
                pass
            self.hbo_max_button.clicked.connect(
                lambda: webbrowser.open_new_tab(
                    movies[self.movie_id].services[ServiceName.HBO_MAX]
                )
            )
        else:
            self.hbo_max_button.setVisible(False)
        if ServiceName.HULU in service_names:
            self.hulu_button.setVisible(True)
            try:
                self.hulu_button.clicked.disconnect()
            except RuntimeError:
                pass
            self.hulu_button.clicked.connect(
                lambda: webbrowser.open_new_tab(
                    movies[self.movie_id].services[ServiceName.HULU]
                )
            )
        else:
            self.hulu_button.setVisible(False)
        if ServiceName.NETFLIX in service_names:
            self.netflix_button.setVisible(True)
            try:
                self.netflix_button.clicked.disconnect()
            except RuntimeError:
                pass
            self.netflix_button.clicked.connect(
                lambda: webbrowser.open_new_tab(
                    movies[self.movie_id].services[ServiceName.NETFLIX]
                )
            )
        else:
            self.netflix_button.setVisible(False)
        return True

    def is_valid_movie(self, movie_id: str) -> bool:
        try:
            assert movie_id in movies, f"Invalid movie: {movie_id}"
            movie: Movie = movies[movie_id]
            assert isinstance(
                movie.hearted, bool
            ), f"Type error: hearted is a {type(movie.hearted)}"
            assert isinstance(
                movie.xed, bool
            ), f"Type error: xed is a {type(movie.xed)}"
            assert movie.id, "Error: id is falsy"
            assert isinstance(movie.id, str), f"Type error: id is a {type(movie.id)}"
            assert isinstance(
                movie.imdb_rating_percent, int
            ), f"Type error: imdb_rating_percent is a {type(movie.imdb_rating_percent)}"
            assert isinstance(
                movie.imdb_vote_count, int
            ), f"Type error: imdb_vote_count is a {type(movie.imdb_vote_count)}"
            assert movie.poster_url, "Error: poster_url is falsy"
            assert isinstance(
                movie.poster_url, str
            ), f"Type error: poster_url is a {type(movie.poster_url)}"
            assert movie.title, "Error: title is falsy"
            assert isinstance(
                movie.title, str
            ), f"Type error: title is a {type(movie.title)}"
            assert isinstance(
                movie.genres, list
            ), f"Type error: genres is a {type(movie.genres)}"
            assert isinstance(
                movie.genres[0], str
            ), f"Type error: genres[0] is a {type(movie.genres[0])}"
            assert movie.regions, "Error: regions is falsy"
            assert isinstance(
                movie.regions, list
            ), f"Type error: regions is a {type(movie.regions)}"
            assert isinstance(
                movie.regions[0], CountryCode
            ), f"Type error: regions[0] is a {type(movie.regions[0])}"
            assert movie.release_year, "Error: release_year is falsy"
            assert isinstance(
                movie.release_year, int
            ), f"Type error: release_year is a {type(movie.release_year)}"
            assert isinstance(
                movie.runtime_minutes, int
            ), f"Type error: runtime_minutes is a {type(movie.runtime_minutes)}"
            assert movie.runtime_minutes, "Error: runtime_minutes is falsy"
            assert movie.cast, "Error: cast is falsy"
            assert isinstance(
                movie.cast, list
            ), f"Type error: cast is a {type(movie.cast)}"
            assert isinstance(
                movie.cast[0], str
            ), f"Type error: cast[0] is a {type(movie.cast[0])}"
            assert movie.directors, "Error: directors is falsy"
            assert isinstance(
                movie.directors, list
            ), f"Type error: directors is a {type(movie.directors)}"
            assert isinstance(
                movie.directors[0], str
            ), f"Type error: directors[0] is a {type(movie.directors[0])}"
            assert isinstance(
                movie.overview, str
            ), f"Type error: overview is a {type(movie.overview)}"
            assert isinstance(
                movie.tagline, str
            ), f"Type error: tagline is a {type(movie.tagline)}"
            assert isinstance(
                movie.services, dict
            ), f"Type error: services is a {type(movie.services)}"
            assert movie.services, "Error: services is falsy"
            assert valid_services(
                movie.services
            ), f"Error: invalid service(s): {movie.services}"
        except AssertionError as e:
            print(f"    {e}")
            return False
        return True
