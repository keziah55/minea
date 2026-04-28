import os
from PySide6.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt
from .services import Services
from .input_listener import InputController


class Minea(QMainWindow):

    def __init__(self, services: Services):
        super().__init__()

        print(f"MINEA running in process {os.getpid()}")

        self._services = services

        self._text_edit = QTextEdit()
        self._text_edit.setReadOnly(True)
        self._text_edit.setText("Hello!")

        self._log_pane = QTextEdit()
        self._log_pane.setReadOnly(True)

        tcp_config = self._services.config_manager.get_config_section("tcp")
        self._input_controller = InputController(tcp_config["host"], tcp_config["port"])
        self._input_controller.received_input.connect(self._received_cmd)
        self._input_controller.log_msg.connect(self._received_log_msg)

        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self._text_edit)
        splitter.addWidget(self._log_pane)

        self.setCentralWidget(splitter)

        self._input_controller.start()

    def _received_cmd(self, cmd: str):
        self._text_edit.append(f"Received cmd: {cmd}")

    def _received_log_msg(self, msg: str):
        self._log_pane.append(msg)

    def closeEvent(self, event):
        self._input_controller.stop()
        return super().closeEvent(event)
