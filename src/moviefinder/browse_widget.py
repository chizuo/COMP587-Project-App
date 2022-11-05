from moviefinder.item import Item
from moviefinder.item_widget import ItemWidget
from PySide6 import QtWidgets


class BrowseWidget(QtWidgets.QWidget):
    def __init__(self, items: list[Item], main_window: QtWidgets.QMainWindow):
        QtWidgets.QWidget.__init__(self)
        self.items = items
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)
        self.row_layouts = [QtWidgets.QHBoxLayout(), QtWidgets.QHBoxLayout()]
        self.row_items: list[list[Item]] = []  # <= 4 items per row, any # of rows
        i = 0
        while i < len(self.items):
            self.row_items.append(self.items[i : i + 4])  # noqa: E203
            i += 4
        self.hearted_items: list[Item] = []
        self.xed_items: list[Item] = []
        for i in range(2 if len(self.items) >= 8 else 1):
            for j, _ in enumerate(self.row_items[i]):
                item_widget = ItemWidget(self.row_items[i][j])
                item_widget.poster_button.clicked.connect(
                    lambda self=self, w=item_widget: self.main_window.item_menu.show(
                        w.item
                    )
                )
                self.row_layouts[i].addWidget(item_widget)
            self.layout.addLayout(self.row_layouts[i])
