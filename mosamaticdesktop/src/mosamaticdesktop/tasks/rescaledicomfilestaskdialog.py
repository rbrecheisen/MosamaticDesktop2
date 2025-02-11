from PySide6.QtWidgets import QDialog, QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout


class RescaleDicomFilesTaskDialog(QDialog):
    def __init__(self, parent=None):
        super(RescaleDicomFilesTaskDialog, self).__init__(parent)
        self.setWindowTitle('RescaleDicomFilesTaskDialog parameters')
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
        if self._task_params is None:
            self._task_params = {}
        # self._task_params['delay'] = self._delay_spinbox.value()
        super(RescaleDicomFilesTaskDialog, self).accept()

    def reject(self):
        self._task_params = None
        super(RescaleDicomFilesTaskDialog, self).reject()

    def get_params(self):
        return self._task_params