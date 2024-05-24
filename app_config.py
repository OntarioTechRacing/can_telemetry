"""Config manager class for CAN Telemetry App."""

import json
import os

from app import CANTelemetryApp

DEFAULT_CONFIG_FILE = "start.json"
DEFAULT_CONFIG_APP_KEY = "app"  # JSON key value for (telemetry) app config.
DEFAULT_CONFIG_GUI_KEY = "gui"  # JSON key value for GUI config.
DEFAULT_CONFIG_DBC_KEY = "dbc"  # JSON key value for CAN DBC config.


class CANTelemetryAppConfig:
    def __init__(
        self,
        app_json: str,
        gui_ui: str,
        dbc: str,
    ):
        """CANTelemetryAppConfig class initialization.

        Args:
            app_json: CAN telemetry app json file path.
            gui_ui: Native xml .ui format file from QT Designer.
        """
        # File extension verification.
        assert app_json[-5:] == ".json", "Expected .dbc file path."
        assert gui_ui[-3:] == ".ui", "Expected .ui file path."
        assert dbc[-4:] == ".dbc", "Expected .dbc file path."

        # Attribute setting.
        self.app_json = app_json
        self.gui_ui = gui_ui
        self.dbc = dbc

    @classmethod
    def init_from_dir(cls, dir_path: str):
        json_config_path = os.path.join(dir_path, DEFAULT_CONFIG_FILE)

        try:
            with open(json_config_path, "r") as file:
                json_data = json.load(file)
        except Exception as e:
            return f"An error occurred: {e}"

        # Validate config keys.
        try:
            app_json_data = os.path.join(
                dir_path, json_data[DEFAULT_CONFIG_APP_KEY]
            )
        except KeyError:
            raise RuntimeWarning(
                f"No telemetry .json file found, expected json key value "
                f"{DEFAULT_CONFIG_APP_KEY}"
            )
        try:
            gui_ui_data = os.path.join(
                dir_path, json_data[DEFAULT_CONFIG_GUI_KEY]
            )
        except KeyError:
            raise RuntimeWarning(
                f"No gui .ui file found, expected json key value "
                f"{DEFAULT_CONFIG_GUI_KEY}"
            )
        try:
            dbc_data = os.path.join(dir_path, json_data[DEFAULT_CONFIG_DBC_KEY])
        except KeyError:
            raise RuntimeWarning(
                f"No DBC .dbc file found, expected json key value "
                f"{DEFAULT_CONFIG_DBC_KEY}"
            )

        return cls(app_json=app_json_data, gui_ui=gui_ui_data, dbc=dbc_data)

    def init_app(self) -> CANTelemetryApp:
        return CANTelemetryApp.from_json_file(self.app_json)
