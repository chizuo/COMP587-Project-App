import json
from typing import Any

from moviefinder.item import Item
from moviefinder.resources import sample_movies_json_path
from moviefinder.user import User
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class BrowseMenu(QtWidgets.QWidget):
    def __init__(self, user: User, main_window: QtWidgets.QMainWindow):
        super().__init__(main_window)
        self.user = user
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)
        self.options_button = main_window.create_options_button(self)
        self.layout.addWidget(self.options_button, alignment=Qt.AlignRight)
        title_label = QtWidgets.QLabel("<h1>browse</h1>", self)
        title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layout.addWidget(title_label)
        self.items: list[Item] = self.load_items()
        self.item_buttons_layout = QtWidgets.QVBoxLayout()
        for item in self.items:
            button = QtWidgets.QPushButton(item.title, self)
            button.clicked.connect(
                lambda self=self, item=item: self.main_window.item_menu.show(item)
            )
            self.item_buttons_layout.addWidget(button)
        self.layout.addLayout(self.item_buttons_layout)

    def load_items(self) -> list[Item]:
        items: list[Item] = []
        with open(sample_movies_json_path, "r", encoding="utf8") as file:
            service_obj: dict[str, Any] = json.load(file)
            # total_pages: int = service_obj["total_pages"]
            items_data: list[dict] = service_obj["movies"]
            for item_data in items_data:
                items.append(Item(item_data, self.user))
        return items
