from typing import Optional

from moviefinder.item_menu import ItemMenu
from moviefinder.item_widget import ItemWidget
from moviefinder.items import items
from PySide6 import QtWidgets


class BrowseWidget(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        QtWidgets.QWidget.__init__(self)
        self._START_ROW_COUNT = 2
        self._ITEMS_PER_ROW = 4
        self._START_ITEM_COUNT = self._START_ROW_COUNT * self._ITEMS_PER_ROW
        self.__shown_item_count = 0
        self._MAX_SHOWN_ITEMS = 10 * self._ITEMS_PER_ROW
        assert len(items) >= self._START_ITEM_COUNT, len(items)
        self.main_window = main_window
        self.item_menu: Optional[ItemMenu] = None
        self.layout = QtWidgets.QVBoxLayout(self)
        self.items_layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.items_layout)
        self.layout.addSpacerItem(QtWidgets.QSpacerItem(1, 100))
        self.item_widgets: list[ItemWidget] = []
        self.add_row()
        self.add_row()

    def update_item_widgets(self) -> None:
        for item_widget in self.item_widgets:
            item_widget.update_item_data()

    def show_item_menu(self, item_id: str) -> None:
        if self.item_menu is None:
            self.item_menu = ItemMenu(self.main_window)
            self.main_window.central_widget.addWidget(self.item_menu)
        if not self.item_menu.update_item_data(item_id):
            print(f'Error: item "{item_id}" is invalid.')
        else:
            self.main_window.central_widget.setCurrentWidget(self.item_menu)

    def add_row(self) -> None:
        if (
            self.__shown_item_count >= self._MAX_SHOWN_ITEMS
            or self.__shown_item_count == len(items)
        ):
            return
        self.row_layout = QtWidgets.QHBoxLayout()
        newly_shown_item_count = 0
        for i, item_id in enumerate(items):
            if i < self.__shown_item_count:
                continue
            if newly_shown_item_count >= self._ITEMS_PER_ROW:
                break
            item_widget = ItemWidget(item_id)
            if not item_widget.ok:
                continue
            item_widget.poster_button.clicked.connect(
                lambda self=self, item_id=item_id: self.show_item_menu(item_id)
            )
            self.row_layout.addWidget(item_widget)
            self.item_widgets.append(item_widget)
            newly_shown_item_count += 1
            self.__shown_item_count += 1
        self.items_layout.addLayout(self.row_layout)
