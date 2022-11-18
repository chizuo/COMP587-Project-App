import webbrowser
from textwrap import dedent

import requests
from moviefinder.abstract_item_widget import AbstractItemWidget
from moviefinder.abstract_user_widget import AbstractUserWidget
from moviefinder.buttons import init_buttons
from moviefinder.items import items
from moviefinder.resources import corner_up_left_arrow_icon_path
from moviefinder.scaled_label import ScaledLabel
from moviefinder.user import User
from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class ItemMenu(AbstractUserWidget, AbstractItemWidget):
    def __init__(self, item_id: str, user: User, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.item_id = item_id
        self.user = user
        self.layout = QtWidgets.QVBoxLayout(self)
        top_buttons_layout = QtWidgets.QHBoxLayout()
        self.back_button = QtWidgets.QPushButton()
        self.back_button.setIcon(QtGui.QIcon(corner_up_left_arrow_icon_path))
        self.back_button.clicked.connect(
            lambda user=self.user: main_window.show_browse_menu(user)
        )
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
        self.apple_tv_plus_button = QtWidgets.QPushButton("Apple TV+")
        stream_buttons_layout = QtWidgets.QHBoxLayout()
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
        self.update_item_data(self.item_id)

    def update_item_data(self, item_id: str) -> None:
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
        service_names = items[self.item_id].streaming_services.keys()
        if "Apple TV+" in service_names:
            self.apple_tv_plus_button.setVisible(True)
            try:
                self.apple_tv_plus_button.clicked.disconnect()
            except RuntimeError:
                pass
            self.apple_tv_plus_button.clicked.connect(
                lambda: webbrowser.open_new_tab(
                    items[self.item_id].streaming_services["Apple TV+"]
                )
            )
        else:
            self.apple_tv_plus_button.setVisible(False)
        if "Disney+" in service_names:
            self.disney_plus_button.setVisible(True)
            try:
                self.disney_plus_button.clicked.disconnect()
            except RuntimeError:
                pass
            self.disney_plus_button.clicked.connect(
                lambda: webbrowser.open_new_tab(
                    items[self.item_id].streaming_services["Disney+"]
                )
            )
        else:
            self.disney_plus_button.setVisible(False)
        if "HBO Max" in service_names:
            self.hbo_max_button.setVisible(True)
            try:
                self.hbo_max_button.clicked.disconnect()
            except RuntimeError:
                pass
            self.hbo_max_button.clicked.connect(
                lambda: webbrowser.open_new_tab(
                    items[self.item_id].streaming_services["HBO Max"]
                )
            )
        else:
            self.hbo_max_button.setVisible(False)
        if "Hulu" in service_names:
            self.hulu_button.setVisible(True)
            try:
                self.hulu_button.clicked.disconnect()
            except RuntimeError:
                pass
            self.hulu_button.clicked.connect(
                lambda: webbrowser.open_new_tab(
                    items[self.item_id].streaming_services["Hulu"]
                )
            )
        else:
            self.hulu_button.setVisible(False)
        if "Netflix" in service_names:
            self.netflix_button.setVisible(True)
            try:
                self.netflix_button.clicked.disconnect()
            except RuntimeError:
                pass
            self.netflix_button.clicked.connect(
                lambda: webbrowser.open_new_tab(
                    items[self.item_id].streaming_services["Netflix"]
                )
            )
        else:
            self.netflix_button.setVisible(False)
