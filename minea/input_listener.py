import socket
from typing import NamedTuple

from PySide6.QtCore import QObject, QThread, Signal, Slot


class SocketInfo(NamedTuple):
    """Data required to use TCP/IP socket."""

    host: str
    port: int


class InputListener(QObject):
    """
    Object that listens to socket and send input via `received_input` signal.

    Call `start()` to start listening to socket. Call `stop()` directly to stop.

    Parameters
    ----------
    socket_info
        `SocketInfo` object with host and port to connect to for server.
    """

    received_input = Signal(str)
    """Signal emitted with data received from socket."""

    log_msg = Signal(str)
    """Signal emitted with general info about the `InputListener`."""

    def __init__(self, socket_info: SocketInfo):
        super().__init__()

        self._run = False

        self._tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tcp_socket.bind(socket_info)
        self._tcp_socket.listen(1)
        self.log_msg.emit(f"TCP socket created with {socket_info}")

    @Slot()
    def stop(self):
        """Stop socket loop."""
        self.log_msg.emit("Stopping InputListener")
        self._run = False

    def start(self):
        """Start socket reading in loop."""

        self._run = True

        while self._run:

            connection, client = self._tcp_socket.accept()

            self.log_msg.emit(f"Connected to client IP: {client}")

            msg = ""

            with connection:
                while True:
                    data = connection.recv(1024)
                    msg += data.decode()
                    if not data:
                        self.received_input.emit(msg)
                        break

        self._tcp_socket.close()


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

    received_input = Signal(str)

    _request_listener_stop = Signal()

    def __init__(self):
        super().__init__()

        self._socket_info = SocketInfo(host="127.0.0.1", port=64632)

        self._thread = QThread()
        self._listener = InputListener(self._socket_info)

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
        tcp_socket = socket.create_connection(self._socket_info)
        tcp_socket.sendall(b"")
        tcp_socket.close()

        self._thread.quit()

    @Slot(str)
    def _received_input(self, cmd: str):
        """Send `received_input` signal."""
        self.received_input.emit(cmd)
