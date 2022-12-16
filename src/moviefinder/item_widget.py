import requests
from moviefinder.abstract_item_widget import AbstractItemWidget
from moviefinder.buttons import init_buttons
from moviefinder.items import items
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class ItemWidget(AbstractItemWidget):
    """A custom widget for displaying one item's poster and buttons.

    Unlike ``item_menu``, this class is intended to be put into the layout of a larger
    widget or menu such as ``browse_widget``.
    """

    def __init__(self, item_id: str):
        QtWidgets.QWidget.__init__(self)
        self.ok = True
        if item_id is None:
            self.ok = False
            print(f'Error: item "{id}" is invalid.')
            return
        self.item_id = item_id
        self.layout = QtWidgets.QVBoxLayout(self)
        self.poster_button = QtWidgets.QPushButton()
        response = requests.get(items[self.item_id].poster_url)
        if not response:
            self.ok = False
            print(f'Error: item "{id}"\'s poster URL is invalid.')
            return
        POSTER_WIDTH = 235
        POSTER_HEIGHT = 350
        poster_pixmap = QtGui.QPixmap()
        poster_pixmap.loadFromData(response.content)
        poster_pixmap.scaledToWidth(5)
        poster_icon = QtGui.QIcon(poster_pixmap)
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
            POSTER_WIDTH // 2 - 10
        )
        self.heart_button = QtWidgets.QPushButton()
        self.heart_button.setStyleSheet(button_style_sheet)
        buttons_layout.addWidget(self.heart_button)
        self.x_button = QtWidgets.QPushButton()
        self.x_button.setStyleSheet(button_style_sheet)
        buttons_layout.addWidget(self.x_button)
        buttons_layout.addStretch()
        self.update_item_data()
        self.layout.addLayout(buttons_layout)

    def update_item_data(self) -> None:
        assert self.item_id is not None
        init_buttons(self, self.item_id)
