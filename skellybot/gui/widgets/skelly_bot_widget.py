import logging
import sys
import time

from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget

logger = logging.getLogger(__name__)


class ChatBot(QThread):
    reply_signal: pyqtSignal = pyqtSignal(str)
    message_signal: pyqtSignal = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.message: str = ""

    @pyqtSlot(str)
    def receive_message(self, message: str) -> None:
        self.message = message
        if not self.isRunning():
            self.start()

    def run(self) -> None:
        time.sleep(1)  # Simulate reply delay
        self.reply_signal.emit(f"ChatBot: I heard you say '{self.message}'")


class ChatApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.bot = ChatBot()
        self.bot.reply_signal.connect(self.receive_reply)
        self.bot.message_signal.connect(self.bot.receive_message)
        self.init_ui()

    def init_ui(self) -> None:
        self.chat_transcript_area: QTextEdit = QTextEdit()
        self.chat_transcript_area.setReadOnly(True)

        self.input_area: QLineEdit = QLineEdit()
        self.input_area.returnPressed.connect(self.enter_pressed)

        self.send_button: QPushButton = QPushButton("Send")
        self.send_button.clicked.connect(self.enter_pressed)

        vbox: QVBoxLayout = QVBoxLayout()
        vbox.addWidget(self.chat_transcript_area)
        vbox.addWidget(self.input_area)
        vbox.addWidget(self.send_button)

        self.setLayout(vbox)

    def enter_pressed(self) -> None:
        if self.send_button.isEnabled():
            text: str = self.input_area.text()
            self.chat_transcript_area.append("You: " + text)
            self.input_area.clear()
            self.send_button.setText("Awaiting Reply...")
            self.send_button.setEnabled(False)
            self.bot.message_signal.emit(text)

    def receive_reply(self, text: str) -> None:
        self.chat_transcript_area.append(text)
        self.bot.quit()
        self.send_button.setText("Send")
        self.send_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    chat_app = ChatApp()
    chat_app.show()

    sys.exit(app.exec())
