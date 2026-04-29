import socket
from PySide6.QtCore import QObject, QThread, Signal, Slot

from ..utils import TcpConfig, CommandConfig
from ..services import Services


class InputListener(QObject):
    """
    Object that listens to socket and send input via `received_input` signal.

    Parameters
    ----------
    tcp_config
        `TcpConfig` object with host and port to connect to for server.
    """

    received_input = Signal(list)
    """Signal emitted with command and args received from socket."""

    log_msg = Signal(str)
    """Signal emitted with general info about the `InputListener`."""

    def __init__(self, tcp_config: TcpConfig, cmd_config: CommandConfig):
        super().__init__()

        self._run = False

        self._cmd_config = cmd_config

        self._tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tcp_socket.bind(tcp_config)
        self._tcp_socket.listen(1)
        self.log_msg.emit(f"TCP socket created with {tcp_config}")

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
                        cmd = msg.split(self._cmd_config.sep)
                        self.received_input.emit(cmd)
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

    received_input = Signal(list)

    log_msg = Signal(str)

    _request_listener_stop = Signal()

    def __init__(self, services: Services):
        super().__init__()

        self._tcp_config = services.tcp_config
        self._listener = InputListener(tcp_config=self._tcp_config, cmd_config=services.cmd_config)

        self._thread = QThread()
        self._listener.moveToThread(self._thread)

        self._thread.finished.connect(self._listener.deleteLater)
        self._thread.started.connect(self._listener.start)
        self._listener.received_input.connect(self._received_input)
        self._listener.log_msg.connect(self.log_msg.emit)

        self._request_listener_stop.connect(self._listener.stop)

    def start(self):
        """Start listening to stdin."""
        self._thread.start()

    def stop(self):
        """Stop listening to stdin and quite thread."""
        self._listener.stop()
        # self._request_listener_stop.emit()
        tcp_socket = socket.create_connection(self._tcp_config)
        tcp_socket.sendall(b"")
        tcp_socket.close()

        self._thread.quit()

    @Slot(str)
    def _received_input(self, cmd: list[str]):
        """Send `received_input` signal."""
        self.received_input.emit(cmd)
