import logging
import sys

from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget, QMessageBox

from skellybot.bot.bot import Bot
from skellybot.gui.chat_window.chat_thread_worker import ChatThreadWorker

logger = logging.getLogger(__name__)


class ChatWidget(QWidget):
    def __init__(self,
                 bot:Bot = Bot()) -> None:
        super().__init__()
        self._chat_thread_worker = ChatThreadWorker(bot=bot)
        self._chat_thread_worker.reply_signal.connect(self.receive_reply)
        self._chat_thread_worker.message_signal.connect(self._chat_thread_worker.receive_message)
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
            self._chat_thread_worker.message_signal.emit(text)

    def receive_reply(self, text: str) -> None:
        self.chat_transcript_area.append(text)
        self._chat_thread_worker.quit()
        self.send_button.setText("Send")
        self.send_button.setEnabled(True)

    def reset_chat(self) -> None:
        confirmation = QMessageBox.question(
            self, 'Reset Chat', "Are you sure you want to reset the chat_window?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.StandardButton.Yes:
            self.chat_transcript_area.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    chat_app = ChatWidget()
    chat_app.show()

    sys.exit(app.exec())
