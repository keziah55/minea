from PySide6.QtCore import QObject, QThread, Signal, Slot
import selectors
import sys


class InputListener(QObject):
    """
    Object that listens to stdin and send input via `received_input` signal.

    Call `start()` to start listening to `stdin`. Call `stop()` directly to stop.

    Parameters
    ----------
    loop_time
        Number of milliseconds to block stdin and loop for. Default is 100ms.
    """

    received_input = Signal(list)

    def __init__(self, loop_time: int = 100):
        super().__init__()

        self._run = False
        self._loop_time = loop_time / 1000

        # use selector with stdin so it does not block indefinitely
        # see `selector.select` below - it blocks for `timeout` ms
        self._selector = selectors.DefaultSelector()
        self._selector.register(sys.stdin, selectors.EVENT_READ)

    @Slot()
    def stop(self):
        """Stop `stdin` loop."""
        self._run = False

    def start(self):
        """Start `stdin` reading in loop."""

        self._run = True

        while self._run:

            events = self._selector.select(timeout=self._loop_time)
            for key, _ in events:
                cmd = key.fileobj.readline()
                self.received_input.emit([cmd])


class InputController(QObject):
    """
    Object to manage `InputListener` in thread.

    Received commands are send via the `received_input` signal.

    Call `start()` to start listening to `stdin` and `stop()` to stop.

    Parameters
    ----------
    loop_time_ms
        Number of milliseconds to block stdin and loop for. Default is 100ms.
    """

    received_input = Signal(list)

    _request_listener_stop = Signal()

    def __init__(self, loop_time_ms: int = 100):
        super().__init__()

        self._loop_time_ms = loop_time_ms

        self._thread = QThread()
        self._listener = InputListener(loop_time=self._loop_time_ms)

        self._listener.moveToThread(self._thread)

        self._thread.finished.connect(self._listener.deleteLater)
        self._thread.started.connect(self._listener.start)
        self._listener.received_input.connect(self._received_input)

        self._request_listener_stop.connect(self._listener.stop)

    def start(self):
        """Start listening to stdin."""
        self._thread.start()

    def stop(self):
        """Stop listening to stdin and quite thread."""
        self._listener.stop()
        self._thread.exit()
        self._thread.wait(self._loop_time_ms * 1.5)

    @Slot(list)
    def _received_input(self, cmd: list[str]):
        """Send `received_input` signal."""
        self.received_input.emit(cmd)
