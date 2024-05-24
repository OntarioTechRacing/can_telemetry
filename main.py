"""Main application module."""

import sys

from PyQt6 import QtWidgets

from app_config import CANTelemetryAppConfig
from gui import MainWindow

if __name__ == "__main__":

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
