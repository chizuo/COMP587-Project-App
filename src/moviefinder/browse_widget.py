from moviefinder.item import Item
from moviefinder.item_widget import ItemWidget
from PySide6 import QtWidgets


class BrowseWidget(QtWidgets.QWidget):
    def __init__(self, items: list[Item], main_window: QtWidgets.QMainWindow):
        QtWidgets.QWidget.__init__(self)
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)
        self.row_layouts = [QtWidgets.QHBoxLayout(), QtWidgets.QHBoxLayout()]
        self.row_items: list[list[Item]] = []  # <= 4 items per row, any # of rows
        i = 0
        while i < len(items):
            self.row_items.append(items[i : i + 4])  # noqa: E203
            i += 4
        self.hearted_items: list[Item] = []
        self.xed_items: list[Item] = []
        for i in range(2 if len(items) >= 8 else 1):
            for item in self.row_items[i]:
                item_widget = ItemWidget(item)
                item_widget.poster_button.clicked.connect(
                    lambda self=self, item=item: self.main_window.item_menu.show(item)
                )
                item_widget.heart_button.clicked.connect(
                    lambda self=self, item=item, w=item_widget: self.on_heart_click(
                        item, w
                    )
                )
                item_widget.x_button.clicked.connect(
                    lambda self=self, item=item, w=item_widget: self.on_x_click(item, w)
                )
                self.row_layouts[i].addWidget(item_widget)
            self.layout.addLayout(self.row_layouts[i])

    def on_heart_click(self, item: Item, widget: ItemWidget) -> None:
        self.hearted_items.append(item)
        widget.heart_button.setDisabled(True)
        widget.x_button.setDisabled(True)

    def on_x_click(self, item: Item, widget: ItemWidget) -> None:
        self.xed_items.append(item)
        widget.heart_button.setDisabled(True)
        widget.x_button.setDisabled(True)
        widget.setVisible(False)
