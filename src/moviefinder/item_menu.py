import webbrowser
from textwrap import dedent
from typing import Optional

import requests
from moviefinder.abstract_item_widget import AbstractItemWidget
from moviefinder.buttons import init_buttons
from moviefinder.country_code import CountryCode
from moviefinder.item import Item
from moviefinder.item import ServiceName
from moviefinder.items import items
from moviefinder.resources import corner_up_left_arrow_icon_path
from moviefinder.scaled_label import ScaledLabel
from moviefinder.validators import valid_services
from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class ItemMenu(AbstractItemWidget):
    """A menu that displays info about one movie or show.

    After creating an ItemMenu object, call ``update_item_data`` to choose which movie
    or show it should display when opened.
    """

    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.item_id: Optional[str] = None
        top_buttons_layout = QtWidgets.QHBoxLayout()
        self.back_button = QtWidgets.QPushButton()
        self.back_button.setIcon(QtGui.QIcon(corner_up_left_arrow_icon_path))
        self.back_button.clicked.connect(main_window.show_browse_menu)
        top_buttons_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        self.options_button = main_window.create_options_button(self)
        top_buttons_layout.addWidget(self.options_button, alignment=Qt.AlignRight)
        self.layout.addLayout(top_buttons_layout)
        self.item_layout = QtWidgets.QHBoxLayout()
        self.poster_label = ScaledLabel()
        self.item_layout.addWidget(self.poster_label)
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
        self.item_layout.addLayout(self.right_layout)
        self.layout.addLayout(self.item_layout)

    def update_item_data(self, item_id: str) -> bool:
        """Returns True if successful, False otherwise.

        This function may fail if the item's data does not make sense.
        """
        if not item_id or not self.is_valid_item(item_id):
            return False
        self.item_id = item_id
        init_buttons(self, self.item_id)
        response = requests.get(items[self.item_id].poster_url)
        poster_pixmap = QtGui.QPixmap()
        poster_pixmap.loadFromData(response.content)
        self.poster_label.setPixmap(poster_pixmap)
        hours = items[self.item_id].runtime_minutes // 60
        minutes = items[self.item_id].runtime_minutes % 60
        duration = f"{hours}h {minutes}m" if hours else f"{minutes}m"
        rating = f"{items[self.item_id].imdb_rating_percent}/100"
        self.right_text_browser.setText(
            dedent(
                f"""\
                <h1>{items[self.item_id].title}</h1>
                <p><em>{items[self.item_id].tagline}</em></p>
                <p>{"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join(
                    (str(items[self.item_id].release_year), rating, duration)
                )}</p>
                <p>{", ".join(items[self.item_id].genres)}</p>
                <h2>Overview</h2>
                {items[self.item_id].overview}
                <h2>Cast</h2>
                {", ".join(items[self.item_id].cast)}
                <h2>Directors</h2>
                {", ".join(items[self.item_id].directors)}
                """
            )
        )
        service_names = items[self.item_id].services.keys()
        if ServiceName.APPLE_TV_PLUS in service_names:
            self.apple_tv_plus_button.setVisible(True)
            try:
                self.apple_tv_plus_button.clicked.disconnect()
            except RuntimeError:
                pass
            self.apple_tv_plus_button.clicked.connect(
                lambda: webbrowser.open_new_tab(
                    items[self.item_id].services[ServiceName.APPLE_TV_PLUS]
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
                    items[self.item_id].services[ServiceName.DISNEY_PLUS]
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
                    items[self.item_id].services[ServiceName.HBO_MAX]
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
                    items[self.item_id].services[ServiceName.HULU]
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
                    items[self.item_id].services[ServiceName.NETFLIX]
                )
            )
        else:
            self.netflix_button.setVisible(False)
        return True

    def is_valid_item(self, item_id: str) -> bool:
        try:
            assert item_id in items, f"Invalid item: {item_id}"
            item: Item = items[item_id]
            assert isinstance(
                item.hearted, bool
            ), f"Type error: hearted is a {type(item.hearted)}"
            assert isinstance(item.xed, bool), f"Type error: xed is a {type(item.xed)}"
            assert item.id, "Error: id is falsy"
            assert isinstance(item.id, str), f"Type error: id is a {type(item.id)}"
            assert isinstance(
                item.imdb_rating_percent, int
            ), f"Type error: imdb_rating_percent is a {type(item.imdb_rating_percent)}"
            assert isinstance(
                item.imdb_vote_count, int
            ), f"Type error: imdb_vote_count is a {type(item.imdb_vote_count)}"
            assert item.poster_url, "Error: poster_url is falsy"
            assert isinstance(
                item.poster_url, str
            ), f"Type error: poster_url is a {type(item.poster_url)}"
            assert item.title, "Error: title is falsy"
            assert isinstance(
                item.title, str
            ), f"Type error: title is a {type(item.title)}"
            assert isinstance(
                item.genres, list
            ), f"Type error: genres is a {type(item.genres)}"
            assert isinstance(
                item.genres[0], str
            ), f"Type error: genres[0] is a {type(item.genres[0])}"
            assert item.regions, "Error: regions is falsy"
            assert isinstance(
                item.regions, list
            ), f"Type error: regions is a {type(item.regions)}"
            assert isinstance(
                item.regions[0], CountryCode
            ), f"Type error: regions[0] is a {type(item.regions[0])}"
            assert item.release_year, "Error: release_year is falsy"
            assert isinstance(
                item.release_year, int
            ), f"Type error: release_year is a {type(item.release_year)}"
            assert isinstance(
                item.runtime_minutes, int
            ), f"Type error: runtime_minutes is a {type(item.runtime_minutes)}"
            assert item.runtime_minutes, "Error: runtime_minutes is falsy"
            assert item.cast, "Error: cast is falsy"
            assert isinstance(
                item.cast, list
            ), f"Type error: cast is a {type(item.cast)}"
            assert isinstance(
                item.cast[0], str
            ), f"Type error: cast[0] is a {type(item.cast[0])}"
            assert item.directors, "Error: directors is falsy"
            assert isinstance(
                item.directors, list
            ), f"Type error: directors is a {type(item.directors)}"
            assert isinstance(
                item.directors[0], str
            ), f"Type error: directors[0] is a {type(item.directors[0])}"
            assert isinstance(
                item.overview, str
            ), f"Type error: overview is a {type(item.overview)}"
            assert isinstance(
                item.tagline, str
            ), f"Type error: tagline is a {type(item.tagline)}"
            assert isinstance(
                item.services, dict
            ), f"Type error: services is a {type(item.services)}"
            assert item.services, "Error: services is falsy"
            assert valid_services(
                item.services
            ), f"Error: invalid service(s): {item.services}"
        except AssertionError as e:
            print(f"    {e}")
            return False
        return True
