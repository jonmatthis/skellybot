from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog

from skellybot.gui.gui_main import logger
from skellybot.gui.widgets.skelly_bot_widget import RunButtonWidget


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

        self.folder_open_button = QPushButton('Load a folder')
        self._layout.addWidget(self.folder_open_button)
        self.folder_open_button.clicked.connect(self._open_session_folder_dialog)

        self._path_to_folder_label = QLabel("No folder selected")
        self._layout.addWidget(self._path_to_folder_label)

        self.run_button = RunButtonWidget(self)
        self._layout.addWidget(self.run_button)

    def _open_session_folder_dialog(self):
        self._folder_path = QFileDialog.getExistingDirectory(None, "Choose a folder")
        self._path_to_folder_label.setText(self._folder_path)
