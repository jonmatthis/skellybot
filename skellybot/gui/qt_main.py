import logging

from PyQt6.QtWidgets import QApplication

from skellybot.gui.main_window.main_window import MainWindow

logger = logging.getLogger(__name__)


def qt_main():
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    qt_main()
