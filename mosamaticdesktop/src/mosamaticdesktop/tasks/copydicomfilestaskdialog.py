from PySide6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton, QHBoxLayout


class CopyDicomFilesTaskDialog(QDialog):
    def __init__(self, parent=None):
        super(CopyDicomFilesTaskDialog, self).__init__(parent)
        self.setWindowTitle('CopyDicomFilesTask parameters')
        self._task_params = None
        self._decompress_checkbox = QCheckBox('Decompress', self)
        accept_button = QPushButton('Save', self)
        accept_button.clicked.connect(self.accept)
        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.reject)
        button_layout = QHBoxLayout()
        button_layout.addWidget(accept_button)
        button_layout.addWidget(cancel_button)
        layout = QVBoxLayout()
        layout.addWidget(self._decompress_checkbox)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def accept(self):
        if self._task_params is None:
            self._task_params = {}
        self._task_params['decompress'] = 'true' if self._decompress_checkbox.isChecked() else 'false'
        super(CopyDicomFilesTaskDialog, self).accept()

    def reject(self):
        self._task_params = None
        super(CopyDicomFilesTaskDialog, self).reject()

    def get_params(self):
        return self._task_params