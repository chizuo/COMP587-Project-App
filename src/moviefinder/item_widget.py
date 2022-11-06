import requests
from moviefinder.abstract_item_widget import AbstractItemWidget
from moviefinder.buttons import init_buttons
from moviefinder.item import Item
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class ItemWidget(AbstractItemWidget):
    """A custom widget for displaying one item's poster and buttons.

    Unlike ``item_menu``, this class is intended to be put into the layout of a larger
    widget or menu such as ``browse_widget``.
    """

    def __init__(self, item: Item):
        QtWidgets.QWidget.__init__(self)
        self.item = item
        self.layout = QtWidgets.QVBoxLayout(self)
        self.poster_button = QtWidgets.QPushButton()
        response = requests.get(item.poster_url)
        poster_pixmap = QtGui.QPixmap()
        poster_pixmap.loadFromData(response.content)
        poster_pixmap.scaledToWidth(5)
        poster_icon = QtGui.QIcon(poster_pixmap)
        self.poster_button.setIcon(poster_icon)
        self.poster_button.setIconSize(QtCore.QSize(235, 350))
        self.poster_button.setMaximumSize(self.poster_button.iconSize())
        self.layout.addWidget(self.poster_button)
        buttons_layout = QtWidgets.QHBoxLayout()
        self.heart_button = QtWidgets.QPushButton()
        buttons_layout.addWidget(self.heart_button)
        self.x_button = QtWidgets.QPushButton()
        buttons_layout.addWidget(self.x_button)
        init_buttons(self)
        self.layout.addLayout(buttons_layout)
