from PySide6.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout
from .input_listener import InputController

class Minea(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self._text_edit = QTextEdit()
        self._text_edit.setReadOnly(True)
        self._text_edit.setText("Hello!")

        self._input_controller = InputController()
        self._input_controller.received_input.connect(self._received_cmd)

        self.setCentralWidget(self._text_edit)

        self._input_controller.start()

    def _received_cmd(self, cmd:list[str]):
        
        self._text_edit.append(f"Received cmd: {' '.join(cmd)}")

    def closeEvent(self, event):
        self._input_controller.stop()
        return super().closeEvent(event)