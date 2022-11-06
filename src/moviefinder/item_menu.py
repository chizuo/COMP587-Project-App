import webbrowser
from textwrap import dedent

import requests
from moviefinder.abstract_item_widget import AbstractItemWidget
from moviefinder.abstract_user_widget import AbstractUserWidget
from moviefinder.buttons import init_buttons
from moviefinder.item import Item
from moviefinder.resources import corner_up_left_arrow_icon_path
from moviefinder.scaled_label import ScaledLabel
from moviefinder.user import User
from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class ItemMenu(AbstractUserWidget, AbstractItemWidget):
    def __init__(self, user: User, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.user = user
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)
        top_buttons_layout = QtWidgets.QHBoxLayout()
        self.back_button = QtWidgets.QPushButton()
        self.back_button.setIcon(QtGui.QIcon(corner_up_left_arrow_icon_path))
        self.back_button.clicked.connect(
            lambda self=self, user=self.user: self.main_window.show_browse_menu(user)
        )
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
        heart_and_x_buttons_layout = QtWidgets.QHBoxLayout()
        self.heart_button = QtWidgets.QPushButton()
        heart_and_x_buttons_layout.addWidget(self.heart_button)
        self.x_button = QtWidgets.QPushButton()
        heart_and_x_buttons_layout.addWidget(self.x_button)
        self.right_layout.addLayout(heart_and_x_buttons_layout)
        stream_buttons_layout = QtWidgets.QHBoxLayout()
        self.apple_tv_plus_button = QtWidgets.QPushButton("Apple TV+")
        stream_buttons_layout.addWidget(self.apple_tv_plus_button)
        self.disney_plus_button = QtWidgets.QPushButton("Disney+")
        stream_buttons_layout.addWidget(self.disney_plus_button)
        self.hbo_max_button = QtWidgets.QPushButton("HBO Max")
        stream_buttons_layout.addWidget(self.hbo_max_button)
        self.hulu_button = QtWidgets.QPushButton("Hulu")
        stream_buttons_layout.addWidget(self.hulu_button)
        self.netflix_button = QtWidgets.QPushButton("Netflix")
        stream_buttons_layout.addWidget(self.netflix_button)
        self.right_layout.addLayout(stream_buttons_layout)
        self.item_layout.addLayout(self.right_layout)
        self.layout.addLayout(self.item_layout)

    def show(self, item: Item) -> None:
        self.item = item
        init_buttons(self)
        response = requests.get(self.item.poster_url)
        poster_pixmap = QtGui.QPixmap()
        poster_pixmap.loadFromData(response.content)
        self.poster_label.setPixmap(poster_pixmap)
        hours = self.item.runtime_minutes // 60
        minutes = self.item.runtime_minutes % 60
        duration = f"{hours}h {minutes}m" if hours else f"{minutes}m"
        rating = f"{self.item.imdb_rating_percent}/100"
        self.right_text_browser.setText(
            dedent(
                f"""\
                <h1>{self.item.title}</h1>
                <p><em>{self.item.tagline}</em></p>
                <p>{"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join(
                    (str(self.item.release_year), rating, duration)
                )}</p>
                <p>{", ".join(self.item.genres)}</p>
                <h2>Overview</h2>
                {self.item.overview}
                <h2>Cast</h2>
                {", ".join(self.item.cast)}
                <h2>Directors</h2>
                {", ".join(self.item.directors)}
                """
            )
        )
        service_names = self.item.streaming_services.keys()
        if "Apple TV+" in service_names:
            self.apple_tv_plus_button.setVisible(True)
            self.apple_tv_plus_button.clicked.connect(
                lambda: webbrowser.open_new_tab(
                    self.item.streaming_services["Apple TV+"]
                )
            )
        else:
            self.apple_tv_plus_button.setVisible(False)
        if "Disney+" in service_names:
            self.disney_plus_button.setVisible(True)
            self.disney_plus_button.clicked.connect(
                lambda: webbrowser.open_new_tab(self.item.streaming_services["Disney+"])
            )
        else:
            self.disney_plus_button.setVisible(False)
        if "HBO Max" in service_names:
            self.hbo_max_button.setVisible(True)
            self.hbo_max_button.clicked.connect(
                lambda: webbrowser.open_new_tab(self.item.streaming_services["HBO Max"])
            )
        else:
            self.hbo_max_button.setVisible(False)
        if "Hulu" in service_names:
            self.hulu_button.setVisible(True)
            self.hulu_button.clicked.connect(
                lambda: webbrowser.open_new_tab(self.item.streaming_services["Hulu"])
            )
        else:
            self.hulu_button.setVisible(False)
        if "Netflix" in service_names:
            self.netflix_button.setVisible(True)
            self.netflix_button.clicked.connect(
                lambda: webbrowser.open_new_tab(self.item.streaming_services["Netflix"])
            )
        else:
            self.netflix_button.setVisible(False)
        self.main_window.central_widget.setCurrentWidget(self)
