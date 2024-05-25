"""
Config manager class for CAN Telemetry App.
"""

import json
import os
from app import CANTelemetryApp

DEFAULT_CONFIG_FILE = "config.json"  # JSON file for config keys
DEFAULT_CONFIG_APP_KEY = "app"  # JSON key value for (telemetry) app config
DEFAULT_CONFIG_GUI_KEY = "gui"  # JSON key value for GUI config
DEFAULT_CONFIG_DBC_KEY = "dbc"  # JSON key value for CAN DBC config


class CANTelemetryAppConfig:
    """
    Configuration manager for the CAN Telemetry App.

    Attributes:
        app_json (str): Path to the CAN telemetry app JSON configuration file
        gui_ui (str): Path to the GUI configuration file in .ui format
        dbc (str): Path to the CAN DBC configuration file
    """

    def __init__(self, app_json: str, gui_ui: str, dbc: str):
        """
        Initializes the CANTelemetryAppConfig class with file paths.

        Args:
            app_json (str): Path to the CAN telemetry app JSON configuration file
            gui_ui (str): Path to the GUI configuration file in .ui format
            dbc (str): Path to the CAN DBC configuration file

        Raises:
            AssertionError: If any file path does not have the expected file extension
        """
        # File extension verification
        assert app_json.endswith(".json"), "Expected .json file path"
        assert gui_ui.endswith(".ui"), "Expected .ui file path"
        assert dbc.endswith(".dbc"), "Expected .dbc file path"

        # Attribute setting
        self.app_json = app_json
        self.gui_ui = gui_ui
        self.dbc = dbc

    @classmethod
    def init_from_dir(cls, dir_path: str):
        """
        Initializes a CANTelemetryAppConfig instance from a directory.

        Args:
            dir_path (str): Path to the directory containing the configuration files

        Returns:
            CANTelemetryAppConfig: An initialized instance of CANTelemetryAppConfig

        Raises:
            RuntimeWarning: If expected keys are missing in the JSON configuration file
            Exception: If there is an error reading the JSON configuration file
        """
        json_config_path = os.path.join(dir_path, DEFAULT_CONFIG_FILE)

        try:
            # Open and load the JSON configuration file
            with open(json_config_path, "r") as file:
                json_data = json.load(file)
        except Exception as e:
            return f"An error occurred: {e}"

        # Validate and extract config keys
        try:
            app_json_data = os.path.join(dir_path, json_data[DEFAULT_CONFIG_APP_KEY])
        except KeyError:
            raise RuntimeWarning(
                f"No telemetry .json file found, expected JSON key: {DEFAULT_CONFIG_APP_KEY}"
            )

        try:
            gui_ui_data = os.path.join(dir_path, json_data[DEFAULT_CONFIG_GUI_KEY])
        except KeyError:
            raise RuntimeWarning(
                f"No GUI .ui file found, expected JSON key: {DEFAULT_CONFIG_GUI_KEY}"
            )

        try:
            dbc_data = os.path.join(dir_path, json_data[DEFAULT_CONFIG_DBC_KEY])
        except KeyError:
            raise RuntimeWarning(
                f"No DBC .dbc file found, expected JSON key: {DEFAULT_CONFIG_DBC_KEY}"
            )

        return cls(app_json=app_json_data, gui_ui=gui_ui_data, dbc=dbc_data)

    def init_app(self) -> CANTelemetryApp:
        """
        Initializes the CANTelemetryApp using the configuration JSON file.

        Returns:
            CANTelemetryApp: An instance of CANTelemetryApp initialized with the app JSON configuration
        """
        return CANTelemetryApp.from_json_file(self.app_json)
