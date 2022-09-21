from PySide6 import QtWidgets


class MovieFinder(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Movie Finder")
        self.showMaximized()
