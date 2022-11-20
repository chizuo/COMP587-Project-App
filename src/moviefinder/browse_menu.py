from moviefinder.abstract_user_widget import AbstractUserWidget
from moviefinder.browse_widget import BrowseWidget
from moviefinder.user import User
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


class BrowseMenu(AbstractUserWidget):
    def __init__(self, user: User, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.user = user
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)
        self.options_button = main_window.create_options_button(self)
        self.layout.addWidget(self.options_button, alignment=QtCore.Qt.AlignRight)
        title_label = QtWidgets.QLabel("<h1>browse</h1>", self)
        title_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.layout.addWidget(title_label)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_bar = InfiniteScrollBar()
        self.scroll_bar.at_bottom.connect(self.show_more_items)
        self.scroll_area.setVerticalScrollBar(self.scroll_bar)
        self.browse_widget = BrowseWidget(self.user, main_window)
        self.scroll_area.setWidget(self.browse_widget)
        self.layout.addWidget(self.scroll_area)

    def update_item_widgets(self) -> None:
        self.browse_widget.update_item_widgets()

    def show_more_items(self) -> None:
        self.browse_widget.show_more_items()
