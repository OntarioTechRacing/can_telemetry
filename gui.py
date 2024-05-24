"""Main application class for GUI handling."""
import typing

from PyQt6 import QtWidgets, uic
import json
from typing import Any, Dict, Optional, Tuple


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ui_file_path: str, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi(ui_file_path, self)


# def load_init():
#     open("config.json", "r")
#     with open("config.json", "r") as config_file:
#         config = json.load(config_file)
#         return config
#     app = config['gui']
#     app = config['app']
#     app = config['dbc']

def load_init() -> Tuple[Dict[str, Any], Optional[str], Optional[str], Optional[str]]:
    """
    Load configuration settings from a JSON file.

    Opens 'config.json', reads its contents, and extracts specific settings.

    Returns:
        Tuple containing:
        - config (Dict[str, Any]): The full configuration dictionary.
        - gui (Optional[str]): The 'gui' configuration if available, otherwise None.
        - app (Optional[str]): The 'app' configuration if available, otherwise None.
        - dbc (Optional[str]): The 'dbc' configuration if available, otherwise None.
    """
    with open("config.json", "r") as config_file:
        config: Dict[str, Any] = json.load(config_file)

    # Extract specific settings from the configuration
    gui: Optional[str] = config.get('gui')
    app: Optional[str] = config.get('app')
    dbc: Optional[str] = config.get('dbc')

    return config, gui, app, dbc

# Dict[str, Any] indicates that config is a dictionary with string keys and values of any type.
# Optional[str] indicates that the values of gui, app, and dbc can be strings or None.
# The return type of the function is a tuple containing the config dictionary and the values of gui, app, and dbc.
#
# The config dictionary type remains Dict[str, Any] because JSON can contain various types
# (e.g., strings, numbers, lists, dictionaries).

import json
from typing import Any, Dict, List, Optional, Tuple, Union


def load_example() -> Dict[str, Any]:
    """
    Load configuration settings from 'example.json'.

    Opens 'example.json', reads its contents, and extracts specific settings.

    Returns:
        Dict containing the configuration settings with the following keys:
        - dbc_file_path (str): Path to the DBC file.
        - interface (str): Interface type.
        - bit_rate (int): Bit rate value.
        - hardware_filters (Optional[Any]): Hardware filters, which can be of any type or None.
        - base_log_file_path (str): Base path for log files.
        - csv_logging (bool): Flag indicating if CSV logging is enabled.
        - ascii_logging (bool): Flag indicating if ASCII logging is enabled.
        - sim_messages (List[Dict[str, Union[float, int, bool, List[int], Optional[Any]]]]): List of simulated messages.
    """
    with open("example.json", "r") as config_file:
        config: Dict[str, Any] = json.load(config_file)

    return config

# Dict[str, Any] indicates that config is a dictionary with string keys and values of any type.
# The config dictionary type remains Dict[str, Any] because JSON can contain various types (e.g., strings, numbers, lists, dictionaries).

#TODO: Return individual keys for use in initialization:
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