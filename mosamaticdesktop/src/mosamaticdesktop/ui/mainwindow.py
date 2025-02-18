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
    QDialog,
    QMessageBox,
    QProgressBar,
)
from PySide6.QtGui import QGuiApplication, QIcon, QAction
from PySide6.QtCore import QOperatingSystemVersion

from mosamaticdesktop.tasks.taskregistry import TASK_REGISTRY
from mosamaticdesktop.tasks.pipeline import Pipeline
from mosamaticdesktop.utils import LOGGER
from mosamaticdesktop.ui.helpdialog import HelpDialog
from mosamaticdesktop.ui.logdialog import LogDialog

BASE_DIR = str(Path(__file__).resolve().parent.parent)
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._task = None
        self._task_params = None
        self._pipeline = None
        self._directory_combo = None 
        self._tasks_combo = None
        self._task_run_button = None
        self._task_cancel_button = None
        self._task_params_button = None
        self._input_group = None
        self._tasks_group = None
        self._pipeline_group = None
        self._pipeline_config_label = None
        self._pipeline_run_button = None
        self._progress_bar = None
        self._task_status = None
        self._log_dialog = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Mosamatic Desktop 2.0')
        self.setWindowIcon(QIcon(os.path.join(RESOURCES_DIR, 'letter-m.png')))
        self._log_dialog = LogDialog(self)
        help_action = QAction('Show user manual', self)
        help_action.triggered.connect(self.show_help)
        help_menu = self.menuBar().addMenu('Help')
        help_menu.addAction(help_action)
        logs_action = QAction('Show logs', self)
        logs_action.triggered.connect(self.show_logs)
        logs_menu = self.menuBar().addMenu('Logs')
        logs_menu.addAction(logs_action)
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
        select_dir_button = QPushButton('Select input directory', self)
        select_dir_button.clicked.connect(self.select_input_directory)
        self._directory_combo = QComboBox()
        self._directory_combo.setEditable(True)
        #### Hack for quick testing
        # if QOperatingSystemVersion.current() >= QOperatingSystemVersion(QOperatingSystemVersion.Windows10):
        #     self._directory_combo.addItem('D:\\Mosamatic\\Mosamatic Desktop 2.0\\input')
        # else:
        #     self._directory_combo.addItem('/Users/ralph/Desktop/downloads/mosamaticdesktop/input')
        ####
        input_group_layout = QVBoxLayout()
        input_group_layout.addWidget(select_dir_button)
        input_group_layout.addWidget(self._directory_combo)
        self._input_group.setLayout(input_group_layout)

    def init_tasks_group(self):
        self._tasks_group = QGroupBox('Tasks')
        self._tasks_combo = QComboBox()
        self._tasks_combo.addItem(None)
        self._tasks_combo.addItems(TASK_REGISTRY.keys())
        self._tasks_combo.setEditable(False)
        self._task_params_button = QPushButton('Set task parameters', self)
        self._task_params_button.clicked.connect(self.set_task_params)
        self._task_run_button = QPushButton('Run task', self)
        self._task_run_button.clicked.connect(self.run_task)
        self._task_run_button.setEnabled(False)
        self._task_cancel_button = QPushButton('Cancel task', self)
        self._task_cancel_button.clicked.connect(self.cancel_task)
        self._task_cancel_button.setEnabled(False)
        self._progress_bar = QProgressBar(self, minimum=0, maximum=100)
        self._task_status = QLabel('Status: idle')
        tasks_group_layout = QVBoxLayout()
        tasks_group_layout.addWidget(self._tasks_combo)
        tasks_group_layout.addWidget(self._task_params_button)
        tasks_group_layout.addWidget(self._task_run_button)
        tasks_group_layout.addWidget(self._task_cancel_button)
        tasks_group_layout.addWidget(self._progress_bar)
        tasks_group_layout.addWidget(self._task_status)
        self._tasks_group.setLayout(tasks_group_layout)

    def init_pipeline_group(self):
        self._pipeline_group = QGroupBox('Pipeline')
        load_pipeline_config_button = QPushButton('Load pipeline config', self)
        load_pipeline_config_button.clicked.connect(self.load_pipeline_config)
        self._pipeline_config_label = QLabel('No config file selected')
        self._pipeline_run_button = QPushButton('Run pipeline', self)
        self._pipeline_run_button.clicked.connect(self.run_pipeline)
        pipeline_group_layout = QVBoxLayout()
        pipeline_group_layout.addWidget(load_pipeline_config_button)
        pipeline_group_layout.addWidget(self._pipeline_config_label)
        pipeline_group_layout.addWidget(self._pipeline_run_button)
        self._pipeline_group.setLayout(pipeline_group_layout)

    def show_help(self):
        help_dialog = HelpDialog()
        help_dialog.show()

    def show_logs(self):
        self._log_dialog.show()

    def select_input_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select directory', dir=BASE_DIR)
        if directory and directory not in [self._directory_combo.itemText(i) for i in range(self._directory_combo.count())]:
            self._directory_combo.addItem(directory)
            self._directory_combo.setCurrentText(directory)
        else:
            pass

    def set_task_params(self):
        self._task_params = None
        task_name = self._tasks_combo.currentText()
        if task_name and task_name != '':
            task_dialog = TASK_REGISTRY[task_name][1](self)
            if task_dialog.exec() == QDialog.Accepted:
                self._task_params = task_dialog.get_params()
                self._task_run_button.setEnabled(True)
            else:
                LOGGER.info('No task parameters set')
                self._task_run_button.setEnabled(False)

    def run_task(self):
        input_dir = self._directory_combo.currentText()
        if input_dir and input_dir != '':
            self._progress_bar.setValue(0)
            self._task_params_button.setEnabled(False)
            self._task_run_button.setEnabled(False)
            self._task_cancel_button.setEnabled(True)
            task_name = self._tasks_combo.currentText()
            self._task = TASK_REGISTRY[task_name][0](
                input_dir=self._directory_combo.currentText(), 
                params=self._task_params
            )
            self._task.progress.connect(self.update_task_progress)
            self._task.status.connect(self.update_task_status)
            self._task.log.connect(self.update_task_log)
            self._task.start()
        else:
            QMessageBox.warning(self, 'Input directory', 'No input directory selected')

    def cancel_task(self):
        if self._task is not None:
            self._task.cancel()
        self._task_params_button.setEnabled(True)
        self._task_run_button.setEnabled(True)
        self._task_cancel_button.setEnabled(False)

    def load_pipeline_config(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open pipeline config', dir=BASE_DIR)
        if file_path and file_path.endswith('.yaml'):
            self._pipeline = Pipeline(file_path, main_window=self)
            self._pipeline_config_label.setText(file_path)
        else:
            self._pipeline_config_label.setText('No config file selected')

    def run_pipeline(self):
        self._pipeline_run_button.setEnabled(False)
        if self._pipeline:
            self._pipeline.run()
        self._pipeline_run_button.setEnabled(True)

    def update_task_progress(self, progress):
        self._progress_bar.setValue(progress)

    def update_task_status(self, status):
        self._task_status.setText(f'Status: {status}')
        if status == 'completed' or status == 'failed' or status == 'canceled':
            self._task_run_button.setEnabled(False)
            self._task_cancel_button.setEnabled(False)          
            self._task_params_button.setEnabled(True)
            if status == 'completed':
                output_dir = self._task.get_output_dir()
                self._directory_combo.addItem(output_dir)
                self._directory_combo.setCurrentText(output_dir)

    def update_task_log(self, message):
        self._log_dialog.append_log(message)

    def center_window(self):
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))