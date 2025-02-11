from PySide6.QtWidgets import QDialog, QPushButton, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout


class MuscleFatSegmentationTaskDialog(QDialog):
    def __init__(self, parent=None):
        super(MuscleFatSegmentationTaskDialog, self).__init__(parent)
        self.setWindowTitle('MuscleFatSegmentationTask parameters')
        self._task_params = None
        self._model_dir = None
        self._open_model_dir_button = QPushButton('Open model directory', self)
        self._open_model_dir_button.clicked.connect(self.open_model_directory)
        self._model_dir_label = QLabel('Model directory:', self)
        accept_button = QPushButton('Save', self)
        accept_button.clicked.connect(self.accept)
        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.reject)
        button_layout = QHBoxLayout()
        button_layout.addWidget(accept_button)
        button_layout.addWidget(cancel_button)
        layout = QVBoxLayout()
        layout.addWidget(self._open_model_dir_button)
        layout.addWidget(self._model_dir_label)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def open_model_directory(self):
        self._model_dir = QFileDialog.getExistingDirectory(self, 'Select directory')
        if self._model_dir:
            self._model_dir_label.setText(f'Model directory: {self._model_dir}')

    def accept(self):
        if self._task_params is None:
            self._task_params = {}
        self._task_params['model_dir'] = self._model_dir
        super(MuscleFatSegmentationTaskDialog, self).accept()

    def reject(self):
        self._task_params = None
        super(MuscleFatSegmentationTaskDialog, self).reject()

    def get_params(self):
        return self._task_params