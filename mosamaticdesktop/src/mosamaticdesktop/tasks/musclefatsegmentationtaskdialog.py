from PySide6.QtWidgets import QDialog, QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout


# TODO: Add QFileDialog for loading model files!!!

class MuscleFatSegmentationTaskDialog(QDialog):
    def __init__(self, parent=None):
        super(MuscleFatSegmentationTaskDialog, self).__init__(parent)
        self.setWindowTitle('MuscleFatSegmentationTask parameters')
        self._task_params = None
        # self._delay_spinbox = QSpinBox(self, minimum=0, singleStep=1)
        # accept_button = QPushButton('Save', self)
        # accept_button.clicked.connect(self.accept)
        # cancel_button = QPushButton('Cancel', self)
        # cancel_button.clicked.connect(self.reject)
        # button_layout = QHBoxLayout()
        # button_layout.addWidget(accept_button)
        # button_layout.addWidget(cancel_button)
        # layout = QVBoxLayout()
        # layout.addWidget(self._delay_spinbox)
        # layout.addLayout(button_layout)
        # self.setLayout(layout)

    def accept(self):
        if self._task_params is None:
            self._task_params = {}
        self._task_params['delay'] = self._delay_spinbox.value()
        super(MuscleFatSegmentationTaskDialog, self).accept()

    def reject(self):
        self._task_params = None
        super(MuscleFatSegmentationTaskDialog, self).reject()

    def get_params(self):
        return self._task_params