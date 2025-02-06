import sys
import importlib.metadata

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from mosamaticdesktop.tasks.task import Task


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
        button2 = QPushButton('Cancel', self)
        button2.clicked.connect(self.cancel_task)
        layout = QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        widget.setLayout(layout)

    def start_task(self):
        if self.thread is None or not self.thread.isRunning():
            self.thread = Task()
            self.thread.progress.connect(self.update_ui)
            self.thread.status.connect(self.update_status)
            self.thread.start()

    def cancel_task(self):
        if self.thread is not None:
            self.thread.cancel()

    def update_ui(self, progress):
        print(f'Progress: {progress}')

    def update_status(self, status):
        print(f'Status: {status}')


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