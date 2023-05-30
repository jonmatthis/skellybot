import logging
import sys
import time

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit, QApplication

logger = logging.getLogger(__name__)

class ChatBot(QThread):
    reply_signal = pyqtSignal(str)

    def run(self):
        time.sleep(1)  # Simulate reply delay
        self.reply_signal.emit("ChatBot: This is a dummy reply")


class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.bot = ChatBot()
        self.bot.reply_signal.connect(self.receive_reply)

        self.init_ui()

    def init_ui(self):
        self.chat_transcript_area = QTextEdit()
        self.chat_transcript_area.setReadOnly(True)

        self.input_area = QLineEdit()
        self.input_area.returnPressed.connect(self.enter_pressed)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.enter_pressed)

        vbox = QVBoxLayout()
        vbox.addWidget(self.chat_transcript_area)
        vbox.addWidget(self.input_area)
        vbox.addWidget(self.send_button)

        self.setLayout(vbox)

    def enter_pressed(self):
        if self.send_button.isEnabled():
            text = self.input_area.text()
            self.chat_transcript_area.append("You:" + text)
            self.input_area.clear()
            self.send_button.setText("Awaiting Reply...")
            self.send_button.setEnabled(False)

            if not self.bot.isRunning():
                self.bot.start()

    def receive_reply(self, text):
        self.chat_transcript_area.append(text)
        self.bot.quit()
        self.send_button.setText("Send")
        self.send_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    chat_app = ChatApp()
    chat_app.show()

    sys.exit(app.exec())
