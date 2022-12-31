from PySide6 import QtCore
from PySide6 import QtWidgets


class LoadingDialog:
    """A context manager that shows a loading dialog."""

    def __enter__(self) -> None:
        self.__dialog = QtWidgets.QProgressDialog("Loading...", "", 0, 0)
        self.__dialog.setWindowModality(QtCore.Qt.WindowModal)
        self.__dialog.setCancelButton(None)
        self.__dialog.show()
        self.__dialog.setValue(0)
        QtWidgets.QApplication.processEvents()  # For the dialog to not be blank.

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.__dialog.cancel()
