from PySide6.QtWidgets import QPushButton, QFileDialog, QLabel, QVBoxLayout, QComboBox

from mosamaticdesktop.tasks.taskdialog import TaskDialog


class MuscleFatSegmentationL3TaskDialog(TaskDialog):
    def __init__(self, parent=None):
        super(MuscleFatSegmentationL3TaskDialog, self).__init__(parent)
        self._model_dir = None
        self._model_label = QLabel('Select model type', self)
        self._model_combobox = QComboBox(self)
        self._model_combobox.addItems(['tensorflow', 'torch'])
        self._model_version_label = QLabel('Select model version', self)
        self._model_version_combobox = QComboBox(self)
        self._model_version_combobox.addItem('1.0')
        self._open_model_dir_button = QPushButton('Open model directory', self)
        self._open_model_dir_button.clicked.connect(self.open_model_directory)
        self._model_dir_label = QLabel('Model directory:', self)
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._model_label)
        self._layout.addWidget(self._model_combobox)
        self._layout.addWidget(self._model_version_label)
        self._layout.addWidget(self._model_version_combobox)
        self._layout.addWidget(self._open_model_dir_button)
        self._layout.addWidget(self._model_dir_label)
        self.init_ui()

    def get_content_layout(self):
        return self._layout

    def open_model_directory(self):
        self._model_dir = QFileDialog.getExistingDirectory(self, 'Select directory')
        if self._model_dir:
            self._model_dir_label.setText(f'Model directory: {self._model_dir}')

    def update_params(self):
        self.set_param('model_type', self._model_combobox.currentText())
        self.set_param('model_version', float(self._model_version_combobox.currentText()))
        self.set_param('model_dir', self._model_dir)