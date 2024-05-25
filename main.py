"""Main application module."""

import sys
import json
from typing import List

from PyQt6 import QtWidgets

from app_config import CANTelemetryAppConfig
from gui import MainWindow

if __name__ == "__main__":

    start = "start.json"
    # Open the file and read its contents
    try:
        with open(start, 'r') as file:
            content = file.read()
            if not content:
                print(f"The file {start} is empty.")
            else:
                print("Content:", content)
    except FileNotFoundError:
        print(f"The file {start} does not exist.")
    except IOError as e:
        print(f"An IOError occurred: {e}")

    # Load JSON data from a file
    try:
        app_list = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit()  # Exit the program if JSON decoding fails

    # Now `data` contains the JSON content
    print("Data:", app_list)

    app_dir: str = ""
    keep_running: bool = True
    while keep_running:
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
