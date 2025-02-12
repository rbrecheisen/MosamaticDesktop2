from PySide6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton, QHBoxLayout


class DecompressDicomFilesTaskDialog(QDialog):
    def __init__(self, parent=None):
        super(DecompressDicomFilesTaskDialog, self).__init__(parent)
        self.setWindowTitle('DecompressDicomFilesTask parameters')
        self._task_params = None
        accept_button = QPushButton('Save', self)
        accept_button.clicked.connect(self.accept)
        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.reject)
        button_layout = QHBoxLayout()
        button_layout.addWidget(accept_button)
        button_layout.addWidget(cancel_button)
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def accept(self):
        super(DecompressDicomFilesTaskDialog, self).accept()

    def reject(self):
        super(DecompressDicomFilesTaskDialog, self).reject()

    def get_params(self):
        return self._task_params