from moviefinder.browse_widget import BrowseWidget
from moviefinder.checkable_combo_box import CheckableComboBox
from moviefinder.items import items
from moviefinder.user import user
from PySide6 import QtCore
from PySide6 import QtWidgets


class InfiniteScrollBar(QtWidgets.QScrollBar):
    at_bottom = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.valueChanged.connect(self.emit_at_bottom_if_true)

    def emit_at_bottom_if_true(self) -> None:
        if self.value() == self.maximum():
            self.at_bottom.emit()


class BrowseMenu(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        QtWidgets.QWidget.__init__(self)
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)
        self.options_button = main_window.create_options_button(self)
        self.layout.addWidget(self.options_button, alignment=QtCore.Qt.AlignRight)
        self.genres_combo_box = CheckableComboBox(self)
        self.genres_combo_box.addItems(user.genre_habits.keys())
        self.genres_combo_box.popup_hidden.connect(
            self.reload_browse_widget_if_genres_changed
        )
        self.genres_combo_box.setCurrentData(items.genres)
        self.layout.addWidget(self.genres_combo_box)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_bar = InfiniteScrollBar()
        self.scroll_bar.at_bottom.connect(self.add_row)
        self.scroll_area.setVerticalScrollBar(self.scroll_bar)
        self.browse_widget = BrowseWidget(main_window)
        self.scroll_area.setWidget(self.browse_widget)
        self.layout.addWidget(self.scroll_area)

    def reload_browse_widget_if_genres_changed(self) -> None:
        new_genres = self.genres_combo_box.currentText().split(", ")
        if new_genres != items.genres:
            items.genres = new_genres
            self.browse_widget = BrowseWidget(self.main_window)
            self.scroll_area.setWidget(self.browse_widget)

    def reload_browse_widget(self) -> None:
        self.browse_widget = BrowseWidget(self.main_window)
        self.scroll_area.setWidget(self.browse_widget)

    def update_item_widgets(self) -> None:
        self.browse_widget.update_item_widgets()

    def add_row(self) -> None:
        self.browse_widget.add_row()
