"""
Main application class for GUI handling.
"""

from PyQt6 import QtWidgets, uic


class AppWindow(QtWidgets.QMainWindow):
    """
    Main window class for the GUI application.

    Args:
        ui_file_path (str): Path to the .ui file for the GUI
        parent: Optional parent widget

    Attributes:
        None.
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
    def __init__(self, ui_file_path: str, apps_list: list):
        """
        Initializes the MainWindow class. Cannot have a Parent.
        The ui file must have a QComboBox widget called "comboBox"

        Args:
            ui_file_path (str): Path to the .ui file for the GUI
            apps_list (list): List of (apps) to display
        """
        super().__init__(None)
        # Load the .ui file
        uic.loadUi(ui_file_path, self)

        # Get the QComboBox widget from the loaded UI
        combo_box = self.findChild(QtWidgets.QComboBox, 'comboBox')

        # Populate the QComboBox widget with items from the list
        combo_box.addItems(apps_list)

# TODO: Return individual keys for use in initialization:
"""CANTelemetryApp class initialization.

Args:
    dbc_file_path (str): File path of DBC file
    interface (CANInterface): Interface CANInterface enum type, default VIRTUAL
    bit_rate (int): Bit rate of CAN bus instance, default 500000
    hardware_filters: Hardware filters to specify
    base_log_file_path (str): Base filepath of all log output files, defaults
    csv_logging (bool): Boolean to enable CSV logging, default False
    ascii_logging (bool): Boolean to enable ASCII logging, default False
    sim_messages: Simulation messages, interface must be SIM enum
"""