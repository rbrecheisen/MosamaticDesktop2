from PySide6.QtWidgets import QSpinBox, QVBoxLayout

from mosamaticdesktop.tasks.taskdialog import TaskDialog


class CopyFilesTaskDialog(TaskDialog):
    def __init__(self, parent=None):
        super(CopyFilesTaskDialog, self).__init__(parent)
        self._delay_spinbox = QSpinBox(self, minimum=0, singleStep=1)
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._delay_spinbox)
        self.init_ui()

    def get_content_layout(self):
        return self._layout
    
    def update_params(self):
        self.set_param('delay', self._delay_spinbox.value())