from PySide6.QtWidgets import QDialog, QVBoxLayout, QCheckBox


class CopyDicomFilesTaskDialog(QDialog):
    def __init__(self, parent=None):
        super(CopyDicomFilesTaskDialog, self).__init__(parent)
        self.setWindowTitle('CopyDicomFilesTask parameters')
        self._task_params = None
        self._decompress_checkbox = QCheckBox('Decompress', self)
        layout = QVBoxLayout()
        layout.addWidget(self._decompress_checkbox)
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