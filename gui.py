"""Main application class for GUI handling."""

from typing import Any, Dict, Optional, Tuple

from PyQt6 import QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ui_file_path: str, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi(ui_file_path, self)


# TODO: Return individual keys for use in initialization:
"""CANTelemetryApp class initialization.

Args:
    dbc_file_path: File path of DBC file.
    interface: Interface CANInterface enum type, default VIRTUAL.
    bit_rate: Bit rate of CAN bus instance, default 500000.
    hardware_filters: Hardware filters to specify.
    base_log_file_path: Base filepath of all log output files, defaults.
    csv_logging: Boolean to enable CSV logging, default False.
    ascii_logging: Boolean to enable ASCII logging, default False.
    sim_messages: Simulation messages, interface must be SIM enum.
"""
