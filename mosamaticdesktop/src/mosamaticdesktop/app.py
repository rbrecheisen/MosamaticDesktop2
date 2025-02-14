import sys
import argparse
import importlib.metadata

from PySide6.QtWidgets import QApplication

from mosamaticdesktop.ui.mainwindow import MainWindow
from mosamaticdesktop.server.api import main as server
from mosamaticdesktop.utils import LOGGER


def run_desktop():
    app_module = sys.modules["__main__"].__package__
    # Retrieve the app's metadata
    metadata = importlib.metadata.metadata(app_module)

    QApplication.setApplicationName(metadata["Formal-Name"])

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


def run_server():
    server()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', action='store_true', help='Runs in server mode')
    args = parser.parse_args()
    if args.server:
        LOGGER.info('Running in server mode...')
        run_server()
    else:
        LOGGER.info('Running UI...')
        run_desktop()


if __name__ == '__main__':
    main()