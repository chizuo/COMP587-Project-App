from threading import Thread
from typing import Callable

from PySide6 import QtCore


class Worker(QtCore.QObject):
    """A worker that executes a function in a separate thread.

    Emits a ``done`` signal when the function has finished executing. What the function
    returns will be emitted in the ``done`` signal.
    """

    # TODO: attempting to emit the `done` signal with None may cause an error.
    # https://stackoverflow.com/questions/21102591/pyside-pyqt-signal-that-can-transmit-any-value-including-none  # noqa: E501

    done = QtCore.Signal(object)

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.is_running = False

    def start(self, fn: Callable, *args, **kwargs):
        """Starts the worker thread.

        Parameters
        ----------
        fn : Callable
            The function to be executed in the worker thread. What this function returns
            will be emitted in the ``done`` signal, so any function connected to the
            ``done`` signal should be able to handle the return value of ``fn``.
        *args
            The positional arguments to be passed to ``fn``.
        **kwargs
            The keyword arguments to be passed to ``fn``.
        """
        Thread(target=self.__exec, args=(fn, *args), kwargs=kwargs, daemon=True).start()

    def __exec(self, fn: Callable, *args, **kwargs):
        self.is_running = True
        self.done.emit(fn(*args, **kwargs))
        self.is_running = False
