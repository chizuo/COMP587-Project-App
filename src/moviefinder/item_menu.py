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
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__(main_window)
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)
        top_buttons_layout = QtWidgets.QHBoxLayout()
        self.back_button = QtWidgets.QPushButton()
        self.back_button.setIcon(QtGui.QIcon(corner_up_left_arrow_path))
        top_buttons_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        self.options_button = self.main_window.create_options_button(self)
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
        self.stream_buttons_layout = QtWidgets.QHBoxLayout()
        self.apple_tv_plus_button = QtWidgets.QPushButton("Apple TV+")
        self.stream_buttons_layout.addWidget(self.apple_tv_plus_button)
        self.disney_plus_button = QtWidgets.QPushButton("Disney+")
        self.stream_buttons_layout.addWidget(self.disney_plus_button)
        self.hbo_max_button = QtWidgets.QPushButton("HBO Max")
        self.stream_buttons_layout.addWidget(self.hbo_max_button)
        self.hulu_button = QtWidgets.QPushButton("Hulu")
        self.stream_buttons_layout.addWidget(self.hulu_button)
        self.netflix_button = QtWidgets.QPushButton("Netflix")
        self.stream_buttons_layout.addWidget(self.netflix_button)
        self.right_layout.addLayout(self.stream_buttons_layout)
        self.item_layout.addLayout(self.right_layout)
        self.layout.addLayout(self.item_layout)

    def show(self, item: Item) -> None:
        response = requests.get(item.poster_url)
        poster_pixmap = QtGui.QPixmap()
        poster_pixmap.loadFromData(response.content)
        self.poster_label.setPixmap(poster_pixmap)
        hours = item.runtime_minutes // 60
        minutes = item.runtime_minutes % 60
        duration = f"{hours}h {minutes}m" if hours else f"{minutes}m"
        rating = f"{item.imdb_rating_percent}/100"
        self.right_text_browser.setText(
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
            )
        )
        service_names = item.streaming_services.keys()
        if "Apple TV+" in service_names:
            self.apple_tv_plus_button.setVisible(True)
            self.apple_tv_plus_button.clicked.connect(
                lambda: webbrowser.open_new_tab(item.streaming_services["Apple TV+"])
            )
        else:
            self.apple_tv_plus_button.setVisible(False)
        if "Disney+" in service_names:
            self.disney_plus_button.setVisible(True)
            self.disney_plus_button.clicked.connect(
                lambda: webbrowser.open_new_tab(item.streaming_services["Disney+"])
            )
        else:
            self.disney_plus_button.setVisible(False)
        if "HBO Max" in service_names:
            self.hbo_max_button.setVisible(True)
            self.hbo_max_button.clicked.connect(
                lambda: webbrowser.open_new_tab(item.streaming_services["HBO Max"])
            )
        else:
            self.hbo_max_button.setVisible(False)
        if "Hulu" in service_names:
            self.hulu_button.setVisible(True)
            self.hulu_button.clicked.connect(
                lambda: webbrowser.open_new_tab(item.streaming_services["Hulu"])
            )
        else:
            self.hulu_button.setVisible(False)
        if "Netflix" in service_names:
            self.netflix_button.setVisible(True)
            self.netflix_button.clicked.connect(
                lambda: webbrowser.open_new_tab(item.streaming_services["Netflix"])
            )
        else:
            self.netflix_button.setVisible(False)
        self.main_window.central_widget.setCurrentWidget(self)
