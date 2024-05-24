"""Main application module."""

import sys
import json
from typing import List

from PyQt6 import QtWidgets

from app_config import CANTelemetryAppConfig
from gui import MainWindow

if __name__ == "__main__":

    # Initialize with an empty list
    data: List[str] = ["ERROR"] #: Config File not in root directory.

    # Load JSON data from a file
    with open('start.json', 'r') as file:
        data = json.load(file)



    project_dir = "/" #path for the starting point of the app.
   # take a config file that has the location of app 1

    app_dir: str = ""



    # Load config.
    config = CANTelemetryAppConfig.init_from_dir(app_dir)

    # Init telemetry backend app.
    telemetry = config.init_app()
    telemetry.start()

    # Init and run GUI.
    gui = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow(config.gui_ui)
    mainWindow.show()

    try:
        gui.exec()
    except KeyboardInterrupt:  # GUI closed.
        pass
    finally:
        telemetry.stop()
        telemetry.join()
