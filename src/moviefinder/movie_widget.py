from moviefinder.abstract_movie_widget import AbstractMovieWidget
from moviefinder.buttons import init_buttons
from moviefinder.movie import POSTER_HEIGHT
from moviefinder.movie import POSTER_WIDTH
from moviefinder.movies import movies
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class MovieWidget(AbstractMovieWidget):
    """A custom widget for displaying one movie's poster and buttons.

    Unlike ``movie_menu``, objects of this class are intended to be put into the layout
    of a larger widget or menu such as ``browse_widget``.
    """

    def __init__(self, movie_id: str):
        QtWidgets.QWidget.__init__(self)
        self.__ok: bool = True
        if movie_id is None:
            self.__ok = False
            print("Error: `movie_id` must not be None.")
            return
        if movie_id == "":
            self.__ok = False
            print("Error: `movie_id` must not be an empty string.")
            return
        self.movie_id = movie_id
        self.layout = QtWidgets.QVBoxLayout(self)
        self.poster_button = QtWidgets.QPushButton()
        self.poster_button.setStyleSheet(
            "QPushButton:hover { background-color: none; }"
        )
        self.poster_button.setFlat(True)
        poster_icon = QtGui.QIcon(movies[self.movie_id].poster_pixmap)
        self.poster_button.setIcon(poster_icon)
        self.poster_button.setIconSize(QtCore.QSize(POSTER_WIDTH, POSTER_HEIGHT))
        self.poster_button.setMaximumSize(self.poster_button.iconSize())
        self.layout.addWidget(self.poster_button)
        buttons_layout = QtWidgets.QHBoxLayout()
        button_style_sheet = """
            QPushButton {
                width: %spx;
            }
            """ % (
            POSTER_WIDTH // 2 - 15
        )
        self.heart_button = QtWidgets.QPushButton()
        self.heart_button.setStyleSheet(button_style_sheet)
        buttons_layout.addWidget(self.heart_button)
        self.x_button = QtWidgets.QPushButton()
        self.x_button.setStyleSheet(button_style_sheet)
        buttons_layout.addWidget(self.x_button)
        buttons_layout.addStretch()
        self.update_movie_buttons()
        self.layout.addLayout(buttons_layout)

    def update_movie_buttons(self) -> None:
        assert self.movie_id is not None
        init_buttons(self, self.movie_id)

    def __bool__(self) -> bool:
        return self.__ok
