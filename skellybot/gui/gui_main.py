import logging

from PyQt6.QtWidgets import QApplication

from skellybot.gui.widgets.main_window import MainWindow

logger = logging.getLogger(__name__)


def gui_main():
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    gui_main()
