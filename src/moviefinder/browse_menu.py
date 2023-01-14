from moviefinder.browse_widget import BrowseWidget
from moviefinder.checkable_combo_box import CheckableComboBox
from moviefinder.loading_dialog import LoadingDialog
from moviefinder.movies import movies
from moviefinder.user import show_message_box
from moviefinder.user import user
from PySide6 import QtCore
from PySide6 import QtWidgets


class InfiniteScrollBar(QtWidgets.QScrollBar):
    """A scroll bar that emits a signal when it nears and when it reaches the bottom."""

    at_bottom = QtCore.Signal()
    near_bottom = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setTracking(False)
        self.valueChanged.connect(self.emit_at_bottom_if_true)
        self.valueChanged.connect(self.emit_near_bottom_if_true)

    def emit_at_bottom_if_true(self) -> None:
        if self.value() == self.maximum():
            self.at_bottom.emit()

    def emit_near_bottom_if_true(self) -> None:
        if self.value() >= self.maximum() - self.pageStep():
            self.near_bottom.emit()


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
        self.genres_combo_box.setCurrentData(movies.genres)
        self.layout.addWidget(self.genres_combo_box)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_bar = InfiniteScrollBar()
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_bar.near_bottom.connect(self.add_row)
        self.scroll_area.setVerticalScrollBar(self.scroll_bar)
        self.browse_widget = BrowseWidget(main_window)
        if self.scroll_bar.value() == self.scroll_bar.maximum():
            self.add_row()
        self.scroll_area.setWidget(self.browse_widget)
        self.layout.addWidget(self.scroll_area)

    def reload_browse_widget_if_genres_changed(self) -> None:
        if self.main_window.is_quitting:
            return
        new_genres = self.genres_combo_box.currentText().split(", ")
        if not new_genres:
            show_message_box("Error: you must select at least one genre.")
            self.genres_combo_box.setCurrentData(movies.genres)
            return
        if new_genres != movies.genres:
            with LoadingDialog():
                movies.genres = new_genres
                self.main_window.clear_movies()
                if not movies.load():
                    show_message_box("Error: unable to connect to the service.")
                    return
                self.reload_browse_widget()

    def reload_browse_widget(self) -> None:
        self.browse_widget = BrowseWidget(self.main_window)
        self.scroll_area.setWidget(self.browse_widget)

    def update_movies_buttons(self) -> None:
        self.browse_widget.update_movies_buttons()

    def add_row(self) -> None:
        self.browse_widget.add_row()
