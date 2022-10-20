import webbrowser
from textwrap import dedent

import requests
from moviefinder.item import Item
from moviefinder.resources import corner_up_left_arrow_path
from moviefinder.scaled_label import ScaledLabel
from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class ItemMenu(QtWidgets.QWidget):
    def __init__(self, item: Item, main_window: QtWidgets.QMainWindow):
        super().__init__(main_window)
        self.layout = QtWidgets.QVBoxLayout(self)
        top_buttons_layout = QtWidgets.QHBoxLayout()
        self.back_button = QtWidgets.QPushButton()
        self.back_button.setIcon(QtGui.QIcon(corner_up_left_arrow_path))
        top_buttons_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        top_buttons_layout.addWidget(
            main_window.options_button, alignment=Qt.AlignRight
        )
        self.layout.addLayout(top_buttons_layout)
        item_layout = QtWidgets.QHBoxLayout()
        response = requests.get(item.poster_url)
        poster_pixmap = QtGui.QPixmap()
        poster_pixmap.loadFromData(response.content)
        poster_label = ScaledLabel()
        poster_label.setPixmap(poster_pixmap)
        item_layout.addWidget(poster_label)
        hours = item.runtime_minutes // 60
        minutes = item.runtime_minutes % 60
        duration = f"{hours}h {minutes}m" if hours else f"{minutes}m"
        rating = f"{item.imdb_rating_percent}/100"
        right_layout = QtWidgets.QVBoxLayout()
        right_label = QtWidgets.QLabel(
            dedent(
                f"""\
                <h1>{item.title}</h1>
                <p><em>{item.tagline}</em></p>
                <p>{"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join(
                    (str(item.release_year), rating, duration)
                )}</p>
                <p>{", ".join(item.genres)}</p>
                <h2>Overview</h2>
                {item.overview}
                <h2>Cast</h2>
                {", ".join(item.cast)}
                <h2>Directors</h2>
                {", ".join(item.directors)}
                """
            ),
            self,
        )
        right_label.setWordWrap(True)
        right_scroll_area = QtWidgets.QScrollArea()
        right_scroll_area.setWidget(right_label)
        right_scroll_area.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        right_layout.addWidget(right_scroll_area)
        self.stream_buttons_layout = QtWidgets.QHBoxLayout()
        for name, url in item.streaming_services.items():
            button = QtWidgets.QPushButton(name)
            button.clicked.connect(lambda: webbrowser.open_new_tab(url))
            self.stream_buttons_layout.addWidget(button)
        right_layout.addLayout(self.stream_buttons_layout)
        item_layout.addLayout(right_layout)
        self.layout.addLayout(item_layout)
