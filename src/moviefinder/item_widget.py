import requests
from moviefinder.item import Item
from moviefinder.resources import black_x_icon_path
from moviefinder.resources import empty_heart_icon_path
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class ItemWidget(QtWidgets.QWidget):
    def __init__(self, item: Item):
        QtWidgets.QWidget.__init__(self)
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
        self.heart_button.setIcon(QtGui.QIcon(empty_heart_icon_path))
        buttons_layout.addWidget(self.heart_button)
        self.heart_button_clicked = False
        self.x_button = QtWidgets.QPushButton()
        self.x_button.setIcon(QtGui.QIcon(black_x_icon_path))
        buttons_layout.addWidget(self.x_button)
        self.x_button_clicked = False
        self.layout.addLayout(buttons_layout)
