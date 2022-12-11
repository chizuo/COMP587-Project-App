from itertools import zip_longest
from typing import Optional

from moviefinder.item_menu import ItemMenu
from moviefinder.item_widget import ItemWidget
from moviefinder.items import items
from moviefinder.user import User
from PySide6 import QtWidgets


def grouper(iterable, n, *, incomplete="fill", fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == "fill":
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == "strict":
        return zip(*args, strict=True)
    if incomplete == "ignore":
        return zip(*args)
    else:
        raise ValueError("Expected fill, strict, or ignore")


class BrowseWidget(QtWidgets.QWidget):
    def __init__(self, user: User, main_window: QtWidgets.QMainWindow):
        QtWidgets.QWidget.__init__(self)
        self._START_ROW_COUNT = 2
        self._ITEMS_PER_ROW = 4
        self._START_ITEM_COUNT = self._START_ROW_COUNT * self._ITEMS_PER_ROW
        assert len(items) >= self._START_ITEM_COUNT, len(items)
        self.user = user
        self.main_window = main_window
        self.item_menu: Optional[ItemMenu] = None
        self.layout = QtWidgets.QVBoxLayout(self)
        self.items_layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.items_layout)
        self.layout.addSpacerItem(QtWidgets.QSpacerItem(1, 100))
        self.item_widgets: list[ItemWidget] = []
        self._row_count = 0
        for ids in grouper(items, self._ITEMS_PER_ROW):
            self._row_count += 1
            if self._row_count > 2:
                break
            self.__add_row(ids)

    def update_item_widgets(self) -> None:
        for item_widget in self.item_widgets:
            item_widget.update_item_data()

    def show_item_menu(self, item_id: str) -> None:
        if self.item_menu is None:
            self.item_menu = ItemMenu(self.user, self.main_window)
            self.main_window.central_widget.addWidget(self.item_menu)
        if not self.item_menu.update_item_data(item_id):
            print(f'Error: item "{item_id}" is invalid.')
        else:
            self.main_window.central_widget.setCurrentWidget(self.item_menu)

    def show_more_items(self) -> None:
        if self._row_count >= 10:
            return
        i = 0
        for ids in grouper(items, self._ITEMS_PER_ROW):
            if i < self._row_count:
                i += 1
                continue
            self.__add_row(ids)
            break
        self._row_count += 1

    def __add_row(self, ids: tuple[str]) -> None:
        self.row_layout = QtWidgets.QHBoxLayout()
        for id in ids:
            if id is not None:
                item_widget = ItemWidget(id)
                item_widget.poster_button.clicked.connect(
                    lambda self=self, id=id: self.show_item_menu(id)
                )
                self.row_layout.addWidget(item_widget)
                self.item_widgets.append(item_widget)
        self.items_layout.addLayout(self.row_layout)
