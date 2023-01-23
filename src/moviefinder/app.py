import sys
from importlib import metadata as importlib_metadata

from moviefinder.main_window import MainWindow
from PySide6 import QtWidgets


def main():
    # Linux desktop environments use app's .desktop file to integrate the app
    # to their application menus. The .desktop file of this app will include
    # StartupWMClass key, set to app's formal name, which helps associate
    # app's windows to its menu movie.
    #
    # For association to work any windows of the app must have WMCLASS
    # property set to match the value set in app's desktop file. For PySide2
    # this is set with setApplicationName().

    # Find the name of the module that was used to start the app
    app_module = sys.modules["__main__"].__package__
    # Retrieve the app's metadata
    metadata = importlib_metadata.metadata(app_module)

    QtWidgets.QApplication.setApplicationName(metadata["Formal-Name"])

    QtWidgets.QApplication.setStyle("Fusion")
    sys.argv += ["-platform", "windows:darkmode=1"]
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(
        """
        QWidget {
            font-size: 14px;
            color: #b1b1b1;
            background-color: #1e1e1e;
            selection-background-color: #3daee9;
            selection-color: #ffffff;
            background-clip: border;
        }
        QLineEdit, QComboBox, QCheckBox::indicator:unchecked, QToolButton, QMenu {
            background-color: #323232;
        }
        QToolButton:hover, QPushButton:hover, QMenu::item:selected {
            background-color: #515151;
        }
        QComboBox {
            selection-background-color: #515151;
        }
        QPushButton, QToolButton {
            font-weight: bold;
            padding: 5px;
        }
        QPushButton, QToolButton:pressed {
            background-color: #424242;
        }
        QScrollBar:vertical {
            border: none;
            background: #323232;
            width: 14px;
        }
        QScrollBar::handle:vertical {
            background: #424242;
            min-height: 20px;
        }
        QGroupBox {
            border: 2px solid #323232;
            border-radius: 5px;
            margin-top: 24px;
        }
        """
    )
    main_window = MainWindow()  # noqa: F841
    sys.exit(app.exec())
