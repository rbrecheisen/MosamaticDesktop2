import sys
import importlib.metadata

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QGroupBox, QFileDialog, QLabel, QComboBox

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.pipeline import Pipeline


class MosamaticDesktopQt20(QMainWindow):
    def __init__(self):
        super().__init__()
        self._task = None
        self._directory_combo = None 
        self._pipeline = Pipeline('D:\\SoftwareDevelopment\\GitHub\MosamaticDesktop2.0\\pipeline.yaml')
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Mosamatic Desktop 2.0")
        widget = QWidget()
        self.setCentralWidget(widget)

        input_group = QGroupBox('Input')
        select_dir_button = QPushButton('Select input directory:', self)
        self._directory_combo = QComboBox()
        self._directory_combo.setEditable(True)
        input_group_layout = QVBoxLayout()
        input_group_layout.addWidget(select_dir_button)
        input_group_layout.addWidget(self._directory_combo)
        input_group.setLayout(input_group_layout)

        tasks_group = QGroupBox('Tasks')
        button1 = QPushButton('Run task', self)
        button2 = QPushButton('Cancel task', self)
        tasks_group_layout = QVBoxLayout()
        tasks_group_layout.addWidget(button1)
        tasks_group_layout.addWidget(button2)
        tasks_group.setLayout(tasks_group_layout)

        pipeline_group = QGroupBox('Pipeline')
        button3 = QPushButton('Run pipeline', self)
        pipeline_group_layout = QVBoxLayout()
        pipeline_group_layout.addWidget(button3)
        pipeline_group.setLayout(pipeline_group_layout)

        select_dir_button.clicked.connect(self.select_directory)
        button1.clicked.connect(self.start_task)
        button2.clicked.connect(self.cancel_task)
        button3.clicked.connect(self.run_pipeline)

        layout = QVBoxLayout()
        layout.addWidget(input_group)
        layout.addWidget(tasks_group)
        layout.addWidget(pipeline_group)
        widget.setLayout(layout)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select directory')
        if directory and directory not in [self._directory_combo.itemText(i) for i in range(self._directory_combo.count())]:
            self._directory_combo.addItem(directory)
            self._directory_combo.setCurrentText(directory)
        else:
            pass

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