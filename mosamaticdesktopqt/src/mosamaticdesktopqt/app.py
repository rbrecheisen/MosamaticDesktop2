"""
My first application
"""

import sys
import time
import importlib.metadata

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout
from PySide6.QtCore import QThread, Signal


class Task(QThread):
    progress = Signal(int)

    def run(self):
        for i in range(5):
            if self.isInterruptionRequested():
                return
            time.sleep(1)
            self.progress.emit(i + 20)
        print('Task completed')


class MosamaticDesktopQt20(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Mosamatic Desktop Qt 2.0")
        
        self.button1 = QPushButton('Run task')
        self.button1.clicked.connect(self.start_task)
        # self.button2 = QPushButton('Cancel task')
        # self.button2.clicked.connect(self.cancel_task)

        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        # layout.addWidget(self.button2)
        self.setLayout(layout)

    def start_task(self):
        if self.thread is None or not self.thread.isRunning():
            self.thread = Task()
            self.thread.progress.connect(self.update_ui)
            self.thread.start()

    def update_ui(self, progress):
        print(f'Progress: {progress}')


def main():
    # Linux desktop environments use an app's .desktop file to integrate the app
    # in to their application menus. The .desktop file of this app will include
    # the StartupWMClass key, set to app's formal name. This helps associate the
    # app's windows to its menu item.
    #
    # For association to work, any windows of the app must have WMCLASS property
    # set to match the value set in app's desktop file. For PySide6, this is set
    # with setApplicationName().

    # Find the name of the module that was used to start the app
    app_module = sys.modules["__main__"].__package__
    # Retrieve the app's metadata
    metadata = importlib.metadata.metadata(app_module)

    QApplication.setApplicationName(metadata["Formal-Name"])

    app = QApplication(sys.argv)
    main_window = MosamaticDesktopQt20()
    sys.exit(app.exec())
