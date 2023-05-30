import logging

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog

from skellybot.gui.widgets.skelly_bot_widget import SkellyBotWidget

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        logger.info("Initializing the main window")
        super().__init__()

        self.setGeometry(100, 100, 600, 600)

        widget = QWidget()
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widget.setLayout(self._layout)
        self.setCentralWidget(widget)


        self._path_to_folder_label = QLabel("No folder selected")
        self._layout.addWidget(self._path_to_folder_label)
        self._layout.addWidget(SkellyBotWidget())

