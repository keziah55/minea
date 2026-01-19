import os
from PySide6.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout


class Minea(QMainWindow):

    def __init__(self):
        super().__init__()

        print(f"MINEA running in process {os.getpid()}")

        self._text_edit = QTextEdit()
        self._text_edit.setReadOnly(True)
        self._text_edit.setText("Hello!")

        self.setCentralWidget(self._text_edit)

        self._input_controller.start()

    def _received_cmd(self, cmd: list[str]):

        self._text_edit.append(f"Received cmd: {' '.join(cmd)}")

    def closeEvent(self, event):
        self._input_controller.stop()
        return super().closeEvent(event)
