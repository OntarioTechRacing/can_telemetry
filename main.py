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

from PyQt6 import QtWidgets

from app_config import CANTelemetryAppConfig
from gui import AppWindow, MainWindow


def run_app(app_dir: str):
    """Run the selected telemetry application.

    Args:
        app_dir (str): Directory containing the app's configuration files.
    """
    # Load configuration settings from the app directory.
    config = CANTelemetryAppConfig.init_from_dir(app_dir)

    # Initialize telemetry backend application based on loaded configuration.
    telemetry = config.init_app()
    telemetry.start()

    # Initialize and display the graphical user interface (GUI) for the selected app.
    gui = QtWidgets.QApplication(sys.argv)
    app_window = AppWindow(config.gui_ui)
    app_window.show()

    try:
        # Run the GUI event loop for the app.
        gui.exec()
    except KeyboardInterrupt:  # Handle GUI closure by user.
        pass
    finally:
        # Stop the telemetry backend application and clean up resources.
        telemetry.stop()
        telemetry.join()


if __name__ == "__main__":
    ##Loading json
    with open('example.json') as f:
        app_list = json.load(f)
    ##serializing
    json_string = json.dumps(app_list)

    start = "start.json"
    # Open the file and read its contents
    try:
        with open(start, 'r') as file:
            content = file.read()
            if not content:
                print(f"The file {start} is empty.")
                sys.exit(1)  # Exit if the start file is empty
            else:
                print("Content:", content)
    except FileNotFoundError:
        print(f"The file {start} does not exist.")
        sys.exit(1)
    except IOError as e:
        print(f"An IOError occurred: {e}")
        sys.exit(1)

    # Load JSON data from a file
    try:
        app_list = json.loads(content)['list-of-app-directories']
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)  # Exit the program if JSON decoding fails

    # Now `app_list` contains the JSON content
    print("App List:", app_list)

    app = QtWidgets.QApplication(sys.argv)

    keep_running = True
    while keep_running:
        # Show the main window for app selection
        app_selector = MainWindow("main_window.ui", app_list)
        app_selector.show()

        # Run the GUI event loop for the main window
        app.exec()

        # Check if an app was selected
        selected_app = app_selector.selected_app
        if selected_app:
            # Run the selected app
            run_app(selected_app)
        else:
            keep_running = False  # Exit the loop if no app is selected

    # Exit the application
    sys.exit()
