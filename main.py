"""Main application module.

This module serves as the entry point for the CAN Telemetry Application.
It initializes the telemetry backend and graphical user interface (GUI),
loads configuration settings, and manages the application lifecycle.

Attributes:
    None.
"""

import sys
import json
from typing import List

from PyQt6 import QtWidgets, uic

from app_config import CANTelemetryAppConfig
from gui import AppWindow, MainWindow

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

    app_dir: str = ""  # Default app directory
    keep_running: bool = True

    app_selector = MainWindow("start.ui", app_list)

    while keep_running:
        # Load configuration settings from the app directory.
        config = CANTelemetryAppConfig.init_from_dir(app_dir)

        # Initialize telemetry backend application based on loaded configuration.
        telemetry = config.init_app()
        telemetry.start()

        # Initialize and display the graphical user interface (GUI).
        gui = QtWidgets.QApplication(sys.argv)
        mainWindow = AppWindow(config.gui_ui)
        mainWindow.show()

        try:
            # Run the GUI event loop.
            gui.exec()
        except KeyboardInterrupt:  # Handle GUI closure by user.
            pass
        finally:
            # Stop the telemetry backend application and clean up resources.
            telemetry.stop()
            telemetry.join()
