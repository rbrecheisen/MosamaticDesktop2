"""
My first application
"""

import sys
import time
import importlib.metadata

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QThread, Signal


class Task(QThread):
    progress = Signal(int)

    def run(self):
        for i in range(5):
            if self.isInterruptionRequested():
                return
            time.sleep(1)
            self.progress.emit((i+1) * 20)


class MosamaticDesktopQt20(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Mosamatic Desktop Qt 2.0")
        widget = QWidget()
        self.setCentralWidget(widget)
        button1 = QPushButton('Run task', self)
        button1.clicked.connect(self.start_task)
        layout = QVBoxLayout()
        layout.addWidget(button1)
        widget.setLayout(layout)

    def start_task(self):
        if self.thread is None or not self.thread.isRunning():
            self.thread = Task()
            self.thread.progress.connect(self.update_ui)
            self.thread.start()

    def update_ui(self, progress):
        print(f'Progress: {progress}')


def main():
    app_module = sys.modules["__main__"].__package__
    # Retrieve the app's metadata
    metadata = importlib.metadata.metadata(app_module)

    QApplication.setApplicationName(metadata["Formal-Name"])

    app = QApplication(sys.argv)
    main_window = MosamaticDesktopQt20()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()