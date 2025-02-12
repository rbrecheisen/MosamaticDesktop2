from PySide6.QtWidgets import QPushButton, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout

from mosamaticdesktop.tasks.taskdialog import TaskDialog


class MuscleFatSegmentationTaskDialog(TaskDialog):
    def __init__(self, parent=None):
        super(MuscleFatSegmentationTaskDialog, self).__init__(parent)
        self._model_dir = None
        self._open_model_dir_button = QPushButton('Open model directory', self)
        self._open_model_dir_button.clicked.connect(self.open_model_directory)
        self._model_dir_label = QLabel('Model directory:', self)

    def get_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self._open_model_dir_button)
        layout.addWidget(self._model_dir_label)
        return layout

    def open_model_directory(self):
        self._model_dir = QFileDialog.getExistingDirectory(self, 'Select directory')
        if self._model_dir:
            self._model_dir_label.setText(f'Model directory: {self._model_dir}')

    def update_params(self):
        self.set_param('model_dir', self._model_dir)