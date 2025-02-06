import sys
import importlib.metadata

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.pipeline import Pipeline


class MosamaticDesktopQt20(QMainWindow):
    def __init__(self):
        super().__init__()
        self._task = None
        self._pipeline = Pipeline('D:\\SoftwareDevelopment\\GitHub\MosamaticDesktop2.0\\pipeline.yaml')
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Mosamatic Desktop Qt 2.0")
        widget = QWidget()
        self.setCentralWidget(widget)
        button1 = QPushButton('Run task', self)
        button1.clicked.connect(self.start_task)
        button2 = QPushButton('Cancel task', self)
        button2.clicked.connect(self.cancel_task)
        button3 = QPushButton('Run pipeline', self)
        button3.clicked.connect(self.run_pipeline)
        layout = QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        widget.setLayout(layout)

    def start_task(self):
        if self._task is None or not self._task.isRunning():
            self._task = Task(
                input_dir='D:\\Mosamatic\\Mosamatic Desktop 2.0\\input',
                output_dir='D:\\Mosamatic\\Mosamatic Desktop 2.0\\copyfilestask1',
            )
            self._task.progress.connect(self.update_ui)
            self._task.status.connect(self.update_status)
            self._task.start()

    def cancel_task(self):
        if self._task is not None:
            self._task.cancel()

    def run_pipeline(self):
        self._pipeline.run()

    def update_ui(self, progress):
        pass

    def update_status(self, status):
        pass


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