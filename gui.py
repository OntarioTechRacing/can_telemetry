"""Main application class for GUI handling."""

from PyQt6 import QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ui_file_path: str, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi(ui_file_path, self)
