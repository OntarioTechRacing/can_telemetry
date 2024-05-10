"""Config manager class for CAN Telemetry App."""


class CANTelemetryAppConfig:
    def __init__(
        self,
        app_json: str,
        py_gui: str,
        py_gui_requirements: str,
        xml_gui: str | None = None,
    ):
        """CANTelemetryAppConfig class initialization.

        Args:
            app_json: CAN telemetry app json file path.
            py_gui: Python PyQT gui file path.
            py_gui_requirements: PIP requirements file for Python GUI.
            xml_gui: Reference native xml .ui format file for QT Designer.
        """
        # Remove empty strings and default to None.
        if isinstance(xml_gui, str) and not xml_gui:
            xml_gui = None

        # File extension verification.
        assert app_json[-5:] == ".json", "Expected .dbc file path."
        assert py_gui[-3:] == ".py", "Expected .py file path."
        assert py_gui_requirements[-4:] == ".txt", "Expected .txt file path."
        assert xml_gui[-3:] == ".ui", "Expected .ui file path."

        # Attribute setting.
        self.app_json = app_json
        self.py_gui = py_gui
        self.py_gui_requirements = py_gui_requirements
        self.xml_gui = xml_gui
