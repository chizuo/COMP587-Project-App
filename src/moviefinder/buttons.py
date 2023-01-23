from moviefinder.abstract_movie_widget import AbstractMovieWidget
from moviefinder.movies import movies
from moviefinder.resources import empty_heart_icon_path
from moviefinder.resources import filled_heart_icon_path
from moviefinder.resources import red_x_icon_path
from moviefinder.service_name import ServiceName
from moviefinder.user import user
from PySide6 import QtGui
from PySide6 import QtWidgets


def init_buttons(widget: AbstractMovieWidget, movie_id: str, browse_widget) -> None:
    """Connects, sets icons for, & disables/enables a widget's buttons.

    If the widget's buttons already have any connections on the ``clicked`` signal, all
    of these connections will be disconnected first.
    """
    w = widget
    id = movie_id
    bw = browse_widget
    try:
        w.heart_button.clicked.disconnect()
    except RuntimeError:
        pass
    try:
        w.x_button.clicked.disconnect()
    except RuntimeError:
        pass
    w.heart_button.clicked.connect(
        lambda __on_h_click=__on_heart_click, w=w, id=id: __on_h_click(w, id)
    )
    w.x_button.clicked.connect(
        lambda __on_x_click=__on_x_click, id=id, bw=bw: __on_x_click(id, bw)
    )
    if movies[id].hearted:
        w.heart_button.setIcon(QtGui.QIcon(filled_heart_icon_path))
        w.x_button.setDisabled(True)
    else:
        w.heart_button.setIcon(QtGui.QIcon(empty_heart_icon_path))
        w.x_button.setDisabled(False)
    w.x_button.setIcon(QtGui.QIcon(red_x_icon_path))


def __on_heart_click(widget: AbstractMovieWidget, movie_id: str) -> None:
    """Responds to a widget's heart button being clicked."""
    if not movies[movie_id].hearted:
        movies[movie_id].hearted = True
        widget.heart_button.setIcon(QtGui.QIcon(filled_heart_icon_path))
        widget.x_button.setDisabled(True)
        for genre in movies[movie_id].genres:
            if genre not in user.genre_habits:
                print(f"Genre '{genre}' not in user's genre habits.")
            else:
                user.genre_habits[genre] += 1
    else:
        movies[movie_id].hearted = False
        widget.heart_button.setIcon(QtGui.QIcon(empty_heart_icon_path))
        widget.x_button.setDisabled(False)
        for genre in movies[movie_id].genres:
            if genre not in user.genre_habits:
                print(f"Genre '{genre}' not in user's genre habits.")
            else:
                user.genre_habits[genre] -= 1


def __on_x_click(movie_id: str, browse_widget) -> None:
    """Responds to a widget's x button being clicked."""
    del movies[movie_id]
    browse_widget.movie_widgets[movie_id].setParent(None)
    del browse_widget.movie_widgets[movie_id]
    user.declined_movies.append(movie_id)
    browse_widget.reset_movies_layout()


def add_services_groupbox(widget: QtWidgets.QWidget) -> None:
    """Adds a groupbox with checkboxes for streaming services to the widget.

    The widget's layout must be a ``QtWidgets.QFormLayout``.

    Attributes added
    ----------------
    services_group_box : QtWidgets.QGroupBox
    amazon_prime_checkbox : QtWidgets.QCheckBox
    apple_tv_plus_checkbox : QtWidgets.QCheckBox
    disney_plus_checkbox : QtWidgets.QCheckBox
    hulu_checkbox : QtWidgets.QCheckBox
    netflix_checkbox : QtWidgets.QCheckBox
    """
    widget.services_group_box = QtWidgets.QGroupBox("services")
    services_layout = QtWidgets.QVBoxLayout()
    widget.amazon_prime_checkbox = QtWidgets.QCheckBox(ServiceName.AMAZON_PRIME.value)
    widget.amazon_prime_checkbox.setChecked(ServiceName.AMAZON_PRIME in user.services)
    services_layout.addWidget(widget.amazon_prime_checkbox)
    widget.apple_tv_plus_checkbox = QtWidgets.QCheckBox(ServiceName.APPLE_TV_PLUS.value)
    widget.apple_tv_plus_checkbox.setChecked(ServiceName.APPLE_TV_PLUS in user.services)
    services_layout.addWidget(widget.apple_tv_plus_checkbox)
    widget.disney_plus_checkbox = QtWidgets.QCheckBox(ServiceName.DISNEY_PLUS.value)
    widget.disney_plus_checkbox.setChecked(ServiceName.DISNEY_PLUS in user.services)
    services_layout.addWidget(widget.disney_plus_checkbox)
    widget.hulu_checkbox = QtWidgets.QCheckBox(ServiceName.HULU.value)
    widget.hulu_checkbox.setChecked(ServiceName.HULU in user.services)
    services_layout.addWidget(widget.hulu_checkbox)
    widget.netflix_checkbox = QtWidgets.QCheckBox(ServiceName.NETFLIX.value)
    widget.netflix_checkbox.setChecked(ServiceName.NETFLIX in user.services)
    services_layout.addWidget(widget.netflix_checkbox)
    widget.services_group_box.setLayout(services_layout)
    widget.layout.addRow(widget.services_group_box)
