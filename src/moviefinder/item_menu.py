from textwrap import dedent

from moviefinder.item import Item
from moviefinder.resources import corner_up_left_arrow_path
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
        left_layout = QtWidgets.QVBoxLayout()
        poster_picture = QtGui.QPixmap()
        poster_picture.load(item.poster_link)
        poster_label = QtWidgets.QLabel()
        poster_label.setPixmap(poster_picture)
        left_layout.addWidget(poster_label)
        # left_layout.addWidget()  # TODO: item.trailer_link
        # left_layout.addWidget()  # TODO: item.stream_link
        item_layout.addLayout(left_layout)

        # title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        minutes = int(item.duration.total_seconds() // 60)
        hours = int(minutes // 60)
        minutes %= 60
        duration = f"{hours}h {minutes}m" if hours else f"{minutes}m"
        right_label = QtWidgets.QLabel(
            dedent(
                f"""\
                <h1>{item.title}</h1>
                {"       ".join(
                    (str(item.release_year), item.age_rating, item.rating, duration)
                )}
                {", ".join(item.keywords)}
                <h2>Synopsis</h2>
                {item.synopsis}
                <h2>Cast</h2>
                {", ".join(item.cast)}
                <h2>Directors</h2>
                {", ".join(item.directors)}
                <h2>Writers</h2>
                {", ".join(item.writers)}
                <h2>Companies</h2>
                {", ".join(item.companies)}
                """
            ),
            self,
        )
        right_label.setWordWrap(True)
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(right_label)
        item_layout.addWidget(scroll_area)
        self.layout.addLayout(item_layout)
