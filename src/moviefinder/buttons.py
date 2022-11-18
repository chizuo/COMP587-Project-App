from moviefinder.abstract_item_widget import AbstractItemWidget
from moviefinder.items import items
from moviefinder.resources import black_x_icon_path
from moviefinder.resources import empty_heart_icon_path
from moviefinder.resources import filled_heart_icon_path
from moviefinder.resources import red_x_icon_path
from PySide6 import QtGui


def init_buttons(widget: AbstractItemWidget) -> None:
    """Connects, sets icons for, & disables/enables a widget's buttons."""
    widget.heart_button.clicked.connect(
        lambda __on_heart_click=__on_heart_click, w=widget: __on_heart_click(w)
    )
    widget.x_button.clicked.connect(
        lambda __on_x_click=__on_x_click, w=widget: __on_x_click(w)
    )
    if items[widget.item_id].hearted:
        widget.heart_button.setIcon(QtGui.QIcon(filled_heart_icon_path))
        widget.x_button.setDisabled(True)
    else:
        widget.heart_button.setIcon(QtGui.QIcon(empty_heart_icon_path))
        widget.x_button.setDisabled(False)
    if items[widget.item_id].xed:
        widget.x_button.setIcon(QtGui.QIcon(red_x_icon_path))
        widget.heart_button.setDisabled(True)
    else:
        widget.x_button.setIcon(QtGui.QIcon(black_x_icon_path))
        widget.heart_button.setDisabled(False)


def __on_heart_click(widget: AbstractItemWidget) -> None:
    """Responds to a widget's heart button being clicked."""
    if not items[widget.item_id].hearted:
        items[widget.item_id].hearted = True
        widget.heart_button.setIcon(QtGui.QIcon(filled_heart_icon_path))
        widget.x_button.setDisabled(True)
    else:
        items[widget.item_id].hearted = False
        widget.heart_button.setIcon(QtGui.QIcon(empty_heart_icon_path))
        widget.x_button.setDisabled(False)


def __on_x_click(widget: AbstractItemWidget) -> None:
    """Responds to a widget's x button being clicked."""
    if not items[widget.item_id].xed:
        items[widget.item_id].xed = True
        widget.x_button.setIcon(QtGui.QIcon(red_x_icon_path))
        widget.heart_button.setDisabled(True)
    else:
        items[widget.item_id].xed = False
        widget.x_button.setIcon(QtGui.QIcon(black_x_icon_path))
        widget.heart_button.setDisabled(False)
