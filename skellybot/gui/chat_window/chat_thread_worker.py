import logging
import time

from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot

from skellybot.bot.bot import Bot

logger = logging.getLogger(__name__)

class ChatThreadWorker(QThread):
    reply_signal: pyqtSignal = pyqtSignal(str)
    message_signal: pyqtSignal = pyqtSignal(str)

    def __init__(self,
                 bot:Bot) -> None:
        super().__init__()
        self.bot = bot
        self.message: str = ""

    @pyqtSlot(str)
    def receive_message(self, message: str) -> None:
        self.message = message
        if not self.isRunning():
            self.start()

    def run(self) -> None:
        response = self.bot.run_agent(self.message)
        self.reply_signal.emit(f"ChatBot: {response}")
