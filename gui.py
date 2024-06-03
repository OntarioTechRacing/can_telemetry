# gui.py

from typing import List
from PyQt6 import QtWidgets, uic


class AppWindow(QtWidgets.QMainWindow):
    """
    Main window class for the GUI application.

    Args:
        ui_file_path (str): Path to the .ui file for the GUI
        parent: Optional parent widget
    """

    def __init__(self, ui_file_path: str, parent=None):
        """
        Initializes the MainWindow class.

        Args:
            ui_file_path (str): Path to the .ui file for the GUI
            parent: Optional parent widget
        """
        super(AppWindow, self).__init__(parent)
        uic.loadUi(ui_file_path, self)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ui_file_path: str, apps_list: List[str]):
        """
        Initializes the MainWindow class. The UI file must have a QComboBox widget called "comboBox".

        Args:
            ui_file_path (str): Path to the .ui file for the GUI.
            apps_list (List[str]): List of apps to display in the QComboBox.
        """
        super().__init__()
        # Load the .ui file
        uic.loadUi(ui_file_path, self)

        # Get the QComboBox widget from the loaded UI
        self.combo_box = self.findChild(QtWidgets.QComboBox, 'comboBox')

        # Check if the QComboBox widget was found
        if self.combo_box is None:
            raise ValueError("QComboBox widget with object name 'comboBox' not found in the UI file.")

        # Populate the QComboBox widget with items from the list
        self.combo_box.addItems(apps_list)

        # Get the QPushButton widget from the loaded UI
        self.open_button = self.findChild(QtWidgets.QPushButton, 'openButton')

        # Check if the QPushButton widget was found
        if self.open_button is None:
            raise ValueError("QPushButton widget with object name 'openButton' not found in the UI file.")

        # Connect the button click event to the launch_app method
        self.open_button.clicked.connect(self.launch_app)

        # Variable to store the selected app directory
        self.selected_app = None

    def launch_app(self):
        """Handles the open button click event to launch the selected app."""
        # Get the selected item from the combo box
        self.selected_app = self.combo_box.currentText()
        # Close the main window
        self.close()
