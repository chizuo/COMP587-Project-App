from moviefinder.movie_menu import MovieMenu
from moviefinder.movie_widget import MovieWidget
from moviefinder.movies import movies
from PySide6 import QtWidgets


class BrowseWidget(QtWidgets.QWidget):
    """A widget that displays a list of movies and shows.

    This widget is deleted and recreated every time the user changes the genres,
    services, and/or region.
    """

    def __init__(self, main_window: QtWidgets.QMainWindow):
        QtWidgets.QWidget.__init__(self)
        self.__START_ROW_COUNT = 2
        self.__MOVIES_PER_ROW = 4
        self.__total_shown_movie_count = 0
        self.__MAX_SHOWN_MOVIES = 30 * self.__MOVIES_PER_ROW
        self.main_window = main_window
        self.movie_menu: MovieMenu | None = None
        self.layout = QtWidgets.QVBoxLayout(self)
        self.movies_layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.movies_layout)
        self.layout.addSpacerItem(QtWidgets.QSpacerItem(1, 100))
        self.movie_widgets: dict[str, MovieWidget] = {}  # movie_id: MovieWidget
        self.__row_movie_count = 0
        self.row_layout = QtWidgets.QHBoxLayout()
        if movies:
            self.load_starting_movie_rows()
        else:
            self.layout.addWidget(
                QtWidgets.QLabel(
                    "No movies match your chosen genres, services, and region."
                )
            )

    def load_starting_movie_rows(self) -> None:
        for _ in range(self.__START_ROW_COUNT):
            self.add_row()

    def update_movie_widgets(self) -> None:
        for movie_widget in self.movie_widgets.values():
            movie_widget.update_movie_data()

    def show_movie_menu(self, movie_id: str) -> None:
        if self.movie_menu is None:
            self.movie_menu = MovieMenu(self.main_window)
            self.main_window.central_widget.addWidget(self.movie_menu)
        if not self.movie_menu.update_movie_data(
            movie_id, self.movie_widgets[movie_id].poster_pixmap
        ):
            print(f'Error: movie "{movie_id}" is invalid.')
        else:
            self.main_window.central_widget.setCurrentWidget(self.movie_menu)

    def add_row(self) -> None:
        if self.__total_shown_movie_count >= self.__MAX_SHOWN_MOVIES:
            print("Maximum number of movies shown.")
            return
        if self.__total_shown_movie_count >= len(movies) - 2 * self.__MOVIES_PER_ROW:
            if not movies.load():
                return
        is_new_row = False
        if self.__row_movie_count == 0:
            is_new_row = True
        elif self.__row_movie_count >= self.__MOVIES_PER_ROW:
            is_new_row = True
            self.__row_movie_count = 0
            self.row_layout = QtWidgets.QHBoxLayout()
        for i, movie_id in enumerate(movies):
            if i < self.__total_shown_movie_count:
                continue
            if self.__row_movie_count >= self.__MOVIES_PER_ROW:
                break
            movie_widget = MovieWidget(movie_id)
            if not movie_widget:
                continue
            movie_widget.poster_button.clicked.connect(
                lambda self=self, movie_id=movie_id: self.show_movie_menu(movie_id)
            )
            self.row_layout.addWidget(movie_widget)
            self.movie_widgets[movie_id] = movie_widget
            self.__row_movie_count += 1
            self.__total_shown_movie_count += 1
        if is_new_row:
            self.movies_layout.addLayout(self.row_layout)
        else:
            scroll_bar = self.main_window.browse_menu.scroll_bar
            scroll_bar.setValue(scroll_bar.maximum() - 1)
