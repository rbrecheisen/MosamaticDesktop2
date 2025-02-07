import os

from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, 
    QPushButton, 
    QVBoxLayout, 
    QWidget, 
    QGroupBox, 
    QFileDialog, 
    QComboBox,
    QLabel,
)
from PySide6.QtGui import QGuiApplication, QIcon

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.tasks.registry import TaskRegistry
from mosamaticdesktop.tasks.pipeline import Pipeline

RESOURCES_DIR = str(Path(__file__).resolve().parent.parent / 'resources')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._task = None
        self._task_params = None
        self._pipeline = None
        self._directory_combo = None 
        self._tasks_combo = None
        self._input_group = None
        self._tasks_group = None
        self._pipeline_group = None
        self._pipeline_config_label = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Mosamatic Desktop 2.0')
        self.setWindowIcon(QIcon(os.path.join(RESOURCES_DIR, 'letter-m.png')))
        widget = QWidget()
        self.setCentralWidget(widget)
        self.init_input_group()
        self.init_tasks_group()
        self.init_pipeline_group()
        layout = QVBoxLayout()
        layout.addWidget(self._input_group)
        layout.addWidget(self._tasks_group)
        layout.addWidget(self._pipeline_group)
        widget.setLayout(layout)
        self.center_window()
        self.resize(400, 300)

    def init_input_group(self):
        self._input_group = QGroupBox('Input')
        select_dir_button = QPushButton('Select input directory:', self)
        select_dir_button.clicked.connect(self.select_directory)
        self._directory_combo = QComboBox()
        self._directory_combo.setEditable(True)
        input_group_layout = QVBoxLayout()
        input_group_layout.addWidget(select_dir_button)
        input_group_layout.addWidget(self._directory_combo)
        self._input_group.setLayout(input_group_layout)

    def init_tasks_group(self):
        self._tasks_group = QGroupBox('Tasks')
        self._tasks_combo = QComboBox()
        task_names = [entry.value[0].__name__ for entry in TaskRegistry]
        self._tasks_combo.addItems(task_names)
        self._tasks_combo.setEditable(False)
        task_params_button = QPushButton('Set task parameters', self)
        task_params_button.clicked.connect(self.set_task_params)
        task_run_button = QPushButton('Run task', self)
        task_run_button.clicked.connect(self.run_task)
        tasks_group_layout = QVBoxLayout()
        tasks_group_layout.addWidget(self._tasks_combo)
        tasks_group_layout.addWidget(task_params_button)
        tasks_group_layout.addWidget(task_run_button)
        self._tasks_group.setLayout(tasks_group_layout)

    def init_pipeline_group(self):
        self._pipeline_group = QGroupBox('Pipeline')
        load_pipeline_config_button = QPushButton('Load pipeline config', self)
        load_pipeline_config_button.clicked.connect(self.load_pipeline_config)
        self._pipeline_config_label = QLabel('No config file selected')
        run_pipeline_button = QPushButton('Run pipeline', self)
        run_pipeline_button.clicked.connect(self.run_pipeline)
        pipeline_group_layout = QVBoxLayout()
        pipeline_group_layout.addWidget(load_pipeline_config_button)
        pipeline_group_layout.addWidget(self._pipeline_config_label)
        pipeline_group_layout.addWidget(run_pipeline_button)
        self._pipeline_group.setLayout(pipeline_group_layout)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select directory')
        if directory and directory not in [self._directory_combo.itemText(i) for i in range(self._directory_combo.count())]:
            self._directory_combo.addItem(directory)
            self._directory_combo.setCurrentText(directory)
        else:
            pass

    def set_task_params(self):
        pass

    def run_task(self):
        pass

    def load_pipeline_config(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open pipeline config')
        if file_path and file_path.endswith('.yaml'):
            self._pipeline = Pipeline(file_path)
            self._pipeline_config_label.setText(file_path)
        else:
            self._pipeline_config_label.setText('No config file selected')

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
        if self._pipeline:
            self._pipeline.run()

    def update_ui(self, progress):
        pass

    def update_status(self, status):
        pass

    def center_window(self):
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))
        pass
