from PySide6.QtCore import QObject, QThread, Signal, Slot

class InputListener(QObject):

    received_input = Signal(list)

    def __init__(self):
        super().__init__()
        self._run = False

    @Slot()
    def stop(self):
        self._run = False

    def start(self):
        self._run = True

        while self._run:
            cmd = input()
            # strip whitespace
            # cmd = [s.strip() for s in " ".split(cmd)]
            self.received_input.emit([cmd])


class InputController(QObject):

    received_input = Signal(list)

    _request_listener_stop = Signal()

    def __init__(self):
        super().__init__()

        self._thread = QThread()
        self._listener = InputListener()

        self._listener.moveToThread(self._thread)

        self._thread.finished.connect(self._listener.deleteLater)
        self._thread.started.connect(self._listener.start)
        self._listener.received_input.connect(self._received_input)

        self._request_listener_stop.connect(self._listener.stop)

    def start(self):
        self._thread.start()

    def stop(self):
        self._request_listener_stop.emit()
        self._thread.exit()
        self._thread.wait(100)


    @Slot(list)
    def _received_input(self, cmd: list[str]):
        self.received_input.emit(cmd)
