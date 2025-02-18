from PySide6.QtWidgets import QLabel, QSpinBox, QVBoxLayout

from mosamaticdesktop.tasks.taskdialog import TaskDialog


class RescaleDicomFilesTaskDialog(TaskDialog):
    def __init__(self, parent=None):
        super(RescaleDicomFilesTaskDialog, self).__init__(parent)
        self._target_size_label = QLabel('Target size', self)
        self._target_size_spinner = QSpinBox(self, minimum=16, maximum=1024, singleStep=16, value=512)
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._target_size_label)
        self._layout.addWidget(self._target_size_spinner)
        self.init_ui()

    def get_content_layout(self):
        return self._layout
    
    def update_params(self):
        self.set_param('target_size', self._target_size_spinner.value())