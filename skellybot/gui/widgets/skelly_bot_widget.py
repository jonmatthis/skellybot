import logging
import sys
import time

from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget, QMessageBox

logger = logging.getLogger(__name__)

class SkellyBotThread(QThread):
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


class SkellyBotWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.bot = SkellyBotThread()
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

        self.reset_button: QPushButton = QPushButton("Reset Chat")
        self.reset_button.clicked.connect(self.reset_chat)

        vbox: QVBoxLayout = QVBoxLayout()
        vbox.addWidget(self.chat_transcript_area)
        vbox.addWidget(self.input_area)
        vbox.addWidget(self.send_button)
        vbox.addWidget(self.reset_button)

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

    def reset_chat(self) -> None:
        confirmation = QMessageBox.question(
            self, 'Reset Chat', "Are you sure you want to reset the chat?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.StandardButton.Yes:
            self.chat_transcript_area.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    chat_app = SkellyBotWidget()
    chat_app.show()

    sys.exit(app.exec())
