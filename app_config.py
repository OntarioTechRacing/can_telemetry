"""Config manager class for CAN Telemetry App."""


class CANTelemetryAppConfig:
    def __init__(
        self,
        app_json: str,
        gui_ui: str,
    ):
        """CANTelemetryAppConfig class initialization.

        Args:
            app_json: CAN telemetry app json file path.
            gui_ui: Native xml .ui format file from QT Designer.
        """
        # File extension verification.
        assert app_json[-5:] == ".json", "Expected .dbc file path."
        assert gui_ui[-3:] == ".ui", "Expected .ui file path."

        # Attribute setting.
        self.app_json = app_json
        self.gui_ui = gui_ui
