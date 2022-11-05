from moviefinder.abstract_item_widget import AbstractItemWidget
from moviefinder.resources import black_x_icon_path
from moviefinder.resources import empty_heart_icon_path
from moviefinder.resources import filled_heart_icon_path
from moviefinder.resources import red_x_icon_path
from PySide6 import QtGui


def init_buttons(widget: AbstractItemWidget) -> None:
    """Connects, sets icons for, & disables/enables a widget's buttons."""
    widget.heart_button.clicked.connect(
        lambda on_heart_click=on_heart_click, w=widget: on_heart_click(w)
    )
    widget.x_button.clicked.connect(
        lambda on_x_click=on_x_click, w=widget: on_x_click(w)
    )
    if widget.item.hearted:
        widget.heart_button.setIcon(QtGui.QIcon(filled_heart_icon_path))
        widget.x_button.setDisabled(True)
    else:
        widget.heart_button.setIcon(QtGui.QIcon(empty_heart_icon_path))
        widget.x_button.setDisabled(False)
    if widget.item.xed:
        widget.x_button.setIcon(QtGui.QIcon(red_x_icon_path))
        widget.heart_button.setDisabled(True)
    else:
        widget.x_button.setIcon(QtGui.QIcon(black_x_icon_path))
        widget.heart_button.setDisabled(False)


def on_heart_click(widget: AbstractItemWidget) -> None:
    """Responds to a widget's heart button being clicked."""
    if not widget.item.hearted:
        widget.item.hearted = True
        widget.heart_button.setIcon(QtGui.QIcon(filled_heart_icon_path))
        widget.x_button.setDisabled(True)
    else:
        widget.item.hearted = False
        widget.heart_button.setIcon(QtGui.QIcon(empty_heart_icon_path))
        widget.x_button.setDisabled(False)


def on_x_click(widget: AbstractItemWidget) -> None:
    """Responds to a widget's x button being clicked."""
    if not widget.item.xed:
        widget.item.xed = True
        widget.x_button.setIcon(QtGui.QIcon(red_x_icon_path))
        widget.heart_button.setDisabled(True)
    else:
        widget.item.xed = False
        widget.x_button.setIcon(QtGui.QIcon(black_x_icon_path))
        widget.heart_button.setDisabled(False)
